import pygame
import random
import math


class Enemy:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.speed = 100
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.hits = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)

    def move_towards_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        length = math.sqrt(dx ** 2 + dy ** 2)
        dx /= length
        dy /= length
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
