# 14 Hours of Python Game Development - from Beginner to Advanced
# Instructor: Tech With Tim
# Followed along and coded by: Jose 'Joe' Ruiz
# Space Shooter (Medium)

# Description: Medium‑difficulty space shooter game that teaches
#              sprites, collisions, waves, and game loops.
# ============================================================

# ------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------
import sys
import random
from pathlib import Path

import pygame


# ------------------------------------------------------------
# INITIAL SETUP
# ------------------------------------------------------------
pygame.init()
pygame.mixer.init()

# Window size and basic settings
WINDOW_WIDTH  = 750
WINDOW_HEIGHT = 750
FPS           = 60

WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors (RGB)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)


# ------------------------------------------------------------
# ASSET LOADING (USING pathlib)
# ------------------------------------------------------------
BASE_DIR   = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# Enemy ships
RED_SPACE_SHIP   = pygame.image.load(ASSETS_DIR / "pixel_ship_red_small.png")
GREEN_SPACE_SHIP = pygame.image.load(ASSETS_DIR / "pixel_ship_green_small.png")
BLUE_SPACE_SHIP  = pygame.image.load(ASSETS_DIR / "pixel_ship_blue_small.png")

# Player ship
YELLOW_SPACE_SHIP = pygame.image.load(ASSETS_DIR / "pixel_ship_yellow.png")

# Lasers
RED_LASER    = pygame.image.load(ASSETS_DIR / "pixel_laser_red.png")
GREEN_LASER  = pygame.image.load(ASSETS_DIR / "pixel_laser_green.png")
BLUE_LASER   = pygame.image.load(ASSETS_DIR / "pixel_laser_blue.png")
YELLOW_LASER = pygame.image.load(ASSETS_DIR / "pixel_laser_yellow.png")

# Background (scaled to window size)
BG = pygame.transform.scale(
    pygame.image.load(ASSETS_DIR / "background-black.png"),
    (WINDOW_WIDTH, WINDOW_HEIGHT),
)


# ------------------------------------------------------------
# SOUND EFFECTS (Using pathlib)
# ------------------------------------------------------------
BULLET_SOUND = pygame.mixer.Sound(ASSETS_DIR / "bullet_sound.mp3")
HIT_SOUND    = pygame.mixer.Sound(ASSETS_DIR / "hit_sound.mp3")

# Optional: Adjust volume (0.0 to 1.0)
BULLET_SOUND.set_volume(0.5)
HIT_SOUND.set_volume(0.5)


# ------------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------------
def collide(obj1, obj2) -> bool:
    """Check if two masked objects overlap (pixel‑perfect collision)."""
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


# ------------------------------------------------------------
# LASER CLASS
# ------------------------------------------------------------
class Laser:
    """Represents a single laser shot fired by a ship."""

    def __init__(self, x: int, y: int, img: pygame.Surface) -> None:
        # Store position and image
        self.x = x
        self.y = y
        self.img = img

        # Create a mask for pixel‑perfect collision
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window: pygame.Surface) -> None:
        """Draw the laser at its current position."""
        window.blit(self.img, (self.x, self.y))

    def move(self, vel: int) -> None:
        """Move the laser vertically by a given velocity."""
        self.y += vel

    def off_screen(self, height: int) -> bool:
        """
        Return True if the laser has moved outside the visible window.
        We check if it's above the top or below the bottom.
        """
        return self.y <= 0 or self.y >= height

    def collision(self, obj) -> bool:
        """Return True if this laser collides with another object."""
        return collide(self, obj)


# ------------------------------------------------------------
# BASE SHIP CLASS
# ------------------------------------------------------------
class Ship:
    """Base class for all ships (player and enemies)."""

    COOLDOWN = 30  # Frames between shots

    def __init__(self, x: int, y: int, health: int = 100) -> None:
        # Position and health
        self.x = x
        self.y = y
        self.health = health

        # Images (set by subclasses)
        self.ship_img: pygame.Surface | None = None
        self.laser_img: pygame.Surface | None = None

        # Laser list and cooldown counter
        self.lasers: list[Laser] = []
        self.cool_down_counter = 0

    def draw(self, window: pygame.Surface) -> None:
        """Draw the ship and all its lasers."""
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel: int, obj) -> None:
        """
        Move all lasers fired by this ship.
        If a laser goes off‑screen, remove it.
        If a laser hits the given object, reduce its health.
        """
        self._handle_cooldown()

        for laser in self.lasers[:]:
            laser.move(vel)

            if laser.off_screen(WINDOW_HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def _handle_cooldown(self) -> None:
        """Update the cooldown counter so ships can't shoot every frame."""
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self) -> None:
        """
        Fire a laser from the ship's current position.
        Only allowed if cooldown is ready.
        """
        if self.cool_down_counter == 0 and self.laser_img is not None:
            BULLET_SOUND.play()  # 🔊 play firing sound

            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self) -> int:
        """Return the width of the ship image."""
        return self.ship_img.get_width()

    def get_height(self) -> int:
        """Return the height of the ship image."""
        return self.ship_img.get_height()


