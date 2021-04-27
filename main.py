import pygame
import math
import sys
import os
import csv
import random
from pygame.locals import *
from enum import IntEnum
from data.camera.camera import *
from data.physics import *
vec = pygame.math.Vector2

pygame.init()

FPS = 60
Clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# define game variables
GRAVITY = 1
GRAVITY_FORCE_LIMIT = 15
ROWS = 15
COLS = 50
TILE_SIZE = round(SCREEN_HEIGHT / ROWS)
TILE_TYPES = 264

# level
level = 0
global level_complete
level_complete = False
# define player action variables
moving_left = False
moving_right = False


# scale
scale = 1

# store tiles in a list
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'platformer/data/images/Tiles/{x}.png')
    if x == 210 or x == 210:
        img = pygame.transform.scale(img, (TILE_SIZE, round(
            TILE_SIZE/(img.get_width()/img.get_height()))))
    elif not x == 101:
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

green_key_image = pygame.image.load(
    f'platformer/data/images/Items/green_key.png')
health_image = pygame.image.load(
    f'platformer/data/images/Other/health.png')
health_image = pygame.transform.scale(
    health_image, (int(TILE_SIZE), int(TILE_SIZE)))
health_image_width = health_image.get_width()

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


def draw_background(canvas, offset_x, offset_y):
    canvas.blit(sky_background_image, (0, 0))

    width = sky_background_image.get_width()
    for x in range(2):
        canvas.blit(rocks_background_image,
                    (round(x*width - offset_x*0.1), round(0-offset_y*0.3)))
        canvas.blit(mountain_background_image,
                    (round(x*width - offset_x*0.15), round(0-offset_y*0.3)))
        canvas.blit(clouds1_background_image,
                    (round(x*width - offset_x*0.2), round(0-offset_y*0.3)))
        canvas.blit(clouds2_background_image,
                    (round(x*width - offset_x*0.3), round(0-offset_y*0.3)))
        canvas.blit(clouds3_background_image,
                    (round(x*width - offset_x*0.25), round(0-offset_y*0.3)))
        canvas.blit(clouds4_background_image,
                    (round(x*width - offset_x*0.3), round(0-offset_y*0.3)))


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


# reset level data
def reset_level():
    decoration_group.empty()
    water_group.empty()
    key_group.empty()
    enemies_group.empty()
    collectible_group.empty()
    exit_group.empty()
    checkpoints_group.empty()

    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)

    return data


def load_level():
    global level
    level += 1
    bg_scroll = 0
    world_data = reset_level()
    # load in level data and create world
    with open(f'platformer/data/maps/level{level}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    world = World()
    player, camera, all_platforms = world.process_data(world_data)

    return world, player, camera, all_platforms


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
        self.invisible_obstacles_list = []

    def process_data(self, data):
        self.level_length = len(data[0])
        self.platforms = []
        # iterate through each value in level data file
        platform_id = 0
        for y, row in enumerate(data):
            platform = []
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)

                    if tile in (66, 67, 68, 69, 70, 88, 89, 90, 92, 94, 95, 96, 110, 111, 112, 115):
                        self.obstacles_list.append(tile_data)
                    elif tile == 71:
                        platform.append(PlatformPart(
                            img, x*TILE_SIZE, y*TILE_SIZE))

                    elif tile == 72:
                        platform.append(PlatformPart(
                            img, x*TILE_SIZE, y*TILE_SIZE))

                    elif tile == 73:
                        platform.append(PlatformPart(
                            img, x*TILE_SIZE, y*TILE_SIZE))
                        new_surface = pygame.Surface((
                            int(len(platform) * TILE_SIZE), int(TILE_SIZE)))

                        self.platforms.append(Platform(platform[0].rect.x, platform[0].rect.y, len(
                            platform)*TILE_SIZE, TILE_SIZE, platform, new_surface, platform_id))
                        platform_id += 1
                        platform = []
                    elif tile == 101:
                        key = Collectible(
                            'Key', img, x * TILE_SIZE, y * TILE_SIZE)
                        key_group.add(key)
                    elif tile in (130, 152, 174):
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 210 or tile == 211:
                        new_spike = Spike(img, x * TILE_SIZE, y * TILE_SIZE)
                        spikes_group.add(new_spike)
                    elif tile in (232, 234, 254, 256):
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile == 238:  # create player
                        player = Entity(0, x * TILE_SIZE,
                                        y * TILE_SIZE, 5)
                        camera = Camera(player)
                        border = Border(
                            camera, player, self.get_world_length())
                        camera.setmethod(border)
                    elif tile == 239:  # create enemy
                        new_enemy = Entity(1, x * TILE_SIZE,
                                           y * TILE_SIZE, 2)
                        enemies_group.add(new_enemy)
                    elif tile == 56:  # create invis tile
                        self.invisible_obstacles_list.append(tile_data)
                    elif tile == 263:
                        new_checkpoint = Checkpoint(
                            img, x * TILE_SIZE, y * TILE_SIZE)
                        checkpoints_group.add(new_checkpoint)

        return player, camera, self.platforms

    def draw(self, canvas, offset_x, offset_y):
        for tile in self.obstacles_list:
            canvas.blit(tile[0], (round(tile[1].x - offset_x),
                                  round(tile[1].y - offset_y), tile[1].width, tile[1].height))
            pygame.draw.rect(canvas, (255, 0, 0),
                             (round(tile[1].x - offset_x), round(tile[1].y - offset_y), tile[1].width, tile[1].height), 2)
            # pygame.draw.rect(canvas, (255, 255, 12),
            #                  (tile[1].x, tile[1].y, tile[1].width, tile[1].height), 2)

    def get_world_length(self):
        return self.level_length * TILE_SIZE


