from hacadet import pg, SOUND_PATHS


class SoundManager:
    def __init__(self):
        pg.mixer.init()
        self.sounds = {
            'high': pg.mixer.Sound(SOUND_PATHS['high']),
            'medium': pg.mixer.Sound(SOUND_PATHS['medium'])
        }

    def play(self, alert_type):
        self.sounds[alert_type].play()

    def stop(self, alert_type):
        self.sounds[alert_type].stop()
