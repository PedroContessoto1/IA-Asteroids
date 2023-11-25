import matplotlib.pyplot as plt
from asteroids_env import AsteroidsEnv
from qlearning_agent import QLearningAgent
import pickle
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import random
import sys

# Inicialização do ambiente e variáveis...
recompensas_medias_por_geracao = []  # Armazena as médias das recompensas totais por geração
env = AsteroidsEnv()
n_actions = 5
state_space = 40  # Definido conforme a necessidade
n_agents = 5
n_episodes = 10
n_geracoes = 5  # Número de gerações
intervalo_print = 5  # Define a frequência de prints

melhor_agente = None

def carregar_agente_salvo(caminho_arquivo, n_actions, state_space):
    with open(caminho_arquivo, 'rb') as file:
        q_table_carregada, media_recompensas = pickle.load(file)
    agente = QLearningAgent(n_actions, state_space)
    agente.q_table = q_table_carregada
    return agente, media_recompensas

def criar_agentes_influenciados(n_agents, state_space, melhor_agente, variancia_parametros=0.1):
    novos_agentes = []

    for _ in range(n_agents):
        agente = QLearningAgent(n_actions, state_space)

        # Introduz variação nos parâmetros do agente
        agente.alpha = max(0.0, min(1.0, melhor_agente.alpha + random.uniform(-variancia_parametros, variancia_parametros)))
        agente.gamma = max(0.0, min(1.0, melhor_agente.gamma + random.uniform(-variancia_parametros, variancia_parametros)))
        agente.epsilon = max(0.0, min(1.0, melhor_agente.epsilon + random.uniform(-variancia_parametros, variancia_parametros)))

        # Inicializa a tabela Q do agente
        agente.q_table = {}  # Cada agente começa com sua própria tabela Q vazia

        novos_agentes.append(agente)

    return novos_agentes


def treinar_agente(agent_idx, agent, n_episodes, env):
    pontos_por_episodio = []

    for episode in range(n_episodes):
        env =  AsteroidsEnv()
        state = env.reset()
        done = False
        total_recompensa = 0

        while not done:
            state = env.ambiente.obter_estado_do_jogo()
            discretized_state = agent.discretize_state(state)
            action = agent.choose_action(discretized_state)

            next_state, recompensa, done, _ = env.step(action)
            
            discretized_next_state = agent.discretize_state(next_state)
            agent.learn(discretized_state, action, recompensa, discretized_next_state)
            total_recompensa += recompensa
            #print(discretized_next_state)

            state = next_state
        
        # Captura os pontos ao final de cada episódio
        pontos_episodio = env.ambiente.gerenciador.pontos
        pontos_por_episodio.append(pontos_episodio)
        print(f"Agente {agent_idx + 1}, Episódio {episode + 1}, Total de Recompensas: {total_recompensa}, Pontos: {pontos_episodio}")
        total_recompensa = 0

    media_pontos = sum(pontos_por_episodio) / n_episodes

    return pontos_por_episodio, media_pontos

try:
    melhor_agente, melhor_agente_recompensa = carregar_agente_salvo('melhor_agente_qtable.pkl', n_actions, state_space)
    print(f"Agente salvo carregado com sucesso. Média de recompensas: {melhor_agente_recompensa}")
except FileNotFoundError:
    melhor_agente_recompensa = -np.inf  # Inicializa com um valor muito baixo para o melhor agente
    melhor_agente = None
    print("Nenhum agente salvo encontrado. Iniciando com um novo agente.")

for geracao in range(n_geracoes):
    print(f"Iniciando Geração {geracao + 1}")

    melhor_pontuacao_geracao = -np.inf
    melhor_agente_geracao = None
    agents = criar_agentes_influenciados(n_agents, state_space, melhor_agente)

    with ThreadPoolExecutor(max_workers=n_agents) as executor:
        futures = [executor.submit(treinar_agente, idx, agent, n_episodes, env) for idx, agent in enumerate(agents)]
        results = [future.result() for future in futures]

    for idx, (_, media_pontos) in enumerate(results):
        if media_pontos > melhor_pontuacao_geracao:
            melhor_pontuacao_geracao = media_pontos
            melhor_agente_geracao = agents[idx]

    if melhor_pontuacao_geracao > melhor_agente_recompensa:  # Aqui pode precisar ajustar a variável de comparação
        melhor_agente_recompensa = melhor_pontuacao_geracao  # Aqui também
        melhor_agente = melhor_agente_geracao
        print(f"Novo melhor agente encontrado na Geração {geracao + 1} com média de pontos: {melhor_pontuacao_geracao}")
        with open('melhor_agente_qtable.pkl', 'wb') as file:
            pickle.dump((melhor_agente.q_table, melhor_pontuacao_geracao), file)
    else:
        print(f"Melhor agente mantido da Geração {geracao + 1}")

    # Calculando a média de recompensas por agente
    medias_recompensas_por_agente = [np.mean(rewards) for _, rewards in results]

    # Números dos agentes para o eixo X
    numeros_dos_agentes = range(1, n_agents + 1)

    # Plotando o gráfico
    plt.bar(numeros_dos_agentes, medias_recompensas_por_agente)
    plt.xlabel('Agente')
    plt.ylabel('Recompensa Média')
    plt.title(f'Desempenho Médio dos Agentes na Geração {geracao + 1}')
    plt.xticks(numeros_dos_agentes)  # Isso garante que todos os números dos agentes sejam mostrados no eixo X
    plt.savefig(f'geracao_{geracao + 1}_comparacao_agentes.png')
    plt.close()
    

    # Calculando a média de recompensas por episódio para cada agente
    medias_recompensas = [np.mean(rewards) for _, rewards in results]

    # Identificando o melhor agente com base na média de recompensas
    best_agent_idx = medias_recompensas.index(max(medias_recompensas))
    melhor_agente = agents[best_agent_idx]

    # Após o treinamento de cada geração
    media_recompensa_geracao = sum(medias_recompensas) / len(medias_recompensas)
    recompensas_medias_por_geracao.append(media_recompensa_geracao)
    print(f"Recompensa média da Geração {geracao + 1}: {media_recompensa_geracao}")

    print(f"Melhor Agente da Geração {geracao + 1}: {best_agent_idx + 1}, Média de Recompensas: {medias_recompensas[best_agent_idx]}")


# Plotando o gráfico comparativo de todas as gerações
plt.figure()
plt.plot(range(1, n_geracoes + 1), recompensas_medias_por_geracao, marker='o')
plt.xlabel('Geração')
plt.ylabel('Recompensa Média')
plt.title('Comparação das Recompensas Médias por Geração')
plt.xticks(range(1, n_geracoes + 1))  # Garante que o eixo x mostre todas as gerações
plt.grid(True)
plt.savefig('comparacao_geracoes.png')
plt.close()