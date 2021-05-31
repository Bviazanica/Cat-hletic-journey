import pygame
import sys
import os
import csv
import random
from pygame import Vector2
from pygame import mouse
from pygame.locals import *
from data.button import Button
from data.camera.camera import *
from data.physics import *
from data.utility import *
from enum import IntEnum
from data.json_reader import *
from data.cut_scenes import *
from data.globals import *
from data.sound_handler import *

vec = pygame.math.Vector2

mixer.init()
pygame.init()
pygame.mixer.music.set_volume(0.5)
music_handler = SoundHandler()
Clock = pygame.time.Clock()
FPS = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
FULLSCREEN = False
# define game variables
GRAVITY = round(SCREEN_HEIGHT / 12)
GRAVITY_FORCE_LIMIT = round(SCREEN_HEIGHT / 50)
ROWS = 15
COLS = 50
TILE_SIZE = round(SCREEN_HEIGHT / ROWS)
TILE_TYPES = 264

BORDER_LEFT, BORDER_RIGHT = 0,0

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (240, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 191, 255)
YELLOW = (255, 255, 0)
DARKGRAY = (40, 40, 40)

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
    Disappear = 9,
    Extra = 10

monitor_size = [pygame.display.Info().current_w,pygame.display.Info().current_h]
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

#cursor
pygame.mouse.set_cursor(*pygame.cursors.tri_left)

sfx_dic = load_sounds()
music_list = load_music_names()
json_data = get_json_data()
level_cols = json_data['level_1']['COLS']
intro_scene = True
tutorial = True

blue_fish_image = pygame.image.load(
    f'platformer/data/images/entities/Fish/Idle/0.png').convert_alpha()

dead_fish = load_images('entities/Dead_fish')

cloud_image = pygame.image.load(
    f'platformer/data/images/entities/Cloud/cloud.png').convert_alpha()

button_clicked = pygame.image.load(
    f'platformer/data/images/interface/button_1.png').convert_alpha()
slider_line = pygame.image.load(
    f'platformer/data/images/interface/slider_line.png').convert_alpha()
green_slider_down = pygame.image.load(
    f'platformer/data/images/interface/green_slider_down.png').convert_alpha()
sound_on = pygame.image.load(
    f'platformer/data/images/interface/sound_on.png').convert_alpha()
sound_off = pygame.image.load(
f'platformer/data/images/interface/sound_off.png').convert_alpha()
toggle_on = pygame.image.load(
    f'platformer/data/images/interface/toggle_on.png').convert_alpha()
toggle_off = pygame.image.load(
    f'platformer/data/images/interface/toggle_off.png').convert_alpha()

toggle_on = pygame.transform.smoothscale(toggle_on, (TILE_SIZE*2, TILE_SIZE))
toggle_off = pygame.transform.smoothscale(toggle_off, (TILE_SIZE*2, TILE_SIZE))

fake_platform_green = pygame.image.load(
    f'platformer/data/images/tiles/68.png').convert_alpha()
fake_ground_green = pygame.image.load(
    f'platformer/data/images/tiles/66.png').convert_alpha()

health_image = pygame.image.load(
    f'platformer/data/images/other/health.png').convert_alpha()

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
bubble_image =  pygame.image.load(
    f'platformer/data/images/other/bubble.png').convert_alpha()
health_item_image = pygame.image.load(
    f'platformer/data/images/tiles/59.png').convert_alpha()

player_head_image =  pygame.image.load(
    f'platformer/data/images/other/player_head.png').convert_alpha()
friend_head_image =  pygame.image.load(
    f'platformer/data/images/other/friend_head.png').convert_alpha()
guard_head_image =  pygame.image.load(
    f'platformer/data/images/other/guard_head.png').convert_alpha()

skull_image = pygame.image.load(
    f'platformer/data/images/items/cage/skull.png').convert_alpha()
cage_back_image = pygame.image.load(
    f'platformer/data/images/items/cage/cage_back.png').convert_alpha()
cage_opened_image = pygame.image.load(
    f'platformer/data/images/items/cage/cage_opened.png').convert_alpha()
cage_closed_image = pygame.image.load(
    f'platformer/data/images/items/cage/cage_closed.png').convert_alpha()

effect_durations = {
    'Bubble':5000,
    'Boost':5000
}

background_images = [sky_background_image, rocks_background_image, mountain_background_image, \
                    clouds1_background_image, clouds2_background_image, clouds3_background_image, \
                        clouds4_background_image]


# create sprite groups
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
fish_group = pygame.sprite.Group()
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
cages_group = pygame.sprite.Group()

projectiles_group = pygame.sprite.Group()
friend_group = pygame.sprite.Group()
guardian_group = pygame.sprite.Group()

class Tutorial:
    def __init__(self, player, started_time):
        self.name = 'tutorial'
        self.step = 0
        self.current_time = 0
        self.cut_scene_running = True
        self.started_time = started_time

        self.player = player
        self.new_step = True
        self.game_finished = False
        self.dialogue_in_progress = False
        self.image = None

        self.text = {
            'one': "Jump - W or Space, Left - A, right - D",
            'two': "Collect fishes and save your friend!"
        }
        self.text_counter = 0
        self.time_in_scene = 0

    def update(self, time_passed, tick):
        self.current_time = time_passed
        pressed = pygame.key.get_pressed()
        enter = pressed[pygame.K_RETURN]
        self.player.set_action(int(Animation_type.Idle))
        if enter  and self.current_time - self.started_time > 1000:
            sfx_dic['skip'].play()
            self.cut_scene_running = False
            self.player.locked = False
        else:
            if self.step==0:
                if self.new_step:
                    self.player.locked = True
                    self.new_step = False

                if self.current_time - self.started_time > 1500:
                    if int(self.text_counter) < len(self.text['one']):
                        self.text_counter += 0.2
                        self.time_in_scene = self.current_time
                    elif self.current_time - self.time_in_scene > 5000:
                        self.step = 1
                        self.new_step = True
                        self.text_counter = 0
                
            
            if self.step == 1:
                if self.new_step:
                    self.player.locked = True
                    self.new_step = False

                if int(self.text_counter) < len(self.text['two']):
                    self.text_counter += 0.2
                    self.time_in_scene = self.current_time
                elif self.current_time - self.time_in_scene > 3000:
                    self.step = 2
                    self.new_step = True
                    self.player.locked =False
                    self.text_counter = 0

            if self.step == 2:
                    self.cut_scene_running = False  

        return self.cut_scene_running

    def draw(self, canvas):
            if self.step == 0:
                draw_text(
                    self.text['one'][0:int(self.text_counter)],
                    40,
                    WHITE,
                    canvas,
                    SCREEN_WIDTH/2,
                    SCREEN_HEIGHT - SCREEN_HEIGHT*0.08,
                    'midtop',
                    TILE_SIZE
                )
            if self.step == 1:
                draw_text(
                    self.text['two'][0:int(self.text_counter)],
                    40,
                    WHITE,
                    canvas,
                    SCREEN_WIDTH/2,
                    SCREEN_HEIGHT - SCREEN_HEIGHT*0.08,
                    'midtop',
                    TILE_SIZE
                )

class CutSceneOne:
    def __init__(self, player, wingman,friend, started_time):
        self.name = 'intro scene'
        self.step = 0
        self.current_time = 0
        self.cut_scene_running = True
        self.started_time = started_time

        self.player = player
        self.friend = friend
        self.wingman = wingman

        self.new_step = True
        self.game_finished = False
        self.dialogue_in_progress = False
        self.image = player_head_image

        self.text = {
            'one': "I must save him!...",
        }
        self.last_sound_played = 0
        self.last_text_counter = 0
        self.text_counter = 0
        self.time_in_scene = 0

    def update(self, time_passed, tick):
        self.current_time = time_passed
        
        pressed = pygame.key.get_pressed()
        enter = pressed[pygame.K_RETURN]
        self.last_text_counter = self.text_counter
        if enter:
            sfx_dic['skip'].play()
            self.cut_scene_running = False
            exit = random.choice(exit_group.sprites())
            self.player.rect.x = exit.rect.x
            self.player.locked = False
        else:
            if self.step==0:
                if self.new_step:
                    self.player.set_action(int(Animation_type.Walk))
                    self.friend.set_action(int(Animation_type.Walk))
                    self.player.locked = True
                    self.friend.locked = False
                    self.new_step = False
                    self.wingman.health_points = 1

                wingman_hitbox =  pygame.Rect(
                    (self.wingman.rect.centerx - self.wingman.rect.width/3, self.wingman.rect.y, self.wingman.rect.width/3, self.wingman.rect.height))

                if wingman_hitbox.colliderect(self.friend.rect) == False:
                    self.player.rect.x += (self.player.speed/3) * tick
                    self.friend.rect.x += (self.friend.speed/3) * tick
                    self.wingman.rect.x += (self.wingman.speed*1.2) * tick
                else:
                    self.step = 1
                    self.new_step = True
                    
            if self.step == 1:
                if self.new_step:
                    self.player.set_action(int(Animation_type.Idle))
                    self.friend.set_action(int(Animation_type.Death))
                    self.new_step = False
                self.friend.frame_index= 0
                self.wingman.rect.x += (self.wingman.speed*1.2) * tick
                self.wingman.rect.y -= (self.wingman.speed/2) * tick
                self.friend.rect.topleft = self.wingman.rect.center

                if self.wingman.health_points == 0:
                    self.step = 2
                    self.new_step = True
                    self.text_counter = 0
                
            if self.step == 2:
                if self.new_step:
                    self.new_step = False
                    
                if int(self.text_counter) < len(self.text['one']):
                    self.dialogue_in_progress = True
                    self.text_counter += 0.2
                    self.time_in_scene = self.current_time
                elif self.current_time - self.time_in_scene > 3000:
                    self.dialogue_in_progress = False
                    self.step = 3
                    self.new_step=True
                    
            if self.step == 3:
                if self.new_step:
                    self.new_step = False
                    self.player.set_action(int(Animation_type.Run))
                self.player.rect.x += self.player.speed * tick
            if self.step == 4:
                    self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, canvas):
        if self.dialogue_in_progress:
            if round(self.text_counter) % 2 == 0 and round(self.text_counter) != round(self.last_text_counter):
                    if self.last_sound_played != 1:
                        sfx_dic['talk_1'].play()
                        self.last_sound_played = 1
                    else:
                        sfx_dic['talk_2'].play()
                        self.last_sound_played = 2
            if self.step == 2:
                draw_text(
                    self.text['one'][0:int(self.text_counter)],
                    40,
                    WHITE,
                    canvas,
                    SCREEN_WIDTH/4,
                    SCREEN_HEIGHT - SCREEN_HEIGHT*0.08,
                    'topleft',
                    TILE_SIZE
                )

