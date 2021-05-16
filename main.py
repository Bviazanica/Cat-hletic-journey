import pygame
import math
import sys
import os
import csv
import random
from pygame.locals import *
from data.button import Button
from enum import IntEnum
from data.camera.camera import *
from data.physics import *
from data.utility import *
from data.json_reader import *
vec = pygame.math.Vector2

pygame.init()

FPS = 60
Clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

# define game variables
GRAVITY = 50
GRAVITY_FORCE_LIMIT = 15
ROWS = 15
COLS = 200
TILE_SIZE = round(SCREEN_HEIGHT / ROWS)
TILE_TYPES = 264

platforms_json_data = platforms_data()
# font
font = pygame.font.Font('platformer/data/font/kenney_blocks.ttf', 70)

# scale
scale = 1
wingman_image = pygame.image.load(
    f'platformer/data/images/entities/Wingman/Walk/0.png').convert_alpha()
wingman_image = pygame.transform.scale(
    wingman_image, (TILE_SIZE, TILE_SIZE))

cloud_image = pygame.image.load(
    f'platformer/data/images/entities/Cloud/cloud.png').convert_alpha()

button_clicked = pygame.image.load(
    f'platformer/data/images/interface/button_1.png').convert_alpha()

fake_platform_green = pygame.image.load(
    f'platformer/data/images/tiles/68.png').convert_alpha()
fake_ground_green = pygame.image.load(
    f'platformer/data/images/tiles/66.png').convert_alpha()

fake_platform_green = pygame.transform.scale(
    fake_platform_green, (TILE_SIZE, TILE_SIZE))
fake_ground_green = pygame.transform.scale(
    fake_ground_green, (TILE_SIZE, TILE_SIZE))


green_key_image = pygame.image.load(
    f'platformer/data/images/items/green_key.png').convert_alpha()
health_image = pygame.image.load(
    f'platformer/data/images/other/health.png').convert_alpha()
health_image = pygame.transform.scale(
    health_image, (int(TILE_SIZE), int(TILE_SIZE)))
health_image_width = health_image.get_width()

sky_background_image = pygame.image.load(
    f'platformer/data/images/backgrounds/level1/sky.png').convert_alpha()
rocks_background_image = pygame.image.load(
    f'platformer/data/images/backgrounds/level1/rocks_1.png').convert_alpha()
mountain_background_image = pygame.image.load(
    f'platformer/data/images/backgrounds/level1/rocks_2.png').convert_alpha()
clouds1_background_image = pygame.image.load(
    f'platformer/data/images/backgrounds/level1/clouds_1.png').convert_alpha()
clouds2_background_image = pygame.image.load(
    f'platformer/data/images/backgrounds/level1/clouds_2.png').convert_alpha()
clouds3_background_image = pygame.image.load(
    f'platformer/data/images/backgrounds/level1/clouds_3.png').convert_alpha()
clouds4_background_image = pygame.image.load(
    f'platformer/data/images/backgrounds/level1/clouds_4.png').convert_alpha()

bubble_item_image = pygame.image.load(
    f'platformer/data/images/tiles/57.png').convert_alpha()
boost_item_image = pygame.image.load(
    f'platformer/data/images/tiles/58.png').convert_alpha()
health_item_image = pygame.image.load(
    f'platformer/data/images/tiles/59.png').convert_alpha()

bubble_image =  pygame.image.load(
    f'platformer/data/images/other/bubble.png').convert_alpha()

effect_durations = {
    'Bubble':5000,
    'Boost':5000
}

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

bubble_image = pygame.transform.scale(
    bubble_image, (TILE_SIZE*2, TILE_SIZE*2))
bubble_rect = bubble_image.get_rect()
# create sprite groups
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
collectible_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
checkpoints_group = pygame.sprite.Group()
spikes_group = pygame.sprite.Group()
fake_platforms_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()
clouds_group = pygame.sprite.Group()
wingmans_group = pygame.sprite.Group()
levers_group = pygame.sprite.Group()
snakes_group = pygame.sprite.Group()
item_boxes_group = pygame.sprite.Group()
def draw_background(canvas, offset_x, offset_y):
    canvas.blit(sky_background_image, (0, 0))