class Entity(pygame.sprite.Sprite):
    def __init__(self, entity_id, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.entity_id = entity_id
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
        self.air_timer = 0

        self.keys = 0
        self.checkpoint_position = vec(0, 0)

        # rect properties
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.collision_treshold = 16

        if self.entity_id == 0:
            self.health_points = 1
        elif self.entity_id == 1:
            self.health_points = 1

    def update(self, current_time, tick):
        self.local_time = current_time
        self.update_animation()

    def move(self, moving_left, moving_right):

        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed

        if moving_right:
            dx = self.speed

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > GRAVITY_FORCE_LIMIT:
            self.vel_y = GRAVITY_FORCE_LIMIT

        dy += self.vel_y

        self.in_air = True

        if self.entity_id == 1:
            for tile in world.invisible_obstacles_list:
                # check collision in the x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    self.direction *= -1

        if self.entity_id == 0:
            if self.rect.left + dx < 0 or self.rect.right + dx > (world.level_length * TILE_SIZE):
                dx = 0

        if self.rect.y + dy < 0:
            dy = 0
            self.vel_y = 0

        # print(dy)
        on_platform = None
        for platform in all_platforms:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if above platform
                if abs((self.rect.bottom) - platform.rect.top) <= self.collision_treshold:
                    on_platform = platform
                if platform.move_x != 0:
                    dx += platform.direction * platform.speed
        self.rect, colls, on_platform = move_with_collisions(
            self, [dx, dy], world.obstacles_list, all_platforms, enemies_group)

        if colls['bottom'] or colls['bottom-platform']:
            self.vel_y = 0
            self.air_timer = 0
            self.in_air = False
            dy = 0
        else:
            self.air_timer += 1

        if colls['top']:
            self.vel_y = 0

    def ai(self):
        if self.direction == 1:
            ai_moving_right = True
        else:
            ai_moving_right = False
        ai_moving_left = not ai_moving_right

        self.move(ai_moving_left, ai_moving_right)

    def reset_position(self, position):
        self.rect.x = round(position[0])
        self.rect.y = round(position[1])

    def hurt(self):
        if self.health_points - 1 > 0:
            self.health_points -= 1
            self.reset_position(self.checkpoint_position)

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(pygame.transform.flip(self.image, self.flip, False), (int(self.rect.x -
                                                                              offset_x), int(self.rect.y -
                                                                                             offset_y)))

        if self.entity_id == 0:
            pygame.draw.rect(canvas, (255, 0, 0), (round(self.rect.x - offset_x),
                                                   round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

    def draw_keys(self, canvas):
        canvas.blit(green_key_image, (round(10*scale), round(10*scale)))

    def draw_health(self, canvas):
        x = 10
        for health in range(self.health_points):
            canvas.blit(health_image, (x, SCREEN_HEIGHT - 50*scale))
            x += health_image_width + 5*scale

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


class PlatformPart(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, parts, surface, id):
        pygame.sprite.Sprite.__init__(self)
        self.platform_id = id
        self.parts = parts

        self.image = surface
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.determine_movement_by_id(self.platform_id)

    def update(self):
        dx = 0
        dy = 0

        if self.move_x:
            dx = self.direction * self.speed

        if self.move_y:
            dy = self.direction * self.speed

        for tile in world.invisible_obstacles_list:
            # check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx *= -1
                self.direction *= -1
            elif tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                dy *= -1
                self.direction *= -1
        for tile in world.obstacles_list:
            # check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx *= -1
                self.direction *= -1
            elif tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                dy *= -1
                self.direction *= -1

        self.rect.x += dx
        self.rect.y += dy
        # if self.platform_id == 2:
        #     print(dy)

    def draw(self, canvas, offset_x, offset_y):
        for x, part in enumerate(self.parts):
            self.image.blit(part.image, (x*TILE_SIZE, 0))
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))
        pygame.draw.rect(canvas, (255, 0, 0), (round(self.rect.x - offset_x),
                                               round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

    def determine_movement_by_id(self, id):
        if id == 0:
            self.direction = 1
            self.speed = 1
            self.move_x = 0
            self.move_y = 1
        elif id == 1:
            self.direction = 1
            self.speed = 1
            self.move_x = 0
            self.move_y = 1
        elif id == 2:
            self.direction = 1
            self.speed = 1
            self.move_x = 1
            self.move_y = 0
        elif id == 3:
            self.direction = 1
            self.speed = 1
            self.move_x = 1
            self.move_y = 0


class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))


class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x - offset_x),
                                 round(self.rect.y-offset_y)))

    def collide_water(self, target):
        if pygame.sprite.collide_rect(self, target):
            target.hurt()