class CutSceneTwo:
    def __init__(self, player, guard, started_time):
        self.name = 'scene 2'
        self.step = 0
        self.current_time = 0
        self.cut_scene_running = True
        self.started_time = started_time

        self.player = player
        self.guard = guard

        self.new_step = True
        self.game_finished = False
        self.image = player_head_image
        self.dialogue_in_progress = False

        self.text = {
            'one': "I will take 20 of your fishes...",
            'two-option-1': "You can go on...",
            'two-option-2': "You didn't bring enough..."
        }
        self.last_sound_played = 0
        self.last_text_counter = 0
        self.text_counter = 0
        self.time_in_scene = 0

    def update(self, time_passed, tick):
        self.current_time = time_passed
        pressed = pygame.key.get_pressed()
        enter = pressed[pygame.K_RETURN]
        if enter:
            sfx_dic['skip'].play()
            self.cut_scene_running = False
            if self.player.fish >= 40:
                exit = random.choice(exit_group.sprites())
                self.player.rect.x = exit.rect.x
                self.player.locked = False
            else:
                self.player.alive = False
                self.player.health_points = 0

        self.last_text_counter = self.text_counter
        if self.step == 0:
            if self.new_step:
                self.player.set_action(int(Animation_type.Idle))
                self.player.speed = 0
                self.player.locked = True
                self.new_step = False
            if self.current_time - self.started_time > 2000:
                self.new_step = True
                self.step = 1
                self.text_counter = 0

        if self.step == 1:
            if self.new_step:
                self.new_step = False
                self.image = guard_head_image
            if int(self.text_counter) < len(self.text['one']):
                self.dialogue_in_progress = True
                self.text_counter += 0.2
                self.time_in_scene = self.current_time
            elif self.current_time - self.time_in_scene > 2000:
                self.step = 2
                self.dialogue_in_progress = False
                self.new_step = True
                self.text_counter = 0
    
        if self.step == 2:
            if self.new_step:
                self.new_step = False
                self.image = guard_head_image

            if self.player.fish >= 40:
                if int(self.text_counter) < len(self.text['two-option-1']):
                    self.text_counter += 0.2
                    self.dialogue_in_progress = True
                    self.time_in_scene = self.current_time
                elif self.current_time - self.time_in_scene > 2000:
                    self.step = 3
                    self.dialogue_in_progress = False
                    self.new_step = True
                    self.text_counter = 0
                    
            elif self.player.fish < 40:
                if int(self.text_counter) < len(self.text['two-option-2']):
                    self.dialogue_in_progress = True
                    self.text_counter += 0.2
                    self.time_in_scene = self.current_time
                elif self.current_time - self.time_in_scene > 2000:
                    self.step = 3
                    self.dialogue_in_progress = False
                    self.new_step = True
                    self.text_counter = 0
            
        if self.step == 3:
            if self.new_step:
                self.new_step = False

            if self.player.fish >= 40:
                self.guard.set_action(int(Animation_type.Extra))
                self.guard.frame_index = 1
                self.player.speed = 3*TILE_SIZE
                self.player.rect.x += self.player.speed * tick
                self.player.set_action(int(Animation_type.Walk))

            elif self.player.fish < 40:
                self.guard.set_action(int(Animation_type.Extra))
                self.guard.frame_index = 0
                self.player.speed = 3*TILE_SIZE
                self.player.rect.x += -self.player.speed * tick
                self.player.set_action(int(Animation_type.Walk))
                self.player.flip = True
                self.dialogue_in_progress = False

            if self.player.in_death_animation:
                self.new_step = False
                self.player.health_points = 0
                self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, canvas):
        if self.dialogue_in_progress:
            if round(self.text_counter) % 2 == 0 and round(self.text_counter) != round(self.last_text_counter):
                    if self.last_sound_played != 1:
                        sfx_dic['talk_1'].play()
                        self.last_sound_played = 1
                    else:
                        sfx_dic['talk_2'].play()
                        self.last_sound_played = 2
            if self.step == 1:
                draw_text(
                    self.text['one'][0:int(self.text_counter)],
                    40,
                    WHITE,
                    canvas,
                    SCREEN_WIDTH/4,
                    SCREEN_HEIGHT - SCREEN_HEIGHT*0.08,
                    'topleft',
                    TILE_SIZE
                )
            elif self.step == 2 and self.player.fish >= 40:
                draw_text(
                    self.text['two-option-1'][0:int(self.text_counter)],
                    40,
                    WHITE,
                    canvas,
                    SCREEN_WIDTH/4,
                    SCREEN_HEIGHT - SCREEN_HEIGHT*0.08,
                    'topleft',
                    TILE_SIZE
                )
            elif self.step == 2 and self.player.fish < 40:
                draw_text(
                    self.text['two-option-2'][0:int(self.text_counter)],
                    40,
                    WHITE,
                    canvas,
                    SCREEN_WIDTH/4,
                    SCREEN_HEIGHT - SCREEN_HEIGHT*0.08,
                    'topleft',
                    TILE_SIZE
                )

class FinalCutScene:
    def __init__(self, player,friend, started_time):
        self.name = 'final scene'
        self.step = 0
        self.current_time = 0
        self.cut_scene_running = True
        self.started_time = started_time

        self.player = player
        self.friend = friend

        self.new_step = True

        self.dialogue_in_progress = False
        self.image = player_head_image
        self.dim_screen = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT)).convert_alpha()
        self.opacity = 0
        self.start_to_dim = False
        self.game_finished = False

        self.text = {
            'one': "Thank you for saving me!",
            'two': "Let's get some fish and milk now.",
            'three': "Good idea.",
            'four': "Thanks for playing!",
            'five': "Game by:",
            'six': "Branislav Viazanica"
        }
        self.last_sound_played = 0
        self.last_text_counter = 0
        self.text_counter = 0
        self.time_in_scene = 0

    def update(self, time_passed, tick):
        self.current_time = time_passed
        pressed = pygame.key.get_pressed()
        enter = pressed[pygame.K_RETURN]
        if enter:
            sfx_dic['skip'].play()
            self.new_step = True
            self.step = 5

        self.last_text_counter = self.text_counter
        if self.step == 0:
            if self.new_step:
                self.new_step = False
                self.player.locked = True
                self.player.moving_left = self.player.moving_right = False
                self.player.set_action(int(Animation_type.Idle))
                
            if self.current_time - self.started_time > 2000:
                self.new_step = True
                self.step = 1
                self.text_counter = 0

        if self.step == 1:
            if self.new_step:
                self.new_step = False
                self.friend.locked = False
                self.friend.vel_y = 0
                if self.friend.in_air:
                    self.friend.set_action(int(Animation_type.Jump))
                self.time_in_scene = self.current_time
            
            if not self.friend.in_air:
                self.friend.set_action(int(Animation_type.Idle))

            if self.current_time - self.time_in_scene > 2000:
                self.step = 2
                self.new_step = True

        if self.step == 2:
            if self.new_step:
                self.new_step = False
                self.image = friend_head_image
                self.friend.flip = False
                self.player.direction = -1
            
            if int(self.text_counter) < len(self.text['one']):
                    self.dialogue_in_progress = True
                    self.text_counter += 0.2
                    self.time_in_scene = self.current_time
                
            elif self.player.rect.colliderect(self.friend.rect.x + (self.friend.speed/3 * tick) \
                 + self.friend.rect.width, self.friend.rect.y, self.friend.rect.width, self.friend.rect.height):
                self.step = 3
                self.dialogue_in_progress = False
                self.new_step = True
                self.text_counter = 0
                self.friend.set_action(int(Animation_type.Idle))
            else:
                self.friend.set_action(int(Animation_type.Walk))
                self.friend.rect.x += self.friend.speed/3 *tick
            
        
        if self.step == 3:
            if self.new_step:
                self.new_step = False
                self.image = player_head_image

            if int(self.text_counter) < len(self.text['two']):
                    self.dialogue_in_progress = True
                    self.text_counter += 0.2
                    self.time_in_scene = self.current_time
            elif self.current_time - self.time_in_scene > 2000:
                self.step = 4
                self.dialogue_in_progress = False
                self.new_step = True
                self.text_counter = 0
            
        if self.step == 4:
            if self.new_step:
                self.new_step = False
                self.image = friend_head_image

            if int(self.text_counter) < len(self.text['three']):
                    self.dialogue_in_progress = True
                    self.text_counter += 0.2
                    self.time_in_scene = self.current_time
            elif self.current_time - self.time_in_scene > 2000:
                self.step = 5
                self.dialogue_in_progress = False
                self.new_step = True
                self.text_counter = 0
        
        if self.step == 5:
            if self.new_step:
                self.new_step = False
                self.friend.set_action(int(Animation_type.Walk))
                self.player.set_action(int(Animation_type.Walk))
                self.player.direction = -1
                self.friend.flip = True
                self.game_finished = True
                self.time_in_scene = self.current_time
            
            if self.current_time - self.time_in_scene > 3000:
                self.step = 6

            self.friend.rect.x += -self.friend.speed/3 *tick
            self.player.rect.x += -self.player.speed/3 *tick

        if self.step == 6:
            if self.new_step:
                self.new_step = False
            
            if int(self.text_counter) < len(self.text['four']):
                    self.text_counter += 0.15
                    self.time_in_scene = self.current_time
            elif self.current_time - self.time_in_scene > 1000:
                self.start_to_dim = True
                self.opacity += 2
                if self.opacity > 255:
                    self.opacity = 255
                    self.step = 7
                    self.new_step = True
                    self.text_counter = 0
                    self.start_to_dim = False
                self.dim_screen.fill((0, 0, 0, self.opacity))

        if self.step == 7:
            if self.new_step:
                self.new_step = False
                self.opacity = 0
                self.start_to_dim = False

            if int(self.text_counter) < len(self.text['six']):
                    self.text_counter += 0.15
                    self.time_in_scene = self.current_time
            elif self.current_time - self.time_in_scene > 1000:
                self.start_to_dim = True
                self.opacity += 2
                if self.opacity > 255:
                    self.opacity = 255
                    self.new_step = True
                    self.text_counter = 0
                    self.start_to_dim = False
                    self.cut_scene_running = False
                    self.player.alive = False
                self.dim_screen.fill((0, 0, 0, self.opacity))
                
        return self.cut_scene_running

    def draw(self, canvas):
        if self.dialogue_in_progress:
            if round(self.text_counter) % 2 == 0 and round(self.text_counter) != round(self.last_text_counter) \
                and self.step < 6:
                    if self.last_sound_played != 1:
                        sfx_dic['talk_1'].play()
                        self.last_sound_played = 1
                    else:
                        sfx_dic['talk_2'].play()
                        self.last_sound_played = 2
            if self.step == 2:
                draw_text(
                    self.text['one'][0:int(self.text_counter)],
                    40,
                    WHITE,
                    canvas,
                    SCREEN_WIDTH/4,
                    SCREEN_HEIGHT - SCREEN_HEIGHT*0.08,
                    'topleft',
                    TILE_SIZE
                )
            if self.step == 3:
                draw_text(
                    self.text['two'][0:int(self.text_counter)],
                    40,
                    WHITE,
                    canvas,
                    SCREEN_WIDTH/4,
                    SCREEN_HEIGHT - SCREEN_HEIGHT*0.08,
                    'topleft',
                    TILE_SIZE
                )
            if self.step == 4:
                draw_text(
                    self.text['three'][0:int(self.text_counter)],
                    40,
                    WHITE,
                    canvas,
                    SCREEN_WIDTH/4,
                    SCREEN_HEIGHT - SCREEN_HEIGHT*0.08,
                    'topleft', 
                    TILE_SIZE
                )
        elif self.game_finished:
            if self.step == 6:
                draw_text(
                        self.text['four'][0:int(self.text_counter)],
                        70,
                        WHITE,
                        canvas,
                        SCREEN_WIDTH/2,
                        SCREEN_HEIGHT/2,
                        'midtop', 
                        TILE_SIZE
                )
                
            elif self.step == 7:
                draw_text(
                        self.text['five'][0:int(self.text_counter)],
                        70,
                        WHITE,
                        canvas,
                        SCREEN_WIDTH/2,
                        SCREEN_HEIGHT/2 - SCREEN_HEIGHT*0.05,
                        'midtop', 
                        TILE_SIZE
                )
                draw_text(
                        self.text['six'][0:int(self.text_counter)],
                        70,
                        WHITE,
                        canvas,
                        SCREEN_WIDTH/2,
                        SCREEN_HEIGHT/2 + SCREEN_HEIGHT*0.05,
                        'midtop', 
                        TILE_SIZE
                        
                )
            if self.start_to_dim:
                    canvas.blit(self.dim_screen, (0, 0))
