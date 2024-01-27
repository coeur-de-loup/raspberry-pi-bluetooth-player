import pygame
import threading
import logging

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

def play_wav(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(-1)
    while pygame.mixer.music.get_busy():
        continue

# Replace 'yourfile.wav' with the path to your WAV file
#play_wav('./test.wav')

class Player:
    def __init__(self):
        pygame.mixer.init()
        self.current_track = None
        self.playback_thread = None


    def load(self, filename):
        self.current_track = filename
        pygame.mixer.music.load(filename)

    def play(self):
        logging.info('play')
        if self.current_track is not None:
            # Stop existing playback thread if it's running
            if self.playback_thread and self.playback_thread.is_alive():
                self.stop()

            # Start a new playback thread
            self.playback_thread = threading.Thread(target=self._playback)
            self.playback_thread.start()

    def _playback(self):
        pygame.mixer.music.play(-1)
        while pygame.mixer.music.get_busy():
            continue  # Keep playing until the track is no longer busy

    def stop(self):
        logging.info('stop')
        pygame.mixer.music.stop()
        # Optionally join the thread if needed
        if self.playback_thread:
            self.playback_thread.join()

if __name__ == '__main__':
    p = Player()
    p.load('./test.wav')
    p.play()