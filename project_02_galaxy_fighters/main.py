# 14 Hours of Python Game Development - from Beginner to Advanced
# Instructor: Tech With Tim
# Followed along and coded by: Jose 'Joe' Ruiz
# Galaxy Fighters (Easy)
# ============================================================

# IMPORTS & INITIAL SETUP
# ------------------------------------------------------------
import sys
import pygame
from pathlib import Path

pygame.init()
pygame.mixer.init()

# ------------------------------------------------------------
# PATH SETUP (MODERN PATHLIB)
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

# ------------------------------------------------------------
# WINDOW SETTINGS
# ------------------------------------------------------------
WINDOW_WIDTH  = 800
WINDOW_HEIGHT = 600

WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Galaxy Fighters")

# ------------------------------------------------------------
# COLORS (ALL CAPS CONSTANTS)
# ------------------------------------------------------------
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (255, 0,   0)
YELLOW = (255, 255, 0)

# ------------------------------------------------------------
# GAME CONSTANTS
# ------------------------------------------------------------
FPS             = 60
PLAYER_SPEED    = 5
BULLET_SPEED    = 7
MAX_BULLETS     = 3
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

# A vertical border separating both players
BORDER = pygame.Rect(WINDOW_WIDTH // 2 - 5, 0, 10, WINDOW_HEIGHT)

# ------------------------------------------------------------
# SOUND EFFECTS
# ------------------------------------------------------------
BULLET_HIT_SOUND = pygame.mixer.Sound(ASSETS / "Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound(ASSETS / "Gun+Silencer.mp3")

# ------------------------------------------------------------
# FONTS
# ------------------------------------------------------------
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

# ------------------------------------------------------------
# CUSTOM EVENTS
# ------------------------------------------------------------
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT    = pygame.USEREVENT + 2

# ------------------------------------------------------------
# LOAD IMAGES
# ------------------------------------------------------------
yellow_ship_img = pygame.image.load(ASSETS / "spaceship_yellow.png")
yellow_ship_img = pygame.transform.rotate(
    pygame.transform.scale(yellow_ship_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90
)

red_ship_img = pygame.image.load(ASSETS / "spaceship_red.png")
red_ship_img = pygame.transform.rotate(
    pygame.transform.scale(red_ship_img, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270
)

space_bg = pygame.transform.scale(
    pygame.image.load(ASSETS / "space.png"),
    (WINDOW_WIDTH, WINDOW_HEIGHT)
)

# ============================================================
# DRAWING FUNCTION
# ============================================================
def draw_window(red, yellow, red_bullets, yellow_bullets,
                red_health, yellow_health):
    """
    Draws everything on the screen each frame.
    """

    # Draw background
    WINDOW.blit(space_bg, (0, 0))

    # Draw center border
    pygame.draw.rect(WINDOW, BLACK, BORDER)

    # Draw health text
    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", True, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", True, WHITE)

    WINDOW.blit(red_health_text, (WINDOW_WIDTH - red_health_text.get_width() - 10, 10))
    WINDOW.blit(yellow_health_text, (10, 10))

    # Draw spaceships
    WINDOW.blit(yellow_ship_img, (yellow.x, yellow.y))
    WINDOW.blit(red_ship_img, (red.x, red.y))

    # Draw bullets
    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    pygame.display.update()

# ============================================================
# MOVEMENT FUNCTIONS
# ============================================================
def yellow_handle_movement(keys, yellow):
    """
    Moves the yellow spaceship using WASD keys.
    """

    # Move LEFT
    if keys[pygame.K_a] and yellow.x - PLAYER_SPEED > 0:
        yellow.x -= PLAYER_SPEED

    # Move RIGHT (cannot cross border)
    if keys[pygame.K_d] and yellow.x + PLAYER_SPEED + yellow.width < BORDER.x:
        yellow.x += PLAYER_SPEED

    # Move UP
    if keys[pygame.K_w] and yellow.y - PLAYER_SPEED > 0:
        yellow.y -= PLAYER_SPEED

    # Move DOWN
    if keys[pygame.K_s] and yellow.y + PLAYER_SPEED + yellow.height < WINDOW_HEIGHT - 10:
        yellow.y += PLAYER_SPEED


def red_handle_movement(keys, red):
    """
    Moves the red spaceship using arrow keys.
    """

    # Move LEFT (cannot cross border)
    if keys[pygame.K_LEFT] and red.x - PLAYER_SPEED > BORDER.x + BORDER.width:
        red.x -= PLAYER_SPEED

    # Move RIGHT
    if keys[pygame.K_RIGHT] and red.x + PLAYER_SPEED + red.width < WINDOW_WIDTH:
        red.x += PLAYER_SPEED

    # Move UP
    if keys[pygame.K_UP] and red.y - PLAYER_SPEED > 0:
        red.y -= PLAYER_SPEED

    # Move DOWN
    if keys[pygame.K_DOWN] and red.y + PLAYER_SPEED + red.height < WINDOW_HEIGHT - 10:
        red.y += PLAYER_SPEED

# ============================================================
# BULLET HANDLING
# ============================================================
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    """
    Moves bullets and checks for collisions.
    """

    # Yellow bullets move RIGHT
    for bullet in yellow_bullets[:]:
        bullet.x += BULLET_SPEED

        # If bullet hits red ship
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        # If bullet goes off screen
        elif bullet.x > WINDOW_WIDTH:
            yellow_bullets.remove(bullet)

    # Red bullets move LEFT
    for bullet in red_bullets[:]:
        bullet.x -= BULLET_SPEED

        # If bullet hits yellow ship
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)

        # If bullet goes off screen
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# ============================================================
# WINNER TEXT
# ============================================================
def draw_winner(text):
    """
    Displays the winner text for 5 seconds.
    """

    winner_surface = WINNER_FONT.render(text, True, WHITE)
    WINDOW.blit(
        winner_surface,
        (
            WINDOW_WIDTH // 2 - winner_surface.get_width() // 2,
            WINDOW_HEIGHT // 2 - winner_surface.get_height() // 2
        )
    )

    pygame.display.update()
    pygame.time.delay(5000)

# ============================================================
# MAIN GAME LOOP
# ============================================================
def main():
    """
    Main game loop. Handles movement, bullets, collisions,
    drawing, and win conditions.
    """

    # Create player rectangles
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # Bullet lists
    red_bullets = []
    yellow_bullets = []

    # Player health
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    running = True

    while running:
        clock.tick(FPS)

        # ----------------------------------------------------
        # EVENT HANDLING
        # ----------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # Shooting bullets
            if event.type == pygame.KEYDOWN:

                # Yellow shoots with LEFT CTRL
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10, 5
                    )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                # Red shoots with RIGHT CTRL
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x,
                        red.y + red.height // 2 - 2,
                        10, 5
                    )
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            # Hit detection events
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        # ----------------------------------------------------
        # CHECK WINNER
        # ----------------------------------------------------
        winner_text = ""

        if red_health <= 0:
            winner_text = "YELLOW WINS!"

        if yellow_health <= 0:
            winner_text = "RED WINS!"

        if winner_text:
            draw_winner(winner_text)
            break

        # ----------------------------------------------------
        # MOVEMENT & BULLETS
        # ----------------------------------------------------
        keys = pygame.key.get_pressed()

        yellow_handle_movement(keys, yellow)
        red_handle_movement(keys, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # ----------------------------------------------------
        # DRAW EVERYTHING
        # ----------------------------------------------------
        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    # Restart game after winner screen
    main()

# ============================================================
# PROGRAM ENTRY POINT
# ============================================================
if __name__ == "__main__":
    main()