# manager for cutscenes
class CutSceneManager:
    def __init__(self, canvas):
        self.cut_scenes_complete = []
        self.cut_scene = None
        self.cut_scene_running = False

        self.canvas = canvas
        self.window_size = 0

        self.canvas_height = self.canvas.get_height()

    def start_cut_scene(self, cut_scene):
        if cut_scene.name not in self.cut_scenes_complete:
            self.cut_scenes_complete.append(cut_scene.name)
            self.cut_scene = cut_scene
            self.cut_scene_running = True

    def end_cut_scene(self):
        self.cut_scene = None
        self.cut_scene_running = False

    def update(self, time_passed, time_passed_seconds):
        if self.cut_scene_running:
            if self.cut_scene.game_finished and self.window_size < self.canvas_height*0.5:
                self.window_size += 2
            elif self.window_size < self.canvas_height*0.2:
                self.window_size += 2
            self.cut_scene_running = self.cut_scene.update(
                time_passed, time_passed_seconds)
        else:
            self.end_cut_scene()

    def draw(self):
        if self.cut_scene_running:
            # Draw rects generic to all cut scenes
            pygame.draw.rect(self.canvas, BLACK,
                             (0, 0, self.canvas.get_width(), self.window_size))
            pygame.draw.rect(self.canvas, BLACK,
                             (0, SCREEN_HEIGHT-self.window_size, self.canvas.get_width(), self.window_size))
            
            if self.window_size >= self.canvas_height*0.2 and self.cut_scene.dialogue_in_progress:
                canvas.blit(self.cut_scene.image, (SCREEN_WIDTH/10, self.canvas_height - self.canvas_height*0.01 - self.cut_scene.image.get_height()))
            # Draw specific cut scene details
            self.cut_scene.draw(self.canvas)


def draw_background(canvas, offset_x, offset_y, background_images):
    for x in range(3):
        parallax_variable = 0.1
        for image in background_images:
            canvas.blit(image, ((x * SCREEN_WIDTH - round(offset_x * parallax_variable)), 0 - offset_y*parallax_variable))
            parallax_variable += 0.05

# load all images & animations
def load_entity_animations():
    animation_types = ['Death', 'Fall', 'Idle', 'Jump', 'Run', 'Slide', 'Walk', 'Attack', 'Appear', 'Disappear', 'Extra']
    entity_types = ['Player', 'Green_enemy', 'Spikeman', 'Wingman','Snake', 'Fish', 'Friend', 'Guardian', 'Flyingman', 'Projectile']

    list_of_loaded_animations = []
    for entity_type in entity_types:
        entity_animations = []
        # load all entity images
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
                    # scaling images to correct size
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
                    elif  entity_type == 'Fish':
                        img = pygame.transform.smoothscale(
                            img, (TILE_SIZE, int(TILE_SIZE*(img.get_height()/img.get_width()))))
                    elif entity_type == 'Wingman':
                        img = pygame.transform.smoothscale(
                            img, (TILE_SIZE*4 , TILE_SIZE*2))
                    elif entity_type == 'Player' or entity_type == 'Friend':
                        img = pygame.transform.smoothscale(
                            img, (TILE_SIZE*2 , TILE_SIZE*2))
                    elif entity_type == 'Projectile':
                        if i == 0:
                            img = pygame.transform.smoothscale(
                                img, (round(TILE_SIZE*(img.get_width()/img.get_height()*0.75)), round(TILE_SIZE*0.75)))
                        else:
                            img = pygame.transform.smoothscale(
                                img, (round(TILE_SIZE*0.75), round(TILE_SIZE*(img.get_height()/img.get_width())*0.75)))
                    elif entity_type == 'Guardian':
                        img = pygame.transform.smoothscale(
                            img, (TILE_SIZE*4 , TILE_SIZE*4))
                    elif entity_type == 'Flyingman':
                        img = pygame.transform.scale(
                            img, (TILE_SIZE ,TILE_SIZE))
                    elif entity_type == 'Green_enemy':
                        img = pygame.transform.smoothscale(
                            img, (TILE_SIZE, TILE_SIZE))
                    else:
                        img = pygame.transform.scale(
                            img, (TILE_SIZE, TILE_SIZE))
                    temp_list.append(img)
                entity_animations.append(temp_list)
            else:
                entity_animations.append([])
        list_of_loaded_animations.append(entity_animations)
    return list_of_loaded_animations

#list of with all animations
animations_list = load_entity_animations()

# create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * level_cols
    world_data.append(r)


# reset level data
def reset_level():
    decoration_group.empty()
    water_group.empty()
    fish_group.empty()
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
    cages_group.empty()
    projectiles_group.empty()
    friend_group.empty()
    guardian_group.empty()
    
    # create empty tile list
    data = []
    for row in range(ROWS):
        r = [-1] * level_cols
        data.append(r)
    return data

#loading level from csv file
def load_level(level, img_list):
    global BORDER_LEFT
    global BORDER_RIGHT
    global level_cols
    level += 1
    level_cols = json_data[f'level_{level}']['COLS']
    world_data = reset_level()
    # load in level data and create world
    with open(f'platformer/data/maps/level{level}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    #set variables depending on level
    cut_scene_manager = CutSceneManager(canvas)
    world = World()
    player, camera, all_platforms, invisible_blocks = world.process_data(
        world_data, img_list, level)
    BORDER_LEFT = 0
    BORDER_RIGHT = world.level_length * TILE_SIZE

    return world, player, camera, all_platforms, invisible_blocks, level, cut_scene_manager, BORDER_LEFT, BORDER_RIGHT

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
        cage_id = 0
        for y, row in enumerate(data):
            platform = []
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)

                    #set objects to array based on id of tile
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
                    elif tile == 12:
                        new_decoration = Decoration(random.choice(dead_fish), x * TILE_SIZE, y*TILE_SIZE)
                        decoration_group.add(new_decoration)
                    elif tile == 20:
                        new_cage = Cage(x*TILE_SIZE, y*TILE_SIZE, cage_id)
                        cage_id += 1
                        cages_group.add(new_cage)
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
                            platform[0].rect.x, platform[0].rect.y, platform, new_surface, platform_id, 3*TILE_SIZE, level))
                        platform_id += 1
                        platform = []
                    elif tile == 74:
                        self.platforms.append(Platform(
                            x*TILE_SIZE, y*TILE_SIZE, 1, img, platform_id,3*TILE_SIZE, level))
                        platform_id += 1
                    elif tile == 110:
                        if x == 7:
                            new_fake_platform = FakePlatform(
                                x * TILE_SIZE, y*TILE_SIZE, 3, 3, 'fall', fake_platform_id, 4*TILE_SIZE)
                            fake_platform_id += 1
                            fake_platforms_group.add(new_fake_platform)
                            self.platforms.append(new_fake_platform)
                    elif tile == 101:
                        img = random.choice(animations_list[5][2])
                        new_fish = Collectible(
                            'Fish', img, x * TILE_SIZE, y * TILE_SIZE)
                        fish_group.add(new_fish)    
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
                            new_fish = Collectible(
                            'Fish', blue_fish_image, x * TILE_SIZE, y * TILE_SIZE )
                            fish_group.add(new_fish)
                    elif tile == 237:
                        new_flyingman = Entity(8, x*TILE_SIZE, y*TILE_SIZE, 3*TILE_SIZE)
                        enemies_group.add(new_flyingman)
                    elif tile == 238:  # create player
                        player = Entity(0, x * TILE_SIZE,
                                        y * TILE_SIZE + TILE_SIZE, 6*TILE_SIZE)
                        camera = Camera(player,SCREEN_WIDTH, SCREEN_HEIGHT)
                        camera_type = Border(
                                camera, player, self.get_world_length())
                                                            
                        camera.setmethod(camera_type)
                    elif tile == 239:  # create enemy
                        new_enemy = Entity(1, x * TILE_SIZE,
                                           y * TILE_SIZE, 3*TILE_SIZE)
                        enemies_group.add(new_enemy)
                    elif tile == 240:  # create Cloud
                        new_cloud = Cloud(cloud_image, x * TILE_SIZE,
                                           y * TILE_SIZE)
                        clouds_group.add(new_cloud)
                    elif tile == 258:  # create Snake
                        new_snake = Snake(4, x * TILE_SIZE,
                                           y * TILE_SIZE)
                        snakes_group.add(new_snake)
                    elif tile == 259: # create Wingman
                        new_wingman = Entity(3,x * TILE_SIZE, y * TILE_SIZE, 4*TILE_SIZE)
                        wingmans_group.add(new_wingman)
                    elif tile == 260: # create Spikeman
                        new_spikeman = Entity(2,  x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE, 3*TILE_SIZE)
                        enemies_group.add(new_spikeman)
                    elif tile == 261:  # create Friend
                        new_friend = Entity(6,  x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE, 6*TILE_SIZE)
                        friend_group.add(new_friend)
                    elif tile == 262: # create Guardian
                        new_guardian = Entity(7,  x * TILE_SIZE, y * TILE_SIZE + TILE_SIZE, 3*TILE_SIZE)
                        guardian_group.add(new_guardian)
                    elif tile == 263: # create Checkpoint
                        new_checkpoint = Checkpoint(
                            img, x * TILE_SIZE, y * TILE_SIZE, x)
                        checkpoints_group.add(new_checkpoint)

        return player, camera, self.platforms, self.invisible_blocks_list

    #draw all tiles
    def draw(self, canvas, offset_x, offset_y):
        for tile in self.obstacles_list:
            canvas.blit(tile[0], (round(tile[1].x - offset_x),
                                  round(tile[1].y - offset_y), tile[1].width, tile[1].height))
            # pygame.draw.rect(canvas, RED,
            #                  (round(tile[1].x - offset_x), round(tile[1].y - offset_y), tile[1].width, tile[1].height), 2)
            # pygame.draw.rect(canvas, YELLOW,
            #                  (tile[1].x, tile[1].y, tile[1].width, tile[1].height), 2)

    def get_world_length(self):
        return self.level_length * TILE_SIZE

