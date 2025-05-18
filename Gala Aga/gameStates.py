import pygame
import time
from random import randint
from objects import *
from const import *

pygame.mixer.init()

pygame.mixer.music.load('sounds/background_music.mp3')
pygame.mixer.music.set_volume(0.1)
points_font = pygame.font.Font('PressStart2P-Regular.ttf', 12)
stage_font = pygame.font.Font('PressStart2P-Regular.ttf', 12)

msg_render_pos = (0+20, randint(0+80, hgt//2))

waiting_next_stage = False
waiting_start_time = pygame.time.get_ticks()

def MENU(screen, player, effects_surface):
	if not pygame.mixer.music.get_busy():
		pygame.mixer.music.play(-1)

	def MainMenu():
		nonlocal effects_surface
		title_font = pygame.font.Font('PressStart2P-Regular.ttf', 36)
		subtitle_font = pygame.font.Font('PressStart2P-Regular.ttf', 10)
		start_font = pygame.font.Font('PressStart2P-Regular.ttf', 10)

		titleA = title_font.render("GALA", True, (255, 30, 0))
		titleB = title_font.render("AGA", True, (0, 30, 255))
		credit_text = subtitle_font.render("feito por jakezin", True, (255, 255, 255))

		current_time = pygame.time.get_ticks()
		show_start = (current_time // 500) % 2 == 0

		if effects_surface is None:
			effects_surface = pygame.Surface((wdt, hgt))
			effects_surface.fill((0, 0, 0))
			for i in range(200):
				pygame.draw.rect(
					effects_surface, 
					(randint(0, 255), randint(0, 255), randint(0, 255)), 
					(randint(0, wdt), randint(0, hgt), 2, 2)
				)

		screen.fill((0, 0, 0))
		screen.blit(effects_surface, (0, 0))

		screen.blit(titleA, (wdt // 2 - titleA.get_width() // 2, hgt // 8))
		screen.blit(titleB, (wdt // 2 - titleB.get_width() // 2, hgt // 8 + 40))
		screen.blit(player.img, (titleA.get_width() // 2 + 50, hgt // 8 + 35))
		screen.blit(player.img, (titleA.get_width() // 2 + titleA.get_width() + 80, hgt // 8 + 35))

		if show_start:
			start_text = start_font.render("Pressione 'SPACE' para Iniciar", True, (255, 255, 0))
			shadow = start_font.render("Pressione 'SPACE' para Iniciar", True, (0, 0, 0))
			x = wdt // 2 - start_text.get_width() // 2
			y = hgt // 4 + 40
			screen.blit(shadow, (x + 2, y + 2))
			screen.blit(start_text, (x, y))

		screen.blit(credit_text, (wdt // 2 - credit_text.get_width() // 2, hgt // 3.8))

	MainMenu()
	return effects_surface


def PLAYING(screen, player, enemies, bullets, stage, keys, bullet_cooldown):
	global waiting_next_stage, waiting_start_time
	pygame.mouse.set_visible(False)

	stage_render = stage_font.render(f"STAGE {stage}", True, (255, 255, 255))
	vidas_font = pygame.font.Font('PressStart2P-Regular.ttf', 12)
	vidas_render = vidas_font.render(f"VIDAS {player.vida}", True, (255, 0, 0))
	points_render = points_font.render(f"PONTOS {player.pontos}", True, (255, 255, 255))	
	perk_font = pygame.font.Font('PressStart2P-Regular.ttf', 12)
	perk_render = perk_font.render('+ VIDA!', True, (255, 255, 0))

	#desenha o player
	player.update()
	player.draw(screen) 
	#desenha o hud
	screen.blit(points_render, (wdt // 2 - 180, 30))
	screen.blit(stage_render, (wdt // 2 - 40, 30))
	screen.blit(vidas_render, (wdt // 2 + 80, 30))	

	#tirozinho pew pew
	if bullet_cooldown == 0 and keys[pygame.K_q]:
		player.laser_sound.play()
		bullets.append(Bullet(player.rect.centerx-3, player.rect.top))
		bullet_cooldown = 10	

	if bullet_cooldown > 0:
		bullet_cooldown -= 1	

	#colisao do inimigo com o player
	for enemy in enemies[:]:
		if player.rect.colliderect(enemy.rect):
			player.vida -= 10
			enemies.remove(enemy)
			vidas_render = vidas_font.render(f"VIDAS {player.vida}", True, (255, 0, 0))
			if player.vida == 0:
				return 'game_over', stage, bullet_cooldown	

	#colisao do inimigo com a bala
	for enemy in enemies:
		enemy.move()
		enemy.draw(screen)	

	for bullet in bullets[:]:
		bullet.move()
		bullet.draw(screen) 
		if bullet.off_screen(hgt):
			bullets.remove(bullet)
			continue	
		for enemy in enemies[:]:
			if bullet.collide(enemy):
				enemies.remove(enemy)
				player.pontos += 1
				if bullet in bullets:
					bullets.remove(bullet)
				break	

	#conta os inimigos e respawna eles
	if len(enemies) == 0 and not waiting_next_stage:
		waiting_next_stage = True
		waiting_start_time = pygame.time.get_ticks()
		return 'jogando', stage, bullet_cooldown

#	perk_font = pygame.font.Font('PressStart2P-Regular.ttf', 12)

	#tempinho antes de spawnar os bixo
	if waiting_next_stage:
		if pygame.time.get_ticks() - waiting_start_time >= 2000:
			stage += 1
			player.vida += 20
			perk_render = perk_font.render('+ VIDA!', True, (255, 255, 0))
			#extende a lista dos enemies e cria mais outros, spawn
			enemies.extend(CriarInimigos(10 * stage // 2))
			waiting_next_stage = False

		for enemy in enemies:
			enemy.speed += 2*stage//2
		msg_font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
		msg_render = msg_font.render('Próxima Fase!', True, (255, 255, 255))

		screen.blit(msg_render, (msg_render_pos))

	return 'jogando', stage, bullet_cooldown


def GAMEOVER(screen, player, enemies, bullets, stage, keys):
	pygame.mixer.music.stop()
	screen.fill((0, 0, 0))
	pygame.mouse.set_visible(True)

	game_over_font = pygame.font.Font('PressStart2P-Regular.ttf', 20)
	game_over_render = game_over_font.render("GAME OVER", True, (255, 255, 255))

	try_font = pygame.font.Font('PressStart2P-Regular.ttf', 12)
	try_render = try_font.render('Aperte R para tentar novamente.', False, (255, 255, 0))

	screen.blit(game_over_render, (wdt // 2 - 100, hgt // 2 - 180))
	screen.blit(try_render, (wdt // 2 - 180, hgt // 2 - 100))

	if keys[pygame.K_r]:
		pygame.mixer.music.play(-1)
		player = Player('sprites/spaceship.png')
		enemies = CriarInimigos(10)
		bullets.clear()
		stage = 0
		player.vida = 100
		player.pontos = 0
		return 'jogando', player, enemies, bullets, stage

	return 'game_over', player, enemies, bullets, stage
