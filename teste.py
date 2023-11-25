import pickle

caminho_arquivo = 'melhor_agente_qtable.pkl'

# Carregar a tabela Q
with open(caminho_arquivo, 'rb') as file:
    q_table, melhor_agente_recompensa = pickle.load(file)

# Agora, q_table contém a tabela Q e media_recompensas a média de recompensa
melhor_agente_recompensa = 600

# Salvar a tabela Q modificada
with open(caminho_arquivo, 'wb') as file:
    pickle.dump((q_table, melhor_agente_recompensa), file)
