import os
import math
import pygame
from pygame import mixer
pygame.mixer.init(48000, -16, 1, 1024)
mixer.init()
pygame.font.init()
#loads fake platforms
def load_fake_platform_tiles(width, height, surface, TILE_SIZE, ground_image, platform_image):
    for x in range(width):
        for y in range(height):
            if x == 0:
                surface.blit(platform_image, (y*TILE_SIZE, x*TILE_SIZE))
            else:
                surface.blit(ground_image, (y*TILE_SIZE, x*TILE_SIZE))
    return surface

def load_fonts_to_dic():
    dict = {}
    for i in range(500):
        font = pygame.font.Font('platformer/data/font/caramel_sweets.ttf', i)
        dict[i] = font
    return dict

#main function for drawing texts
def draw_text(text, size, color, surface, x, y, draw_position, TILE_SIZE):
    if text:
        text = text.upper()
        size = round((TILE_SIZE / 100) * size)
        font = fonts[size]
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        if draw_position == 'midtop':
            textrect.midtop = (x, y)
        elif draw_position == 'topleft':
            textrect.topleft = (x, y)
        elif draw_position == 'center':
            textrect.center = (x,y)
        elif draw_position == 'topright':
            textrect.topright = (x,y)
        elif draw_position == 'left':
            textrect.left = x
            textrect.centery = y
        surface.blit(textobj, textrect)

# is entity close check
def is_close(object1_rect, object2_rect, distance):
    return math.hypot(object2_rect.centerx-object1_rect.centerx, object2_rect.centery-object1_rect.centery) < float(distance)

def load_images(type_of_image_and_sprite):
    images = []
    for i in os.listdir(f'platformer/data/images/{type_of_image_and_sprite}'):
        new_image = pygame.image.load(
            f'platformer/data/images/{type_of_image_and_sprite}/{i}').convert_alpha()
        images.append(new_image)
    
    return images

def load_images_to_dic(path):
    dict = {}
    name = ''
    for file in os.listdir(f'platformer/data/images/{path}'):
        new_image = pygame.image.load(
            f'platformer/data/images/{path}/{file}').convert_alpha()
        name = file
        string_size = len(name)
        sliced_name = name[:string_size - 4]
        dict[sliced_name] = new_image
    return dict

def load_sounds():
    dict = {}
    name = ''
    for file in os.listdir(f'platformer/data/sounds/sfx'):
        new_file = pygame.mixer.Sound(f'platformer/data/sounds/sfx/{file}')
        name = file
        string_size = len(name)
        sliced_name = name[:string_size - 4]
        dict[sliced_name] = new_file
    return dict

def load_music_names():
    music_names = []
    for name in os.listdir(f'platformer/data/sounds/music'):
        music_names.append(name)
    return music_names

#scaling images to certain size
def transform_images(images, width, height, smooth):
    images_list = []
    for i in images:
        if smooth:
            img = pygame.transform.smoothscale(
                i, (width, height))
        else:
            img = pygame.transform.scale(
                i, (width, height))
        images_list.append(img)

    return images_list
#returns images from array
def return_images_from_list(images):
    new_images = []
    for i in images:
        new_images.append(i)
    return (new_images)

#simple collision
def simple_collision_check(sprite, entities):
        collision = False
        for en in entities:
            if pygame.sprite.collide_rect(sprite, en):
                collision = True

        return collision

fonts = load_fonts_to_dic()