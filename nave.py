import math
import pygame
from tiro import Tiro
from config import LARGURA, ALTURA
import time


class Nave:
    def __init__(self, x, y, angulo=0):
        self.x = x
        self.y = y
        self.angulo = angulo
        self.velocidade = 0
        self.aceleracao = 0.005  # Valor mais baixo para a aceleração
        self.velocidade_max = 5  # Velocidade máxima reduzida
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.desaceleracao = 0.98
        self.velocidade_rotacao = 5  # Velocidade de rotação reduzida
        self.tiros = []
        self.imagem_original = pygame.image.load('img/nave.png')
        self.imagem_original = pygame.transform.scale(self.imagem_original, (40, 40))
        self.rect = self.imagem_original.get_rect(center=(self.x, self.y))
        self.tempo_ultimo_tiro = time.time()
        self.intervalo_tiro = 200

    def desenhar(self, tela):
        imagem_rotacionada = pygame.transform.rotate(self.imagem_original, -self.angulo - 90)  # Rotaciona a imagem
        rect_rotacionado = imagem_rotacionada.get_rect(center=self.rect.center)  # Obtém o novo retângulo após a rotação
        tela.blit(imagem_rotacionada, rect_rotacionado.topleft)


    def rotacionar_esquerda(self):
        # Rotaciona a nave para a esquerda
        self.angulo -= self.velocidade_rotacao

    def rotacionar_direita(self):
        # Rotaciona a nave para a direita
        self.angulo += self.velocidade_rotacao


    def atualizar_posicao(self):
        # Atualiza a posição com base na velocidade atual
        self.velocidade_x *= self.desaceleracao
        self.velocidade_y *= self.desaceleracao
        self.x += self.velocidade_x
        self.y += self.velocidade_y

        # Lógica para reaparecer do outro lado da tela
        if self.x > LARGURA:
            self.x = 0
        elif self.x < 0:
            self.x = LARGURA

        if self.y > ALTURA:
            self.y = 0
        elif self.y < 0:
            self.y = ALTURA

        tiros_vivos = []

        for tiro in self.tiros:
            if tiro.atualizar_posicao():
                tiros_vivos.append(tiro)
        
        self.tiros = tiros_vivos
        self.rect.center = (self.x, self.y)

    def atirar(self):
        # Ajuste para que o tiro comece na frente da nave
        inicio_x = self.x + math.cos(math.radians(self.angulo)) * 20
        inicio_y = self.y + math.sin(math.radians(self.angulo)) * 20
        novo_tiro = Tiro(inicio_x, inicio_y, self.angulo)
        self.tiros.append(novo_tiro)
        # Atualiza o tempo do último tiro
        self.tempo_ultimo_tiro = time.time()

    def pode_atirar(self):
        tempo_atual = time.time()
        return tempo_atual - self.tempo_ultimo_tiro >= 0.2


    def detectar_colisao_nave(self, asteroide):
        distancia = math.sqrt((self.x - asteroide.x)**2 + (self.y - asteroide.y)**2)
        raio_asteroide = 10 if asteroide.tamanho == 1 else 20 if asteroide.tamanho == 2 else 30
        raio_nave = 20  # Supondo que a nave tenha um raio aproximado para a colisão
        return distancia < (raio_nave + raio_asteroide)
    
    def acelerar(self):
        # Acelera a nave na direção atual
        if self.velocidade < self.velocidade_max:
            self.velocidade_x += math.cos(math.radians(self.angulo)) * self.aceleracao
            self.velocidade_y += math.sin(math.radians(self.angulo)) * self.aceleracao

    def desacelerar(self):
        # Desacelera a nave gradualmente
        self.velocidade_x *= self.desaceleracao
        self.velocidade_y *= self.desaceleracao