#main class for entities
class Entity(pygame.sprite.Sprite):
    def __init__(self, entity_id, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.entity_id = entity_id
        self.alive = True

        self.x = x
        self.y = y

        self.speed = speed
        self.direction = 1

        self.moving_left = False
        self.moving_right = False

        self.vel_y = 0
        self.jump = False
        self.jump_force = round(SCREEN_HEIGHT/35)
        self.jump_vel = SCREEN_HEIGHT*3
        self.in_air = True
        self.flip = False

        self.locked = False

        self.animation_list = animations_list[self.entity_id]
        self.frame_index = 0

        self.update_time = 0
        self.local_time = 0
        self.air_timer = 0

        self.fish = 0
        self.checkpoint_position = vec(0, 0)

        self.invulnerability = False
        self.reset_invulnerability = False
        self.boosted = False

        self.invulnerability_start_time = 0
        self.reset_invulnerability_time = 0
        self.boost_start_time = 0
        
        self.determine_entity_default_setup(self.entity_id)
        
        self.rect.bottom = y
        self.rect.x = x
        self.collision_treshold = 25

        if self.entity_id == 0:
            self.health_points = 5
        elif self.entity_id == 3:
            self.health_points = 6
            self.hitbox = pygame.Rect(self.rect.x + self.rect.width/4, self.rect.y, self.rect.width/2, self.rect.height)
        elif self.entity_id != 0:
            self.health_points = 1
            self.direction = random.choice([-1,1])

        self.new_state = False
        
        self.in_death_animation = False

        self.desired = Vector2(0,0)
        self.acceleration =  Vector2(0,0)
        # how fast the acceleration vector follows desired vec
        self.max_force = 0.2
        self.approach_radius = 2*TILE_SIZE

        self.on_platform = False
        self.was_on_platform = False

    def update(self, current_time, tick, world, all_platforms, level):
        self.local_time = current_time

        #control the effects of items
        if self.entity_id == 0:
            if self.invulnerability and self.local_time - self.invulnerability_start_time > effect_durations['Bubble']:
                self.invulnerability = False
            if self.boosted and self.local_time - self.boost_start_time > effect_durations['Boost']:
                self.speed = 6*TILE_SIZE
                self.boosted = False

        #if outside of bounds, gets hurt
        if self.rect.x > world.get_world_length() or self.rect.x + self.rect.width < 0 or \
                        self.rect.y + self.rect.height < 0 or self.rect.y > SCREEN_HEIGHT:
            self.hurt(True, 'out of bounds')

        # invulnerability when respawning
        if self.in_death_animation == False:
            if self.entity_id == 0:
                if self.reset_invulnerability:
                    if self.local_time - self.reset_invulnerability_time > 2000:
                        self.reset_invulnerability = False

                self.move(self.moving_left, self.moving_right, world, all_platforms,tick,level)
                self.flip = True if self.direction < 0 else False

            #entity behavior based on id and level
            elif self.entity_id == 1 or self.entity_id == 2:
                self.set_action(int(Animation_type.Walk))
                self.determine_movement()
                self.move(self.moving_left, self.moving_right, world, all_platforms,tick, level)
            elif self.entity_id == 3:
                if level == 4:
                    if self.rect.y + self.rect.height + 2*TILE_SIZE > SCREEN_HEIGHT:
                        self.rect.y = SCREEN_HEIGHT - self.rect.height - 2*TILE_SIZE
                        self.direction *= -1
                    elif self.rect.y < 0:
                        self.rect.y = 0
                        self.direction *= -1
                elif level == 5:
                    if not self.diving:
                        self.rect.x += self.speed * self.direction * tick # wingman
                        if self.rect.x < BORDER_LEFT:
                            self.rect.x = BORDER_LEFT
                            self.direction *= -1
                        elif self.rect.x + self.rect.width > BORDER_RIGHT:
                            self.rect.x = BORDER_RIGHT - self.rect.width
                            self.direction *= -1
                    # self.rect.y += self.speed * self.direction * tick
                    self.hitbox = pygame.Rect(self.rect.x + self.rect.width/4, self.rect.y, self.rect.width/2, self.rect.height)
            elif self.entity_id == 6: #friend code
                self.move(self.moving_left, self.moving_right, world, all_platforms,tick, level)

            if self.air_timer > 0 and self.was_on_platform:
                self.vel_y = 1
        else:
            if not self.entity_id in (2, 8):
                self.set_action(int(Animation_type.Death))

        
        self.update_animation()

    def move(self, moving_left, moving_right, world, all_platforms,tick, level):
        dx = 0
        dy = 0

        self.was_on_platform = self.on_platform

        if moving_left and moving_right:
            dx = self.speed * tick * self.direction
        elif moving_left:
            dx = -self.speed * tick
        elif moving_right:
            dx = self.speed * tick
        
        # apply gravity
        self.vel_y = apply_gravitation(self.vel_y, GRAVITY, tick, GRAVITY_FORCE_LIMIT)

        dy += self.vel_y
        self.in_air = True

        dx= round(dx)
        dy = round(dy)

        #bounds for x axis
        if self.rect.left + dx < BORDER_LEFT or self.rect.right + dx > BORDER_RIGHT:
                if self.entity_id != 0:
                    self.direction *= -1
                dx = 0
                
        #enemy entities bounce of tiles
        if self.entity_id != 0:
            for tile in world.bounds_tiles_list:
                # check collision in the x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                    self.direction *= -1
                    dx = 0
                    
        #player damaging the boss
        if self.entity_id == 0 and level == 5:
            for wingman in wingmans_group:
                if wingman.alive:
                    if abs((self.rect.bottom) - wingman.hitbox.top) <= self.collision_treshold and (self.rect.x + self.rect.width >= wingman.hitbox.x) and (self.rect.x <= wingman.hitbox.x + wingman.hitbox.width):
                        if wingman.stunned == True and self.vel_y > 0 and not self.reset_invulnerability:
                            wingman.hurt(False, 'player')
                            sfx_dic['bounce'].play()
                            jump_vel = tick * -self.jump_vel
                            if jump_vel < -self.jump_force:
                                jump_vel = -self.jump_force
                            self.vel_y = jump_vel
                            self.jump = True
                            self.on_platform = False
                            wingman.stunned = False

            # when near the fake platform, activate it
            for fake_platform in fake_platforms_group:
                if fake_platform.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height):
                    fake_platform.activated = True

            #spike collision
            for spike in spikes_group:
                if spike.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height) \
                     and not self.invulnerability and not self.reset_invulnerability:
                    self.hurt(False, 'spike')
            
            #cloud collision
            for cloud in clouds_group:
                if cloud.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height) \
                    and not self.invulnerability and not self.reset_invulnerability:
                    self.hurt(False, 'cloud')
        
        # top border 
        if self.rect.y + dy < 0:
            dy = 0
            self.vel_y = 0

        # speed on moving platform
        for platform in all_platforms:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if platform.move_x != 0:
                    if dx == 0:
                        dx += platform.direction * platform.speed * tick
                    elif dx < 0 and platform.direction == 1:
                        dx += -(platform.direction * platform.speed * tick)
                    elif dx > 0 and platform.direction == -1:
                        dx += -(platform.direction * platform.speed * tick)
                    
                    
        dx = round(dx)
        dy = round(dy)
        
        #apply collisions to movement
        self.rect, colls = move_with_collisions(
            self,[dx, dy], world.obstacles_list, all_platforms, enemies_group, world.invisible_blocks_list, item_boxes_group,sfx_dic, tick)
        
        #events after collision are set
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

    # determine whether to flip picutre
    def determine_movement(self):
        if self.direction == 1:
            self.moving_right = True
            self.flip = False
        else:
            self.moving_right = False
            self.flip = True
        self.moving_left = not self.moving_right
    
    #default setup for different entities
    def determine_entity_default_setup(self,entity_id):
        # rect properties
        if entity_id == 0 or self.entity_id == 6:
            self.action = int(Animation_type.Idle)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect(width=TILE_SIZE, height=TILE_SIZE*2 - TILE_SIZE//3)
            if self.entity_id==6:
                self.locked = True
        elif entity_id == 3:
            self.action = int(Animation_type.Walk)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.states = {'shoot': 'shoot', 'dive': 'dive', 'hide':'hide', 'drop':'drop'}
            self.cooldowns = {'shoot': 3000, 'drop': 10000, 'global': 1000}
            self.shoot_timer = self.drop_timer = self.global_timer = -100000
            self.stunned = False
            self.stun_timer = 0

            self.diving = False
            self.dropped = 0
            self.shot = 0
        elif entity_id == 7:
            self.action = int(Animation_type.Idle)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
            self.flip = True
        else:
            self.action = int(Animation_type.Walk)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect()
    
    #flyingman behavior
    def ai(self, player, tick):
        self.acceleration += self.seek_with_approach(player.rect.center, tick)
        self.avoid_sprites(enemies_group)
        self.rect.center += self.acceleration

    #wingman shooting
    def shoot(self, pattern, speed, desired):
        self.shoot_timer = self.local_time
        self.shot += 1
        if pattern == 'basic':
            sfx_dic['shoot'].play()
            new_projectile = Projectile(self.rect.centerx, self.rect.bottom, speed, desired, 1)
            projectiles_group.add(new_projectile)
        elif pattern == 'spray':
            spread = 20
            sfx_dic['shoot_1'].play()
            for i in range(3):
                new_desired_vector = desired.rotate(spread)
                new_desired_vector.normalize_ip()
                new_projectile = Projectile(self.rect.centerx, self.rect.bottom, speed, new_desired_vector, 1)
                projectiles_group.add(new_projectile)
                spread -= 20

    #wingman dropping entites
    def drop(self, stage, position):
        self.dropped += 1
        self.drop_timer = self.local_time
        sfx_dic['drop'].play()
        if stage == 1:
            new_entity = Entity(1, position[0], position[1], 4*TILE_SIZE)
            enemies_group.add(new_entity)
            
        elif stage == 3:
            choice = random.randrange(0, 10)
            if choice < 3:
                new_entity = Snake(4, position[0], position[1])
                snakes_group.add(new_entity)
            elif choice < 3:
                new_entity = Entity(8, position[0], position[1], 3*TILE_SIZE)
                enemies_group.add(new_entity)
            elif choice < 10:
                new_entity = Entity(1, position[0], position[1], 4*TILE_SIZE)
                enemies_group.add(new_entity)
            
    #after player is damaged, resets position to checkpoint
    def reset_position(self, position):
        sfx_dic['reset_position'].play()
        self.rect.x = round(position[0])
        self.rect.y = round(position[1])
        self.reset_invulnerability_time = self.local_time
        self.reset_invulnerability = True
        self.vel_y = 0

    #avoid other flyingman entities
    def avoid_sprites(self, sprites):
        for sprite in sprites:
            if sprite != self and sprite.entity_id == 8:
                distance = Vector2(self.rect.centerx - sprite.rect.centerx,
                                   self.rect.centery - sprite.rect.centery)
                if 0 < distance.length() < TILE_SIZE and self.acceleration.length() != 0:
                    self.acceleration += distance.normalize()
                    self.acceleration.scale_to_length(2.0)
                elif distance.length() == 0:
                    self.acceleration += Vector2(0, 0)

    #damage to entity
    def hurt(self, out_of_bounds, who_hurt_me):
        if not self.in_death_animation:
            if self.health_points - 1 > 0:
                if not out_of_bounds:
                    if self.entity_id != 3:
                        self.in_death_animation = True
                        self.health_points -= 1
                        if self.entity_id == 0:
                            sfx_dic['death'].play()
                        else:
                            sfx_dic['hit'].play()
                    else:
                        self.health_points -= 1
                        sfx_dic['hit'].play()
                else:
                    self.health_points -= 1
                    self.reset_position(self.checkpoint_position)

            else:
                self.health_points -= 1
                if not out_of_bounds:
                    if self.entity_id == 3:
                        self.kill()
                        sfx_dic['hit'].play()
                    else:
                        self.in_death_animation = True
                        if self.entity_id == 0:
                            sfx_dic['death'].play()
                        else:
                            sfx_dic['hit'].play()
                else:
                    if self.entity_id != 0:
                        self.kill()
                    self.alive = False

    # follow target ai function
    def seek_with_approach(self, target, tick):
        # vector from position -> target position
        self.desired = (
            target - Vector2(self.rect.centerx, self.rect.centery))
        distance_length = self.desired.length()
        if not distance_length == 0:
            self.desired.normalize_ip()
            if distance_length < self.approach_radius:
                self.desired *= distance_length / self.approach_radius * self.speed * tick
            else:
                self.desired *= self.speed * tick

            # vector from acceleration vector to desired vector position
            steer = (self.desired - self.acceleration)

            # scale of vector to have correct length
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            return steer
        else:
            return Vector2(0, 0)

    #use item near you
    def use(self, possible_use_item_list, snake_group, cage_group, current_time):
        for item in possible_use_item_list:
            if self.rect.colliderect(item.rect):
                sfx_dic['use'].play()
                if item.lever_type == 'green':
                    if item.activated:
                        item.action(snake_group, 'Appear')
                    else:
                        item.action(snake_group, 'Disappear')
                        item.activation_time = current_time
                elif item.lever_type == 'red':
                    if item.activated:
                        item.action(cage_group, False)
                    else:
                        item.action(cage_group, True)
                break
    
    #draw entities
    def draw(self, canvas, offset_x, offset_y):
        if self.entity_id == 0 or self.entity_id == 6:
            #change alpha while invulnerable after reset
            if self.reset_invulnerability and self.entity_id == 0:
                self.image.set_alpha(100)
            else:
                self.image.set_alpha(255)
                
            canvas.blit(pygame.transform.flip(self.image, self.flip, False), (round(self.rect.x -
                                                                                offset_x - TILE_SIZE//2), round(self.rect.y -
                                                                                                    offset_y - TILE_SIZE//4)))                                                                             
        else:
            canvas.blit(pygame.transform.flip(self.image, self.flip, False), (round(self.rect.x -
                                                                                offset_x), round(self.rect.y - offset_y)))  
        pygame.draw.rect(canvas, RED, (round(self.rect.x - offset_x),
                                                   round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)                                                                                                                                                                      
        # bubble rect on player                                                                                
        if self.entity_id == 0:
            bubble_rect = bubble_image.get_rect()
            bubble_rect.center = self.rect.center
            if self.invulnerability:
                canvas.blit(bubble_image, (bubble_rect.x - offset_x,bubble_rect.y - offset_y))

    #draw amount of fish player collected
    def draw_fish(self, canvas):    
        canvas.blit(blue_fish_image, (TILE_SIZE//4, TILE_SIZE//4))

    #draw health of player
    def draw_health(self, canvas):
        for x in range(self.health_points):
            canvas.blit(health_image, (TILE_SIZE/4 + x*TILE_SIZE + x*TILE_SIZE//8, SCREEN_HEIGHT - health_image.get_height()))

    #updating images and rects
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        if self.entity_id == 7:
            ANIMATION_COOLDOWN = 300
        if self.entity_id == 2 or self.entity_id == 8:
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
    #set new animation
    def set_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = self.local_time

#part of platform
class PlatformPart(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

# moving platform
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, parts, surface, id,speed, level):
        pygame.sprite.Sprite.__init__(self)
        self.platform_id = id
        self.parts = parts

        self.image = surface
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.speed = speed

        self.rect.x = x
        self.rect.y = y

        self.move_x, self.move_y, self.direction = self.determine_movement_by_id(id, level)

    def update(self, world, tick):
        dx = 0
        dy = 0
        if self.move_x:
            dx = self.direction * self.speed * tick
        if self.move_y:
            dy = self.direction * self.speed * tick
        dx = round(dx)
        dy = round(dy)

        #bounds tiles for platforms
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
            # pygame.draw.rect(canvas, RED, (round(self.rect.x - offset_x),
                                                #    round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)
        else:
            for x, part in enumerate(self.parts):
                self.image.blit(part.image, (x*TILE_SIZE, 0))
            canvas.blit(self.image, (round(self.rect.x -
                                           offset_x), round(self.rect.y - offset_y)))
            # pygame.draw.rect(canvas, RED, (round(self.rect.x - offset_x),
                                                #    round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

    #from loaded json data, determine behavior
    def determine_movement_by_id(self,id, level):
        data = json_data[f'level_{level}']['platforms'][id]
        return data['move_x'],data['move_y'],data['direction']

#Items
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
                self,[dx, dy], world.obstacles_list, all_platforms, enemies_group, world.invisible_blocks_list, item_boxes_group, sfx_dic,tick)

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                    offset_x), round(self.rect.y - offset_y)))

    #action for item
    def action(self, target, current_time):
        if self.item_type == 'Health':
            target.health_points +=1
        elif self.item_type == 'Bubble':
            target.invulnerability = True
            target.invulnerability_start_time = current_time
        elif self.item_type == 'Boost':
            target.boosted = True
            target.boost_start_time = current_time
            target.speed = 1.2 * target.speed
        
#decorations for map
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

#Water
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

    def collide_water(self, target, level):
        if pygame.sprite.collide_rect(self, target):
            target.hurt(False, 'water')
            if level == 4 and target.entity_id == 0:
                return True
              
#Mystery box   
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

#Items you can collect
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
        pygame.draw.rect(canvas, RED,
                         (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

    def collect(self, player):
        if pygame.sprite.collide_rect(self, player):
            if self.type == 'Fish':
                sfx_dic['collect'].play()
                player.fish += 1
                self.kill()

#Platform which just looks and as a normal platform but isnt
class FakePlatform(pygame.sprite.Sprite):
    def __init__(self, x, y, width_in_tiles, height_in_tiles, action, id, speed):
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
        self.speed = speed
        self.move_x = 0
        self.move_y = 0

        self.activated = False

    def update(self, world, tick):
        if self.activated:
            self.execute_action(tick)

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))
        # pygame.draw.rect(canvas, RED,
        #                  (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

    def execute_action(self, tick):
        if self.action == 'fall':
            self.rect.y += round(self.speed *tick)

#Invisible blocks
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
        # pygame.draw.rect(canvas, RED,
        #                  (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

#Exit to next level
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

#Projectiles
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, desired, direction):
        pygame.sprite.Sprite.__init__(self)
        self.entity_id = 9

        self.animation_list = animations_list[self.entity_id]
        self.action = int(Animation_type.Idle)
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.speed = speed
        self.direction = direction
        self.desired = desired
        self.position = Vector2(x,y)
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.local_time = 0
        self.update_time = 0
    def update(self, current_time, tick):
        self.local_time = current_time

        #determine movement
        self.position[0] += (self.speed * tick * self.desired[0] * self.direction)
        self.position[1] += (self.speed * tick * self.desired[1] * self.direction)

        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]

        self.update_animation()
        previous_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = previous_center

    def draw(self, canvas, offset_x, offset_y):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))

        # pygame.draw.rect(canvas, RED,
        #                  (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)
    def update_animation(self):
        ANIMATION_COOLDOWN = 80
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

#Cage for friend
class Cage(pygame.sprite.Sprite):
    def __init__(self, x, y, id):
        pygame.sprite.Sprite.__init__(self)
        
        self.cage_id = id

        self.is_open = False
        self.have_skull = True
        
        if self.cage_id == 0:
            self.have_skull = False

        self.new_state = False
        
        self.image = cage_closed_image

        self.rect = self.image.get_rect()
        self.rect.midtop = (x, y)
        
    def update(self):
        if self.new_state:
            lefttop_position = self.rect.topleft
            if self.is_open:
                self.image = cage_opened_image
            else:
                self.image = cage_closed_image

            self.rect = self.image.get_rect()
            self.rect.topleft = lefttop_position

    def draw(self, canvas, offset_x, offset_y):
        if self.have_skull:
            canvas.blit(skull_image, (round(self.rect.x -
                                       offset_x), round(self.rect.bottom - skull_image.get_height()*1.1 - offset_y)))
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))

    def draw_back(self, canvas, offset_x, offset_y):
        canvas.blit(cage_back_image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))
