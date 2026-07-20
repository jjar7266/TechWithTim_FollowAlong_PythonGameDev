# 14 Hours of Python Game Development - from Beginner to Advanced
# Instructor: Tech With Tim
# Followed along and coded by: Jose 'Joe' Ruiz
# Car Racing Game (Medium)
# main.py part 1

import pygame
import time
import math
from pathlib import Path
from utils import scale_image

pygame.init()

# ------------------------------------------------------------
# ASSET LOADING (using pathlib)
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
IMGS_DIR = BASE_DIR / "imgs"

# Load images
GRASS         = pygame.image.load(IMGS_DIR / "grass.jpg")
TRACK         = pygame.image.load(IMGS_DIR / "track.png")
TRACK_BORDER  = pygame.image.load(IMGS_DIR / "track-border.png")
FINISH        = pygame.image.load(IMGS_DIR / "finish.png")

RED_CAR       = pygame.image.load(IMGS_DIR / "red-car.png")
GREEN_CAR     = pygame.image.load(IMGS_DIR / "green-car.png")
GREY_CAR      = pygame.image.load(IMGS_DIR / "grey-car.png")
PURPLE_CAR    = pygame.image.load(IMGS_DIR / "purple-car.png")
WHITE_CAR     = pygame.image.load(IMGS_DIR / "white-car.png")

# ------------------------------------------------------------
# SCALE IMAGES
# ------------------------------------------------------------
TRACK        = scale_image(TRACK, 0.8)                # shrink track
TRACK_BORDER = scale_image(TRACK_BORDER, 0.8)  # same size as track
GRASS        = scale_image(GRASS, 2.5)
RED_CAR      = scale_image(RED_CAR, 0.55)
GREEN_CAR    = scale_image(GREEN_CAR, 0.55)
GREY_CAR     = scale_image(GREY_CAR, 0.55)
PURPLE_CAR   = scale_image(PURPLE_CAR, 0.55)
WHITE_CAR    = scale_image(WHITE_CAR, 0.55)

# Window matches scaled track
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

FPS = 60


# Draw Function
def draw(win, images):
    for img, pos in images:
        win.blit(img, pos)


# ------------------------------------------------------------
# GAME LOOP
# ------------------------------------------------------------
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0))]


while run:
    clock.tick(FPS)

    draw(WIN, images)

    

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
