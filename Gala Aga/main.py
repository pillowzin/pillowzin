import pygame
import time
from const import *
from objects import *
from random import randint
from gameStates import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((wdt, hgt))
pygame.display.set_caption("GALA AGA")
clock = pygame.time.Clock()
wait_start_time = None
running = True

#objetos
player = Player('sprites/spaceship.png')
enemies = CriarInimigos(10)
bullets = []

#estados do jogo
game_state = 'menu'
effects_surface = None
stage = 0
bullet_cooldown = 0

#loop'do jogaaaaaaaaaao
while running:
	screen.fill((0, 0, 0))
	clock.tick(60)
	keys = pygame.key.get_pressed()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
				break

	if game_state == 'menu':
		effects_surface = MENU(screen, player, effects_surface)
		if keys[pygame.K_SPACE]:
			game_state = 'jogando'
	elif game_state == 'jogando':
		game_state, stage, bullet_cooldown = PLAYING(screen, player, enemies, bullets, stage, keys, bullet_cooldown)
	elif game_state == 'game_over':
		game_state, player, enemies, bullets, stage = GAMEOVER(screen, player, enemies, bullets, stage, keys)

	pygame.display.flip()

pygame.quit()