#Spike class
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
        pygame.draw.rect(canvas, RED,
                         (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

#Snake class
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

        #Snake states
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

            if self.rect.colliderect(player.rect) and not player.invulnerability and \
                 not player.reset_invulnerability and not player.in_death_animation:
                self.state = self.states['Attack']
                sfx_dic['snake_hit'].play()
                self.new_state = True

            self.flip = True if player.rect.center > self.rect.center else False
            
            #Setting animation based on state
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
                    player.hurt(False, 'Snake')

            self.rect, colls = move_with_collisions(
                self,[dx, dy], world.obstacles_list, all_platforms, enemies_group, world.invisible_blocks_list, item_boxes_group,sfx_dic, tick)
            self.update_animation()


    def draw(self, canvas, offset_x, offset_y):
        if self.active:
            canvas.blit(pygame.transform.flip(self.image, self.flip, False), (round(self.rect.x -
                                                                              offset_x), round(self.rect.y -
                                                                                             offset_y)))
            pygame.draw.rect(canvas, RED,
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

#Class for checkpoint
class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, img, x, y, id):
        pygame.sprite.Sprite.__init__(self)
        self.id = id
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y +
                            (TILE_SIZE - self.image.get_height()))

        self.location = (x, y)
        self.active = True

    def update(self, player):
        if self.rect.colliderect(player.rect) and self.active:
            player.checkpoint_position = vec(
                self.rect.centerx, self.rect.y + TILE_SIZE - player.rect.height)
            sfx_dic['checkpoint'].play()
            for checkpoint in checkpoints_group:
                if checkpoint.rect.x < self.rect.x:
                    checkpoint.active = False
                elif checkpoint == self:
                    self.active = False
                    break

    def draw(self, canvas, offset_x, offset_y, level):
        canvas.blit(self.image, (round(self.rect.x -
                                       offset_x), round(self.rect.y - offset_y)))
        
        is_lowest_id = True
        for c in checkpoints_group:
            if c != self and c.id < self.id:
                is_lowest_id = False
        
        if is_lowest_id:
            if level != 5 and level != 4:
                draw_text('start', 30 , WHITE, canvas, self.rect.centerx -offset_x, self.rect.y + self.rect.height/4 - offset_y, 'midtop', TILE_SIZE)
            elif level == 4:
                draw_text('Run!', 30 , WHITE, canvas, self.rect.centerx -offset_x, self.rect.y + self.rect.height/4 - offset_y, 'midtop', TILE_SIZE)
            elif level == 5:
                draw_text('careful', 20 , WHITE, canvas, self.rect.centerx -offset_x, self.rect.y + self.rect.height/4 - offset_y, 'midtop', TILE_SIZE)
        else:
            draw_text('checkpoint', 20 , WHITE, canvas, self.rect.centerx -offset_x, self.rect.y + self.rect.height/4 - offset_y, 'midtop', TILE_SIZE)
        pygame.draw.rect(canvas, RED,
                         (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)
    
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

#Simple cloud class
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
        pygame.draw.rect(canvas, RED,
                         (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

#Lever for items
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
        if self.lever_type == 'green':
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
        pygame.draw.rect(canvas, RED,
                         (round(self.rect.x - offset_x), round(self.rect.y - offset_y), self.rect.width, self.rect.height), 2)

    #resets lever effect
    def reset_to_default(self):
        self.image = self.images_list[1]
        self.rect = self.image.get_rect()
        self.rect.midtop = self.location

    #action on lever activation
    def action(self, group, state):
        self.new_state = True
        self.activated = not self.activated
        if self.lever_type == 'green':
            for member in group:
                member.state = member.states[state]
                member.new_state = True
                member.active = True

        elif self.lever_type == 'red':
            for member in group:
                member.is_open = state
                member.new_state = True


#main game function                      
def game():
    # needed variables
    global level_complete
    global background_images
    global bubble_image
    global health_image
    global fake_platform_green
    global fake_ground_green
    global intro_scene
    global skull_image
    global cage_opened_image
    global cage_closed_image
    global cage_back_image
    global player_head_image
    global friend_head_image
    global guard_head_image
    global tutorial
    global BORDER_LEFT
    global BORDER_RIGHT
    level_complete = False
    
    # level
    if intro_scene:
        level = 0
    else:
        level = 1
    # store tiles in a list
    img_list = []
    for x in range(TILE_TYPES):
        img = pygame.image.load(f'platformer/data/images/tiles/{x}.png').convert_alpha()
        if x == 210 or x == 211:
            img = pygame.transform.smoothscale(img, (TILE_SIZE, round(
                TILE_SIZE/(img.get_width()/img.get_height()))))
        elif x == 263:
            img = pygame.transform.scale(img, (TILE_SIZE*2, 
                TILE_SIZE))
        else:
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)

    running = True
    game_finished = False
    game_over = False
    boss_fight = False
    start_fight = False
    new_stage = True
    stage = 0
    current_time = 0
    timer = 0
    counter = 0
    new_camera = False

    last_camera_coord = 0.0,0.0

    health_image = pygame.transform.smoothscale(
            health_image, (TILE_SIZE, TILE_SIZE))
    bubble_image = pygame.transform.smoothscale(
            bubble_image, (TILE_SIZE*2, TILE_SIZE*2))
    skull_image = pygame.transform.smoothscale(
            skull_image, (TILE_SIZE*2, TILE_SIZE*2))
    cage_opened_image = pygame.transform.smoothscale(
            cage_opened_image, (TILE_SIZE*4, TILE_SIZE*5))

    #transforming images to right size
    scenes_head_images = transform_images([player_head_image, friend_head_image, guard_head_image], TILE_SIZE*2, TILE_SIZE*2, True)
    background_images = transform_images(background_images, SCREEN_WIDTH, SCREEN_HEIGHT, True)
    random_images = transform_images([fake_platform_green, fake_ground_green], TILE_SIZE, TILE_SIZE, False)
    cage_related_images = transform_images([cage_back_image, cage_closed_image], TILE_SIZE*2, TILE_SIZE*5, True)

    #returning images to use
    player_head_image, friend_head_image, guard_head_image = return_images_from_list(scenes_head_images)
    cage_back_image, cage_closed_image = return_images_from_list(cage_related_images)
    fake_platform_green, fake_ground_green = return_images_from_list(random_images)
    world, player, camera, all_platforms, invisible_blocks, \
    level,cut_scene_manager,BORDER_LEFT, BORDER_RIGHT = load_level(
        2, img_list)

    # Main game loop.
    while running:
        time_per_frame = Clock.tick(FPS)
        tick = time_per_frame / 1000.0
        current_time += time_per_frame
        screen.fill(BLACK)
        canvas.fill(BLACK)

        # print(Clock.get_fps())
        if level_complete:
            world, player, camera, all_platforms, invisible_blocks,\
            level,cut_scene_manager,BORDER_LEFT, BORDER_RIGHT = load_level(
                level, img_list)
            level_complete = False
        if tick > 0.3:
            tick = 0.2

        if player.alive == False:
            if game_over == False:
                sfx_dic['death_screen'].play()
            game_over = True
            world, player, camera, all_platforms, invisible_blocks, level \
               = game_over_menu(player,level, img_list)

        #only assign value if object exist
        guard = friend = wingman = None
        if bool(friend_group):
            friend = random.choice(friend_group.sprites())
        if bool(guardian_group):  
            guard = random.choice(guardian_group.sprites())
        if bool(wingmans_group):
            wingman = random.choice(wingmans_group.sprites())
        
        # User input
        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not player.locked:
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
                            sfx_dic['jump_2'].play()
                            jump_vel = tick * -player.jump_vel
                            if jump_vel < -player.jump_force:
                                jump_vel = -player.jump_force
                            player.vel_y = jump_vel
                            player.jump = True
                            player.on_platform = False

                # keyboard button released
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        player.moving_left = False
                        if player.moving_right:
                            player.direction = 1
                    if event.key == pygame.K_d:
                        player.moving_right = False
                        if player.moving_left:
                            player.direction = -1
                    if event.key == pygame.K_w:
                        pass
                    if event.key == pygame.K_e:
                        player.use(levers_group, snakes_group, cages_group, current_time)

        #player animations
        if not player.in_death_animation and not player.locked:
            if player.in_air:
                player.set_action(int(Animation_type.Jump))
            elif player.moving_left or player.moving_right:
                player.set_action(int(Animation_type.Run))
            else:
                player.set_action(int(Animation_type.Idle))

        #camera update in levels
        if level == 4 and new_stage:
            new_stage = False
            camera_type = Auto(camera, player)
            camera.setmethod(camera_type)
            new_camera = True
        
        elif level == 5:
            if stage == 0 and start_fight:
                stage = 1
                boss_fight = True
                new_stage = True
                BORDER_LEFT, BORDER_RIGHT = 0 + last_camera_coord[0], 0 + last_camera_coord[0] + SCREEN_WIDTH
        
            if boss_fight and new_stage and stage == 1:
                camera = None
                print("camera non")
            
            elif not boss_fight and new_stage and stage == 4:
                BORDER_LEFT, BORDER_RIGHT = 0, world.get_world_length()
                camera = Camera(player,SCREEN_WIDTH, SCREEN_HEIGHT)
                camera_type = Border(camera, player, world.get_world_length())
                camera.setmethod(camera_type)
                new_stage = False
                new_camera = True
                print('new cam')

        #if player is alive update everything
        if player.alive:
            # Update methods
            player.update(current_time, tick,  world, all_platforms, level)
            cut_scene_manager.update(current_time, tick)
            for platform in all_platforms:
                platform.update(world, tick)

            for enemy in enemies_group:
                enemy.update(current_time, tick, world, all_platforms,level)
                if enemy.entity_id == 8:
                    enemy.ai(player, tick)

            if guard:
                guard.update(current_time, tick, world, all_platforms,level)

            if wingman:
                #wingman behavior in level
                if level == 4:
                    if player.rect.x + player.rect.width < camera.offset.x and not player.in_death_animation:
                        player.hurt(True, 'Border')
                        camera.offset.x = 0
                        projectiles_group.empty()
                    if player.rect.x + player.rect.width + 20*TILE_SIZE> world.get_world_length():
                        wingman.rect.x += wingman.speed*3 * tick
                    else:
                        wingman.rect.x = round(camera.offset.x) + SCREEN_WIDTH - wingman.rect.width
                    if new_camera:
                        wingman.rect.y += wingman.speed * wingman.direction * tick
                        if abs(wingman.rect.y - player.rect.y) < TILE_SIZE and wingman.local_time - \
                             wingman.shoot_timer > wingman.cooldowns['shoot']:
                            wingman.shoot('basic', 5*TILE_SIZE, Vector2(-1,0))
                # wingman behavior in level
                if level == 5:
                    # boss fight stages
                    if stage == 0 and new_stage:
                        new_stage = False
                        wingman.speed = 0
                        

                    if stage == 1:
                        if new_stage:
                            new_stage = False
                            wingman.speed = 4*TILE_SIZE

                        if wingman.local_time - wingman.global_timer > wingman.cooldowns['global'] and not wingman.diving:
                            wingman.global_timer = current_time
                            if wingman.local_time - wingman.shoot_timer > wingman.cooldowns['shoot']:
                                desired = player.rect.center - \
                                    Vector2(wingman.rect.centerx, wingman.rect.centery)
                                desired.normalize_ip()
                                wingman.shoot('basic', 5*TILE_SIZE, desired)
                            elif wingman.local_time - wingman.drop_timer > wingman.cooldowns['drop']:
                                wingman.drop(stage, (wingman.rect.centerx, wingman.rect.bottom))
                            elif wingman.dropped >= 3 and wingman.shot >= 3:
                                wingman.diving = True

                        #wingman going down
                        elif wingman.diving and not wingman.stunned and wingman.stun_timer == 0:
                                dy = wingman.speed*tick
                                for tile in world.obstacles_list:
                                    if tile[1].colliderect(wingman.rect.x, wingman.rect.y + dy, wingman.rect.width, wingman.rect.height):
                                        wingman.rect.bottom = tile[1].top
                                        wingman.stun_timer = wingman.local_time
                                        wingman.dropped = wingman.shot = 0
                                        wingman.stunned = True
                                        dy = 0
                                wingman.rect.y += dy
                        #stun timer
                        elif wingman.stunned:
                            if wingman.local_time - wingman.stun_timer > 3000:
                                wingman.stunned = False
                        #wingman going up
                        elif wingman.stun_timer != 0 and wingman.stunned == False:
                            dy = -wingman.speed*tick
                            if wingman.rect.y + dy < 0:
                                wingman.rect.y = 0
                                wingman.diving = False
                                wingman.stun_timer = 0
                                dy = 0
                                if wingman.health_points <= 3:
                                    new_stage = True
                                    stage = 2
                            wingman.rect.y += dy
                    elif stage == 2:
                        if new_stage:
                            direction = random.choice([-1,1])
                            new_stage = False
                            wingman.speed = 0
                            
                        if current_time - timer > 1500 and counter < 6:
                            sfx_dic['shoot'].play()
                            counter += 1
                            timer = current_time
                            skip = random.choice([0,1,2])
                            direction = -1
                            if direction == -1:
                                spawn_x = BORDER_RIGHT + TILE_SIZE
                            elif direction == 1:
                                spawn_x = BORDER_LEFT - TILE_SIZE
                            
                            helper_multiplier = 1
                            if skip == 1:
                                helper_multiplier = 1.2

                            for i in range(3):
                                if i == skip:
                                    continue
                                projectile = Projectile(spawn_x, SCREEN_HEIGHT - 5*TILE_SIZE - TILE_SIZE*i*2 *helper_multiplier, 6*TILE_SIZE, Vector2(1,0), direction)
                                projectiles_group.add(projectile)

                        elif counter >= 6 and bool(projectiles_group) == False:
                            stage = 3
                            new_stage = True

                    elif stage == 3:
                        if new_stage:
                            new_stage = False
                            wingman.speed = 5*TILE_SIZE
                        
                        if wingman.local_time - wingman.global_timer > wingman.cooldowns['global'] and not wingman.diving:
                                wingman.global_timer = current_time
                                if wingman.local_time - wingman.shoot_timer > wingman.cooldowns['shoot']:
                                    desired = player.rect.center - \
                                            Vector2(wingman.rect.centerx, wingman.rect.centery)
                                    wingman.shoot('spray', 5*TILE_SIZE, desired)

                                elif wingman.local_time - wingman.drop_timer > wingman.cooldowns['drop']:
                                    wingman.drop(stage, (wingman.rect.centerx, wingman.rect.bottom))

                                elif wingman.dropped >= 3 and wingman.shot >= 3:
                                    wingman.diving = True
                        elif wingman.diving and not wingman.stunned and wingman.stun_timer == 0:
                                dy = wingman.speed*tick
                                for tile in world.obstacles_list:
                                    if tile[1].colliderect(wingman.rect.x, wingman.rect.y + dy, wingman.rect.width, wingman.rect.height):
                                        wingman.rect.bottom = tile[1].top
                                        wingman.stun_timer = wingman.local_time
                                        wingman.dropped = wingman.shot = 0
                                        wingman.stunned = True
                                        dy = 0
                                wingman.rect.y += dy
                        
                        elif wingman.stunned:
                            if wingman.local_time - wingman.stun_timer > 3000:
                                wingman.stunned = False
                        
                        elif wingman.stun_timer != 0 and wingman.stunned == False:
                            dy = -wingman.speed*tick
                            if wingman.rect.y + dy < 0:
                                wingman.rect.y = 0
                                wingman.diving = False
                                wingman.stun_timer = 0
                                dy = 0
                            wingman.rect.y += dy
                
                wingman.update(current_time, tick, world, all_platforms,level)

            #end boss fight
            elif boss_fight and stage == 3:
                boss_fight = False
                new_stage = True
                stage = 4
                for snake in snakes_group:
                    snake.new_state = True
                    snake.state = snake.states['Disappear']

            for projectile in projectiles_group:
                projectile.update(current_time,tick)
            
            for projectile in projectiles_group.copy():
                # clearing projectiles outside the bonds, we need offset because projectiles are spawning outside of bonds
                if projectile.rect.x + projectile.rect.width + 3*TILE_SIZE< BORDER_LEFT or projectile.rect.x - 3*TILE_SIZE > BORDER_RIGHT \
                    or projectile.rect.y - projectile.rect.height < 0 or projectile.rect.y > SCREEN_HEIGHT:
                    projectile.kill()
                
                if projectile.rect.colliderect(player.rect) and not player.in_death_animation and \
                    not player.invulnerability and not player.reset_invulnerability:
                        player.hurt(False, 'projectile')
                        projectile.kill()

            # mystery box drop chances
            for box in item_boxes_group:
                box.update(img_list)
                if box.destroy:
                    choice = random.random()
                    print(choice)
                    #spawn item
                    if choice < 0.15:
                        new_item = Item(bubble_item_image, choice, box.rect.x, box.rect.y)
                        items_group.add(new_item)
                    elif choice < 0.30:
                        new_item = Item(health_item_image, choice, box.rect.x, box.rect.y)
                        items_group.add(new_item)
                    elif choice  < 0.45:
                        new_item = Item(boost_item_image,  choice, box.rect.x, box.rect.y)
                        items_group.add(new_item)
                    elif choice  < 0.55:
                        new_spikeman = Entity(2,  box.rect.x, box.rect.top, 3*TILE_SIZE)
                        enemies_group.add(new_spikeman)
                    elif choice  < 0.65:
                        new_snake = Snake(4, box.rect.x, box.rect.top)
                        snakes_group.add(new_snake)
                    elif choice  < 0.75:
                        new_enemy = Entity(1, box.rect.x, box.rect.top, 3*TILE_SIZE)
                        enemies_group.add(new_enemy)  
                    box.kill()

            for snake in snakes_group:
                snake.update(current_time, tick, world, all_platforms, player, item_boxes_group)

            for checkpoint in checkpoints_group:
                checkpoint.update(player)
                if stage == 0 and level == 5:
                    if checkpoint.active == False or checkpoint.rect.x < player.rect.x:
                        start_fight = True
                        player.checkpoint_position = checkpoint.rect.centerx, checkpoint.rect.y + TILE_SIZE - player.rect.height
                        
                elif level == 4:
                    if not new_camera and checkpoint.active == False:
                        new_stage = True

            for lever in levers_group:
                lever.update(current_time, snakes_group)

            for item in items_group:
                item.update(player, current_time, tick, world, all_platforms, item_boxes_group)

            for cage in cages_group:
                cage.update()

            if friend:
                in_cage = simple_collision_check(friend, cages_group)
                friend.update(current_time, tick, world, all_platforms,level)
                if level == 5 and friend.locked == True  and in_cage:
                    friend.rect.x = friend.x - friend.rect.width//2
                    friend.rect.bottom = friend.y - friend.rect.height*0.1
                    friend.flip = True

            for exit in exit_group:
                exit.update(player)
            for block in invisible_blocks.copy():
                if block.visible:
                    world.obstacles_list.append([block.image, block.rect])
                    invisible_blocks.pop(invisible_blocks.index(block))

            for platform in all_platforms.copy():
                if platform.rect.x > world.get_world_length() or platform.rect.x + platform.rect.width < 0 or \
                        platform.rect.y + platform.rect.height < 0 or platform.rect.y > SCREEN_HEIGHT:
                    all_platforms.pop(all_platforms.index(platform))

            if pygame.sprite.spritecollide(player, exit_group, False):
                sfx_dic['level_complete'].play()
                level_complete = True
            
            # adjust camera to player
            if bool(camera):
                if level == 4 and new_camera and not player.in_death_animation:
                    camera.offset.x += 4*TILE_SIZE * tick 
                else:
                    camera.scroll()

                offset_x, offset_y = camera.offset.x, camera.offset.y
                last_camera_coord = offset_x, offset_y 
            else:
                offset_x, offset_y = last_camera_coord

            # Draw methods
            draw_background(canvas, offset_x, offset_y, background_images)
            world.draw(canvas, offset_x, offset_y)

            for decoration in decoration_group:
                decoration.draw(canvas, offset_x, offset_y)

            for platform in all_platforms:
                platform.draw(canvas, offset_x, offset_y)
            
            for spike in spikes_group:
                spike.draw(canvas, offset_x, offset_y)

            for checkpoint in checkpoints_group:
                checkpoint.draw(canvas, offset_x, offset_y, level)

            for box in item_boxes_group:
                box.draw(canvas, offset_x, offset_y)

            for block in invisible_blocks:
                block.draw(canvas, offset_x, offset_y)

            for enemy in enemies_group:
                enemy.draw(canvas, offset_x, offset_y)

            for exit in exit_group:
                exit.draw(canvas, offset_x, offset_y)

            for cage in cages_group:
                cage.draw_back(canvas, offset_x, offset_y)
            
            for projectile in projectiles_group:
                projectile.draw(canvas, offset_x, offset_y)

            if friend:
                if level == 5 and friend.locked:
                    for friend in friend_group:
                        friend.draw(canvas, offset_x, offset_y)
                    for cage in cages_group:
                        cage.draw(canvas, offset_x, offset_y)

                elif friend.locked == False:
                    for cage in cages_group:
                        cage.draw(canvas, offset_x, offset_y)
                    for friend in friend_group:
                        friend.draw(canvas, offset_x, offset_y)

            if wingman:
                wingman.draw(canvas, offset_x, offset_y)

            for water in water_group:
                collision = water.collide_water(player, level)
                if collision:
                    camera.offset.x = 0
                    projectiles_group.empty()
                water.draw(canvas, offset_x, offset_y)

            for fish in fish_group:
                fish.collect(player)
                fish.draw(canvas, offset_x, offset_y)
            
            for snake in snakes_group:
                snake.draw(canvas,offset_x, offset_y)

            for lever in levers_group:
                lever.draw(canvas,offset_x, offset_y)

            for item in items_group:
                item.draw(canvas, offset_x, offset_y)
            
            for cloud in clouds_group:
                cloud.draw(canvas, offset_x, offset_y)
            
            if guard:
                guard.draw(canvas, offset_x, offset_y)

            player.draw(canvas, offset_x, offset_y)
            if not level == 5:
                player.draw_fish(canvas)
            player.draw_health(canvas)
        #cinematics
        if intro_scene:
            if level == 1:
                cut_scene_manager.start_cut_scene(
                                CutSceneOne(player, wingman, friend, current_time))
                intro_scene = False
        elif tutorial:
            if level == 2:
                cut_scene_manager.start_cut_scene(
                                Tutorial(player, current_time))
                tutorial = False
        if level == 3 and pygame.sprite.collide_rect(player, guard):
                cut_scene_manager.start_cut_scene(
                                CutSceneTwo(player, guard, current_time))
        elif level == 5 and bool(wingmans_group) == False:
            for lever in levers_group:
                if lever.activated:
                    cut_scene_manager.start_cut_scene(
                                FinalCutScene(player, friend, current_time))
                    game_finished = True
        
        #finish game and return to menu
        if game_finished and not player.alive:
            running = False
          
        cut_scene_manager.draw()    
        screen.blit(canvas, (0, 0))
        pygame.display.update()

#game over screen
def game_over_menu(player, level, img_list):
    world = None
    camera = None
    all_platforms = None
    invisible_blocks = None
    level = None
    clickable = True
    x = 0
    texts = ['Restart', 'Back to menu']
    number_of_buttons = 2
    buttons = []
    for x, button in enumerate(range(number_of_buttons)):
        button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 +
                        x*button_clicked.get_height()*2, 'menu', texts[x],button_clicked, x)
        buttons.append(button)

    for button in buttons:
        if button.draw(canvas, TILE_SIZE):
            if clickable:
                if button.button_id == 0:
                    world_data = reset_level()
                    world, player, camera, all_platforms, invisible_blocks, \
                    level, cut_scene_manager, BORDER_LEFT, BORDER_RIGHT = load_level(
                        1, img_list)
                elif button.button_id == 1:
                    pygame.quit()
                    sys.exit()
                clickable = False

    return world, player, camera, all_platforms, invisible_blocks, level

#main menu
def main_menu():
    pygame.mixer.music.load(f'platformer/data/sounds/music/{music_list[0]}')
    pygame.mixer.music.play(-1, 0.0, 2500)
    texts = ['Start', 'Settings', 'Credits', 'Quit']
    x = 0
    number_of_buttons = 4
    buttons = []
    for x, button in enumerate(range(number_of_buttons)):
        button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//10 +
                        x*button_clicked.get_height()*2, 'menu', texts[x], button_clicked, x)
        buttons.append(button)
    running = True
    clickable = False
    while running:
        canvas.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        for button in buttons:
            button.rect.centerx = SCREEN_WIDTH//2
            if button.draw(canvas, TILE_SIZE):
                if clickable:
                    if button.button_id == 0:
                        clickable = False
                        game()
                    elif button.button_id == 1:
                        clickable = False
                        settings()
                        
                    elif button.button_id == 2:
                        clickable = False
                        show_credits()
                    elif button.button_id == 3:
                        pygame.quit()
                        sys.exit()
        
       
        clickable = True
        screen.blit(canvas, (0, 0))
        pygame.display.update()


#credits section
def show_credits():
    running = True
    while running:
        canvas.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        draw_text('Credits', 72, WHITE,
                                      canvas, SCREEN_WIDTH//2, 50, 'midtop', TILE_SIZE)
        screen.blit(canvas, (0, 0))
        pygame.display.update()

#settings
def settings():
    number_of_buttons = 3
    buttons = []
    texts = ['Audio', 'Resolution', 'Controls']
    for x, button in enumerate(range(number_of_buttons)):
        button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 +
                        x*button_clicked.get_height()*2, 'menu',texts[x], button_clicked, x)
        buttons.append(button)
    running = True
    clickable = False
    while running:
        canvas.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        for button in buttons:
            button.rect.centerx = SCREEN_WIDTH//2
            if button.draw(canvas, TILE_SIZE):
                if clickable:
                    if button.button_id == 0:
                        audio()
                    elif button.button_id == 1:
                       resolutions()
                    elif button.button_id == 2:
                        controls()
        clickable = True
        draw_text('Settings', 72, WHITE,
                                      canvas, SCREEN_WIDTH//2, 50, 'midtop', TILE_SIZE)
        screen.blit(canvas, (0, 0))
        pygame.display.update()

#show controls
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
        draw_text('Controls', 72, WHITE,
                                      canvas, SCREEN_WIDTH//2, 50, 'midtop', TILE_SIZE)
        screen.blit(canvas, (0, 0))
        pygame.display.update()

#show controls
def audio():
    number_of_buttons = 3
    buttons = []
    texts = ['Master volume', 'Music volume', 'Sound effects']
    types = ['line', 'toggle', 'toggle']
    images = [slider_line, toggle_on, toggle_on]
    for x, button in enumerate(range(number_of_buttons)):
        if types[x] == 'toggle':
            button = Button(SCREEN_WIDTH*0.75 + images[x].get_width(), SCREEN_HEIGHT*0.1 + \
                     x*images[x].get_height()*2, types[x], '', images[x], x)
        else:
            button = Button(SCREEN_WIDTH*0.85, SCREEN_HEIGHT*0.1 + x*images[x].get_height()*2, types[x], '', images[x], x)
        buttons.append(button)
    clickable = False
    running = True
    slider = green_slider_down.get_rect()
    slider_float_value = 0
    slider_line_rect = buttons[0].rect
    while running:
        canvas.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        mouse_pos = pygame.mouse.get_pos()
        if slider.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                slider_float_value = (slider_line_rect.width/(slider_line_rect.width/(mouse_pos[0] - SCREEN_WIDTH*0.75))) / 100
                music_handler.set_master_volume(sfx_dic,slider_float_value)
                slider.centerx = button.rect.x + button.rect.width * music_handler.master_volume
                print(mouse_pos)
        for button in buttons:
            if button.type == 'line':
                # print(slider, music_handler.master_volume)
                slider.bottom = button.rect.top
            draw_text(texts[button.button_id], 36, RED,
                                      canvas, SCREEN_WIDTH*0.5, button.rect.centery, 'left',  TILE_SIZE)
            if button.draw(canvas, TILE_SIZE):
                if clickable:
                    if button.button_id == 0:
                        pass
                    elif button.button_id == 1:
                        music_handler.toggle_music()
                        if music_handler.paused:
                            button.image = toggle_off
                        else:
                            button.image = toggle_on
                    elif button.button_id == 2:
                        music_handler.toggle_sounds(sfx_dic)
                        if music_handler.sounds_off:
                            button.image = toggle_off
                        else:
                            button.image = toggle_on
        clickable = True

        canvas.blit(green_slider_down, (slider.x, slider.y))
        draw_text('Audio', 72, WHITE,
                                      canvas, SCREEN_WIDTH/10, SCREEN_HEIGHT*0.8, 'topleft', TILE_SIZE)
        screen.blit(canvas, (0, 0))
        pygame.display.update()

#setting for resolutions
def resolutions():
    global SCREEN_WIDTH
    global SCREEN_HEIGHT
    global screen
    global canvas
    global TILE_SIZE
    global GRAVITY
    global GRAVITY_FORCE_LIMIT
    global animations_list
    running = True
    number_of_buttons = 3
    buttons = []
    texts = ['800x640','1024x768','Fullscreen']
    for x, button in enumerate(range(number_of_buttons)):
        button = Button(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 +
                        x*button_clicked.get_height()*2, 'menu', texts[x], button_clicked, x)
        buttons.append(button)
    clickable = False
    while running:
        canvas.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        for x,button in enumerate(buttons):
            button.rect.centerx = SCREEN_WIDTH//2
            if button.draw(canvas, TILE_SIZE):
                if clickable:
                    if button.button_id == 0:
                        SCREEN_WIDTH, SCREEN_HEIGHT = 800, 640
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    elif button.button_id == 1:
                        SCREEN_WIDTH, SCREEN_HEIGHT = 1024,768
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                        canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    elif button.button_id == 2:
                        SCREEN_WIDTH, SCREEN_HEIGHT = monitor_size
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                        canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                    TILE_SIZE = round(SCREEN_HEIGHT / ROWS)
                    GRAVITY = round(SCREEN_HEIGHT / 12)
                    GRAVITY_FORCE_LIMIT = round(SCREEN_HEIGHT / 40)
                    animations_list = load_entity_animations()
                
        clickable = True
        draw_text('Resolution', 72, WHITE,
                                      canvas, SCREEN_WIDTH//2, 50, 'midtop', TILE_SIZE)
        screen.blit(canvas, (0, 0))
        pygame.display.update()

#start game
main_menu()
