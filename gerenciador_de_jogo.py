from config import LARGURA, ALTURA
import random
import pygame
from asteroides import Asteroide

class GerenciadorDeJogo:
    def __init__(self, nave):
        self.nave = nave
        self.asteroides = []
        self.game_over = False
        self.fase = 1
        self.pontos = 0
        self.vidas = 3
        self.inicializar_fase()

    def inicializar_fase(self):
        self.asteroides.clear()
        self.criar_asteroides_seguros()

    def criar_asteroides_seguros(self):
        num_asteroides = self.fase * 2  # Aumenta com a fase
        area_segura = 50

        while len(self.asteroides) < num_asteroides:
            x = random.randint(0, LARGURA)
            y = random.randint(0, ALTURA)

            if abs(x - self.nave.x) > area_segura and abs(y - self.nave.y) > area_segura:
                tamanho = random.choice([1, 2, 3])
                self.asteroides.append(Asteroide(x, y, tamanho))

    def atualizar(self):
        # Atualiza a posição dos asteroides
        for asteroide in self.asteroides[:]:
            asteroide.atualizar_posicao()

        # Verifique se todos os asteroides foram destruídos
        if not self.asteroides:
            self.fase += 1  # Avance para a próxima fase
            self.inicializar_fase()  # Inicialize a fase com novos asteroides

    def is_game_over(self):
        return self.game_over