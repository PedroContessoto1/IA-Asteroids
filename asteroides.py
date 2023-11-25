import random
from config import LARGURA, ALTURA
import math
import pygame

class Asteroide:
    def __init__(self, x, y, tamanho):
        self.x = x
        self.y = y
        self.tamanho = tamanho  # 1 para pequeno, 2 para médio, 3 para grande
        self.imagem_original = pygame.image.load('img/asteroide.png')
        # Redimensiona a imagem com base no tamanho
        if tamanho == 1:  # Pequeno
            self.velocidade = 0.3
            self.imagem = pygame.transform.scale(self.imagem_original, (20, 20))
        elif tamanho == 2:  # Médio
            self.velocidade = 0.2
            self.imagem = pygame.transform.scale(self.imagem_original, (40, 40))
        else:  # Grande
            self.velocidade = 0.1
            self.imagem = pygame.transform.scale(self.imagem_original, (60, 60))

        self.rect = self.imagem.get_rect(center=(self.x, self.y))
        self.angulo = random.uniform(0, 360)

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

    def desenhar(self, tela):
        # Ajusta a posição do retângulo (rect) da imagem para o centro atual do asteroide
        self.rect.center = (int(self.x), int(self.y))

        # Desenha a imagem na tela na posição do retângulo
        tela.blit(self.imagem, self.rect.topleft)
    
    def dividir_asteroide(self, asteroide, asteroides):
        if asteroide.tamanho > 1:
            for _ in range(3 if asteroide.tamanho == 2 else 2):
                novo_tamanho = asteroide.tamanho - 1
                novo_asteroide = Asteroide(asteroide.x, asteroide.y, novo_tamanho)
                
                # Ajustando a direção e velocidade dos novos asteroides
                novo_asteroide.angulo = random.uniform(0, 360)
                novo_asteroide.velocidade = asteroide.velocidade + 0.1

                asteroides.append(novo_asteroide)

    def detectar_colisao(self, tiro, asteroide):
        distancia = math.sqrt((tiro.x - asteroide.x)**2 + (tiro.y - asteroide.y)**2)
        raio_asteroide = 10 if asteroide.tamanho == 1 else 20 if asteroide.tamanho == 2 else 30
        return distancia < raio_asteroide
