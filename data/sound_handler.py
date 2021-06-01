import pygame
import random

# music, sounds and volume handling
class SoundHandler(object):
    def __init__(self):
        self.paused = pygame.mixer.music.get_busy()
        self.sounds_off = False
        self.master_volume = 0.5

    # toggling sounds
    def toggle_music(self):
        if self.paused:
            pygame.mixer.music.unpause()
            pygame.mixer.music.set_volume(self.master_volume)
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
        if not self.paused:
            pygame.mixer.music.pause()
        self.paused = not self.paused

        return True
    
    def toggle_sounds(self, sfx):
        if not self.sounds_off:
            self.set_all_sounds_volume(sfx, 0.0)
        elif self.sounds_off:
            self.set_all_sounds_volume(sfx, self.master_volume)
        self.sounds_off = not self.sounds_off

        return True

    def set_all_sounds_volume(self, sfx,float_value):
        for sound in sfx:
            pygame.mixer.Sound.set_volume(sfx[sound], float_value)

    def set_master_volume(self, sfx,float_value):
        self.master_volume = float_value
        if not self.paused:
            pygame.mixer.music.set_volume(self.master_volume)
        if not self.sounds_off:
            self.set_all_sounds_volume(sfx,self.master_volume)

    def music_que(self, music_que, music_list):
        if len(music_que) == 0:
            music_que = music_list[2:-1]
            random_music = random.choice(music_que)
        else:
            random_music = random.choice(music_que)

        music_que.remove(random_music)
        pygame.mixer.music.load(f'platformer/data/sounds/music/{random_music}')
        pygame.mixer.music.play(0, 0.0, 2500)

        return music_que