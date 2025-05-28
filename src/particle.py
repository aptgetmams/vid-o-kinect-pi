# -*- coding: utf-8 -*-
import random

class Particle:
    def __init__(self, pos, vel, color, lifespan=60):
        self.x, self.y = pos
        self.vx, self.vy = vel
        self.color = color
        self.lifespan = lifespan
        self.age = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.age += 1

    def is_alive(self):
        return self.age < self.lifespan

    def draw(self, surface):
        # alpha décroissant
        alpha = max(0, 255 * (1 - self.age / self.lifespan))
        col = (*self.color, int(alpha))
        import pygame
        # dessine un petit cercle
        s = pygame.Surface((8,8), pygame.SRCALPHA)
        pygame.draw.circle(s, col, (4,4), 4)
        surface.blit(s, (int(self.x)-4, int(self.y)-4))
