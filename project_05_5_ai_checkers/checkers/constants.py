# 14 Hours of Python Game Development - from Beginner to Advanced
# Instructor: Tech With Tim
# Followed along and coded by: Jose 'Joe' Ruiz
# PYTHON CHECKERS TUTORIAL A.I. Version - (Medium)
# constants.py

# THIS FILE WILL HOLD ALL THE CONSTANTS (specific to Checkers)

# Import modules
import pygame
from pathlib import Path

# Initialize Pygame
pygame.init()

# CONSTANTS
WIDTH, HEIGHT = 600, 600
ROWS, COLS    = 8, 8
SQUARE_SIZE   = WIDTH // COLS # = 75

# COLORS
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
BLUE  = (  0,   0, 255)
GREY  = (128, 128, 128)
RED   = (255,   0,   0)

# ------------------------------------------------------------
# ASSET LOADING (using pathlib)
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets"

CROWN = pygame.transform.scale(
    pygame.image.load(ASSETS / "crown.png"), (44, 25))


