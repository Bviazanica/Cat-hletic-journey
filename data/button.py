# Setup python
import os
import sys
import pygame
import random


class Button():
    def __init__(self, x, y, type, image, id):
        self.image = image
        self.button_id = id
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    # draw plus action on click
    def draw(self, canvas):
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

        return action