# load all images & animations
def load_entity_animations(scale):
    animation_types = ['Death', 'Fall', 'Idle', 'Jump', 'Run', 'Slide', 'Walk', 'Attack', 'Appear', 'Disappear']
    entity_types = ['Player', 'Green_enemy', 'Spikeman', 'Wingman','Snake']

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
                        f'platformer/data/images/entities/{entity_type}/{animation}/{i}.png').convert_alpha()
                    if entity_type == 'Spikeman':
                        if i == 0:
                            img = pygame.transform.smoothscale(
                                img, (TILE_SIZE, TILE_SIZE))
                        else:
                            img = pygame.transform.smoothscale(
                                img, (TILE_SIZE - round(TILE_SIZE/4), TILE_SIZE ))
                    elif  entity_type == 'Snake':
                        img = pygame.transform.smoothscale(
                            img, (TILE_SIZE, TILE_SIZE))
                    elif entity_type == 'Player' :
                        img = pygame.transform.smoothscale(
                            img, (TILE_SIZE*2, TILE_SIZE*2))
                    else:
                        img = pygame.transform.scale(
                            img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    temp_list.append(img)
                entity_animations.append(temp_list)
            else:
                entity_animations.append([])
        list_of_loaded_animations.append(entity_animations)
    return list_of_loaded_animations


animations_list = load_entity_animations(scale)

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)


# reset level data
def reset_level():
    decoration_group.empty()
    water_group.empty()
    key_group.empty()
    enemies_group.empty()
    collectible_group.empty()
    exit_group.empty()
    checkpoints_group.empty()
    spikes_group.empty()
    fake_platforms_group.empty()
    items_group.empty()
    clouds_group.empty()
    snakes_group.empty()
    wingmans_group.empty()
    levers_group.empty()
    item_boxes_group.empty()
    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data


