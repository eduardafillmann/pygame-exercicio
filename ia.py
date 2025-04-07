import pygame
import sys

# Inicializa o pygame
pygame.init()

# Define as dimensões da janela
largura, altura = 250, 200
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Janela com Botão")

# Define as cores
branco = (255, 255, 255)
cinza = (200, 200, 200)
preto = (0, 0, 0)

# Carrega a sprite sheet do personagem
sprite_sheet = pygame.image.load("Attack.png").convert_alpha()
num_quadros = 8

# Define dimensões dos quadros
quadro_largura = sprite_sheet.get_width() // num_quadros
quadro_altura = sprite_sheet.get_height()

# Extraí os quadros da linha correta da sprite sheet
quadros = [sprite_sheet.subsurface((i * quadro_largura, 52, quadro_largura, quadro_altura - 52)) for i in range(num_quadros)]

# Função para desenhar o botão
def desenha_botao(tela, cor, pos, tamanho, texto):
    fonte = pygame.font.Font(None, 36)
    pygame.draw.rect(tela, cor, (pos[0], pos[1], tamanho[0], tamanho[1]))
    texto_surface = fonte.render(texto, True, preto)
    texto_rect = texto_surface.get_rect(center=(pos[0] + tamanho[0] // 2, pos[1] + tamanho[1] // 2))
    tela.blit(texto_surface, texto_rect)

# Dimensões do botão
largura_botao, altura_botao = 100, 50
x_botao = largura - largura_botao - 10
y_botao = altura - altura_botao - 10
botao = pygame.Rect(x_botao, y_botao, largura_botao, altura_botao)

# Animação
indice_quadro = 0
tempo_animacao = 200
ultimo_tempo = pygame.time.get_ticks()

# Sprite
pos_x = 10
pos_y = 10
velocidade = 2

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if botao.collidepoint(evento.pos):
                rodando = False

    # Armazena posição anterior
    anterior_x = pos_x
    anterior_y = pos_y

    # Movimento
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RIGHT]:
        pos_x += velocidade
    if teclas[pygame.K_LEFT]:
        pos_x -= velocidade
    if teclas[pygame.K_DOWN]:
        pos_y += velocidade
    if teclas[pygame.K_UP]:
        pos_y -= velocidade

    # Limita movimento dentro da tela
    pos_x = max(0, min(pos_x, largura - quadro_largura))
    pos_y = max(0, min(pos_y, altura - (quadro_altura - 52)))  # 52 é o offset usado na sprite

    # Retângulo do sprite na nova posição
    sprite_rect = pygame.Rect(pos_x, pos_y, quadro_largura, quadro_altura - 52)

    # Impede sobrepor o botão
    if sprite_rect.colliderect(botao):
        pos_x = anterior_x
        pos_y = anterior_y
        sprite_rect.x = pos_x
        sprite_rect.y = pos_y

    # Atualiza animação
    agora = pygame.time.get_ticks()
    if agora - ultimo_tempo > tempo_animacao:
        indice_quadro = (indice_quadro + 1) % num_quadros
        ultimo_tempo = agora

    # Desenha tudo
    tela.fill(branco)
    tela.blit(quadros[indice_quadro], (pos_x, pos_y))
    desenha_botao(tela, cinza, botao.topleft, botao.size, "Sair")

    pygame.display.flip()

pygame.quit()
sys.exit()
