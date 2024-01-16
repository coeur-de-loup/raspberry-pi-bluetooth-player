import threading
import RPi.GPIO as GPIO
from .basiccurves import gaussian_flash, log_flash, linear_flash, dynamic_sinusoidal_transition, full
import atexit

R = 32
G = 33
B = 35
PINS = [R,G,B]


def getLedController():
    return LEDController(PINS)
    
class LEDController:
    def __init__(self, pins):
        # Initialize the pins for R, G, B
        self.PINS=pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PINS, GPIO.OUT, initial=GPIO.HIGH)
        self.R, self.G, self.B = pins
        self.r = GPIO.PWM(self.R, 300)
        self.g = GPIO.PWM(self.G, 300)
        self.b = GPIO.PWM(self.B, 300)
        self.methods = {
            'full_green': self.full_green,
            'full_blue': self.full_blue,
            'slow_blue': self.slow_blue,
            'fast_blue': self.fast_blue,
            'slow_green': self.slow_green,
            'fast_green': self.fast_green
        }

        self.current_method = None
        self.lock = threading.Lock()
        #self.set('slow_green')

    def run_method(self, method_name):
        with self.lock:
        # Stop the current method if any
            if self.current_method:
                self.current_method.stop()
                self.current_method.join()

            # Start the new method
            method = self.methods.get(method_name)
            if method:
                self.current_method = method()

    def stop(self):
        method = self.current_method
        if method:
            method.stop()
            method.join()

    def set(self, method_name):
        self.run_method(method_name)



    def initialize_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.PINS, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.output(PINS, GPIO.HIGH)

    def cleanup(self):
        self.set(None)
        GPIO.output(PINS, GPIO.HIGH)
        GPIO.cleanup()

    def off(self):
        for c in self.PINS:
            GPIO.output(c, GPIO.HIGH)

    def full_green(self):
        return full(self.g)
    def full_blue(self):
        return full(self.b)

    def slow_blue(self):
        speed = 0.02
        step = 1
        return gaussian_flash(self.b, speed, step, 100, 55, 30)

    def fast_blue(self):
        speed = 0.002
        step = 1
        return log_flash(self.b, speed, step, 1)

    def fast_green(self):
        speed = 0.0004
        step = 10
        min = 90
        max = 100
        return linear_flash(self.g,speed, step, min, max)

    def slow_green(self):
        min_dc = 40       # Minimum duty cycle
        max_dc = 80       # Maximum duty cycle
        L = 80            # Amplitude of the sinusoidal wave
        b = 0             # Phase shift
        c = 180           # Period of the wave
        base_speed = 0.03 # Base speed
        return dynamic_sinusoidal_transition(self.g, min_dc, max_dc, L, b, c, base_speed)