def load_level(level, img_list):
    level += 1
    world_data = reset_level()
    # load in level data and create world
    with open(f'platformer/data/maps/level{level}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    world = World()
    player, camera, all_platforms, invisible_blocks = world.process_data(
        world_data, img_list, level)

    return world, player, camera, all_platforms, invisible_blocks, level

class Animation_type(IntEnum):
    Death = 0,
    Fall = 1,
    Idle = 2,
    Jump = 3,
    Run = 4,
    Slide = 5,
    Walk = 6,
    Attack = 7,
    Appear = 8,
    Disappear = 9


class World():
    def __init__(self):
        self.obstacles_list = []
        self.bounds_tiles_list = []
        self.invisible_blocks_list = []

    def process_data(self, data, img_list, level):
        self.level_length = len(data[0])
        self.platforms = []

        # iterate through each value in level data file
        platform_id = 0
        fake_platform_id = 0
        for y, row in enumerate(data):
            platform = []
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)

                    if tile in (66, 67, 68, 69, 70, 89, 90, 92, 94, 95, 96, 111, 112, 115):
                        self.obstacles_list.append(tile_data)
                    
                    elif tile == 56:  # create invis tile
                        self.bounds_tiles_list.append(tile_data)
                    elif tile == 57:
                        new_item = Item(bubble_item_image,'Bubble', x*TILE_SIZE, y*TILE_SIZE)
                        items_group.add(new_item)
                    elif tile == 58:
                        new_item = Item(health_item_image,'Health', x*TILE_SIZE, y*TILE_SIZE)
                        items_group.add(new_item)
                    elif tile == 59:
                        new_item = Item(boost_item_image,'Boost', x*TILE_SIZE, y*TILE_SIZE)
                        items_group.add(new_item)
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

                        self.platforms.append(Platform(
                            platform[0].rect.x, platform[0].rect.y, platform, new_surface, platform_id,level))
                        platform_id += 1
                        platform = []
                    elif tile == 74:
                        self.platforms.append(Platform(
                            x*TILE_SIZE, y*TILE_SIZE, 1, img, platform_id, level))
                        platform_id += 1
                    elif tile == 110:
                        if x == 7:
                            new_fake_platform = FakePlatform(
                                x * TILE_SIZE, y*TILE_SIZE, 3, 3, 'fall', fake_platform_id)
                            fake_platform_id += 1
                            fake_platforms_group.add(new_fake_platform)
                            self.platforms.append(new_fake_platform)
                    elif tile == 101:
                        key = Collectible(
                            'Key', img, x * TILE_SIZE, y * TILE_SIZE)
                        key_group.add(key)
                    elif tile in (130, 152, 174):
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)
                    elif tile == 192:
                        new_block = InvisibleBlock(
                            img, x*TILE_SIZE, y*TILE_SIZE)
                        self.invisible_blocks_list.append(new_block)
                    elif tile == 193:
                        new_item_box = ItemBox(
                            img, x*TILE_SIZE, y*TILE_SIZE, 2)
                        item_boxes_group.add(new_item_box)
                    elif tile == 210 or tile == 211:
                        new_spike = Spike(img, x * TILE_SIZE, y * TILE_SIZE)
                        spikes_group.add(new_spike)
                    elif tile == 215:
                        new_item_box = ItemBox(
                            img, x*TILE_SIZE, y*TILE_SIZE, 1)
                        item_boxes_group.add(new_item_box)
                    elif tile == 230:
                        lever = Lever(x * TILE_SIZE, y * TILE_SIZE, 'green')
                        levers_group.add(lever)
                    elif tile == 252:
                        lever = Lever(x * TILE_SIZE, y * TILE_SIZE, 'red')
                        levers_group.add(lever)
                    elif tile in (232, 234, 254, 256):
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                        if tile == 254 and x == 30 and y == 14:
                            key = Collectible(
                            'Key', green_key_image, x * TILE_SIZE, y * TILE_SIZE - 2)
                            key_group.add(key)
                    elif tile == 238:  # create player
                        player = Entity(0, x * TILE_SIZE,
                                        y * TILE_SIZE, 300)
                        camera = Camera(player)
                        camera_type = Border(
                                camera, player, self.get_world_length())
                        camera.setmethod(camera_type)
                    elif tile == 239:  # create enemy
                        new_enemy = Entity(1, x * TILE_SIZE,
                                           y * TILE_SIZE, 150)
                        enemies_group.add(new_enemy)
                    elif tile == 240:  # create Cloud
                        new_cloud = Cloud(cloud_image, x * TILE_SIZE,
                                           y * TILE_SIZE)
                        clouds_group.add(new_cloud)
                    elif tile == 258:  # create Snake
                        new_snake = Snake(4, x * TILE_SIZE,
                                           y * TILE_SIZE)
                        snakes_group.add(new_snake)
                    elif tile == 260: # create Spikeman
                        new_spikeman = Entity(2,  x * TILE_SIZE, y * TILE_SIZE -100, 120)
                        enemies_group.add(new_spikeman)
                    elif tile == 261: # create Wingman
                        new_wingman = Wingman(3,x * TILE_SIZE, y * TILE_SIZE, 200)
                        enemies_group.add(new_wingman)
                    elif tile == 263: # create Checkpoint
                        new_checkpoint = Checkpoint(
                            img, x * TILE_SIZE, y * TILE_SIZE)
                        checkpoints_group.add(new_checkpoint)

        return player, camera, self.platforms, self.invisible_blocks_list

    def draw(self, canvas, offset_x, offset_y):
        for tile in self.obstacles_list:
            canvas.blit(tile[0], (round(tile[1].x - offset_x),
                                  round(tile[1].y - offset_y), tile[1].width, tile[1].height))
            # pygame.draw.rect(canvas, (255, 0, 0),
            #                  (round(tile[1].x - offset_x), round(tile[1].y - offset_y), tile[1].width, tile[1].height), 2)
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

        self.moving_left = False
        self.moving_right = False

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

        self.invulnerability = False
        self.boosted = False

        self.invulnerability_start_time = 0
        self.boost_start_time = 0
        
        # rect properties
        if self.entity_id == 0:
            self.action = int(Animation_type.Idle)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect(width=45, height=70)
        
        elif self.entity_id == 1:
            self.action = int(Animation_type.Walk)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
        
        elif self.entity_id == 2:
            self.action = int(Animation_type.Walk)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
        
        self.rect.topleft = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.collision_treshold = 25

        if self.entity_id == 0:
            self.health_points = 3
        elif self.entity_id != 0:
            self.health_points = 1

       
        self.new_state = False
        # self.states = {'Death':'Death','Fall': 'Fall', 'Idle':'Idle', 'Jump':'Jump','Run':'Run','Slide':'Slide','Walk':'Walk'}
        # self.state = self.states['Idle']
        self.in_death_animation = False

        self.on_platform = False
        self.was_on_platform = False

    def update(self, current_time, tick, world, all_platforms):
        self.local_time = current_time
        if self.invulnerability and self.local_time - self.invulnerability_start_time > effect_durations['Bubble']:
            self.invulnerability = False
        if self.boosted and self.local_time - self.boost_start_time > effect_durations['Boost']:
            self.speed = 300 #nastavit na speed before
            self.boosted = False

        if self.rect.x > world.get_world_length() or self.rect.x + self.rect.width < 0 or \
                        self.rect.y + self.rect.height < 0 or self.rect.y > SCREEN_HEIGHT:
            self.hurt(True)

        if self.in_death_animation == False:
            if self.entity_id == 0:
                self.move(self.moving_left, self.moving_right, world, all_platforms,tick)
                self.flip = True if self.direction < 0 else False

            elif self.entity_id != 0:
                self.set_action(int(Animation_type.Walk))
                self.determine_movement()
                self.move(self.moving_left, self.moving_right, world, all_platforms,tick)

            if self.air_timer > 0 and self.was_on_platform:
                self.vel_y = 1
        else:
            self.set_action(int(Animation_type.Death))

        self.update_animation()

    def move(self, moving_left, moving_right, world, all_platforms,tick):
        dx = 0
        dy = 0

        self.was_on_platform = self.on_platform

        if moving_left:
            dx = -self.speed * tick
        if moving_right:
            dx = self.speed * tick
        
        # apply gravity
        self.vel_y = apply_gravitation(self.vel_y, GRAVITY, tick, GRAVITY_FORCE_LIMIT)

        dy += self.vel_y
        self.in_air = True

        dx= round(dx)
        dy = round(dy)
        
        if self.entity_id != 0:
            for tile in world.bounds_tiles_list:
                # check collision in the x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    self.direction *= -1
                    
            
        if self.entity_id == 0:
            if self.rect.left + dx < 0 or self.rect.right + dx > (world.level_length * TILE_SIZE):
                dx = 0
            for fake_platform in fake_platforms_group:
                if fake_platform.rect.colliderect(self.rect.x + dy, self.rect.y + dy, self.width, self.height):
                    fake_platform.activated = True

            for spike in spikes_group:
                if spike.rect.colliderect(self.rect.x + dy, self.rect.y + dy, self.width, self.height) and not self.invulnerability:
                    self.hurt(False)
            
            for cloud in clouds_group:
                if cloud.rect.colliderect(self.rect.x + dy, self.rect.y + dy, self.width, self.height) and not self.invulnerability:
                    self.hurt(False)
            
        if self.rect.y + dy < 0:
            dy = 0
            self.vel_y = 0

        for platform in all_platforms:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if platform.move_x != 0:
                    dx += platform.direction * platform.speed * tick
        
        dx= round(dx)
        dy = round(dy)
        self.rect, colls = move_with_collisions(
            self,[dx, dy], world.obstacles_list, all_platforms, enemies_group, world.invisible_blocks_list, item_boxes_group)
        
        if colls['bottom'] or colls['bottom-platform']:
            self.air_timer = 0
            self.in_air = False
            self.on_platform = True
            self.jump = False
        else:
            self.air_timer += 1
            self.on_platform = False
            
        if self.entity_id != 0:
            if colls['right'] or colls['left']:
                self.direction *= -1

        if not self.on_platform and self.air_timer > 0 and self.was_on_platform and not self.jump:
            self.vel_y = 1
            self.was_on_platform = False
        if colls['top'] or colls['item-box-top']:
            self.vel_y = 0

    def determine_movement(self):
        if self.direction == 1:
            self.moving_right = True
            self.flip = False
        else:
            self.moving_right = False
            self.flip = True
        self.moving_left = not self.moving_right
        
    def reset_position(self, position):
        self.rect.x = round(position[0])
        self.rect.y = round(position[1])

    def hurt(self, out_of_bounds):
        if not self.in_death_animation:
            if self.health_points - 1 > 0:
                if not out_of_bounds:
                    self.in_death_animation = True
                    self.health_points -= 1
                    print('reset in bound')
                else:
                    self.health_points -= 1
                    self.reset_position(self.checkpoint_position)
                    print('reset out of bound')
            else:
                self.health_points -= 1
                if not out_of_bounds:
                    self.in_death_animation = True
                    print('dead in bound')
                else:
                    if self.entity_id != 0:
                        self.kill()
                    self.alive = False
                    print('dead out of  bound')
            print(f'{self.alive, self.in_death_animation,self.entity_id, self.health_points, self.rect}')

            
    
    def use(self, possible_use_item_list, snakes_group, current_time):
        for item in possible_use_item_list:
            if self.rect.colliderect(item.rect):
                if item.lever_type == 'green':
                    if item.activated:
                        item.action(snakes_group, 'Appear')
                        
                    else:
                        item.action(snakes_group, 'Disappear')
                        item.activation_time = current_time
                elif item.lever_type == 'red':
                    pass
                break
            
    def draw(self, canvas, offset_x, offset_y):
        if self.entity_id == 0:
            canvas.blit(pygame.transform.flip(self.image, self.flip, False), (round(self.rect.x -
                                                                                offset_x - 20), round(self.rect.y -
                                                                                                    offset_y-10)))
        else:
            canvas.blit(pygame.transform.flip(self.image, self.flip, False), (round(self.rect.x -
                                                                                offset_x), round(self.rect.y -
                                                                                                    offset_y)))                                                                                                            
        pygame.draw.rect(canvas, (255, 0, 0), (round(self.rect.x - offset_x),
                                                   round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)                                                                                            
        if self.entity_id == 0:
            bubble_rect.center = self.rect.center
            
            if self.invulnerability:
                canvas.blit(bubble_image, (bubble_rect.x - offset_x,bubble_rect.y - offset_y))


    def draw_keys(self, canvas):
        canvas.blit(green_key_image, (round(10*scale), round(10*scale)))

    def draw_health(self, canvas):
        x = 10
        for health in range(self.health_points):
            canvas.blit(health_image, (x, SCREEN_HEIGHT - 50*scale))
            x += health_image_width + 5*scale

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        if self.entity_id == 2:
            center = self.rect.center
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = center
        else:
            self.image = self.animation_list[self.action][self.frame_index]

        if self.local_time - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = self.local_time
            self.frame_index += 1

        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == int(Animation_type.Death):
                if self.entity_id == 0 and self.health_points != 0:
                    self.reset_position(self.checkpoint_position)
                    self.action = int(Animation_type.Idle)
                    self.in_death_animation = False
                    self.frame_index = 0
                else:
                    if self.entity_id != 0:
                        self.kill()
                    self.alive = False
            else:
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
    def __init__(self, x, y, parts, surface, id, level):
        pygame.sprite.Sprite.__init__(self)
        self.platform_id = id
        self.parts = parts

        self.image = surface
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.move_x, self.move_y, self.speed, self.direction = self.determine_movement_by_id(level)

    def update(self, world, tick):
        dx = 0
        dy = 0
        if self.move_x:
            dx = self.direction * self.speed * tick
        if self.move_y:
            dy = self.direction * self.speed * tick
        dx = round(dx)
        dy = round(dy)

        for tile in world.bounds_tiles_list:
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

    def draw(self, canvas, offset_x, offset_y):
        if self.parts == 1:
            canvas.blit(self.image, (round(self.rect.x -
                                           offset_x), round(self.rect.y - offset_y)))
            # pygame.draw.rect(canvas, (255, 0, 0), (round(self.rect.x - offset_x),
                                                #    round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)
        else:
            for x, part in enumerate(self.parts):
                self.image.blit(part.image, (x*TILE_SIZE, 0))
            canvas.blit(self.image, (round(self.rect.x -
                                           offset_x), round(self.rect.y - offset_y)))
            # pygame.draw.rect(canvas, (255, 0, 0), (round(self.rect.x - offset_x),
                                                #    round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

    def determine_movement_by_id(self,level):
        data = platforms_json_data[f'level_{level}'][self.platform_id]
        return data['move_x'],data['move_y'],data['speed'],data['direction']

class Item(pygame.sprite.Sprite):
    def __init__(self, image, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.entity_id = 10
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
        self.vel_y = 0
    def update(self, target, current_time, tick, world, all_platforms, item_boxes_group):
        dx = 0
        dy = 0
        self.vel_y = apply_gravitation(self.vel_y, GRAVITY, tick, GRAVITY_FORCE_LIMIT)
        dy += self.vel_y
        if self.rect.colliderect(target.rect):
            self.action(target, current_time)
            self.kill()

        self.rect, colls = move_with_collisions(
                self,[dx, dy], world.obstacles_list, all_platforms, enemies_group, world.invisible_blocks_list, item_boxes_group)

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                    offset_x), round(self.rect.y - offset_y)))

    def action(self, target, current_time):
        if self.item_type == 'Health':
            target.health_points +=1
        elif self.item_type == 'Bubble':
            target.invulnerability = True
            target.invulnerability_start_time = current_time
        elif self.item_type == 'Boost':
            target.boosted = True
            target.boost_start_time = current_time
            target.speed += 100
        

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
            target.hurt(False)

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, img, x, y, hits_to_break):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

        self.destroy = False
        self.hits_to_break = hits_to_break
        self.new_state = False

    def update(self, img_list):
        if self.new_state:
            if self.hits_to_break == 0:
                self.new_state = False
                self.destroy = True
            elif self.hits_to_break == 1:
                self.image = img_list[215]
                self.new_state = False
                
    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x - offset_x),
                                 round(self.rect.y-offset_y)))


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
        # pygame.draw.rect(canvas, (255, 0, 0),
        #                  (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

    def collect(self, player):
        if pygame.sprite.collide_rect(self, player):
            if self.type == 'Key':
                player.keys += 1
                self.kill()


class FakePlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, width_in_tiles, height_in_tiles, action, id):
        pygame.sprite.Sprite.__init__(self)

        new_surface = pygame.Surface((
            int(width_in_tiles * TILE_SIZE), int(TILE_SIZE*height_in_tiles)))

        surface = load_fake_platform_tiles(
            width_in_tiles, height_in_tiles, new_surface, TILE_SIZE, fake_ground_green, fake_platform_green)

        self.fake_platform_id = id
        self.action = action
        self.image = surface
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.direction = 1
        self.speed = 200
        self.move_x = 0
        self.move_y = 0

        self.activated = False

    def update(self, world, tick):
        if self.activated:
            self.execute_action(tick)

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))
        # pygame.draw.rect(canvas, (255, 0, 0),
        #                  (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

    def execute_action(self, tick):
        if self.action == 'fall':
            self.rect.y += round(self.speed *tick)


class InvisibleBlock(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

        self.visible = False

    def draw(self, canvas, offset_x, offset_y):
        if self.visible:
            canvas.blit(self.image, (round(self.rect.x -
                                           offset_x), round(self.rect.y - offset_y)))
        # pygame.draw.rect(canvas, (255, 0, 0),
        #                  (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)


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

#TODO crate 
class Crate(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.entity_id = 99
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

    def update(self, target, current_time, tick, world, all_platforms, item_boxes_group):
        dx = 0
        dy = 0
        self.vel_y = apply_gravitation(self.vel_y, GRAVITY, tick, GRAVITY_FORCE_LIMIT)
        dy += self.vel_y

        self.rect, colls = move_with_collisions(
                self,[dx, dy], world.obstacles_list, all_platforms, enemies_group, world.invisible_blocks_list, item_boxes_group)


    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))

