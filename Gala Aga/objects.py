import pygame
from random import randint
from const import *

pygame.init()
pygame.mixer.init()


class Enemy:
    margem_x = 10

    def __init__(self, sprite_sheet, frame_width, frame_height, x, y, speed):
        self.sprite_sheet = sprite_sheet
        self.frame_width = frame_width
        self.frame_height = frame_height

        self.num_frames = sprite_sheet.get_width() // frame_width
        self.current_frame = 0
        self.frame_speed = 6
        self.frame_counter = 0

        self.x = max(self.margem_x, min(x, wdt - self.margem_x - self.frame_width))
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, frame_width, frame_height)

        self.wobble_direction = 1
        self.wobble_count = 0

    def update_animation(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def move(self):
        self.y += self.speed

        self.wobble_count += 1
        if self.wobble_count >= 40:
            self.wobble_direction *= -1
            self.wobble_count = 0

        self.x += self.wobble_direction * 2
        self.x = max(self.margem_x, min(self.x, wdt - self.margem_x - self.frame_width))

        if self.y >= hgt:
            self.y = -100
            self.x = randint(self.margem_x, wdt - self.margem_x - self.frame_width)

        self.rect.topleft = (self.x, self.y)
        self.update_animation()

    def draw(self, screen):
        frame_rect = pygame.Rect(
            self.current_frame * self.frame_width,
            0,
            self.frame_width,
            self.frame_height,
        )
        print(f"Enemy draw - current_frame: {self.current_frame}, frame_rect: {frame_rect}, sprite_sheet size: {self.sprite_sheet.get_size()}")
        frame_img = self.sprite_sheet.subsurface(frame_rect)
        frame_img = pygame.transform.rotate(frame_img, 180)
        screen.blit(frame_img, (self.x, self.y))



# Carrega a sprite original
enemy_spritesheet = pygame.image.load("sprites/enemy.png")

# ESCALA antes de criar inimigos
scale_factor = 2.5  # ou 2.5 ou 3, como quiser
frame_width_original = 16
frame_height_original = 16
num_frames = 2  # quantos frames tem horizontalmente

# Calcula nova largura total
sprite_width_scaled = frame_width_original * num_frames * scale_factor
sprite_height_scaled = frame_height_original * scale_factor

enemy_spritesheet = pygame.transform.scale(
    enemy_spritesheet,
    (int(sprite_width_scaled), int(sprite_height_scaled))
)

# Atualiza frame_width e frame_height
frame_width = int(frame_width_original * scale_factor)
frame_height = int(frame_height_original * scale_factor)

def CriarInimigos(n):
    return [
        Enemy(
            enemy_spritesheet,
            frame_width,
            frame_height,
            randint(0, wdt - frame_width),
            randint(-100, 0),
            randint(2, 4) + randint(0, 3) / 2,
        )
        for _ in range(n)
    ]


class Player:
    def __init__(self, img_path):
        self.img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(
            self.img,
            (int(self.img.get_width() * 1.8), int(self.img.get_height() * 1.8)),
        )

        self.x, self.y = pygame.mouse.get_pos()
        self.rect = self.img.get_rect()
        self.mask = pygame.mask.from_surface(self.img)
        self.pontos = 0
        self.vida = 100
        self.laser_sound = pygame.mixer.Sound("sounds/laser_shoot.mp3")
        self.laser_sound.set_volume(0.2)

    def update(self):
        margem = 10

        self.x, self.y = pygame.mouse.get_pos()
        self.rect.center = (self.x, self.y)
        # Limite pro x
        if self.rect.left < margem:
            self.rect.left = margem
        if self.rect.right > wdt - margem:
            self.rect.right = wdt - margem

        # Limite pro y
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
