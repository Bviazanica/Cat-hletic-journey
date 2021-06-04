# Setup python
import os
from data.utility import draw_text
import sys
import pygame
import random

class Button():
    def __init__(self, x, y, type, text,image, id):
        self.x = x
        self.y = y

        self.image = image
        self.button_id = id
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

        self.text = text

    # draw plus action on click
    def draw(self, canvas, TILE_SIZE):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        canvas.blit(self.image, self.rect)
        if self.type != 'back':
            draw_text(self.text, 60, (255,255,255), canvas, self.rect.centerx, self.rect.centery, 'center', TILE_SIZE)
        else:
            draw_text(self.text, 50, (255,255,255), canvas, self.rect.x, self.rect.bottom, 'topleft', TILE_SIZE)
        # pygame.draw.rect(canvas, (255,0,0),
        #                  (round(self.rect.x), round(self.rect.y ), self.rect.width, self.rect.height), 2)
        return action
