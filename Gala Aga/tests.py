import pygame

pygame.init()

screen = pygame.display.set_mode((500, 500))

enemy_spritesheet = pygame.image.load("sprites/enemy.png")
enemy_spritesheet = pygame.transform.scale(
    enemy_spritesheet,
    (
        int(enemy_spritesheet.get_width() * 2.5),
        int(enemy_spritesheet.get_height() * 2.5),
    ),
)

frame_width = int(16 * 2.5)
frame_height = int(16 * 2.5)

running = True
current_frame = 0
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    frame_rect = pygame.Rect(current_frame * frame_width, 0, frame_width, frame_height)
    frame_img = enemy_spritesheet.subsurface(frame_rect)
    screen.blit(frame_img, (100, 100))

    current_frame = (current_frame + 1) % (enemy_spritesheet.get_width() // frame_width)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
