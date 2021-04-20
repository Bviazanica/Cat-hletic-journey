import pygame
import math
from abc import ABC, abstractmethod
vec = pygame.math.Vector2


class Camera:
    def __init__(self, player):
        self.player = player
        self.offset = vec(0, 0)
        self.offset_float = vec(0, 0)
        self.DISPLAY_W, self.DISPLAY_H = 800, 600
        self.CONST = vec(-self.DISPLAY_W/2 +
                         player.rect.width / 2, -self.DISPLAY_H/2 + player.rect.height/2)

    def setmethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()

# abstract base class for camera


class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass

# camera which follows player


class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x -
                                       self.camera.offset_float.x + self.camera.CONST[0])
        self.camera.offset_float.y += (self.player.rect.y -
                                       self.camera.offset_float.y + self.camera.CONST[1])
        self.camera.offset.x, self.camera.offset.y = int(
            self.camera.offset_float.x), int(self.camera.offset_float.y)

# camera which follows player, but can go to edges


class Border(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x -
                                       self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y -
                                       self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(
            self.camera.offset_float.x), int(self.camera.offset_float.y)

        # x axis handle
        self.camera.offset.x = int(max(
            CAMERA_LEFT, self.camera.offset.x))
        self.camera.offset.x = int(min(
            self.camera.offset.x, CAMERA_RIGHT - self.camera.DISPLAY_W))
        # y axis handle
        self.camera.offset.y = int(max(
            CAMERA_TOP, self.camera.offset.y))
        self.camera.offset.y = int(min(
            self.camera.offset.y, CAMERA_BOTTOM - self.camera.DISPLAY_H))


# camera with automatic linear movement
class Auto(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset.x += 1
