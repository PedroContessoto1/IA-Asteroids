import gym
from gym import spaces
from config import LARGURA, ALTURA
import numpy as np
from ambiente_simulado import AmbienteSimulado

class AsteroidsEnv(gym.Env):
    """Ambiente personalizado do Gym para o jogo de Asteroids"""

    def __init__(self):
        super(AsteroidsEnv, self).__init__()
        self.ambiente = AmbienteSimulado()
        # Define o espaço de ação
        self.action_space = spaces.Discrete(5)  # Esquerda, Direita, Acelerar, Atirar, Desacelerar

        self.fase_atual = 1
        self.vidas_atual = 3

        self.observation_space = spaces.Dict({
            "posicao_nave": spaces.Box(low=np.array([0, 0]), high=np.array([LARGURA, ALTURA]), dtype=np.float32),
            "orientacao_nave": spaces.Box(low=np.array([-360]), high=np.array([360]), dtype=np.float32),
            "asteroides": spaces.Box(low=np.array([[0, 0, 0]] * 10), high=np.array([[LARGURA, ALTURA, np.inf]] * 10), dtype=np.float32),
            "vidas": spaces.Discrete(5),
            "pontos": spaces.Box(low=np.array([0]), high=np.array([np.inf]), dtype=np.float32),
            "fase": spaces.Box(low=np.array([0]), high=np.array([np.inf]), dtype=np.float32),
            "tiros": spaces.Box(low=np.array([[0, 0]] * 5), high=np.array([[LARGURA, ALTURA]] * 5), dtype=np.float32),
        })


    def step(self, action):


         # Execute a ação no ambiente
        acerto, pode_atirar = self.ambiente.executar_acao(action)

        # Adicione a chamada para as novas funções
        evasao = self.ambiente.verificar_evasao()
        taxa_acertos = self.ambiente.calcular_taxa_acertos()
        colisao = self.ambiente.verificar_colisao()

        # Calcular recompensa com base no resultado da ação e nas novas funções
        recompensa = self.calcular_recompensa(action, acerto, colisao, pode_atirar, evasao, taxa_acertos)

        # Obtenha o estado atual do jogo após a ação
        estado = self.ambiente.obter_estado_do_jogo()


        # Verifique se houve uma mudança de fase
        nova_fase = estado["fase"][0]
        if nova_fase > self.fase_atual:
            recompensa_bonus_fase = 20 * nova_fase
            recompensa += recompensa_bonus_fase
            self.fase_atual = nova_fase

        # Verifique se o número de vidas aumentou
        vidas_novas = estado["vidas"][0]
        if vidas_novas > self.vidas_atual:
            recompensa_bonus_vidas = 60  # Valor da recompensa por ganhar uma vida extra
            recompensa += recompensa_bonus_vidas
            self.vidas_atual = vidas_novas  # Atualize o rastreamento do número de vidas

        # Verifique se o jogo terminou
        done = self.ambiente.verificar_fim_de_jogo()
        info = {}

        return estado, recompensa, done, info
    
    def calcular_recompensa(self, action, acerto, colisao, pode_atirar, evasao, taxa_acertos):
        # Define as recompensas para diferentes eventos
        recompensa_acerto = 30 if acerto else 0
        penalidade_colisao = -50 if colisao else 0
        recompensa_evasao = 0.2 if evasao else 0
        recompensa_evasao = -1 if not evasao else 0
        recompensa_taxa_acertos = 4 * taxa_acertos

        # Penalidades ou recompensas adicionais baseadas na ação
        penalidade_tiro = -0.3 if action == 3 and not pode_atirar else 0
        recompensa_tiro = 0.3 if action == 3 and pode_atirar else 0
            

        # Combina todas as recompensas e penalidades
        recompensa = (recompensa_acerto + penalidade_colisao + recompensa_evasao +
                      recompensa_taxa_acertos + penalidade_tiro + recompensa_tiro)
        
        return recompensa

    def reset(self):
        self.ambiente.reset()
        self.fase_atual = 1
        self.vidas_atual = 3
        return self.ambiente.obter_estado_do_jogo()

    def render(self, mode='human'):
        # Implemente a lógica de renderização para visualização e debug
        pass

    def close(self):
        # Qualquer limpeza necessária ao fechar o ambiente
        pass

