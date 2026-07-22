# 14 Hours of Python Game Development - from Beginner to Advanced
# Instructor: Tech With Tim
# Followed along and coded by: Jose 'Joe' Ruiz
# Car Racing Game (Medium)
# main.py

# Import modules
import pygame
import time
import math
from pathlib import Path
from utils import scale_image, blit_rotate_center, blit_text_center

# Initialize Pygame
pygame.init()

# ------------------------------------------------------------
# ASSET LOADING (using pathlib)
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
IMGS_DIR = BASE_DIR / "imgs"

# COLORS
RED = (255, 0, 0)

# Load images
GRASS         = pygame.image.load(IMGS_DIR / "grass.jpg")
TRACK         = pygame.image.load(IMGS_DIR / "track.png")
TRACK_BORDER  = pygame.image.load(IMGS_DIR / "track-border.png")
FINISH        = pygame.image.load(IMGS_DIR / "finish.png")

# Finish line scaling + mask: added in part 2
FINISH       = scale_image(FINISH, 0.8)
FINISH_MASK     = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (118, 222)

# Car images
RED_CAR       = pygame.image.load(IMGS_DIR / "red-car.png")
GREEN_CAR     = pygame.image.load(IMGS_DIR / "green-car.png")
GREY_CAR      = pygame.image.load(IMGS_DIR / "grey-car.png")
PURPLE_CAR    = pygame.image.load(IMGS_DIR / "purple-car.png")
WHITE_CAR     = pygame.image.load(IMGS_DIR / "white-car.png")

# ------------------------------------------------------------
# SCALE IMAGES
# ------------------------------------------------------------
TRACK        = scale_image(TRACK, 0.8)
TRACK_BORDER = scale_image(TRACK_BORDER, 0.8)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

GRASS        = scale_image(GRASS, 2.5)
RED_CAR      = scale_image(RED_CAR, 0.44)
GREEN_CAR    = scale_image(GREEN_CAR, 0.44)
GREY_CAR     = scale_image(GREY_CAR, 0.44)
PURPLE_CAR   = scale_image(PURPLE_CAR, 0.44)
WHITE_CAR    = scale_image(WHITE_CAR, 0.44)

# Window matches scaled track
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)

FPS = 60

# Computer car path (added in part 3)
PATH = [
    (154, 107), (106, 67), (54, 105), (52, 416), (294, 651),
    (346, 632), (369, 466), (446, 425), (522, 463), (542, 625),
    (600, 652), (650, 622), (645, 340), (404, 323), (356, 282),
    (384, 239), (609, 230), (654, 190), (648, 87), (555, 68),
    (288, 69), (249, 99), (243, 340), (197, 365), (152, 322),
    (155, 222),
]