class Snake(pygame.sprite.Sprite):
    def __init__(self,id, x, y ):
        pygame.sprite.Sprite.__init__(self)
        self.entity_id = id

        self.animation_list = animations_list[self.entity_id]
        self.frame_index = 0
        self.action = 2

        self.active = True

        self.vel_y = 0

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.states = {'Idle':'Idle', 'Appear':'Appear', 'Disappear':'Disappear', 'Attack':'Attack'}
        self.state = self.states['Attack']
        self.new_state = False

        self.update_time = 0
        self.local_time = 0

    def update(self,current_time, tick, world, all_platforms, player, item_boxes_group):
        self.local_time = current_time
        
        dx = 0
        dy = 0
        if self.active:
            self.vel_y = apply_gravitation(self.vel_y, GRAVITY, tick, GRAVITY_FORCE_LIMIT)
            dy += self.vel_y
            if is_close(self.rect, player.rect, 50):
                self.state = self.states['Attack']
                self.new_state = True

            self.flip = True if player.rect.center > self.rect.center else False
            
            if self.new_state:
                if self.state == self.states['Idle']:
                    self.set_action(int(Animation_type.Idle))
                    self.new_state = True
                elif self.state == self.states['Appear']:
                    self.set_action(int(Animation_type.Appear))
                elif self.state == self.states['Disappear']:
                    self.set_action(int(Animation_type.Disappear))
                elif self.state == self.states['Attack']:
                    self.set_action(int(Animation_type.Attack))

            self.rect, colls = move_with_collisions(
                self,[dx, dy], world.obstacles_list, all_platforms, enemies_group, world.invisible_blocks_list, item_boxes_group)
            self.update_animation()


    def draw(self, canvas, offset_x, offset_y):
        if self.active:
            canvas.blit(pygame.transform.flip(self.image, self.flip, False), (round(self.rect.x -
                                                                              offset_x), round(self.rect.y -
                                                                                             offset_y)))
            pygame.draw.rect(canvas, (255, 0, 0),
                            (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)


    def update_animation(self):
        ANIMATION_COOLDOWN = 80
        self.image = self.animation_list[self.action][self.frame_index]
        if self.local_time - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = self.local_time
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == int(Animation_type.Disappear):
                self.active = False
            elif self.action == int(Animation_type.Appear):
                self.state = self.states['Idle']
                self.new_state = True
            elif self.action == int(Animation_type.Attack):
                self.new_state = True
                self.state = self.states['Idle']
                self.frame_index = 0
            else:
                self.frame_index = 0

    def set_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = self.local_time


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


class Wingman(pygame.sprite.Sprite):
    def __init__(self,id, x, y, speed):
        self.entity_id = id
        pygame.sprite.Sprite.__init__(self)
        self.image = wingman_image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

        self.location = (x, y)
        self.speed = speed

    def update(self,current_time, tick, world, all_platforms):
        pass
    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))
    
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
            
