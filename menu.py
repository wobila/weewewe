import pygame
import sys


class MainMenu:
    def __init__(self, screen, screen_width, screen_height, clock):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.clock = clock

        self.font = pygame.font.Font(pygame.font.get_default_font(), 32)
        self.title_font = pygame.font.Font(pygame.font.get_default_font(), 48)

        self.buttons = [
            {"text": "Новая игра", "action": "new_game", "rect": None},
            {"text": "Сохранить игру", "action": "save_game", "rect": None},
            {"text": "Выход", "action": "exit", "rect": None}
        ]
        self.selected_button = -1

        self.background = pygame.image.load("0036ad781dee3be50940952e7f6b160a.png").convert()

    def draw_text(self, text, size, x, y, color, selected=False):
        font = self.title_font if selected else self.font
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def draw(self):

        self.screen.blit(self.background, (0, 0))

        self.draw_text("Магия скелета", 48, self.screen_width // 2, self.screen_height // 4,
                       (255, 255, 255))

        button_y = self.screen_height // 2
        for i, button in enumerate(self.buttons):
            color = (255, 255, 255)
            selected = i == self.selected_button
            button_rect = self.draw_text(button["text"], 32, self.screen_width // 2, button_y, color, selected)
            button["rect"] = button_rect
            button_y += 40
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_button = (self.selected_button - 1) % len(self.buttons)
                elif event.key == pygame.K_DOWN:
                    self.selected_button = (self.selected_button + 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN:
                    return self.buttons[self.selected_button]["action"]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        if button["rect"].collidepoint(event.pos):
                            return button["action"]
        return None

    def run(self):
        while True:
            action = self.handle_input()
            if action:
                return action
            self.draw()
            self.clock.tick(60)
