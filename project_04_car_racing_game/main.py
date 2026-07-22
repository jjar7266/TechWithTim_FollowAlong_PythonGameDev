# 14 Hours of Python Game Development - from Beginner to Advanced
# Instructor: Tech With Tim
# Followed along and coded by: Jose 'Joe' Ruiz
# Car Racing Game (Medium)
# main.py

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

# COLORS
RED = (255, 000, 000)

# Load images
GRASS         = pygame.image.load(IMGS_DIR / "grass.jpg")
TRACK         = pygame.image.load(IMGS_DIR / "track.png")
TRACK_BORDER  = pygame.image.load(IMGS_DIR / "track-border.png")
FINISH        = pygame.image.load(IMGS_DIR / "finish.png")

# Added in part 2
FINISH       = scale_image(FINISH, 0.8)
FINISH_MASK     = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (118, 222)

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

# Added in part 2
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)  # added in part 2

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

FPS = 60

# added part 3
PATH = [

       (154, 107), (106, 67), (54, 105), (52, 416), (294, 651),
       (346, 632), (369, 466), (446, 425), (522, 463), (542, 625),
       (600, 652), (650, 622), (645, 340), (404, 323), (356, 282),
       (384, 239), (609, 230), (654, 190), (648, 87), (555, 68),
       (288, 69), (249, 99), (243, 340), (197, 365), (152, 322),
       (155, 222),
    ]



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
        if left:
            self.angle += self.rotation_vel

        elif right:
            self.angle -= self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    # added in part 2
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    # added in part 2
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0



class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (160, 178)  # not the same as instructors starting point

    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()


# added part 3
class ComputerCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (136, 178) # not the same as instructors starting point

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel

    def draw_points(self, win):
        for point in self.path:
            pygame.draw.circle(win, RED, point, 5)

    def draw(self, win):
        super().draw(win)
        # comment this out so you do not see the RED points on the track
        #self.draw_points(win)

    def calculate_angle(self):
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y

        if y_diff == 0:
            desired_radian_angle = math.pi / 2

        else:
            desired_radian_angle = math.atan(x_diff / y_diff)

        if target_y > self.y:
            desired_radian_angle += math.pi

        difference_in_angle = self.angle - math.degrees(desired_radian_angle)
        if difference_in_angle >= 180:
            difference_in_angle -= 360

        if difference_in_angle > 0:
            self.angle -= min(self.rotation_vel, abs(difference_in_angle))

        else:
            self.angle += min(self.rotation_vel, abs(difference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*target):
            self.current_point += 1

    def move(self):
        if self.current_point >= len(self.path):
            return

        self.calculate_angle()
        self.update_path_point()
        super().move()


# Draw Function
def draw(win, images, player_car, computer_car):
    for img, pos in images:
        win.blit(img, pos)

    player_car.draw(win)

    # added part 3
    computer_car.draw(win)

    pygame.display.update()


# Move Player
def move_player(player_car):

    keys = pygame.key.get_pressed()
    moved = False

    # Rotate Car left and right
    if keys[pygame.K_a]:
        player_car.rotate(left=True)

    if keys[pygame.K_d]:
        player_car.rotate(right=True)

    # Move Car forward
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()

    # Move Car backward
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    # Reduce speed
    if not moved:
        player_car.reduce_speed()


# added in part 3 (moved all collision inside function)
def handle_collision(player_car, computer_car):

    # Added in part 2
    if player_car.collide(TRACK_BORDER_MASK) != None:
        player_car.bounce()

    # Added in part 2 and modified in part 3
    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, *FINISH_POSITION)
    if computer_finish_poi_collide != None:
        print("Computer WINS !!")
        player_car.reset()
        computer_car.reset()

    player_finish_poi_collide = player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if player_finish_poi_collide != None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()

        else:
            player_car.reset()
            computer_car.reset()


# ------------------------------------------------------------
# GAME LOOP
# ------------------------------------------------------------
run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
         (FINISH, FINISH_POSITION),
         (TRACK_BORDER, (0, 0))]

player_car = PlayerCar(1.5, 3)

# added part 3
# adjust the path points if you increase the speed
computer_car =ComputerCar(1.5, 3, PATH)

while run:
    clock.tick(FPS)

    draw(WIN, images, player_car, computer_car)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

        # added in part 3 to get points for the computer path
        # commented out after getting all computer path points
        #if event.type == pygame.MOUSEBUTTONDOWN:
        #    pos = pygame.mouse.get_pos()
        #    computer_car.path.append(pos)

    move_player(player_car)
    computer_car.move()

    # added in part 3
    handle_collision(player_car, computer_car)


# print(computer_car.path)
pygame.quit()
