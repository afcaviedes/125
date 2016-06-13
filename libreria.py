import pygame
import sys
from pygame.locals import *

pygame.init()

BLANCO = (255, 255, 255)
VERDE = (42, 142, 40)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)
NARANJA = (255, 181, 70)
MASTER = (24, 124, 123)
GRIS = (130, 130, 130)


fuente = pygame.font.Font(None, 35)
fuente1 = pygame.font.Font(None, 20)
fuente2 = pygame.font.Font(None, 30)
fuenteG = pygame.font.Font(None, 80)
fuenteP = pygame.font.Font(None, 50)

class Opcion:

    ver = False
    def __init__(self, texto, pos, valor, fuente, pantalla):
        self.texto = texto
        self.fuente = fuente
        self.valor = valor
        self.pos = pos
        self.setRect()
        self.dibujar(pantalla)

    def dibujar(self, pantalla):
        self.setRect()
        pantalla.blit(self.rend, self.rect)

    def setRend(self):
        self.rend = self.fuente.render(self.texto, True, self.getColor())

    def getColor(self):
        if(self.ver):
            return ROJO
        else:
            return BLANCO

    def setRect(self):
        self.setRend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
            
