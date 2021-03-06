"""Esta implementacao foi baseada no jogo Snakey feito e referido no livro "Invent Your Own Computer Games with Python" em http://inventwithpython.com e foi usado o pygame - http://pygame.org ."""

###########
# Imports #
###########

""" Aqui sao importados os modulos necessarios ao funcionamento do programa dos
quais se destaca o modulo pygame. O pygame.locals contem todas as constantes
necessarias como MOUSEMOTION, MOUSEBUTTONUP, QUIT, entre outras. Ora este import
constitui apenas uma maneira de facilitar a escrita, por exemplo, em vez de
escrever pygame.locals.QUIT podemos apenas escrever QUIT."""
import random, pygame, sys
from pygame.locals import *

########################
# Constantes/Variáveis #
########################

"""Estas variaveis constantes determinam valores fundamentais para o jogo.
Usando estas constantes em vez de usar os valores directamente sem os atribuir
a uma variavel, e mais facil fazer mudancas visto que so temos de mudar os
valores num sitio - onde sao atribuidos os mesmos a variaveis. Neste jogo
optamos por dividir a janela em celulas(quadrados) que sao areas onde os
segmentos da cobra e do rato podem existir."""

FPS = 14
compJanela = 640 # comprimento da janela em pixels
altJanela = 480 # altura da janela em pixels
tamCel = 20   # tamanho das celulas da janela em pixels 

"""O comprimento da janela e a altura da janela teem que ser multiplos do tamanho
das celulas(quadrados) existentes na grelha """
assert compJanela % tamCel == 0 
assert altJanela % tamCel == 0
compCelulas = int(compJanela / tamCel)
altCelulas = int(altJanela / tamCel)

"""Aqui sao colocados valores constantes para as diferentes cores existentes.
O pygame utiliza tuplos de 3 inteiros para representar cores que servem para
determinar a quantidade de vermelho, verde e azul na cor(RGB)."""
#             R    G    B
BRANCO    = (255, 255, 255)
PRETO     = (  0,   0,   0)
VERMELHO  = (255,   0,   0)
VERDEESCURO= (  0, 100,   0)
AZUL      = (  0,   0, 180)
VERDE     = (  0, 155,   0)
CINZENTO1 = ( 40,  40,  40)
CINZENTO2 = (128, 128, 128)
CORFUNDO  = PRETO


UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # indice da cabeça da cobra

def base():
    """funcao, onde o programa comeca, para a inicializacao do modulo, da janela
    para o jogo e do loop principal. Como as variaveis FPSCLOCK, DISPLAYSURF e
    BASICFONT sao definidas dentro desta funcao, estas sao variaveis locais da
    funcao base() e estas variaveis nao vao existir fora desta funcao, logo
    declarando-as como globais estamos a dizer ao python que queremos que estas
    variaveis sejam globais para serem utilizadas por outras funcoes"""
    
    global FPSCLOCK, DISPLAYSURF, BASICFONT, topScore

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((compJanela, altJanela))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
    pygame.display.set_caption('Hungry Python')

    ecrainicial()

    topScore = 0
    while True:
        correrjogo()
        scoreFinal = (len(cobraCoords) - 3)*10
        if topScore < scoreFinal:
            topScore = scoreFinal
        mostrargameover()
        
            

