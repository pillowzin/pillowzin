import pygame
from const import *

pygame.mixer.init()


class Explosion:
    def __init__(self, x, y, sprite_sheet):
        self.x = x
        self.y = y

        self.frames = []
        self.current_frame = 0
        self.frame_speed = 4
        self.frame_counter = 0
        self.finished = False

        frame_width = 32
        frame_height = 32

        # cortar o spritesheet
        for i in range(5):
            frame = sprite_sheet.subsurface(
                pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            )
            frame = pygame.transform.scale(
                frame, (frame.get_width() * 2, frame.get_height() * 2)
            )
            self.frames.append(frame)

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_speed:
            self.frame_counter = 0
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                self.finished = True

    def draw(self, screen):
        if not self.finished:
            screen.blit(self.frames[self.current_frame], (self.x, self.y))

    def is_finished(self):
        return self.finished
