import pygame
import random
import sys

# Inicialização
pygame.init()

# Tela
largura, altura = 500, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Moto Flex")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (50, 50, 50)
AMARELO = (255, 255, 0)
VERMELHO = (200, 0, 0)
FAIXA_CLARA = (255, 255, 150)

# Fonte
fonte = pygame.font.SysFont("Arial", 36)
fonte_titulo = pygame.font.SysFont("Arial", 60, bold=True)

# Moto
velocidade_moto = 5
moto_largura, moto_altura = 80, 120
moto_img = pygame.image.load("moto.png")
moto_img = pygame.transform.scale(moto_img, (moto_largura, moto_altura))

# Obstáculos
obstaculo_largura, obstaculo_altura = 60, 100
obstaculo_imgs = [pygame.image.load("cones.png")]
obstaculo_imgs = [pygame.transform.scale(img, (obstaculo_largura, obstaculo_altura)) for img in obstaculo_imgs]

class Obstaculo:
    def __init__(self):
        self.img = random.choice(obstaculo_imgs)
        self.largura, self.altura = self.img.get_size()
        self.x = random.randint(0, largura - self.largura)
        self.y = -self.altura
        self.vel = random.randint(4, 7)

    def mover(self, dificuldade):
        self.y += self.vel + dificuldade
        if self.y > altura:
            self.y = -self.altura
            self.x = random.randint(0, largura - self.largura)
            self.vel = random.randint(4, 7)
            self.img = random.choice(obstaculo_imgs)

    def desenhar(self):
        tela.blit(self.img, (self.x, self.y))

    def colidiu_com(self, moto_x, moto_y):
        return (
            moto_y < self.y + self.altura and
            moto_y + moto_altura > self.y and
            moto_x < self.x + self.largura and
            moto_x + moto_largura > self.x
        )

# Funções de tela
def mostrar_texto(texto, fonte, cor, x, y, centralizar=True):
    render = fonte.render(texto, True, cor)
    rect = render.get_rect(center=(x, y)) if centralizar else (x, y)
    tela.blit(render, rect)

def salvar_ranking(nome, pontuacao):
    try:
        with open("ranking.txt", "r") as f:
            linhas = f.readlines()
            scores = []
            for linha in linhas:
                if ":" in linha:
                    n, p = linha.strip().split(":")
                    scores.append((n.strip(), int(p.strip())))
    except FileNotFoundError:
        scores = []

    scores.append((nome, pontuacao))
    scores.sort(key=lambda x: x[1], reverse=True)

    with open("ranking.txt", "w") as f:
        for n, p in scores:
            f.write(f"{n}: {p}\n")

def tela_menu():
    while True:
        tela.fill(CINZA)
        mostrar_texto("MOTO FLEX", fonte_titulo, AMARELO, largura//2, 100)
        mostrar_texto("1 - Jogar", fonte, BRANCO, largura//2, 250)
        mostrar_texto("2 - Ranking", fonte, BRANCO, largura//2, 320)
        mostrar_texto("3 - Sair", fonte, BRANCO, largura//2, 390)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    return tela_nome()
                if evento.key == pygame.K_2:
                    return tela_ranking()
                if evento.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

def tela_nome():
    nome = ""
    ativo = True
    while ativo:
        tela.fill(PRETO)
        mostrar_texto("Digite seu nome:", fonte, AMARELO, largura//2, 200)
        pygame.draw.rect(tela, CINZA, (largura//2 - 150, 250, 300, 50))
        mostrar_texto(nome, fonte, BRANCO, largura//2, 275)
        mostrar_texto("Enter - Confirmar", fonte, BRANCO, largura//2, 400)
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nome != "":
                    return main(nome)
                elif evento.key == pygame.K_BACKSPACE:
                    nome = nome[:-1]
                else:
                    if len(nome) < 10 and evento.unicode.isprintable():
                        nome += evento.unicode

def tela_ranking():
    tela.fill(PRETO)
    mostrar_texto("Ranking", fonte_titulo, AMARELO, largura//2, 80)

    try:
        with open("ranking.txt", "r") as arquivo:
            linhas = arquivo.readlines()
            ultimos = linhas[:5]
    except FileNotFoundError:
        ultimos = ["Sem registros ainda"]

    y = 180
    for linha in ultimos:
        mostrar_texto(linha.strip(), fonte, BRANCO, largura//2, y)
        y += 50

    mostrar_texto("Pressione ESC para voltar", fonte, BRANCO, largura//2, altura - 80)
    pygame.display.update()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return tela_menu()

def tela_gameover(nome, pontuacao):
    tela.fill(PRETO)
    mostrar_texto("GAME OVER", fonte_titulo, VERMELHO, largura//2, 200)
    mostrar_texto(f"{nome}: {pontuacao}", fonte, BRANCO, largura//2, 300)
    mostrar_texto("Pressione R para Reiniciar", fonte, BRANCO, largura//2, 400)
    pygame.display.update()

    salvar_ranking(nome, pontuacao)

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return tela_menu()

# Jogo principal
def main(nome):
    moto_x = largura // 2 - moto_largura // 2
    moto_y = altura - moto_altura - 10
    pontuacao = 0
    obstaculos = [Obstaculo() for _ in range(3)]
    clock = pygame.time.Clock()
    rodando = True

    faixa_offset = 0
    dificuldade = 0

    while rodando:
        tela.fill(CINZA)

        # Faixas da pista
        faixa_altura = 60
        faixa_espaco = 40
        faixa_offset = (faixa_offset + 10 + dificuldade) % (faixa_altura + faixa_espaco)
        for i in range(-faixa_altura, altura, faixa_altura + faixa_espaco):
            pygame.draw.rect(tela, FAIXA_CLARA, (largura//2 - 5, i + faixa_offset, 10, faixa_altura))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimento da moto
        teclas = pygame.key.get_pressed()
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and moto_x > 0:
            moto_x -= velocidade_moto
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and moto_x < largura - moto_largura:
            moto_x += velocidade_moto

        # Desenha moto
        tela.blit(moto_img, (moto_x, moto_y))

        # Obstáculos
        for obstaculo in obstaculos:
            obstaculo.mover(dificuldade)
            obstaculo.desenhar()
            if obstaculo.colidiu_com(moto_x, moto_y):
                tela_gameover(nome, pontuacao)
                rodando = False

        # Pontuação e dificuldade
        pontuacao += 1
        if pontuacao % 500 == 0:
            dificuldade += 1

        mostrar_texto(f"Pontuação: {pontuacao}", fonte, BRANCO, 10, 10, centralizar=False)

        pygame.display.update()
        clock.tick(60)

# Inicia o jogo
tela_menu()
