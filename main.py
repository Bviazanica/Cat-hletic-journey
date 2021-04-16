import pygame
import math
import sys
import os
from pygame.locals import *
from enum import IntEnum
Vector2 = pygame.math.Vector2

pygame.init()

FPS = 60
Clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# define game variables
GRAVITY = 0.75

# define player action variables
moving_left = False
moving_right = False

# scale
scale = 1

# load all images & animations


def load_entity_animations():
    animation_types = ['Death', 'Fall', 'Idle', 'Jump', 'Roll', 'Use', 'Walk']
    entity_types = ['Player']

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

    def convert_map(self, world_data):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.entity_id = 0

        self.alive = True
        self.char_type = char_type
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

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, moving_left, moving_right, current_time, tick):
        self.local_time = current_time
        self.update_animation()
        # reset movement variables
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
            self.vel_y = -11
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y

        dy += int(self.vel_y)

        # check collision with floor
        if self.rect.bottom + dy > 350:
            dy = 350 - self.rect.bottom
            self.in_air = False

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


player = Player('player', 200, 200, 2)
running = True
current_time = 0

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
            if event.key == pygame.K_w and player.alive:
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
    player.update(moving_left, moving_right, current_time, tick_in_seconds)
    # print(f'{player.action, player.frame_index} & {player.local_time, player.update_time}')
    # Draw.
    player.draw()
    pygame.display.update()
