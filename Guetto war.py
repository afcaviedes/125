# -*- coding: cp1252 -*-
from libreria import *

T_PANTALLA = (1000, 600) 

global INCREMENTO_MOV_HOR
INCREMENTO_MOV_HOR = 15

global FPS
global clock
global time_spent

def RelRect(actor, camara):
    return pygame.Rect(actor.rect.x-camara.rect.x, actor.rect.y-camara.rect.y, actor.rect.w, actor.rect.h)

class Camara(object): #CLASE PARA CENTRAR LA CÁMARA EN EL JUGADOR
    
    def __init__(self, pantalla, jugador, anchoNivel, largoNivel):
        self.jugador = jugador
        self.rect = pantalla.get_rect()
        self.rect.center = self.jugador.center
        self.mundo_rect = Rect(0, 0, anchoNivel, largoNivel)

    def actualizar(self):
      if self.jugador.centerx > self.rect.centerx + 25:
          self.rect.centerx = self.jugador.centerx - 25
          
      if self.jugador.centerx < self.rect.centerx - 25:
          self.rect.centerx = self.jugador.centerx + 25

      if self.jugador.centery > self.rect.centery + 25:
          self.rect.centery = self.jugador.centery - 25

      if self.jugador.centery < self.rect.centery - 25:
          self.rect.centery = self.jugador.centery + 25
      self.rect.clamp_ip(self.mundo_rect)

    def dibujarSprites(self, pantalla, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                pantalla.blit(s.imagen, RelRect(s, self))


class Obstaculo(pygame.sprite.Sprite): #CLASE PARA CREAR OBSTACULOS
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.image.load("Mundo/Obstaculo.png").convert()
        self.rect = self.imagen.get_rect()
        self.rect.topleft = [self.x, self.y]
        

class Puerta(pygame.sprite.Sprite): #CLASE PARA CREAR PUERTA
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.imagen = pygame.Surface([25, 25])
        self.imagen.fill(MASTER)
        self.rect = self.imagen.get_rect()
        self.rect.topleft = [self.x, self.y]

        

class Jugador(pygame.sprite.Sprite): #CLASE PARA EL JUGADOR Y SUS COLISIONES
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.vida = 100
        self.ganar = False
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.contacto = False
        self.salto = False
        self.imagen = pygame.image.load('Jugador1/5.png').convert()
        self.rect = self.imagen.get_rect()
        self.correrIzquierda = ["Jugador1/1.png", "Jugador1/2.png",
                                 "Jugador1/1.png", "Jugador1/2.png",
                                 "Jugador1/1.png", "Jugador1/2.png",
                                 "Jugador1/1.png", "Jugador1/2.png"]

        self.correrDerecha = ["Jugador1/3.png", "Jugador1/4.png",
                              "Jugador1/3.png", "Jugador1/4.png",
                              "Jugador1/3.png", "Jugador1/4.png",
                              "Jugador1/3.png", "Jugador1/4.png"]

        self.direccion = "derecha"
        self.rect.topleft = [x, y]
        self.frame = 0

        
    def menosVida1(self):
        self.vida -= 1

    def menosVida2(self):
        self.vida -= 5

    def menosVida3(self):
        self.vida = 0
        
    def actualizar(self, arriba, abajo, izquierda, derecha):
        if arriba:
            if self.contacto:
                if self.direccion == "derecha":
                    self.imagen = pygame.image.load("Jugador1/3.png")
                self.salto = True
                self.movy -= 20
        
        if not abajo and self.direccion == "derecha":
                self.imagen = pygame.image.load('Jugador1/5.png').convert_alpha()

        if not abajo and self.direccion == "izquierda":
            self.imagen = pygame.image.load('Jugador1/4.png').convert_alpha()

        if izquierda:
            self.direccion = "izquierda"
            self.movx = - INCREMENTO_MOV_HOR
            if self.contacto:
                self.frame += 1
                self.imagen = pygame.image.load(self.correrIzquierda[self.frame]).convert_alpha()
                if self.frame == 6:
                    self.frame = 0
            else:
                self.imagen = pygame.image.load("Jugador1/1.png").convert_alpha()

        if derecha:
            self.direccion = "derecha"
            self.movx = + INCREMENTO_MOV_HOR
            if self.contacto:
                self.frame += 1
                self.imagen = pygame.image.load(self.correrDerecha[self.frame]).convert_alpha()
                if self.frame == 6: self.frame = 0
            else:
                self.imagen = pygame.image.load("Jugador1/4.png").convert_alpha()

        if not (izquierda or derecha):
            self.movx = 0
        self.rect.right += self.movx

        self.colision(self.movx, 0, mundo)


        if not self.contacto:
            self.movy += 0.3
            if self.movy > 10:
                self.movy = 10
            self.rect.top += self.movy

        if self.salto:
            self.movy += 2
            self.rect.top += self.movy
            if self.contacto == True:
                self.salto = False

        self.contacto = False
        self.colision(0, self.movy, mundo)


    def colision(self, movx, movy, mundo):
        self.contacto = False
        for o in mundo:
            if self.rect.colliderect(o):
                if movx > 0:
                    self.rect.right = o.rect.left

                if movx < 0:
                    self.rect.left = o.rect.right

                if movy > 0:
                    self.rect.bottom = o.rect.top
                    self.movy = 0
                    self.contacto = True

                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0


class Enemigo1(pygame.sprite.Sprite): #CLASE PARA EL ENEMIGO 1 Y SUS COLISIONES
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.movy = 0
        self.x = x
        self.y = y
        self.contacto = False
        self.salto = False
        self.imagen = pygame.image.load('Enemigo1/saltarIzquierda.png').convert_alpha()
        self.rect = self.imagen.get_rect()
        self.rect.topleft = [x, y]
        

    def actualizar(self):
        if self.contacto:
            self.salto = True
            self.movy -= 20

        self.colision(0, mundo)

        if not self.contacto:
            self.movy += 0.3
            if self.movy > 10:
                self.movy = 10
            self.rect.top += self.movy

        if self.salto:
            self.movy += 2
            self.rect.top += self.movy
            if self.contacto == True:
                self.salto = False

        self.contacto = False
        self.colision(self.movy, mundo)


    def colision(self, movy, mundo):
        self.contacto = False
        for o in mundo:
            if self.rect.colliderect(o):
                if movy > 0:
                    self.rect.bottom = o.rect.top
                    self.movy = 0
                    self.contacto = True

                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0



class Enemigo2(pygame.sprite.Sprite): #CLASE PARA EL ENEMIGO 2 Y SUS COLISIONES
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.movy = 0
        self.movx = 0
        self.x = x
        self.y = y
        self.ciclo = False
        self.contacto = False
        self.salto = False
        self.imagen = pygame.image.load('Jugador/paradoDerecha.png').convert()
        self.rect = self.imagen.get_rect()
        self.correrIzquierda = ["Jugador/correrIzquierda0.png", "Jugador/correrIzquierda1.png",
                                 "Jugador/correrIzquierda2.png", "Jugador/correrIzquierda3.png",
                                 "Jugador/correrIzquierda4.png", "Jugador/correrIzquierda5.png",
                                 "Jugador/correrIzquierda6.png", "Jugador/correrIzquierda7.png"]

        self.correrDerecha = ["Jugador/correrDerecha0.png", "Jugador/correrDerecha1.png",
                              "Jugador/correrDerecha2.png", "Jugador/correrDerecha3.png",
                              "Jugador/correrDerecha4.png", "Jugador/correrDerecha5.png",
                              "Jugador/correrDerecha6.png", "Jugador/correrDerecha7.png"]

        self.direccion = "derecha"
        self.rect.topleft = [x, y]
        self.frame = 0

        

    def actualizar(self, X0, X1):
        if self.ciclo == False:
            derecha = True
            izquierda = False
        else:
            derecha = False
            izquierda = True

        if self.rect.x >= X1:
            self.ciclo = True
            
        if self.rect.x <= X0:
            self.ciclo = False
            

        if izquierda:
            self.direccion = "izquierda"
            self.movx = - INCREMENTO_MOV_HOR
            if self.contacto:
                self.frame += 1
                self.imagen = pygame.image.load(self.correrIzquierda[self.frame]).convert_alpha()
                if self.frame == 6:
                    self.frame = 0
            
        if derecha:
            self.direccion = "derecha"
            self.movx = + INCREMENTO_MOV_HOR
            if self.contacto:
                self.frame += 1
                self.imagen = pygame.image.load(self.correrDerecha[self.frame]).convert_alpha()
                if self.frame == 6: self.frame = 0
            
        if not (izquierda or derecha):
            self.movx = 0
        self.rect.right += self.movx

        self.colision(self.movx, 0, mundo)


        if not self.contacto:
            self.movy += 0.3
            if self.movy > 10:
                self.movy = 10
            self.rect.top += self.movy

        
        self.contacto = False
        self.colision(0, self.movy, mundo)


    def colision(self, movx, movy, mundo):
        self.contacto = False
        for o in mundo:
            if self.rect.colliderect(o):
                if movx > 0:
                    self.rect.right = o.rect.left

                if movx < 0:
                    self.rect.left = o.rect.right

                if movy > 0:
                    self.rect.bottom = o.rect.top
                    self.movy = 0
                    self.contacto = True

                if movy < 0:
                    self.rect.top = o.rect.bottom
                    self.movy = 0




class Enemigo3(pygame.sprite.Sprite): # CLASE PARA EL ENEMIGO 3
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.imagen = pygame.image.load('Enemigo3/baby.png').convert_alpha()
        self.rect = self.imagen.get_rect()
        self.rect.topleft = [x, y]
            



class Nivel(object): # CLASE PARA LEER EL MAPA Y CREAR EL NIVEL
    def __init__(self, archivo):
        self.nivel = []
        self.mundo = []
        self.enemigos1 = pygame.sprite.Group()
        self.enemigos2 = pygame.sprite.Group()
        self.enemigos3 = pygame.sprite.Group()
        self.puertas = pygame.sprite.Group()
        self.todos = pygame.sprite.Group()
        self.linea = open(archivo, "r")

    def crearNivel(self, x, y):
        for l in self.linea:
            self.nivel.append(l)

        for filas in self.nivel:
            for columnas in filas:
                if columnas == "X":
                    obstaculo = Obstaculo(x, y)
                    self.mundo.append(obstaculo)
                    self.todos.add(self.mundo)
                if columnas == "P":
                    self.jugador = Jugador(x, y)
                    self.todos.add(self.jugador)
                if columnas == "E":
                    self.enemigo1 = Enemigo1(x, y)
                    self.enemigos1.add(self.enemigo1)
                    self.todos.add(self.enemigo1)
                if columnas == "F":
                    self.enemigo2 = Enemigo2(x, y)
                    self.enemigos2.add(self.enemigo2)
                    self.todos.add(self.enemigo2)
                """if columnas == "B":
                    self.enemigo3 = Enemigo3(x, y)
                    self.enemigos3.add(self.enemigo3)
                    self.todos.add(self.enemigo3)"""
                if columnas == "T":
                    self.puerta = Puerta(x, y)
                    self.puertas.add(self.puerta)
                    self.todos.add(self.puerta)
                x += 25
            y += 25
            x = 0

    def getSize(self):
        lineas = self.nivel
        linea = max(lineas, key = len)
        self.ancho = (len(linea))*25
        self.largo = (len(lineas))*25
        return (self.ancho, self.largo)



#############################################################################################################

pantalla = pygame.display.set_mode(T_PANTALLA)
pantalla_rect = pantalla.get_rect()
fondo = pygame.image.load("Mundo/Fondo.jpg").convert_alpha()
fondo_rect = fondo.get_rect()

nivel = Nivel("Niveles/Nivel1.txt")
nivel.crearNivel(0,0)
mundo = nivel.mundo
jugador = nivel.jugador

camara = Camara(pantalla, jugador.rect, nivel.getSize()[0], nivel.getSize()[1])
todos = nivel.todos
enemigos1 = nivel.enemigos1
enemigos2 = nivel.enemigos2
enemigos3 = nivel.enemigos3
puertas = nivel.puertas

reloj = pygame.time.Clock()


def Jugar():

    arriba = abajo = izquierda = derecha = False
    x, y = 0, 0

    while True:

        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_UP:
                arriba = True
            if event.type == KEYDOWN and event.key == K_DOWN:
                abajo = True
            if event.type == KEYDOWN and event.key == K_LEFT:
                izquierda = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                derecha = True

            if event.type == KEYUP and event.key == K_UP:
                arriba = False
            if event.type == KEYUP and event.key == K_DOWN:
                abajo = False
            if event.type == KEYUP and event.key == K_LEFT:
                izquierda = False
            if event.type == KEYUP and event.key == K_RIGHT:
                derecha = False

        asize = ((pantalla_rect.w // fondo_rect.w + 1) * fondo_rect.w, (pantalla_rect.h // fondo_rect.h + 1) * fondo_rect.h)
        bg = pygame.Surface(asize)

        for x in range(0, asize[0], fondo_rect.w):
            for y in range(0, asize[1], fondo_rect.h):
                pantalla.blit(fondo, (x, y))

        reloj.tick(30)
        camara.dibujarSprites(pantalla, todos)

        jugador.actualizar(arriba, abajo, izquierda, derecha)
        for e in enemigos1:
            e.actualizar()

        for e in enemigos2:
            e.actualizar(3825, 5500)
        camara.actualizar()
        pygame.display.flip()

        col_obj1 = pygame.sprite.spritecollide(jugador, enemigos1, False)
        for ec in col_obj1:
            jugador.menosVida1()

        col_obj2 = pygame.sprite.spritecollide(jugador, enemigos2, False)
        for ec in col_obj2:
            jugador.menosVida2()

        col_obj3 = pygame.sprite.spritecollide(jugador, enemigos3, False)
        for ec in col_obj3:
            jugador.menosVida3()

        col_objG = pygame.sprite.spritecollide(jugador, puertas, False)
        for ec in col_objG:
            jugador.ganar = True


        puntos = fuente.render("VIDA:", True, BLANCO)
        puntos2 = fuente.render(str(jugador.vida) + "%", True, BLANCO)
        puntos_rect = puntos.get_rect()
        puntos_x = 15   
        puntos_y = 20
        puntos2_rect = puntos.get_rect()
        puntos2_x = 95
        pantalla.blit(puntos, [puntos_x, puntos_y])
        pantalla.blit(puntos2, [puntos2_x, puntos_y])

        if (jugador.vida == 0):
            pygame.display.quit()
            pantalla1 = pygame.display.set_mode(T_PANTALLA)
            texto = fuente.render("L U C H O   H A   M U E R T O", True, BLANCO)
            texto_rect = texto.get_rect()
            texto_x = pantalla1.get_width() / 2 - texto_rect.width / 2       
            texto_y = pantalla1.get_height() / 2 - texto_rect.height / 2
            pantalla1.blit(texto, [texto_x, texto_y])
            pygame.display.flip()

        if (jugador.ganar):
            pygame.display.quit()
            pantalla1 = pygame.display.set_mode(T_PANTALLA)
            texto = fuente.render("L U C H O   H A   E S C A P A D O", True, BLANCO)
            texto_rect = texto.get_rect()
            texto_x = pantalla1.get_width() / 2 - texto_rect.width / 2       
            texto_y = pantalla1.get_height() / 2 - texto_rect.height / 2
            pantalla1.blit(texto, [texto_x, texto_y])
            pygame.display.flip()

        pygame.display.flip()

#############################################################################################################

fuente = pygame.font.Font(None, 40)
fuente2 = pygame.font.Font(None, 24)

terminar = False
fMenu = pygame.font.Font("Cool.ttf", 50)
fMenuT = pygame.font.Font("Dragon.otf", 180)
rMenu = fMenuT.render("Guetto war", True, BLANCO)

Menu = [Opcion("JUGAR", (420, 280), 0, fMenu, pantalla),
        Opcion("SALIR", (428, 400), 2, fMenu, pantalla)]



while not terminar:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        terminar = True
        pantalla.fill((0, 0, 0))
        pantalla.blit(rMenu, [250, 30])
        
        for opcion in Menu:
                if opcion.rect.collidepoint(pygame.mouse.get_pos()):
                        opcion.ver=True
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                if(opcion.valor == 0):
                                    pygame.mouse.set_visible(0)
                                    Jugar()                                           
                                elif(opcion.valor == 2):
                                        terminar = True
                else:
                        opcion.ver = False
                opcion.dibujar(pantalla)
        pygame.display.flip()
pygame.quit()