class Collectible(pygame.sprite.Sprite):
    def __init__(self, coll_type, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = coll_type
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))
        pygame.draw.rect(canvas, (255, 0, 0),
                         (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

    def collect(self, player):
        if pygame.sprite.collide_rect(self, player):
            if self.type == 'Key':
                player.keys += 1
                self.kill()


class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))


class Spike(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))


class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

        self.location = (x, y)
        self.active = True

    def update(self, player):
        if self.rect.colliderect(player.rect) and self.active:
            player.checkpoint_position = vec(
                self.rect.centerx, self.rect.y - 100*scale)
            for checkpoint in checkpoints_group:
                if checkpoint.rect.x < self.rect.x:
                    checkpoint.active = False
                elif checkpoint == self:
                    self.active = False
                    break

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))


running = True
current_time = 0
# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)

# create sprite groups
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
collectible_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
checkpoints_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()

world, player, camera, all_platforms = load_level()
# Game loop.
while running:
    time_per_frame = Clock.tick(FPS)
    tick_in_seconds = time_per_frame / 1000.0
    current_time += time_per_frame
    screen.fill((0, 0, 0))
    canvas.fill((0, 0, 0))

    if level_complete:
        world, player, camera, all_platforms = load_level()
        level_complete = False

    # User input
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
            if event.key == pygame.K_w and player.alive:
                if player.air_timer < 10:
                    player.vel_y = -20
                    player.jump = True

        # keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                player.jump = False

    # Update methods
    for platform in all_platforms:
        platform.update()

    player.update(current_time, tick_in_seconds)
    player.move(moving_left, moving_right)

    for enemy in enemies_group:
        enemy.update(current_time, time_per_frame)
        enemy.ai()

    for checkpoint in checkpoints_group:
        checkpoint.update(player)

    for exit in exit_group:
        exit.update(player)

    if pygame.sprite.spritecollide(player, exit_group, False):
        level_complete = True
    # adjust camera to player
    camera.scroll()
    offset_x, offset_y = camera.offset.x, camera.offset.y
    # Draw methods
    draw_background(canvas, offset_x, offset_y)
    world.draw(canvas, offset_x, offset_y)

    for spike in spikes_group:
        spike.draw(canvas, offset_x, offset_y)

    for checkpoint in checkpoints_group:
        checkpoint.draw(canvas, offset_x, offset_y)

    for platform in all_platforms:
        platform.draw(canvas, offset_x, offset_y)

    for key in key_group:
        key.collect(player)
        key.draw(canvas, offset_x, offset_y)

    for enemy in enemies_group:
        enemy.draw(canvas, offset_x, offset_y)

    for exit in exit_group:
        exit.draw(canvas, offset_x, offset_y)

    for water in water_group:
        water.collide_water(player)
        water.draw(canvas, offset_x, offset_y)

    player.draw(canvas, offset_x, offset_y)
    player.draw_keys(canvas)
    player.draw_health(canvas)
    screen.blit(canvas, (0, 0))

    pygame.display.update()