# ------------------------------------------------------------
# GAME INFO CLASS (levels, timing, state)
# ------------------------------------------------------------
class GameInfo:
    LEVELS = 10  # Total number of levels before final win message

    def __init__(self, level=1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        """Advance to the next level and reset start state."""
        self.level += 1
        self.started = False

    def reset(self):
        """Reset game back to level 1."""
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        """Return True when all levels are completed."""
        return self.level > self.LEVELS

    def start_level(self):
        """Mark level as started and begin timer."""
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        """Return elapsed time since level start."""
        if not self.started:
            return 0
        return round(time.time() - self.level_start_time)


# ------------------------------------------------------------
# ABSTRACT CAR CLASS (shared movement + collision logic)
# ------------------------------------------------------------
class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.088

    def rotate(self, left=False, right=False):
        """Rotate car left or right."""
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        """Draw car with rotation applied."""
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        """Accelerate forward."""
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        """Reverse (slower than forward)."""
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        """Move car based on angle + velocity."""
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        """Return point of impact if car overlaps a mask."""
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        return mask.overlap(car_mask, offset)

    def reset(self):
        """Reset car to starting position."""
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


# ------------------------------------------------------------
# PLAYER CAR
# ------------------------------------------------------------
class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (160, 178)

    def reduce_speed(self):
        """Slow down when not accelerating."""
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        """Reverse direction when hitting border."""
        self.vel = -self.vel
        self.move()


# ------------------------------------------------------------
# COMPUTER CAR (follows path automatically)
# ------------------------------------------------------------
class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (136, 178)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        """Debug: draw path points."""
        for point in self.path:
            pygame.draw.circle(win, RED, point, 5)

    def calculate_angle(self):
        """Rotate car toward next path point."""
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2
        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference = self.angle - math.degrees(desired_radian_angle)
        if difference >= 180:
            difference -= 360

        if difference > 0:
            self.angle -= min(self.rotation_vel, abs(difference))
        else:
            self.angle += min(self.rotation_vel, abs(difference))

    def update_path_point(self):
        """Move to next point when reaching current one."""
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        """Follow path automatically."""
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def next_level(self, level):
        """Increase computer speed each level."""
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.current_point = 0


# ------------------------------------------------------------
# DRAW FUNCTION
# ------------------------------------------------------------
def draw(win, images, player_car, computer_car, game_info):
    """Draw background, UI text, and cars."""
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(f"Level {game_info.level}", 1, (255, 255, 255))
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 90))

    time_text = MAIN_FONT.render(f"Time: {game_info.get_level_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 45))

    vel_text = MAIN_FONT.render(f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height()))

    player_car.draw(win)
    computer_car.draw(win)

    pygame.display.update()


# ------------------------------------------------------------
# MOVE PLAYER INPUT HANDLING
# ------------------------------------------------------------
def move_player(player_car):
    """Handle keyboard input for player movement."""
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)
    if keys[pygame.K_UP]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()


# ------------------------------------------------------------
# COLLISION HANDLING
# ------------------------------------------------------------
def handle_collision(player_car, computer_car, game_info):
    """Handle border collisions, finish line collisions, and win/loss logic."""

    # Player hits track border
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    # Computer crosses finish line → YOU LOSE
    computer_finish = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    if computer_finish != None:
        blit_text_center(WIN, MAIN_FONT, "YOU LOST!!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    # Player crosses finish line → YOU WIN (per-level)
    player_finish = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if player_finish != None:
        # If hitting top of finish line, bounce instead of winning
        if player_finish[1] == 0:
            player_car.bounce()
        else:
            blit_text_center(WIN, MAIN_FONT, "YOU WON !!")
            pygame.display.update()
            pygame.time.wait(3000)

            game_info.next_level()
            player_car.reset()
            computer_car.next_level(game_info.level)


# ------------------------------------------------------------
# MAIN GAME LOOP (wrapped in main())
# ------------------------------------------------------------
def main():
    """Main game loop for the racing game."""

    run = True
    clock = pygame.time.Clock()

    images = [
        (GRASS, (0, 0)),
        (TRACK, (0, 0)),
        (FINISH, FINISH_POSITION),
        (TRACK_BORDER, (0, 0))
    ]

    player_car = PlayerCar(4, 3)
    computer_car = ComputerCar(.5, 3, PATH)
    game_info = GameInfo()

    while run:
        clock.tick(FPS)

        draw(WIN, images, player_car, computer_car, game_info)

        # Start screen (wait for key press)
        while not game_info.started:
            blit_text_center(WIN, MAIN_FONT, f"Press any key to start level {game_info.level}!")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                if event.type == pygame.KEYDOWN:
                    game_info.start_level()

            if not run:
                break

        if not run:
            break

        # Handle quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Movement + collisions
        move_player(player_car)
        computer_car.move()
        handle_collision(player_car, computer_car, game_info)

        # Final victory (after all levels)
        if game_info.game_finished():
            blit_text_center(WIN, MAIN_FONT, "YOU WON THE RACE!!")
            pygame.display.update()
            pygame.time.wait(5000)
            game_info.reset()
            player_car.reset()
            computer_car.reset()
            continue

    pygame.quit()


# ------------------------------------------------------------
# RUN GAME
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
