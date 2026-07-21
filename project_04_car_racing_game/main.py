# 14 Hours of Python Game Development - from Beginner to Advanced
# Instructor: Tech With Tim
# Followed along and coded by: Jose 'Joe' Ruiz
# Car Racing Game (Medium)
# main.py part 1

import pygame
import time
import math
from pathlib import Path
from utils import scale_image, blit_rotate_center

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
RED_CAR      = scale_image(RED_CAR, 0.50)
GREEN_CAR    = scale_image(GREEN_CAR, 0.50)
GREY_CAR     = scale_image(GREY_CAR, 0.50)
PURPLE_CAR   = scale_image(PURPLE_CAR, 0.50)
WHITE_CAR    = scale_image(WHITE_CAR, 0.50)

# Window matches scaled track
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

FPS = 60

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel

        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()



class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (160, 178)  # not the same as instructors starting point


# Draw Function
def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)
    pygame.display.update()


# ------------------------------------------------------------
# GAME LOOP
# ------------------------------------------------------------
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0))]
player_car = PlayerCar(4, 4)

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()
    moved = False

    # Rotate Car left and right
    if keys[pygame.K_a]:
        player_car.rotate(left=True)

    if keys[pygame.K_d]:
        player_car.rotate(right=True)

    # Move Car
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()

    # Reduce speed
    if not moved:
        player_car.reduce_speed()






pygame.quit()
