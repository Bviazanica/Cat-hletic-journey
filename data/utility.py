import os
import math
import pygame

#loads fake platforms
def load_fake_platform_tiles(width, height, surface, TILE_SIZE, ground_image, platform_image):
    for x in range(width):
        for y in range(height):
            if x == 0:
                surface.blit(platform_image, (y*TILE_SIZE, x*TILE_SIZE))
            else:
                surface.blit(ground_image, (y*TILE_SIZE, x*TILE_SIZE))
    return surface

#main function for drawing texts
def draw_text(text, size, color, surface, x, y, mid):
    font = pygame.font.Font('platformer/data/font/kenvector_future.ttf', size)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    if mid:
        textrect.midtop = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# is entity close check
def is_close(object1, object2, distance):
    return math.hypot(object2.centerx-object1.centerx, object2.centery-object1.centery) < float(distance)

def load_images(type_of_image_and_sprite):
    num_of_images = len(os.listdir(
                    f'platformer/data/images/{type_of_image_and_sprite}'))
    images = []
    for i in range(num_of_images):
        new_image = pygame.image.load(
            f'platformer/data/images/{type_of_image_and_sprite}/{i}.png').convert_alpha()
        images.append(new_image)
    
    return images
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