import pygame
import math
import sys
import os
import csv
from pygame.locals import *
from enum import IntEnum
Vector2 = pygame.math.Vector2

pygame.init()

FPS = 60
Clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCROLL_THRESH = 200
# define game variables
GRAVITY = 0.75
ROWS = 15
COLS = 50
TILE_SIZE = round(SCREEN_HEIGHT / ROWS)
TILE_TYPES = 264

# level
level = 1

# define player action variables
moving_left = False
moving_right = False

# background & screen scrolling
screen_scroll = 0
background_scroll = 0

# scale
scale = 1

# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'platformer/data/images/Tiles/{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)


sky_background_image = pygame.image.load(
    f'platformer/data/images/Backgrounds/level1/sky.png')
rocks_background_image = pygame.image.load(
    f'platformer/data/images/Backgrounds/level1/rocks_1.png')
mountain_background_image = pygame.image.load(
    f'platformer/data/images/Backgrounds/level1/rocks_2.png')
clouds1_background_image = pygame.image.load(
    f'platformer/data/images/Backgrounds/level1/clouds_1.png')
clouds2_background_image = pygame.image.load(
    f'platformer/data/images/Backgrounds/level1/clouds_2.png')
clouds3_background_image = pygame.image.load(
    f'platformer/data/images/Backgrounds/level1/clouds_3.png')
clouds4_background_image = pygame.image.load(
    f'platformer/data/images/Backgrounds/level1/clouds_4.png')

sky_background_image = pygame.transform.scale(
    sky_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
rocks_background_image = pygame.transform.scale(
    rocks_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
mountain_background_image = pygame.transform.scale(
    mountain_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
clouds1_background_image = pygame.transform.scale(
    clouds1_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
clouds2_background_image = pygame.transform.scale(
    clouds2_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
clouds3_background_image = pygame.transform.scale(
    clouds3_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
clouds4_background_image = pygame.transform.scale(
    clouds4_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_background():
    screen.blit(sky_background_image, (0, 0))
    width = sky_background_image.get_width()
    for x in range(5):
        screen.blit(rocks_background_image,
                    (int((x * width) - background_scroll * 0.1), 0))
        screen.blit(mountain_background_image,
                    (int((x * width) - background_scroll * 0.3), 0))
        screen.blit(clouds1_background_image,
                    (int((x * width) - background_scroll * 0.4), 0))
        screen.blit(clouds2_background_image,
                    (int((x * width) - background_scroll * 0.4), 0))
        screen.blit(clouds3_background_image,
                    (int((x * width) - background_scroll * 0.5), 0))
        screen.blit(clouds4_background_image,
                    (int((x * width) - background_scroll * 0.6), 0))

# load all images & animations


def load_entity_animations():
    animation_types = ['Death', 'Fall', 'Idle', 'Jump', 'Roll', 'Use', 'Walk']
    entity_types = ['Player', 'Enemy']

    list_of_loaded_animations = []
    for entity_type in entity_types:
        entity_animations = []
        # load all images for the players
        for animation in animation_types:
            # reset temporary list of images
            temp_list = []
            # count number of files in the folder
            if os.path.isdir(f'platformer/data/images/entities/{entity_type}/{animation}'):
                num_of_frames = len(os.listdir(
                    f'platformer/data/images/entities/{entity_type}/{animation}'))

                for i in range(num_of_frames):
                    # print(f'{entity_type} & {animation} - {i}')
                    img = pygame.image.load(
                        f'platformer/data/images/entities/{entity_type}/{animation}/{i}.png')
                    img = pygame.transform.scale(
                        img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)

                entity_animations.append(temp_list)
            else:
                entity_animations.append([])

        list_of_loaded_animations.append(entity_animations)

    return list_of_loaded_animations


animations_list = load_entity_animations()


class Animation_type(IntEnum):
    Death = 0,
    Fall = 1,
    Idle = 2,
    Jump = 3,
    Roll = 4,
    Use = 5,
    Walk = 6,


class World():
    def __init__(self):
        self.obstacles_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        # iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile in (66, 67, 68, 69, 70, 71, 72, 73, 88, 89, 90, 92, 94, 95, 96, 110, 111, 112, 115):
                        self.obstacles_list.append(tile_data)
                    elif tile == 152:
                        key = Collectible(
                            'Key;', img, x * TILE_SIZE, y * TILE_SIZE)
                        key_group.add(key)
                    elif tile in (232, 234, 254, 256):
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile == 238:  # create player
                        player = Player(x * TILE_SIZE,
                                        y * TILE_SIZE, 5)
                    elif tile == 239:  # create player
                        new_enemy = Enemy(x * TILE_SIZE,
                                          y * TILE_SIZE, 5)
                        enemies_group.add(new_enemy)

        return player

    def draw(self):
        for tile in self.obstacles_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 0, 0),
                             (tile[1].x, tile[1].y, tile[1].width, tile[1].height), 2)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.entity_id = 0

        self.alive = True
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = animations_list[self.entity_id]
        self.frame_index = 0
        self.action = 0
        self.update_time = 0
        self.local_time = 0

        self.keys = 0

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, moving_left, moving_right, current_time, tick):
        self.local_time = current_time
        self.update_animation()
        # reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += int(self.vel_y)

        # check for collision
        for tile in world.obstacles_list:
            # check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0

            # check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground, i.e. jumping
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # check if above the ground, i.e. falling
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            dx = 0

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        # update scroll based on player position
        if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and background_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) or (self.rect.left < SCROLL_THRESH and background_scroll > abs(dx)):
            self.rect.x -= dx
            screen_scroll = -dx

        return screen_scroll

    def draw(self):
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if self.local_time - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = self.local_time
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):

            self.frame_index = 0

    def set_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = self.local_time


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.entity_id = 1
        self.alive = True
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = animations_list[self.entity_id]
        self.frame_index = 0
        self.action = 0
        self.update_time = 0
        self.local_time = 0

        self.keys = 0

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self, current_time, tick):
        self.local_time = current_time
        self.update_animation()

        dx = 1
        dy = 0

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += int(self.vel_y)

        # check for collision
        for tile in world.obstacles_list:
            # check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx *= -1
            # check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if above the ground, i.e. falling
                if self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
            dx = 0

        # update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(pygame.transform.flip(
            self.image, self.flip, False), self.rect)

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if self.local_time - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = self.local_time
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def set_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = self.local_time


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll


class Collectible(pygame.sprite.Sprite):
    def __init__(self, coll_type, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = coll_type
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        # scroll
        self.rect.x += screen_scroll
        # check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            if self.type == 'Key':
                player.keys += 1
                # delete the item box
                self.kill()


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll
        if pygame.sprite.collide_rect(self, player):
            level += 1
            # delete the item box
            self.kill()


running = True
current_time = 0
# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# load in level data and create world
layer = 1
with open(f'platformer/data/maps/level{1}layer{layer}.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
# create sprite groups
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
collectible_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

world = World()

player = world.process_data(world_data)


# Game loop.
while running:
    time_per_frame = Clock.tick(FPS)
    tick_in_seconds = time_per_frame / 1000.0
    current_time += time_per_frame
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive and not player.in_air:
                player.jump = True

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    if player.alive:
        if player.in_air:
            player.set_action(Animation_type.Jump)  # 2: jump
        elif moving_left or moving_right:
            player.set_action(Animation_type.Walk)  # 1: run
        else:
            player.set_action(Animation_type.Idle)  # 0: idle

    # Update.
    background_scroll -= screen_scroll
    screen_scroll = player.update(
        moving_left, moving_right, current_time, tick_in_seconds)
    water_group.update()
    enemies_group.update(current_time, tick_in_seconds)
    decoration_group.update()
    exit_group.update()
    # print(f'{player.action, player.frame_index} & {player.local_time, player.update_time}')
    # Draw.
    draw_background()
    world.draw()
    enemies_group.draw(screen)
    water_group.draw(screen)
    player.draw()
    pygame.display.update()
