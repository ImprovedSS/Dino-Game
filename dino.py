import pygame
from pygame.locals import *
from sys import exit
import os #localização de pastas
from random import randrange, choice

pygame.init()
pygame.mixer.init()

#funções
def exibe_mensagem(msg, tamanho_fonte, cor):
    fonte = pygame.font.SysFont('comicsanssms', tamanho_fonte, True, False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem, True, cor) #não pode ser a "msg" direto, pois deve estar em formato de string
    return texto_formatado

def reiniciar_jogo():
    global pontos, velocidade_jogo, colidiu, escolha_obstaculo 
    pontos = 0 
    velocidade_jogo = 10
    colidiu = False
    escolha_obstaculo = choice([0, 1])
    cacto.rect.x = largura
    passaro.rect.x = largura
    dino.rect.y = dino.pos_y_inicial
    dino.pulo = False

#tela
largura = 640
altura = 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Dino Game")

#utilidades
relogio = pygame.time.Clock()
branco = (255, 255, 255)
preto = (0, 0, 0)
largura_altura_img = (32, 32)
velocidade_jogo = 10

#os
diretorio_principal = os.path.dirname(__file__)
diretorio_imagem = os.path.join(diretorio_principal, "Imagem")
diretorio_som = os.path.join(diretorio_principal, "Som")

#sprite sheet 
sprite_sheet = pygame.image.load(os.path.join(diretorio_imagem, "dinoSpritesheet.png")).convert_alpha() #ignora fundo da imagem, caso possível

#classes
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #iniciando utilitários
        self.sprites = []
        self.pulo = False 
        self.som_pulo = pygame.mixer.Sound(os.path.join(diretorio_som, "jump_sound.wav"))
        self.som_pulo.set_volume(1)
        for i in range(3):
            img = sprite_sheet.subsurface((i * 32, 0), (largura_altura_img)) #coordenadas, parâmetros de largura e altura
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.sprites.append(img)
        self.index_lista = 0 
        self.image = self.sprites[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) #adicionando uma máscara para colisões
        self.pos_y_inicial = altura - 64 - 96//2 #metade da altura do dino
        self.rect.center = (100, altura - 64)
    
    def update(self):
        if self.pulo == True:
            if self.rect.y <= 220:
                self.pulo = False
            else:
                self.rect.y -= 20
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20
            else:
                self.rect.y = self.pos_y_inicial
        if self.index_lista > 2:
            self.index_lista = 0
        self.index_lista += 0.25
        self.image = self.sprites[int(self.index_lista)]

    def pular(self):
        self.pulo = True 
        self.som_pulo.play()

class Nuvens(pygame.sprite.Sprite):
    def  __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((7 * 32, 0), (largura_altura_img))
        self.image = pygame.transform.scale(self.image, (32 * 3, 32 * 3))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = largura - randrange(30, 300, 90) 
    
    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
            self.rect.y = randrange(50, 200, 49)
        self.rect.x -= velocidade_jogo

class Chao(pygame.sprite.Sprite):
    def __init__(self, pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((6 * 32, 0), (largura_altura_img))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x * 64, altura - 64) #dimensões afetando

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= 10 #não recebe o velocidade_jogo, estava ocorrendo um bug

class Cacto(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((5 * 32, 0), (largura_altura_img))
        self.image = pygame.transform.scale(self.image, (32 * 2, 32 * 2))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image) #adicionando uma máscara para colisões
        self.rect.center = (largura + 32, altura - 64)
    
    def update(self):
        if escolha_obstaculo == 0:
            if self.rect.topright[0] <= 0:
                self.rect.x = largura
            self.rect.x -= velocidade_jogo

class Passaro(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite_passaro = []
        for i in range(3, 5):
            img = sprite_sheet.subsurface((i * 32, 0), (largura_altura_img))
            img = pygame.transform.scale(img, (32 * 3, 32 * 3))
            self.sprite_passaro.append(img)
        self.index_lista = 0
        self.image = self.sprite_passaro[self.index_lista]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (largura + 48, 240)

    def update(self):
        if escolha_obstaculo == 1:
            if self.rect.topright[0] < 0:
                self.rect.x = largura
            else:
                self.rect.x -= velocidade_jogo

            if self.index_lista > 1:
                self.index_lista = 0
            self.index_lista += 0.13
            self.image = self.sprite_passaro[int(self.index_lista)]

#grupo de sprites
all_sprites = pygame.sprite.Group()

#grupo de obstáculos do dinossauro
obstacles = pygame.sprite.Group()

#objeto / add in group
    #dino
dino = Dino()
all_sprites.add(dino)

    #nuvem
for i in range(4):
    nuvem = Nuvens()
    all_sprites.add(nuvem)

    #chão
for i in range(20): #largura*2 // 64
    chao = Chao(i)
    all_sprites.add(chao)

    #cacto
cacto = Cacto()
all_sprites.add(cacto)
obstacles.add(cacto)

    #pássaro
passaro = Passaro()
all_sprites.add(passaro)
obstacles.add(passaro)

#colisão
som_colisao = pygame.mixer.Sound(os.path.join(diretorio_som, "death_sound.wav"))
som_colisao.set_volume(1)
colidiu = False

#decisão de obstáculo
escolha_obstaculo = choice([0, 1])

#pontuação
pontos = 0
som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_som, "score_sound.wav"))
som_pontuacao.set_volume(1)




while True:
    relogio.tick(30)
    tela.fill(branco)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_UP or event.key == K_SPACE and colidiu == False:
                if dino.rect.y != dino.pos_y_inicial:
                    pass
                else:
                    dino.pular()
            if event.key == K_r and colidiu == True:
                reiniciar_jogo()

    colisoes = pygame.sprite.spritecollide(dino, obstacles, False, pygame.sprite.collide_mask)         
    all_sprites.draw(tela)

    if cacto.rect.topright[0] <= 0 or passaro.rect.topright[0] <= 0:
        escolha_obstaculo = choice([0, 1])
        cacto.rect.x, passaro.rect.x = largura, largura #isso garante que o choice seja usado apenas uma vez, pois o objeto fica fora do limite por tempo suficiente para acontecer várias iterações, algo que quebraria a lógica do código

    if colisoes and colidiu == False: #caso a lista contenha algo(ocorreu uma colisão) e o limitador não tenha sido acionado ainda, esse código será executado
        som_colisao.play()
        colidiu = True
    elif colidiu == True: 
        game_over = exibe_mensagem("GAME OVER", 40, preto)
        rect_game_over = game_over.get_rect()
        rect_game_over.center = (largura / 2, altura / 2)
        tela.blit(game_over, rect_game_over)
        restart = exibe_mensagem("Press R to restart", 22, preto)
        rect_restart = restart.get_rect()
        rect_restart.center = (largura / 2, altura / 2 + 20)
        tela.blit(restart, rect_restart)
    else: #impede "movimentação" das sprites/pausa o jogo
        pontos += 1
        all_sprites.update()
        texto_pontos = exibe_mensagem(pontos, 40, preto)
    
    tela.blit(texto_pontos, (520, 30)) #fica fora do else para continuar sendo escrita na tela

    if pontos % 100 == 0 and colidiu == False:
        som_pontuacao.play()
        if velocidade_jogo < 30: #otimizando código
            velocidade_jogo += 1
        
    

    pygame.display.flip()
