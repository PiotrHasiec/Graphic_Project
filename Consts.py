import numpy as np
class SingletonMeta(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class consts(metaclass=SingletonMeta):
    def __init__(self):
        self.rocket_wav = 'rocket.wav'
        self.player_image = "starship1.png"
        self.player_active_image ="active_starship.png"
        self.rainbow_image ="rainbow_bullets.png"
        self.meteor_image = ["meteor.png","meteor2.png","meteor3.png"]
    def get_rocket_wav(self):
        return self.rocket_wav
    def get_player_image(self):
        return self.player_image
    def get_player_active_image(self):
        return self.player_active_image
    def get_meteor_image(self):
        return self.meteor_image
    def get_rainbow_image(self):
        return self.rainbow_image


