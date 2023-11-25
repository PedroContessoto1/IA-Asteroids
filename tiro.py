import math
import pygame
from config import LARGURA, ALTURA

class Tiro:
    def __init__(self, x, y, angulo):
        self.x = x
        self.y = y
        self.angulo = angulo
        self.velocidade = 2
        self.raio = 2
        self.tempo_de_vida = 300  # Tempo de vida do tiro em frames

    def atualizar_posicao(self):
        self.x += math.cos(math.radians(self.angulo)) * self.velocidade
        self.y += math.sin(math.radians(self.angulo)) * self.velocidade

         # Lógica para reaparecer do outro lado da tela
        if self.x > LARGURA:
            self.x = 0
        elif self.x < 0:
            self.x = LARGURA

        if self.y > ALTURA:
            self.y = 0
        elif self.y < 0:
            self.y = ALTURA

        # Decrementa o tempo de vida
        self.tempo_de_vida -= 1

        # Verifica se o tiro atingiu o fim de sua vida útil
        return self.tempo_de_vida > 0

    def desenhar(self, tela):
        pygame.draw.circle(tela, (0, 255, 255), (int(self.x), int(self.y)), self.raio)
