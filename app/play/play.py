import subprocess
import threading
import logging
import os
import signal

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

class Player:
    def __init__(self):
        logging.info("Initializing player")
        self.current_track = None
        self.playback_thread = None
        self.playback_process = None

    def load(self, filename):
        if not os.path.exists(filename):
            logging.error(f"File not found: {filename}")
            return False
        self.current_track = filename
        logging.info(f"Loaded audio file: {filename}")
        return True

    def play(self):
        logging.info('play')
        if self.current_track is not None:
            logging.info('play____ line 27')
            # Stop existing playback if it's running
            if self.playback_process and self.playback_process.poll() is None:
                logging.info('play____ line 30')
                self.stop()
                logging.info('play____ line 32')

            # Start a new playback thread
            self.playback_thread = threading.Thread(target=self._playback)
            logging.info('play____ line 36')
            self.playback_thread.start()
            logging.info('play____ line 38')

    def _playback(self):
        logging.info('playback____ line 41')
        self.playback_process = subprocess.Popen(['aplay', self.current_track])
        logging.info('playback____ line 43')
        self.playback_process.wait()
        logging.info('playback____ line 45')

    def stop(self):
        logging.info('stop')
        if self.playback_process:
            self.playback_process.send_signal(signal.SIGINT)
            self.playback_process.wait()
        if self.playback_thread:
            self.playback_thread.join()

if __name__ == '__main__':
    p = Player()
    if p.load('../test.wav'):
        p.play()
        input("Press Enter to stop playback...\n")
        p.stop()
