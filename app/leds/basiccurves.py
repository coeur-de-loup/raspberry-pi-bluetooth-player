import RPi.GPIO as GPIO
import time
import math

from .threadwrapper import stoppable


def initialize_gpio(PINS):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PINS, GPIO.OUT, initial=GPIO.HIGH)

@stoppable
def full(p,stop):
    p.start(0)
    while not stop():
        time.sleep(1)
    p.ChangeDutyCycle(100)
        
@stoppable
def linear_flash(p, speed, step, min_dc, max_dc, stop):
    # Ensure min and max duty cycles are within the 0 to 100 range
    min_dc = max(0, min(min_dc, 100))
    max_dc = max(min_dc, min(max_dc, 100))

    p.start(0)

    current_dc = min_dc
    while not stop():
        # Gradually change the duty cycle
        while current_dc < max_dc:
            p.ChangeDutyCycle(current_dc)
            time.sleep(speed)
            current_dc += step * 0.001
            current_dc = min(current_dc, max_dc)  # Ensure not exceeding max_dc

        while current_dc > min_dc:
            p.ChangeDutyCycle(current_dc)
            time.sleep(speed)
            current_dc -= step * 0.001
            current_dc = max(current_dc, min_dc)  # Ensure not going below min_dc
    p.ChangeDutyCycle(100)


def log_scale(value, min_val, max_val, min_out, max_out):
    """Scale value logarithmically from min_val-max_val to min_out-max_out."""
    log_min = math.log(min_val)
    log_max = math.log(max_val)
    scale = (log_max - log_min) / (max_out - min_out)
    return min_out + (math.log(value) - log_min) / scale

@stoppable
def log_flash(p, speed, step, min, stop):
    p.start(0)

    min_val, max_val = min, 100  # Logarithmic range

    while not stop():
        # Increasing brightness
        for i in range(0, 99, step):
            dutyCycle = log_scale(i + min_val, min_val, max_val, 0, 99)
            p.ChangeDutyCycle(dutyCycle)
            time.sleep(speed)

        # Decreasing brightness
        for i in range(101, -1, -step):
            dutyCycle = log_scale(i + min_val, min_val, max_val, 0, 99)
            p.ChangeDutyCycle(dutyCycle)
            time.sleep(speed)
    p.ChangeDutyCycle(100)

def gaussian(x, a, b, c):
    """Gaussian function for smooth transitions.
    
    Args:
    x (float): The input value for which to calculate the output.
    a (float): The peak height of the Gaussian curve. Determines the maximum duty cycle.
    b (float): The position of the center of the peak. Determines the midpoint of the transition.
    c (float): Controls the width of the bell. A smaller c means a narrower peak and steeper edges.
    
    Returns:
    float: The calculated duty cycle based on the Gaussian function.
    """
    return a * math.exp(-((x - b) ** 2) / (2 * c ** 2))

@stoppable
def gaussian_flash(p, speed, step,a,b,c, stop):
    # Parameters for the Gaussian function
    # a: Peak height of the Gaussian curve (maximum duty cycle)
    # b: Center position of the peak (midpoint of the transition)
    # c: Width of the bell (controls the steepness of transition)

    p.start(0)

    while not stop():
        # Increasing brightness
        for i in range(0, 100, step):
            dutyCycle = gaussian(i, a, b, c)
            p.ChangeDutyCycle(dutyCycle)
            time.sleep(speed)

        # Decreasing brightness
        for i in range(101, -1, step):
            dutyCycle = gaussian(i, a, b, c)
            p.ChangeDutyCycle(int(dutyCycle/1000))
            time.sleep(speed)
    p.ChangeDutyCycle(100)

def sinusoidal(x, L, b, c):
    """ Sinusoidal function for smooth transitions. """
    return L / 2 * (1 + math.sin((x - b) * 2 * math.pi / c))

def sinusoidal_derivative(x, L, b, c):
    """ Derivative of the sinusoidal function to determine the rate of change. """
    return L / 2 * math.cos((x - b) * 2 * math.pi / c) * 2 * math.pi / c

@stoppable
def dynamic_sinusoidal_transition(p, min_dc, max_dc, L, b, c, base_speed, stop):
    p.start(0)
    current_dc = min_dc
    target_dc = max_dc
    step = 0.01  # Initial step size

    while not stop():
        while current_dc < target_dc:
            rate_of_change = abs(sinusoidal_derivative(current_dc, L, b, c))
            step = max(0.01, min(1 / (rate_of_change + 1e-6), 1))  # Adjust step size based on rate of change
            speed = base_speed * step
            p.ChangeDutyCycle(current_dc)
            time.sleep(speed)
            current_dc += step
            current_dc = min(current_dc, target_dc)

        while current_dc > min_dc:
            rate_of_change = abs(sinusoidal_derivative(current_dc, L, b, c))
            step = max(0.01, min(1 / (rate_of_change + 1e-6), 1))
            speed = base_speed * step
            p.ChangeDutyCycle(current_dc)
            time.sleep(speed)
            current_dc -= step
            current_dc = max(current_dc, min_dc)

        target_dc, min_dc = min_dc, target_dc 

    p.ChangeDutyCycle(100)
