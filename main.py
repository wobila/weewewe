import pygame
import sys
import os
import math
import random
from menu import MainMenu
from entity import Player
from lvl import Level
from enemy import Enemy


class Projectile:
    def __init__(self, x, y, velocity, speed, image_path):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.speed = speed
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, dt):
        self.x += self.velocity[0] * self.speed * dt
        self.y += self.velocity[1] * self.speed * dt
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


pygame.init()

SCREEN_WIDTH = 1270
SCREEN_HEIGHT = 720
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Магия скелета")

clock = pygame.time.Clock()

main_menu = MainMenu(screen, SCREEN_WIDTH, SCREEN_HEIGHT, clock)

player = None
level = None
enemies = []
projectiles = []
total_kills = 0
pygame.mixer.music.load("dnd.mp3")
pygame.mixer.music.play(-1)
pygame.font.init()
font = pygame.font.Font(None, 36)


def main_menu_loop():
    while True:
        action = main_menu.run()
        if action == "new_game":
            game_loop()
        elif action == "save_game":
            save_game()
        elif action == "exit":
            pygame.quit()
            sys.exit()


def spawn_enemies(num_enemies):
    enemies = []
    for _ in range(num_enemies):
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(100, SCREEN_HEIGHT - 100)
        enemies.append(Enemy(x, y, "enemy.png"))
    return enemies


def game_loop():
    global player, level, enemies, projectiles, total_kills
    num_projectiles_to_kill_enemy = 1
    player = Player(100, 100)
    level = Level(6)
    level.generate_path()
    enemies = spawn_enemies(9)
    projectiles = []
    start_time = pygame.time.get_ticks()
    while True:
        player_rect = pygame.Rect(player.x, player.y, player.rect.width, player.rect.height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_game()
                    main_menu_loop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dx = event.pos[0] - player.x
                    dy = event.pos[1] - player.y
                    length = math.sqrt(dx ** 2 + dy ** 2)
                    dx /= length
                    dy /= length
                    projectiles.append(Projectile(player.x, player.y, (dx, dy), 500, "projectile.png"))

        dt = clock.tick(60) / 1000.0

        keys = pygame.key.get_pressed()

        dx = keys[pygame.K_d] * player.speed * dt - keys[pygame.K_a] * player.speed * dt
        dy = keys[pygame.K_s] * player.speed * dt - keys[pygame.K_w] * player.speed * dt
        player.renewpos(dx, dy)

        screen.fill((31, 28, 29))

        background = pygame.image.load("background_image.png").convert()
        screen.blit(background, (0, 0))

        level.drawroom(player.room)

        player.display()

        if not enemies:
            enemies = spawn_enemies(9)
            num_projectiles_to_kill_enemy += 1

        for enemy in enemies[:]:

            if player_rect.colliderect(enemy.rect):
                player.hp -= 1

            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.rect.width, enemy.rect.height)

            for projectile in projectiles[:]:
                if projectile.rect.colliderect(enemy_rect):
                    enemy.hits += 1
                    projectiles.remove(projectile)
                    if enemy.hits >= num_projectiles_to_kill_enemy:
                        enemies.remove(enemy)
                        total_kills += 1
                        break

            for other_enemy in enemies:
                if other_enemy != enemy:
                    other_enemy_rect = pygame.Rect(other_enemy.x, other_enemy.y, other_enemy.rect.width,
                                                   other_enemy.rect.height)
                    if enemy_rect.colliderect(other_enemy_rect):
                        dx = other_enemy.x - enemy.x
                        dy = other_enemy.y - enemy.y
                        length = math.sqrt(dx ** 2 + dy ** 2)
                        dx /= length
                        dy /= length
                        enemy.move(-dx * enemy.speed * dt, -dy * enemy.speed * dt)

            dx = player.x - enemy.x
            dy = player.y - enemy.y
            length = math.sqrt(dx ** 2 + dy ** 2)
            dx /= length
            dy /= length

            enemy.move(dx * enemy.speed * dt, dy * enemy.speed * dt)

            enemy.draw(screen)

        for projectile in projectiles:
            projectile.update(dt)
            projectile.draw(screen)

        health_text = font.render("Health: {}%".format(player.hp), True, (255, 255, 255))
        screen.blit(health_text, (20, 20))

        if player.hp <= 0:
            enemies_killed_text = font.render("Enemies Killed: {}".format(total_kills), True, (255, 255, 255))
            screen.blit(enemies_killed_text, (20, 50))
            current_time = pygame.time.get_ticks() - start_time
            time_text = font.render("Time: {:02}:{:02}".format(current_time // 60000, (current_time // 1000) % 60),
                                    True,
                                    (255, 255, 255))
            screen.blit(time_text, (20, 80))
            pygame.display.flip()
            pygame.time.wait(3000)
            main_menu_loop()

        pygame.display.flip()

        clock.tick(FPS)


def save_game():
    print("Игра сохранена")


if __name__ == "__main__":
    main_menu_loop()
