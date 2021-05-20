import math
import pygame

def load_fake_platform_tiles(width, height, surface, TILE_SIZE, ground_image, platform_image):
    for x in range(width):
        for y in range(height):
            if x == 0:
                surface.blit(platform_image, (y*TILE_SIZE, x*TILE_SIZE))
            else:
                surface.blit(ground_image, (y*TILE_SIZE, x*TILE_SIZE))
    return surface


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.midtop = (x, y)
    surface.blit(textobj, textrect)

def is_close(object1, object2, distance):
    return math.hypot(object2.centerx-object1.centerx, object2.centery-object1.centery) < float(distance)

def transform_images(images, width, height):
    images_list = []
    for i in images:
        img = pygame.transform.scale(
            i, (width, height))
        images_list.append(img)

    return images_list

def return_images_from_list(images):
    new_images = []
    for i in images:
        new_images.append(i)
    return (new_images)