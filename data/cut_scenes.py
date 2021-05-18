import pygame
from data.utility import draw_text


class CutSceneOne:
    def __init__(self, player, started_time):
        # Variables
        self.name = 'scene'
        self.step = 0
        self.current_time = 0
        self.cut_scene_running = True
        self.started_time = started_time
        # If we need to control the player while a cut scene running
        self.player = player

        # text to render
        self.text = {
            'one': "There are no enemies left...",
            'two': "Time to find a new challange..."
        }
        self.text_counter = 0

    def update(self, time_passed, time_passed_seconds):
        self.current_time = time_passed
        pressed = pygame.key.get_pressed()
        enter = pressed[pygame.K_RETURN]

        if self.step == 0 and self.current_time - self.started_time > 1000:
            self.player.state = self.player.states['IDLING']
            if int(self.text_counter) < len(self.text['one']):
                self.text_counter += 0.2
            else:
                self.step = 1
                self.text_counter = 0

        if self.step == 1:
            if int(self.text_counter) < len(self.text['two']):
                self.text_counter += 0.2
            else:
                self.step = 2

        if self.step == 2:
                self.cut_scene_running = False

        return self.cut_scene_running

    def draw(self, screen, font):

        if self.step == 0:
            draw_text(
                self.text['one'][0:int(self.text_counter)],
                font,
                (255, 255, 255),
                screen,
                400,
                50,
            )

        if self.step == 1:
            draw_text(
                self.text['two'][0:int(self.text_counter)],
                font,
                (255, 255, 255),
                screen,
                400,
                50
            )

# manager for cutscenes


class CutSceneManager:

    def __init__(self, screen):
        self.cut_scenes_complete = []
        self.cut_scene = None
        self.cut_scene_running = False

        # Drawing variables
        self.screen = screen
        self.window_size = 0

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
            if self.window_size < self.screen.get_height()*0.2:
                self.window_size += 2
            self.cut_scene_running = self.cut_scene.update(
                time_passed, time_passed_seconds)
        else:
            self.end_cut_scene()

    def draw(self, font):
        if self.cut_scene_running:
            # Draw rects generic to all cut scenes
            pygame.draw.rect(self.screen, BLACK,
                             (0, 0, self.screen.get_width(), self.window_size))
            pygame.draw.rect(self.screen, BLACK,
                             (0, SCREEN_SIZE[1]-self.window_size, self.screen.get_width(), self.window_size))

            # Draw specific cut scene details
            self.cut_scene.draw(self.screen, font)
