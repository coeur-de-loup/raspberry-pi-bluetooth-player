import subprocess
import threading
import logging
import os
import signal

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

class Player:
    def __init__(self):
        self.current_track = None
        self.blank_track = None
        self.playback_thread = None
        self.playback_process = None

    def load(self, filename):
        if not os.path.exists(filename):
            logging.error(f"File not found: {filename}")
            return False
        self.current_track = filename
        return True

    def load_blank(self, filename):
        if not os.path.exists(filename):
            logging.error(f"Blank file not found: {filename}")
            return False
        self.blank_track = filename
        return True

    def play(self):
        logging.info('play')
        if self.current_track is not None:
            if self.playback_process and self.playback_process.poll() is None:
                self.stop()

            self.playback_thread = threading.Thread(target=self._playback)
            self.playback_thread.start()

    def _playback(self):
        self.playback_process = subprocess.Popen(['aplay', self.current_track])
        self.playback_process.wait()

    def stop(self):
        logging.info('stop')
        if self.playback_process:
            self.playback_process.send_signal(signal.SIGINT)
            self.playback_process.wait()
        if self.playback_thread:
            self.playback_thread.join()

        if self.blank_track:
            self.play_blank()

    def play_blank(self):
        if os.path.exists(self.blank_track):
            if self.playback_process and self.playback_process.poll() is None:
                self.playback_process.send_signal(signal.SIGINT)
                self.playback_process.wait()

            self.playback_process = subprocess.Popen(['aplay', self.blank_track])
            self.playback_process.wait()