# ------------------------------------------------------------
# PLAYER CLASS
# ------------------------------------------------------------
class Player(Ship):
    """Represents the player‑controlled ship."""

    def __init__(self, x: int, y: int, health: int = 100) -> None:
        super().__init__(x, y, health)

        # Set player images
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER

        # Mask for collision
        self.mask = pygame.mask.from_surface(self.ship_img)

        # Store maximum health for drawing the health bar
        self.max_health = health

    def move_lasers(self, vel: int, enemies: list["Enemy"]) -> None:
        """
        Move player lasers.
        If a laser hits an enemy, remove both the laser and the enemy.
        """
        self._handle_cooldown()

        for laser in self.lasers[:]:
            laser.move(vel)

            if laser.off_screen(WINDOW_HEIGHT):
                self.lasers.remove(laser)
            else:
                for enemy in enemies[:]:
                    if laser.collision(enemy):
                        HIT_SOUND.play()  # 🔊 play hit sound
                        
                        enemies.remove(enemy)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window: pygame.Surface) -> None:
        """Draw the player and its health bar."""
        super().draw(window)
        self._draw_healthbar(window)

    def _draw_healthbar(self, window: pygame.Surface) -> None:
        """Draw a red bar (max health) and green bar (current health)."""
        bar_x = self.x
        bar_y = self.y + self.ship_img.get_height() + 10
        bar_width = self.ship_img.get_width()
        bar_height = 10

        # Red background bar (full health)
        pygame.draw.rect(window, RED, (bar_x, bar_y, bar_width, bar_height))

        # Green foreground bar (current health)
        health_ratio = self.health / self.max_health
        pygame.draw.rect(
            window,
            GREEN,
            (bar_x, bar_y, bar_width * health_ratio, bar_height),
        )


# ------------------------------------------------------------
# ENEMY CLASS
# ------------------------------------------------------------
class Enemy(Ship):
    """Represents an enemy ship that moves downward and shoots at the player."""

    COLOR_MAP = {
        "red":   (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue":  (BLUE_SPACE_SHIP, BLUE_LASER),
    }

    def __init__(self, x: int, y: int, color: str, health: int = 100) -> None:
        super().__init__(x, y, health)

        # Set ship and laser images based on color
        self.ship_img, self.laser_img = self.COLOR_MAP[color]

        # Mask for collision
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel: int) -> None:
        """Move the enemy ship downward by a given velocity."""
        self.y += vel

    def shoot(self) -> None:
        """
        Fire a laser from the center bottom of the enemy ship.
        This overrides the base Ship.shoot() to center the bullet.
        """
        if self.cool_down_counter == 0 and self.laser_img is not None:
            laser_x = self.x + self.get_width() // 2 - self.laser_img.get_width() // 2
            laser_y = self.y + self.get_height()
            laser = Laser(laser_x, laser_y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


# ------------------------------------------------------------
# MAIN GAME LOOP
# ------------------------------------------------------------
def main() -> None:
    """Run a single game session of Space Shooter."""

    run = True
    clock = pygame.time.Clock()

    # Game state
    level = 0
    lives = 5

    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies: list[Enemy] = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel  = 5

    player = Player(300, 630)

    lost = False
    lost_count = 0

    def redraw_window() -> None:
        """Draw everything on the screen for the current frame."""
        WIN.blit(BG, (0, 0))

        # Draw HUD text (lives and level)
        lives_label = main_font.render(f"Lives: {lives}", True, WHITE)
        level_label = main_font.render(f"Level: {level}", True, WHITE)

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WINDOW_WIDTH - level_label.get_width() - 10, 10))

        # Draw all enemies
        for enemy in enemies:
            enemy.draw(WIN)

        # Draw player
        player.draw(WIN)

        # If the player has lost, show a message
        if lost:
            lost_label = lost_font.render("You Lost !!", True, WHITE)
            WIN.blit(
                lost_label,
                (
                    WINDOW_WIDTH / 2 - lost_label.get_width() / 2,
                    WINDOW_HEIGHT / 2 - lost_label.get_height() / 2,
                ),
            )

        pygame.display.flip()

    # ------------------------------
    # GAME LOOP
    # ------------------------------
    while run:
        clock.tick(FPS)
        redraw_window()

        # Check for losing conditions
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            # After 3 seconds of showing "You Lost", exit the game loop
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        # Spawn a new wave when all enemies are gone
        if len(enemies) == 0:
            level += 1
            wave_length += 5

            for i in range(wave_length):
                enemy = Enemy(
                    x=random.randrange(50, WINDOW_WIDTH - 100),
                    y=random.randrange(-1500, -100),
                    color=random.choice(["red", "blue", "green"]),
                )
                enemies.append(enemy)

        # Handle events (quit, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Handle keyboard input for player movement and shooting
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel

        if (
            keys[pygame.K_RIGHT]
            and player.x + player_vel + player.get_width() < WINDOW_WIDTH
        ):
            player.x += player_vel

        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel

        if (
            keys[pygame.K_DOWN]
            and player.y + player_vel + player.get_height() + 15 < WINDOW_HEIGHT
        ):
            player.y += player_vel

        if keys[pygame.K_SPACE]:
            player.shoot()

        # Update enemies: movement, lasers, collisions, lives
        for enemy in enemies[:]:
            enemy.move(enemy_vel)

            # Only start enemy lasers and shooting once they enter the screen
            if enemy.y + enemy.get_height() > 0:
                enemy.move_lasers(laser_vel, player)

                # Random chance to shoot each frame
                if random.randrange(0, 2 * FPS) == 1:
                    enemy.shoot()

                # Collision with player
                if collide(enemy, player):
                    player.health -= 10
                    enemies.remove(enemy)

            # Enemy passes bottom of screen → player loses a life
            elif enemy.y + enemy.get_height() > WINDOW_HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # Move player lasers upward and check collisions with enemies
        player.move_lasers(-laser_vel, enemies)


# ------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------
def main_menu() -> None:
    """Display the main menu and wait for the player to start the game."""
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True

    while run:
        WIN.blit(BG, (0, 0))

        title_label = title_font.render("Press the mouse to begin...", True, WHITE)
        title_rect = title_label.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        WIN.blit(title_label, title_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()
    sys.exit()


# ------------------------------------------------------------
# ENTRY POINT
# ------------------------------------------------------------
if __name__ == "__main__":
    main_menu()
