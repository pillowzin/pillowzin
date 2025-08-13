import pygame
import time
from const import *
from objects import *
from random import randint
from gameStates import *
from enemyFactory import get_inimigos_para_fase

pygame.init()
pygame.mixer.init()

window_icon = pygame.image.load('misc/icon.ico')
pygame.display.set_icon(window_icon)
screen = pygame.display.set_mode((wdt, hgt))

pygame.display.set_caption("GALA AGA")
clock = pygame.time.Clock()
wait_start_time = None
running = True

# objetos
player = Player('sprites/spaceship.png')
stage = 1
enemies = get_inimigos_para_fase(stage)
bullets = []

# estados do jogo
game_state = 'menu'
effects_surface = None
bullet_cooldown = 0

# efeito de explosao
explosion_spritesheet = pygame.image.load('sprites/explosion.png').convert_alpha()
explosions = []

# loop do jogo
while running:
    screen.fill((0, 0, 0))
    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    if game_state == 'menu':
        effects_surface = MENU(screen, player, effects_surface)
        if keys[pygame.K_SPACE]:
            game_state = 'jogando'

    elif game_state == 'jogando':
        game_state, stage, bullet_cooldown = PLAYING(
            screen, player, enemies, bullets, stage, keys, bullet_cooldown,
            explosion_spritesheet, explosions, clock
        )
        if game_state == 'stage_cleared':
            game_state = 'stage_cleared_state'
            waiting_next_stage = False  # garante que o timer comece do zero

    elif game_state == 'stage_cleared_state':
        acabou = STAGE_CLEARED(screen)
        if acabou:
            stage += 1
            player.vida += 20
            enemies.clear()
            enemies.extend(get_inimigos_para_fase(stage))

            for enemy in enemies:
                enemy.speed += 2 * stage // 2

            game_state = 'jogando'
    elif game_state == 'game_complete':
        game_state = GAME_COMPLETE(screen, player, keys)

    elif game_state == 'game_over':
        game_state, player, enemies, bullets, stage = GAMEOVER(screen, player, enemies, bullets, stage, keys)

    pygame.display.flip()

pygame.quit()