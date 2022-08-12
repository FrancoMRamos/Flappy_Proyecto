import pygame       # Importamos la librería Pygame
from pygame.locals import *     # Con esto estamos todos los módulos locales de Pygame
import random       # Importamos la librería Random

pygame.init()

clock = pygame.time.Clock()     # Para que se repita la imagen cada cierto tiempo
fps = 60        

# Tamaño de ventana
ancho = 864
alto = 936

ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Flappy Bird')

# Fuenta a mostrar para el puntaje
fuente_boton = pygame.font.SysFont('Montserrat ExtraBold', 60)
fuente_record = pygame.font.SysFont('Montserrat ExtraBold', 20)
blanco = (255, 255, 255)

# Definimos las variables del juego.
posicion_suelo = 0
suelo_velocidad = 4
volar = False
game_over = False
tuberia_espaciado = 150         #px
tuberia_frecuencia = 1500        #milisegundos
tuberia_ultima = pygame.time.get_ticks() - tuberia_frecuencia
puntaje = 0
tuberia_superada = False

# Cargamos las imagenes
bg = pygame.image.load('img/bg.png')
suelo = pygame.image.load('img/ground.png')

def mostrar_puntaje(texto, fuente, text_col, x, y):
    img = fuente.render(texto, True, text_col)
    ventana.blit(img, (x,y))

# Realizamos una clase para el pájaro, en la que están los 3 sprites del mismo que nos ayudarán para su animación.
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.gravedad = 0
        self.clicked = False

    def update(self):

        if volar == True:
            # Velocidad de gravedad
            self.gravedad += 0.5
            if self.gravedad > 8:           # Limitando el incrementro excesivo de la gravedad
                self.gravedad = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.gravedad)

        if game_over == False:
            # Salto del personaje
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.gravedad = -10
                self.clicked = True            #Bandera para la función al presionar click
                

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Manejamos la animación, este será un bucle de 3 sprites que cambiará de sprite cada 5 frames.
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]
                
            # Rotacipon del personaje
            self.image = pygame.transform.rotate(self.images[self.index], self.gravedad*-2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

# Realizamos una clase para las tuberias
class Tuberia(pygame.sprite.Sprite):
    def __init__(self, x, y, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        # position 1 es desde arriba y -1 desde el suelo
        if posicion == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(tuberia_espaciado/2)] 
        if posicion == -1:
            self.rect.topleft = [x, y + int(tuberia_espaciado/2)]
    
    def update(self):
        self.rect.x -= suelo_velocidad
        if self.rect.right < 0:
            self.kill()         #eliminacion de las tuberias sobrantes

bird_group = pygame.sprite.Group()
tuberia_group = pygame.sprite.Group()

flappy = Bird(100, int(alto / 2))
bird_group.add(flappy)

run = True
while run:

    clock.tick(fps)     # Este método nos ayudará a manejar la tasa de fotogramas del programa

    # Agregamos el fondo
    ventana.blit(bg, (0,0))

    bird_group.draw(ventana)
    bird_group.update()
    tuberia_group.draw(ventana)

    # Agregando el suelo 
    ventana.blit(suelo, (posicion_suelo, 768))

    if len(tuberia_group) > 0: 
        if bird_group.sprites()[0].rect.left > tuberia_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < tuberia_group.sprites()[0].rect.right\
            and tuberia_superada == False:
            tuberia_superada = True

        if tuberia_superada == True:
            if bird_group.sprites()[0].rect.left > tuberia_group.sprites()[0].rect.right:
                puntaje += 1

                tuberia_superada = False

    mostrar_puntaje(str(puntaje),fuente_boton, blanco, int(ancho/2), 20)
    # Colision con las tuberias
    if pygame.sprite.groupcollide(bird_group, tuberia_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # Verificacion del personaje en el suelo 
    if flappy.rect.bottom >= 768:
        game_over = True
        volar = False

    if game_over == False and volar == True:
        # creacion nuevas tuberias
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tuberia_ultima > tuberia_frecuencia:
            altura_tuberia = random.randint(-100, 100)
            btm_tuberia = Tuberia(ancho, int(alto / 2) + altura_tuberia, -1)
            top_tuberia = Tuberia(ancho, int(alto / 2) + altura_tuberia, 1)
            tuberia_group.add(btm_tuberia)
            tuberia_group.add(top_tuberia)
            tuberia_ultima = tiempo_actual

        # Agregando movimiento al suelo  
        posicion_suelo -= suelo_velocidad
        if abs(posicion_suelo) > 35:
            posicion_suelo = 0

        tuberia_group.update()

    # Para cerrar el programa, se deberá presionar la X de la ventana de Windows
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and volar == False and game_over == False:   #condicion de inicio
            volar = True

    pygame.display.update()

pygame.quit()