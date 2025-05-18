import pygame
from random import randint
from const import *

pygame.init()
pygame.mixer.init()
img_path = 'Gala Aga/sprites/'

class Enemy:
	margem_x = 10
	def __init__(self, img, x, y, speed):
		self.img = img
		self.x = max(self.margem_x, min(x, wdt-self.margem_x-img.get_width()))
		self.y = y
		self.speed = speed
		self.rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
		self.img = pygame.transform.rotate(self.img, 180)


	def move(self):
		self.y += self.speed
		self.rect.topleft = (self.x, self.y)
		if self.y >= hgt:
			self.y = -100
			self.x = randint(self.margem_x, wdt-self.margem_x - self.img.get_width())
		self.rect.topleft = (self.x, self.y)

	def draw(self, screen):
		screen.blit(self.img, (self.x, self.y))


enemy_img = pygame.image.load('sprites/enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (int(enemy_img.get_width()*2.5), int(enemy_img.get_height()*2.5)))

def CriarInimigos(n):
	return [Enemy(enemy_img, randint(0, wdt), randint(-100, 0), randint(2, 4) + randint(0, 3)/2) for _ in range(n)]


class Player:
	def __init__(self, img_path):
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(
		self.img, (int(self.img.get_width()*1.8), 
		int(self.img.get_height()*1.8)))

		self.x, self.y = pygame.mouse.get_pos()
		self.rect = self.img.get_rect()
		self.mask = pygame.mask.from_surface(self.img)
		self.pontos = 0
		self.vida = 100
		self.laser_sound = pygame.mixer.Sound('sounds/laser_shoot.mp3')
		self.laser_sound.set_volume(0.2)

	def update(self):
		margem = 10

		self.x, self.y = pygame.mouse.get_pos()
		self.rect.center = (self.x, self.y)
		#pro x
		if self.rect.left < margem:
			self.rect.left = margem
		if self.rect.right > wdt - margem:
			self.rect.right = wdt - margem
		
		#pro y de baixo agora
		if self.rect.bottom > hgt - margem:
			self.rect.bottom = hgt - margem
		
		self.x, self.y = self.rect.center
	
	def draw(self, screen):
		screen.blit(self.img, self.rect.topleft)


class Bullet:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.speed = 10
		self.color = (255, 45, 0)
		self.width = 5
		self.height = 10


	def move(self):
		self.y -= self.speed


	def draw(self, screen):
		pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


	def off_screen(self, height):
		return self.y < 0 or self.y > height


	def collide(self, enemy):
		bullet_rect = pygame.Rect(self.x, self.y, self.width, self.height)
		return bullet_rect.colliderect(enemy.rect)

