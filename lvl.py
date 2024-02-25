import pygame
import random


class Level:
    def __init__(self, size):
        self.size = size
        self.grid = [[None] * size for _ in range(size)]

    def generate_path(self):
        pos = [0, 0]
        self.grid[pos[0]][pos[1]] = 'C'
        directions = ['up', 'down', 'right', 'left']
        while pos[0] < self.size - 1 and pos[1] < self.size - 1:
            done = False
            while not done:
                direct = random.choice(directions)
                if direct == 'up':
                    try:
                        if pos[0] - 1 > 0:
                            pos[0] -= 1
                            self.grid[pos[0]][pos[1]] = 'C'
                            done = True
                    except IndexError:
                        continue
                elif direct == 'down':
                    try:
                        pos[0] += 1
                        self.grid[pos[0]][pos[1]] = 'C'
                        done = True
                    except IndexError:
                        continue
                elif direct == 'right':
                    try:
                        pos[1] += 1
                        self.grid[pos[0]][pos[1]] = 'C'
                        done = True
                    except IndexError:
                        continue
                elif direct == 'left':
                    try:
                        if pos[1] - 1 > 0:
                            pos[1] -= 1
                            self.grid[pos[0]][pos[1]] = 'C'
                            done = True
                    except IndexError:
                        continue
        self.generate_rooms()

    def generate_rooms(self):
        self.grid[0][0] = 'S'
        roomtypes = ['R', 'C']
        lastroom = [0, 0]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 'C':
                    self.grid[i][j] = random.choice(roomtypes)
                    lastroom = [i, j]
        self.grid[lastroom[0]][lastroom[1]] = 'E'

    def drawroom(self, roomindex):
        type = self.grid[roomindex[0]][roomindex[1]]
        if type == 'S':
            self.surface = pygame.Surface((0, 0))
            self.rect = self.surface.get_rect(center=(635, 360))

            screen = pygame.display.get_surface()
            screen.blit(self.surface, self.rect)
        if type == 'R':
            self.surface = pygame.Surface((0, 0))
            self.rect = self.surface.get_rect(center=(635, 360))

            screen = pygame.display.get_surface()
            screen.blit(self.surface, self.rect)
        if type == 'C':
            self.surface = pygame.Surface((0, 0))
            self.rect = self.surface.get_rect(center=(635, 360))

            screen = pygame.display.get_surface()
            screen.blit(self.surface, self.rect)
        if type == 'E':
            self.surface = pygame.Surface((0, 0))
            self.rect = self.surface.get_rect(center=(635, 360))

            screen = pygame.display.get_surface()
            screen.blit(self.surface, self.rect)
