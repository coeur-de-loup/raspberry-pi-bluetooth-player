from pickle import FALSE
import threading
import RPi.GPIO as GPIO
import time
from .threadwrapper import stoppable
import http.client


def send_get_request(endpoint):
    base_url = "localhost"
    port = 8000
    
    full_url = f"/{endpoint.lstrip('/')}"

    try:
        conn = http.client.HTTPConnection(base_url, port)
        conn.request("GET", full_url)
        response = conn.getresponse()
        conn.close()
        print(f"GET request sent to {base_url}:{port}{full_url}")
    except Exception as e:
        print(f"An error occurred: {e}")





# Pin Definitions (using BOARD numbering)
input_pin = 29  # Physical pin 29
output_pin = 31 # Physical pin 31

@stoppable
def bouton(stop):
    GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)  # Set pin 31 to be an output pin
    GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pin 29 as an input pin with pull-down resistor

    button_pressed_time = None
    long_press_triggered = False

    try:
        while not stop():
            if GPIO.input(input_pin) == GPIO.HIGH:
                if button_pressed_time is None:
                    # Button is pressed; record the current time
                    button_pressed_time = time.time()
                    long_press_triggered = False

                elif not long_press_triggered and (time.time() - button_pressed_time) >= 3:
                    # Long press detected
                    print("Long Press Detected!")
                    long_press_triggered = True
                    send_get_request("long_press")
                    

            elif GPIO.input(input_pin) == GPIO.LOW:
                if button_pressed_time is not None and not long_press_triggered:
                    # Normal press detected
                    button_pressed_time = None
                    long_press_triggered = False
                    print("Normal Press Detected!")
                    send_get_request("short_press")
                
                # Reset the button state
                button_pressed_time = None
                long_press_triggered = False

            time.sleep(0.01)  # Small delay to prevent CPU overuse

    finally:
        GPIO.cleanup()  # Clean up GPIO on normal exit

# if __name__ == '__main__':
#     try:
#         t = main()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         t.stop()
#         t.join()
#         GPIO.cleanup()

