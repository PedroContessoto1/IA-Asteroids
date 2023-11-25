import pygame
from nave import Nave
from asteroides import Asteroide
from config import LARGURA, ALTURA
from gerenciador_de_jogo import GerenciadorDeJogo
import random
import math
import numpy as np

class AmbienteSimulado:
    def __init__(self):
        self.reset()

    def reset(self):
        # Reinicializa o jogo
        self.nave = Nave(LARGURA // 2, ALTURA // 2)
        self.gerenciador = GerenciadorDeJogo(self.nave)
        self.ultimo_evento = ""
        self.tiros_disparados = 0
        self.tiros_acertados = 0

    def obter_estado_do_jogo(self):
        # Retorna uma representação do estado atual do jogo
        estado = {
            "posicao_nave": np.array([self.nave.x, self.nave.y]),
            "orientacao_nave": np.array([self.nave.angulo]),
            "velocidade_nave": np.array([self.nave.velocidade_x, self.nave.velocidade_y]),  # Inclui a velocidade
            "asteroides": np.array([(asteroide.x, asteroide.y, asteroide.tamanho, asteroide.angulo) for asteroide in self.gerenciador.asteroides]),
            "vidas": np.array([self.gerenciador.vidas]),
            "pontos": np.array([self.gerenciador.pontos]),
            "fase": np.array([self.gerenciador.fase]),
            "tiros": np.array([(tiro.x, tiro.y, tiro.tempo_de_vida) for tiro in self.nave.tiros]),
        }
        return estado

    def executar_acao(self, acao):
        # Executa uma ação no jogo, como mover a nave ou atirar
        pode_atirar = False
        if acao == 0:  # acelerar
            self.nave.acelerar()
        elif acao == 1:  # Mover para a direita
            self.nave.rotacionar_direita()
        elif acao == 2:  # rotacionar_esquerda
            self.nave.rotacionar_esquerda()
        elif acao == 3:  # Atirar
            if self.nave.pode_atirar():
                self.nave.atirar()
                self.tiros_disparados += 1
                pode_atirar = True
        elif acao == 4: 
            self.nave.desacelerar()

        # Atualiza o estado do jogo após a ação
        acerto = self.verificar_acerto()
        self.atualizar()


        return acerto, pode_atirar
    
    def verificar_acerto(self):
        # Esta função verifica se algum tiro acertou um asteroide
        acertos = False

        # Itera sobre uma cópia da lista de tiros para evitar modificações durante a iteração
        for tiro in self.nave.tiros[:]:
            # Itera sobre uma cópia da lista de asteroides
            for asteroide in self.gerenciador.asteroides[:]:
                # Verifica se o tiro atual acertou o asteroide atual
                if self.detectar_colisao(tiro, asteroide):
                    # Atualiza os pontos e remove o tiro da lista
                    self.gerenciador.pontos += 10
                    if self.gerenciador.pontos % 200 == 0:
                        self.gerenciador.vidas += 1 
                    
                    if tiro in self.nave.tiros:
                        self.nave.tiros.remove(tiro)


                    # Se o asteroide for maior do que 1, ele se divide em menores
                    if asteroide.tamanho > 1:
                        self.dividir_asteroide(asteroide)
                    
                    # Remove o asteroide acertado da lista
                    if asteroide in self.gerenciador.asteroides:
                        self.gerenciador.asteroides.remove(asteroide)

                    # Marca que houve um acerto
                    self.tiros_acertados += 1
                    acertos = True
                    break  # Sai do loop de asteroides, pois o tiro já foi processado

        return acertos
    
    def dividir_asteroide(self, asteroide):
        # Divide um asteroide em asteroides menores
        novo_tamanho = asteroide.tamanho - 1
        for _ in range(2):
            novo_asteroide = Asteroide(asteroide.x, asteroide.y, novo_tamanho)
            novo_asteroide.angulo = random.uniform(0, 360)
            novo_asteroide.velocidade = asteroide.velocidade + 0.1
            self.gerenciador.asteroides.append(novo_asteroide)

    def verificar_colisao(self):
        # Verifica se a nave colidiu com um asteroide
        for asteroide in self.gerenciador.asteroides:
            if self.nave.detectar_colisao_nave(asteroide):
                self.gerenciador.vidas -= 1
                self.gerenciador.asteroides.remove(asteroide)
                return True
        return False
    
    def verificar_evasao(self):
        distancia_segura = 70  # Defina um limiar de distância segura
        evadiu = True  # Inicialmente, supomos que a nave evadiu com sucesso

        for asteroide in self.gerenciador.asteroides:
            distancia = math.sqrt((self.nave.x - asteroide.x) ** 2 + (self.nave.y - asteroide.y) ** 2)
            if distancia < distancia_segura:
                evadiu = False  # Se algum asteroide estiver muito próximo, a nave não conseguiu evadir
                break  # Não é necessário verificar os outros asteroides

        return evadiu
    
    def calcular_taxa_acertos(self):
        if self.tiros_disparados > 0:
            return self.tiros_acertados / self.tiros_disparados
        else:
            return 0

    def detectar_colisao(self, objeto1, objeto2):
        # Método para detectar colisão entre dois objetos
        distancia = math.sqrt((objeto1.x - objeto2.x)**2 + (objeto1.y - objeto2.y)**2)
        
        # Definindo o raio para o objeto1 (pode ser a nave ou um tiro)
        raio_objeto1 = 20 if isinstance(objeto1, Nave) else 5  # Supondo que o tiro tenha um raio de 5

        # Definindo o raio para o objeto2 (asteroide)
        raio_objeto2 = 10 if objeto2.tamanho == 1 else 20 if objeto2.tamanho == 2 else 30

        return distancia < (raio_objeto1 + raio_objeto2)


    def atualizar(self):
    # Atualiza o estado do jogo
        self.nave.atualizar_posicao()
        self.gerenciador.atualizar()
        if self.verificar_colisao():
            self.ultimo_evento = "colisao"
        # Remover a chamada para verificar_acerto daqui
        self.verificar_fim_de_jogo()

    def verificar_fim_de_jogo(self):
        if self.gerenciador.vidas <= 0:
            self.gerenciador.game_over = True
            return True
        return False
    
    def desenhar(self, tela):
        for asteroide in self.gerenciador.asteroides:
            asteroide.desenhar(tela)

        self.nave.desenhar(tela)

        for tiro in self.nave.tiros:
            tiro.desenhar(tela)

        # Desenhar a pontuação e as vidas
        font = pygame.font.Font(None, 36)
        text = font.render(f'Pontos: {self.gerenciador.pontos} Vidas: {self.gerenciador.vidas} Fase: {self.gerenciador.fase}', True, (255, 255, 255))
        tela.blit(text, (10, 10))
    
    
