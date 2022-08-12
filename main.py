import pygame       #Importamos la librería Pygame
from pygame.locals import *     #Con esto estamos todos los módulos locales de Pygame

pygame.init()

clock = pygame.time.Clock()     
fps = 60        

#Tamaño de la ventana :D 
ancho = 864
alto = 936

ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Flappy Bird')



#Cargamos las imagenes. 
bg = pygame.image.load('img/bg.png')
suelo = pygame.image.load('img/ground.png')

posicion_suelo = 0
suelo_velocidad = 4


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

    def update(self):

        # Manejamos la animación, este será un bucle de 3 sprites que cambiará de sprite cada 5 frames.
        self.counter += 1
        flap_cooldown = 5

        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]


bird_group = pygame.sprite.Group()

flappy = Bird(100, int(alto / 2))

bird_group.add(flappy)


run = True
while run:

    clock.tick(fps)     #Este método nos ayudará a manejar la tasa de fotogramas del programa

    # Agregamos el fondo 
    ventana.blit(bg, (0,0))

    bird_group.draw(ventana)
    bird_group.update()

    # Agregando el suelo
    ventana.blit(suelo, (posicion_suelo, 768))
    posicion_suelo -= suelo_velocidad
    if abs(posicion_suelo) > 35:
        posicion_suelo = 0

    # Para cerrar el programa, se deberá presionar la X de la ventana de Windows
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()