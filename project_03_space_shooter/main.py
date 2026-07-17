# 14 Hours of Python Game Development - from Beginner to Advanced
# Instructor: Tech With Tim
# Followed along and coded by: Jose 'Joe' Ruiz
# Space Shooter (Medium)
# ============================================================

# Import modules
import pygame
import os
import time
import random

# Initialize Pygame and the mixer
pygame.init()
pygame.mixer.init()

# Create Game Window
WIDTH, HEIGHT = 750, 750

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# COLORS
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y, 50, 50))



# Main Game Loop
def main():
    run = True
    FPS = 60
    level= 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    player_vel = 5

    ship = Ship(300, 650)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))

        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, WHITE)
        level_label = main_font.render(f"Level: {level}", 1, WHITE)

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        ship.draw(WIN)

        pygame.display.update()



    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and ship.x - player_vel > 0:  # LEFT
            ship.x -= player_vel

        if keys[pygame.K_RIGHT] and ship.x + player_vel + 50 < WIDTH:  # RIGHT
            ship.x += player_vel

        if keys[pygame.K_UP] and ship.y - player_vel > 0:  # UP
            ship.y -= player_vel

        if keys[pygame.K_DOWN] and ship.y + player_vel + 50 < HEIGHT:  # DOWN
            ship.y += player_vel


main()
