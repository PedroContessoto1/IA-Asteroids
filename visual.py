import pygame
import pickle
from qlearning_agent import QLearningAgent  # Certifique-se de que essa classe exista
from config import LARGURA, ALTURA
from asteroids_env import AsteroidsEnv

# Carregar o modelo salvo
with open('melhor_agente_qtable.pkl', 'rb') as file:
    q_table, media_recompensas = pickle.load(file)

# Inicializar o ambiente
env = AsteroidsEnv()
ambiente = env.ambiente
gerenciador = ambiente.gerenciador

n_actions = 5  # Atualize conforme necessário
state_space = 25  # Atualize conforme necessário
agent = QLearningAgent(n_actions, state_space)
agent.q_table = q_table

# Inicializar o Pygame
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Asteroids")

# Criar uma superfície para o fundo
fundo_superficie = pygame.Surface(tela.get_size())

# Carregar e otimizar a imagem de fundo
imagem_fundo = pygame.image.load('img/fundo.png')
imagem_fundo = pygame.transform.scale(imagem_fundo, (LARGURA, ALTURA))
imagem_fundo = imagem_fundo.convert() 

# Desenhar a imagem de fundo na superfície do fundo
fundo_superficie.blit(imagem_fundo, (0, 0))

# Loop principal do jogo
rodando = True
recompensa_acumulada = 0  # Inicializa a recompensa acumulada
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # Obter estado atual do jogo
    estado_atual = ambiente.obter_estado_do_jogo()

    # Discretizar o estado
    estado_discretizado = agent.discretize_state(estado_atual)

    # Escolher ação com base no estado discretizado
    acao = agent.choose_action(estado_discretizado)

    # Executar a ação e obter recompensa usando o ambiente Gym
    novo_estado, recompensa, done, _ = env.step(acao)
    estado_discretizado = agent.discretize_state(novo_estado)
    #print(estado_discretizado)
    recompensa_acumulada += recompensa  # Acumula a recompensa
    #print(recompensa_acumulada)

    tela.blit(imagem_fundo, (0, 0))
    ambiente.desenhar(tela)
    pygame.display.update()

    # Verificar se o jogo terminou

    if gerenciador.game_over:
        print("Game Over!")  # Substitua por sua lógica de game over
        break


pygame.quit()
