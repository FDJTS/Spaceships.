import pygame
import sys
import random
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game - Multi Style Edition")

FPS = 60
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def draw_spaceship_cartoon(surface, x, y):
    pygame.draw.polygon(surface, BLUE, [(x, y), (x - 20, y + 40), (x + 20, y + 40)])

def draw_spaceship_realistic(surface, x, y):
    pygame.draw.rect(surface, GREEN, (x - 15, y, 30, 40))
    pygame.draw.circle(surface, WHITE, (x, y + 20), 15)

def draw_spaceship_retro(surface, x, y):
    pygame.draw.rect(surface, RED, (x - 10, y, 20, 30))
    pygame.draw.rect(surface, WHITE, (x - 5, y + 5, 10, 20))

class Enemy:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = -50
        self.speed = random.randint(2, 5)
        self.width = 40
        self.height = 30

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.x = random.randint(50, WIDTH - 50)
            self.y = -50
            self.speed = random.randint(2, 5)

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))

class SpaceshipGame:
    def __init__(self):
        self.spaceship_x = WIDTH // 2
        self.spaceship_y = HEIGHT - 60
        self.speed = 7
        self.enemies = [Enemy() for _ in range(5)]
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)
        self.state = "start"
        self.style_index = 0

    def reset(self):
        self.enemies = [Enemy() for _ in range(5)]
        self.score = 0
        self.spaceship_x = WIDTH // 2
        self.state = "start"

    def draw_text(self, text, x, y, color=WHITE):
        img = self.font.render(text, True, color)
        screen.blit(img, (x, y))

    def draw_spaceship(self):
        if self.style_index == 0:
            draw_spaceship_cartoon(screen, self.spaceship_x, self.spaceship_y)
        elif self.style_index == 1:
            draw_spaceship_realistic(screen, self.spaceship_x, self.spaceship_y)
        else:
            draw_spaceship_retro(screen, self.spaceship_x, self.spaceship_y)

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.spaceship_x > 20:
            self.spaceship_x -= self.speed
        if keys[K_RIGHT] and self.spaceship_x < WIDTH - 20:
            self.spaceship_x += self.speed

    def update(self):
        for enemy in self.enemies:
            enemy.move()
            if (self.spaceship_y < enemy.y + enemy.height and
                self.spaceship_x > enemy.x and
                self.spaceship_x < enemy.x + enemy.width):
                self.state = "game_over"
            if enemy.y > HEIGHT:
                self.score += 1

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(screen)

    def run(self):
        while True:
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if self.state == "start" and event.key == K_RETURN:
                        self.state = "playing"
                    elif self.state == "game_over" and event.key == K_RETURN:
                        self.reset()
                    elif event.key == K_TAB:
                        self.style_index = (self.style_index + 1) % 3

            if self.state == "start":
                self.draw_text("Spaceship Game", WIDTH//2 - 120, HEIGHT//3, WHITE)
                self.draw_text("Press ENTER to Start", WIDTH//2 - 130, HEIGHT//2, WHITE)
                self.draw_text("Press TAB to Change Style", WIDTH//2 - 150, HEIGHT//2 + 40, WHITE)
                self.draw_text("Current Style: " + ["Cartoon", "Realistic", "Retro"][self.style_index], WIDTH//2 - 100, HEIGHT//2 + 80, WHITE)
            elif self.state == "playing":
                self.handle_events()
                self.update()
                self.draw_spaceship()
                self.draw_enemies()
                self.draw_text(f"Score: {self.score}", 10, 10)
            elif self.state == "game_over":
                self.draw_text("GAME OVER", WIDTH//2 - 80, HEIGHT//3, RED)
                self.draw_text(f"Final Score: {self.score}", WIDTH//2 - 100, HEIGHT//2, WHITE)
                self.draw_text("Press ENTER to Restart", WIDTH//2 - 130, HEIGHT//2 + 40, WHITE)

            pygame.display.update()
            clock.tick(FPS)

if __name__ == "__main__":
    SpaceshipGame().run()