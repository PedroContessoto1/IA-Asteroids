import pygame
import math
import random
from nave import Nave
from config import LARGURA, ALTURA
from asteroides import Asteroide
from gerenciador_de_jogo import GerenciadorDeJogo

# Inicializa o Pygame
pygame.init()

# Definindo as dimensões da janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Asteroids")

# Inicializa o rastreador do estado anterior da tecla espaço
espaco_pressionado_anteriormente = False

# Definindo cores
PRETO = (0, 0, 0)

# Criando a nave
nave = Nave(LARGURA // 2, ALTURA // 2)

# Criando o gerenciador de jogo
gerenciador = GerenciadorDeJogo(nave)

# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Preenche a tela com preto
    tela.fill(PRETO)

    # Obtendo as teclas pressionadas
    teclas = pygame.key.get_pressed()

    # Controles
    if teclas[pygame.K_LEFT]:
        nave.rotacionar("ESQUERDA")
    if teclas[pygame.K_RIGHT]:
        nave.rotacionar("DIREITA")
    if teclas[pygame.K_UP]:
        nave.velocidade += nave.aceleracao
        if nave.velocidade > nave.velocidade_max:
            nave.velocidade = nave.velocidade_max

    if teclas[pygame.K_SPACE] and not espaco_pressionado_anteriormente:
        nave.atirar()
    espaco_pressionado_anteriormente = teclas[pygame.K_SPACE]

    # Atualize e desenhe os tiros
    for tiro in nave.tiros[:]:
        if not tiro.atualizar_posicao():
            nave.tiros.remove(tiro)  # Remove o tiro se ele atingiu o fim do tempo de vida
        else:
            tiro.desenhar(tela)

    if gerenciador.game_over:
        print("Game Over!")  # Substitua por sua lógica de game over
        break

    gerenciador.atualizar()
    gerenciador.desenhar(tela)


    # Atualiza a posição da nave
    nave.atualizar_posicao()

    # Desenha a nave
    nave.desenhar(tela)

    # Atualiza a tela
    pygame.display.flip()


# Finaliza o Pygame
pygame.quit()
