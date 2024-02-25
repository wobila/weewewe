import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 1000
        self.slot = 0
        self.room = [0, 0]
        self.speed = 200

        self.image = pygame.image.load("mario.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def renewpos(self, dx, dy):
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)
        if self.x < 0:
            self.x = 1270
            self.room[0] -= 1
        if self.x > 1270:
            self.x = 0
            self.room[0] += 1
        if self.y > 720:
            self.y = 1
            self.room[1] -= 1
        if self.y < 0:
            self.y = 720
            self.room[1] += 1

    def display(self):

        screen = pygame.display.get_surface()
        screen.blit(self.image, self.rect)

    def melee_attack(self):
        pass

    def range_attack(self):
        pass


class Projectile:
    def __init__(self, x, y, direction, speed, image_path):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def move(self, dt):
        dx = self.speed * self.direction[0] * dt
        dy = self.speed * self.direction[1] * dt
        self.x += dx
        self.y += dy
        self.rect.center = (self.x, self.y)