def correrjogo():
    global cobraCoords
    """ Estabelece um ponto de inicio da cobra """
    startx = random.randint(5, compCelulas - 6)
    starty = random.randint(5, altCelulas - 6)
    cobraCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    """ Estabelece um ponto aleatorio para o rato aparecer """
    ratoal = locinicial()

    while True: # loop principal do jogo
        for event in pygame.event.get(): # loop para verificar os eventos
            if event.type == QUIT:
                sair()
            elif event.type == KEYDOWN:
                if (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif event.key == K_ESCAPE:
                    sair()

        """ verifica se a cobra chegou aos limites da janela ou se se mordeu a
        si propria """ 
        if cobraCoords[HEAD]['x'] == -1 or cobraCoords[HEAD]['x'] == compCelulas or cobraCoords[HEAD]['y'] == -1 or cobraCoords[HEAD]['y'] == altCelulas:
            return # game over
        for cobraBody in cobraCoords[1:]:
            if cobraBody['x'] == cobraCoords[HEAD]['x'] and cobraBody['y'] == cobraCoords[HEAD]['y']:
                return # game over

        """ verifica se a cobra comeu um rato """
        if cobraCoords[HEAD]['x'] == ratoal['x'] and cobraCoords[HEAD]['y'] == ratoal['y']:
            """ quando a celula correspondente a cabeca esta na mesma posicao
             da celula do rato a celula que corresponde a cauda nao e removida"""
            ratoal = locinicial() # encontra uma nova localizacao aleatoria para o rato
        else:
            del cobraCoords[-1] # retira o segmento correspondente a cauda

        """ continua o movimento da cobra adicionando uma celula na direcao em
            que esta se esta a movimentar """
        if direction == UP:
            newHead = {'x': cobraCoords[HEAD]['x'], 'y': cobraCoords[HEAD]['y'] - 1}
        elif direction == LEFT:
            newHead = {'x': cobraCoords[HEAD]['x'] - 1, 'y': cobraCoords[HEAD]['y']}
        elif direction == DOWN:
            newHead = {'x': cobraCoords[HEAD]['x'], 'y': cobraCoords[HEAD]['y'] + 1}
        elif direction == RIGHT:
            newHead = {'x': cobraCoords[HEAD]['x'] + 1, 'y': cobraCoords[HEAD]['y']}
        cobraCoords.insert(0, newHead)
        DISPLAYSURF.fill(CORFUNDO)
        
        cobra(cobraCoords)
        rato(ratoal)
        pontuacao((len(cobraCoords) - 3)*10)
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
""" Funcao que mostra a mensagem para pressionar uma tecla."""
def teclamsg():  
    pressKeySurf = BASICFONT.render('Pressione uma tecla.', True, CINZENTO1)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topright = (compJanela - 222, altJanela - 40)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

""" funcao para verificar se foi pressionada alguma tecla."""
def tecla():  
    if len(pygame.event.get(QUIT)) > 0:
        sair()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        sair()
    return keyUpEvents[0].key

"""Funcao que mostra o ecra inicial"""
def ecrainicial():

    titleFont = pygame.font.SysFont('georgia', 50)
    titleSurf = titleFont.render('Hungry Python', True, AZUL)

    graus = 0
    
    while True:
        fundo = pygame.image.load('Awesome-snake-02-525x420.jpg')
        fundoRect = fundo.get_rect()
        DISPLAYSURF.blit(fundo, fundoRect)
        
        rotatedSurf = pygame.transform.rotate(titleSurf, graus)
        rotatedRect = rotatedSurf.get_rect()
        rotatedRect.center = (compJanela / 2, altJanela / 2)
        DISPLAYSURF.blit(rotatedSurf, rotatedRect)
        
        pygame.draw.ellipse(DISPLAYSURF, AZUL, rotatedRect, 2)

        teclamsg()

        if tecla():
            pygame.event.get() # verificar se ocorreu algum evento
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        graus += 5 # rodar 5 graus por cada frame


def sair():
    """Funcao para terminar o programa"""
    pygame.quit()
    sys.exit()
 
""" Esta funcao encontra uma localizacao aleatoria para iniciar a cobra"""
def locinicial(): 
    return {'x': random.randint(0, compCelulas - 1), 'y': random.randint(0, altCelulas - 1)}

""" Funcao que mostra o ecra de game over apos a cobra se ter mordido a si
propria ou ter chegado aos limites da janela"""
def mostrargameover():
    gameOverFont = pygame.font.SysFont('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, VERMELHO)
    overSurf = gameOverFont.render('Over', True, VERMELHO)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (compJanela / 2, 120)
    overRect.midtop = (compJanela / 2, gameRect.height + 120)
    
    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    teclamsg()
    pygame.display.update()
    pygame.time.wait(500)
    tecla() # verificar se foi pressionada alguma tecla durante a execução do jogo
    
    while True:
        if tecla():
            pygame.event.get() # limpar o ecra de game over 
            return
        
""" Funcao que mostra, durante o jogo, a pontuacao """
def pontuacao(score):
    topscoreSurf = BASICFONT.render('Pontuação Máx: %s' % (topScore), True, AZUL)
    topscoreRect = topscoreSurf.get_rect()
    topscoreRect.topright = (600, 20)
    DISPLAYSURF.blit(topscoreSurf, topscoreRect)
    
    scoreSurf = BASICFONT.render('Pontuação: %s' % (score), True, AZUL)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topright = (175, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    
""" Funcao que desenha a cobra """
def cobra(cobraCoords):
    for coord in cobraCoords:
        x = coord['x'] * tamCel
        y = coord['y'] * tamCel
        cobraSegmentRect = pygame.Rect(x, y, tamCel, tamCel)  
        pygame.draw.rect(DISPLAYSURF, VERDE, cobraSegmentRect)
        if coord == cobraCoords[HEAD]:
            cobraCabecaRect = pygame.Rect(x+4, y+4, tamCel - 8, tamCel - 8)
            pygame.draw.rect(DISPLAYSURF, VERDEESCURO, cobraCabecaRect)

"""Funcao que desenha o rato"""
def rato(coord):
    x = coord['x'] * tamCel
    y = coord['y'] * tamCel
    ratoRect = pygame.Rect(x, y, tamCel, tamCel)
    pygame.draw.rect(DISPLAYSURF, CINZENTO2, ratoRect)

if __name__ == '__main__':
    base()