class Cloud(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

        self.location = (x, y)

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))                                                                            
        pygame.draw.rect(canvas, (255, 0, 0),
                         (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

class Lever(pygame.sprite.Sprite):
    def __init__(self, x, y,lever_color):
        pygame.sprite.Sprite.__init__(self)

        self.lever_type = lever_color
        self.images_list = []
        for i in range(3):
            img = pygame.image.load(
                        f'platformer/data/images/items/lever/{lever_color}_lever_{i}.png').convert_alpha()
            self.images_list.append(img)
        self.image = self.images_list[1]

        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

        self.location = self.rect.midtop

        self.activated = False
        self.activation_time = 0
        self.new_state = False
        
    def update(self, current_time, snakes_group):
        # print(f'{self.activation_time, current_time, current_time - self.activation_time}')
        if self.activated and current_time - self.activation_time > 5000:
            self.new_state = True
            self.action(snakes_group, 'Appear')
        if self.new_state:
            if self.activated:
                self.reset_to_default()
                location = self.rect.bottomleft
                self.image = self.images_list[2]
                self.rect = self.image.get_rect()
                self.rect.bottomleft = location
            else:
                self.reset_to_default()
                location = self.rect.bottomright
                self.image = self.images_list[0]
                self.rect = self.image.get_rect()
                self.rect.bottomright = location
            
    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))                                                                            
        pygame.draw.rect(canvas, (255, 0, 0),
                         (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

    def reset_to_default(self):
        self.image = self.images_list[1]
        self.rect = self.image.get_rect()
        self.rect.midtop = self.location

    def action(self,group, state):
        self.new_state = True
        self.activated = not self.activated

        for member in group:
            member.state = member.states[state]
            member.new_state = True
            member.active = not member.active
    
                                
def game():
    # level
    level = 0
    global level_complete
    level_complete = False

    # store tiles in a list
    img_list = []
    for x in range(TILE_TYPES):
        img = pygame.image.load(f'platformer/data/images/tiles/{x}.png').convert_alpha()
        if x == 210 or x == 211:
            img = pygame.transform.scale(img, (TILE_SIZE, round(
                TILE_SIZE/(img.get_width()/img.get_height()))))
        elif x in (229,230,231):
            img = pygame.transform.scale(img, (img.get_width(), img.get_height()))
        elif not x == 101:
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)

    running = True
    current_time = 0

    world, player, camera, all_platforms, invisible_blocks, level = load_level(
        level, img_list)
    # Game loop.
    while running:
        time_per_frame = Clock.tick(FPS)
        tick = time_per_frame / 1000.0
        current_time += time_per_frame
        screen.fill((0, 0, 0))
        canvas.fill((0, 0, 0))
        if level_complete:
            world, player, camera, all_platforms, invisible_blocks, level = load_level(
                level, img_list)
            level_complete = False
        
        if tick > 0.3:
            tick = 0.2
        # User input
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # keyboard presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.moving_left = True
                    player.direction = -1
                if event.key == pygame.K_d:
                    player.moving_right = True
                    player.direction = 1
                if event.key == pygame.K_w and player.alive and player.jump == False and not player.in_death_animation:
                    if player.air_timer < 10:
                        jump_vel = round(-1800 * tick)
                        if jump_vel < -20:
                            jump_vel = -20
                        player.vel_y = jump_vel
                        player.jump = True
                        player.on_platform = False

           
            # keyboard button released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.moving_left = False
                if event.key == pygame.K_d:
                    player.moving_right = False
                if event.key == pygame.K_w:
                    pass
                if event.key == pygame.K_e:
                    player.use(levers_group, snakes_group, current_time)

        if not player.in_death_animation:
            if player.in_air:
                player.set_action(int(Animation_type.Jump))
            elif player.moving_left or player.moving_right:
                player.set_action(int(Animation_type.Run))
            else:
                player.set_action(int(Animation_type.Idle))
        
        if player.alive:
            # Update methods
            for platform in all_platforms:
                platform.update(world, tick)

            player.update(current_time, tick,  world, all_platforms)

            for enemy in enemies_group:
                enemy.update(current_time, tick, world, all_platforms)

            for box in item_boxes_group:
                box.update(img_list)
                if box.destroy:
                    #spawn item
                    if random.random() > 0.05:
                        choice = random.choice(['Bubble', 'Health', 'Boost', 'Spikeman', 'Snake', 'Green_enemy'])
                        if choice == 'Bubble':
                            new_item = Item(bubble_item_image, choice, box.rect.x, box.rect.y)
                            items_group.add(new_item)
                        elif choice == 'Health':
                            new_item = Item(health_item_image, choice, box.rect.x, box.rect.y)
                            items_group.add(new_item)
                        elif choice == 'Boost':
                            new_item = Item(boost_item_image,  choice, box.rect.x, box.rect.y)
                            items_group.add(new_item)
                        elif choice == 'Spikeman':
                            new_spikeman = Entity(2,  box.rect.x, box.rect.top, 120)
                            enemies_group.add(new_spikeman)
                        elif choice == 'Snake':
                            new_snake = Snake(4, box.rect.x, box.rect.top)
                            snakes_group.add(new_snake)
                        elif choice == 'Green_enemy':
                            new_enemy = Entity(1, box.rect.x, box.rect.top, 150)
                            enemies_group.add(new_enemy)

                        
                    box.kill()

            for snake in snakes_group:
                snake.update(current_time, tick, world, all_platforms, player, item_boxes_group)

            for checkpoint in checkpoints_group:
                checkpoint.update(player)

            for lever in levers_group:
                lever.update(current_time, snakes_group)

            for item in items_group:
                item.update(player, current_time, tick, world, all_platforms, item_boxes_group)

            for exit in exit_group:
                exit.update(player)

            for block in invisible_blocks.copy():
                if block.visible:
                    world.obstacles_list.append([block.image, block.rect])
                    invisible_blocks.pop(invisible_blocks.index(block))

            for platform in all_platforms.copy():
                if platform.rect.x > world.get_world_length() or platform.rect.x + platform.rect.width < 0 or \
                        platform.rect.y + platform.rect.height < 0 or platform.rect.y > 800:
                    all_platforms.pop(all_platforms.index(platform))

            if pygame.sprite.spritecollide(player, exit_group, False):
                level_complete = True
            # adjust camera to player
            camera.scroll()
            offset_x, offset_y = camera.offset.x, camera.offset.y
            # Draw methods
            # draw_background(canvas, offset_x, offset_y)

            world.draw(canvas, offset_x, offset_y)
            for spike in spikes_group:
                spike.draw(canvas, offset_x, offset_y)

            for checkpoint in checkpoints_group:
                checkpoint.draw(canvas, offset_x, offset_y)

            for platform in all_platforms:
                platform.draw(canvas, offset_x, offset_y)

            for box in item_boxes_group:
                box.draw(canvas, offset_x, offset_y)

            for block in invisible_blocks:
                block.draw(canvas, offset_x, offset_y)

            for enemy in enemies_group:
                enemy.draw(canvas, offset_x, offset_y)

            for exit in exit_group:
                exit.draw(canvas, offset_x, offset_y)

            for water in water_group:
                water.collide_water(player)
                water.draw(canvas, offset_x, offset_y)

            for key in key_group:
                key.collect(player)
                key.draw(canvas, offset_x, offset_y)
            
            for snake in snakes_group:
                snake.draw(canvas,offset_x, offset_y)

            for lever in levers_group:
                lever.draw(canvas,offset_x, offset_y)

            for item in items_group:
                item.draw(canvas, offset_x, offset_y)
            
            for cloud in clouds_group:
                cloud.draw(canvas, offset_x, offset_y)

            player.draw(canvas, offset_x, offset_y)
            player.draw_keys(canvas)
            player.draw_health(canvas)
        elif player.alive == False:
            world, player, camera, all_platforms, invisible_blocks, level = game_over_menu(player,
                                                                                           level, img_list)

        screen.blit(canvas, (0, 0))
        pygame.display.flip()


def game_over_menu(player, level, img_list):
    world = None
    camera = None
    all_platforms = None
    invisible_blocks = None
    level = None
    clickable = True
    x = 0
    number_of_buttons = 2
    buttons = []
    for x, button in enumerate(range(number_of_buttons)):
        button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 +
                        x*button_clicked.get_height()*2, 'menu', button_clicked, x)
        buttons.append(button)

    for button in buttons:
        if button.draw(canvas):
            if clickable:
                if button.button_id == 0:
                    world_data = reset_level()
                    world, player, camera, all_platforms, invisible_blocks, level = load_level(
                        0, img_list)
                elif button.button_id == 1:
                    pygame.quit()
                    sys.exit()
                clickable = False

    return world, player, camera, all_platforms, invisible_blocks, level


def main_menu():
    x = 0
    number_of_buttons = 5
    buttons = []
    for x, button in enumerate(range(number_of_buttons)):
        button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//10 +
                        x*button_clicked.get_height()*2, 'menu', button_clicked, x)
        buttons.append(button)
    running = True
    clickable = True
    while running:
        clickable = True
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        for button in buttons:
            if button.draw(canvas):
                if clickable:
                    if button.button_id == 0:
                        game()
                    elif button.button_id == 1:
                        controls()
                    elif button.button_id == 2:
                        show_credits()
                    elif button.button_id == 3:
                        settings()
                    elif button.button_id == 4:
                        pygame.quit()
                        sys.exit()
                    clickable = False

        screen.blit(canvas, (0, 0))
        pygame.display.update()


def controls():
    running = True
    while running:
        canvas.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        screen.blit(canvas, (0, 0))
        pygame.display.update()


def show_credits():
    running = True
    while running:
        canvas.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        screen.blit(canvas, (0, 0))
        pygame.display.update()


def settings():
    running = True
    while running:
        canvas.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        screen.blit(canvas, (0, 0))
        pygame.display.update()


main_menu()
