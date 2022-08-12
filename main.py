import pygame # Importamos la librería Pygame
from pygame.locals import * # Con esto estamos importando todos los módulos locales de Pygame

pygame.init()

clock = pygame.time.Clock() # Para que se repita la imagen cada cierto tiempo
fps = 60

# Tamaño de ventana
ancho = 864
alto = 936

ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Flappy Bird')


# Definimos las variables del juego.
posicion_suelo = 0
suelo_velocidad = 4

#Cargando imagenes
bg = pygame.image.load('img/bg.png')
suelo = pygame.image.load('img/ground.png')

run = True
while run:

	clock.tick(fps)     # Este método nos ayudará a manejar la tasa de fotogramas del programa

	# Agregamos el fondo
	ventana.blit(bg, (0,0))

	#Dibujamos y desplazamos el suelo
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