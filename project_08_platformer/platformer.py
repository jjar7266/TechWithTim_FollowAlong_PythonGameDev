# 14 Hours of Python Game Development - from Beginner to Advanced
# Instructor: Tech With Tim
# Followed along and coded by: Jose 'Joe' Ruiz
# Platformer - (Advanced)
# platformer.py

# Import modules
import sys
import random
import math
import pygame
from pathlib import Path

# Initialize Pygame and the mixer
pygame.init()
pygame.mixer.init()

# COLORS
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

FPS = 60
PLAYER_VEL = 5

# Base directory
BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

# Load images
# player_img = pygame.image.load(ASSETS / "player.png").convert_alpha()


# Load sounds
# jump_sound = pygame.mixer.Sound(ASSETS / "jump.wav")


# Load fonts
# main_font = pygame.font.Font(ASSETS / "font.ttf", 32)


# Create the display window
WIDTH, HEIGHT = 800, 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer")


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    folder = ASSETS / dir1 / dir2
    images = [file for file in folder.iterdir() if file.is_file()]

    all_sprites = {}

    for image_path in images:
        sprite_sheet = pygame.image.load(image_path).convert_alpha()

        # Slice the sheet into frames
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        key = image_path.stem  # filename without extension

        if direction:
            all_sprites[key + "_right"] = sprites
            all_sprites[key + "_left"] = flip(sprites)
        else:
            all_sprites[key] = sprites

    return all_sprites


def get_block(size):
    path = ASSETS / "Terrain" / "Terrain.png"
    image = pygame.image.load(path).convert_alpha()

    # Create a transparent surface for the block
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)

    # Select the block region from the terrain sheet
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)

    return pygame.transform.scale2x(surface)


class Player(pygame.sprite.Sprite):
    COLOR = (RED)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "MaskDude", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0


    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy


    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0


    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0


    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()


    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0


    def hit_head(self):
        self.count = 0
        self.y_vel *= -1



    def update_sprite(self):
        sprite_sheet = "idle"
        if self.y_vel < 0:

            if self.jump_count == 1:
                sprite_sheet = "jump"

            elif self.jump_count == 2:
                sprite_sheet = "double_jump"

        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"

        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

        self.update()


    def update(self):
        self.mask = pygame.mask.from_surface(self.sprite)


    def draw(self, win):

        win.blit(self.sprite, (self.rect.x, self.rect.y))



class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)


def get_background(name):
    image = pygame.image.load(ASSETS / "Background" / name).convert_alpha()
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window)

    player.draw(window)

    pygame.display.update()

def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()

            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

        collided_objects.append(obj)

    return collided_objects


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0

    if keys[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)

    if keys[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)

    handle_vertical_collision(player, objects, player.y_vel)


def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Blue.png")

    block_size = 96

    player = Player(100, HEIGHT - 64 * 2, 64, 64)



    floor = [
        Block(i * block_size, HEIGHT - block_size, block_size)
        for i in range(-WIDTH // block_size, WIDTH * 2 // block_size)
    ]

    # Sanity check
    print("Block image size:", floor[0].image.get_size())
    print("Block rect size:" , floor[0].rect.size)


    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        handle_move(player, floor)
        draw(window, background, bg_image, player, floor)


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main(window)
