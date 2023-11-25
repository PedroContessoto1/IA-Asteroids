import numpy as np
import random

class QLearningAgent:
    def __init__(self, n_actions, state_space, alpha=0.1, gamma=0.9, epsilon=0.1, epsilon_decay=0.995):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n_actions = n_actions
        self.state_space = state_space
        self.epsilon_decay = epsilon_decay 

        # Inicialize a q_table aqui. Você pode precisar de uma abordagem diferente
        # dependendo da complexidade do seu espaço de estado.
        self.q_table = {}

    def discretize_state(self, state):
        # Ajustando a granularidade da discretização
        pos_nave_x = int(state["posicao_nave"][0]) // 5
        pos_nave_y = int(state["posicao_nave"][1]) // 5
        orientacao_nave = int(state["orientacao_nave"][0]) // 45

        # Considerando mais asteroides
        asteroides_proximos = sorted(state["asteroides"], key=lambda ast: np.linalg.norm(np.array([ast[0], ast[1]]) - np.array([state["posicao_nave"][0], state["posicao_nave"][1]])))[:3]
        asteroides_info = [(int(ast[0]) // 5, int(ast[1]) // 5, ast[2], ast[3] // 45) for ast in asteroides_proximos]

        vidas = state["vidas"][0]

        # Considerando mais tiros
        tiros_info = [(int(tiro[0]) // 5, int(tiro[1]) // 5, int(tiro[2]) // 10) for tiro in state["tiros"]][:5]

        pontos = state["pontos"][0]

        discretized_state = (pos_nave_x, pos_nave_y, orientacao_nave, *asteroides_info, vidas, *tiros_info, pontos)

        return discretized_state
    
    def decay_epsilon(self):
        # Aplica o decaimento a epsilon
        self.epsilon *= self.epsilon_decay



    def choose_action(self, discretized_state):
        if np.random.random() < self.epsilon:
            return np.random.choice(self.n_actions)
        else:
            # Garanta que a q_table tenha uma entrada para este estado
            if discretized_state not in self.q_table:
                self.q_table[discretized_state] = np.zeros(self.n_actions)
            return np.argmax(self.q_table[discretized_state])

    def learn(self, discretized_state, action, reward, discretized_next_state):
        # Garanta que a q_table tenha entradas para estes estados
        if discretized_state not in self.q_table:
            self.q_table[discretized_state] = np.zeros(self.n_actions)
        if discretized_next_state not in self.q_table:
            self.q_table[discretized_next_state] = np.zeros(self.n_actions)

        predict = self.q_table[discretized_state][action]
        target = reward + self.gamma * np.max(self.q_table[discretized_next_state])
        self.q_table[discretized_state][action] += self.alpha * (target - predict)
