import time
import threading
import RPi.GPIO as GPIO
from .controls import LEDController
import atexit

R = 32
G = 33
B = 35

PINS = [R,G,B]

def ledMaster(l):
    time.sleep(1)
    l.set('full_blue')
    while True:
        time.sleep(1)

 
def main():
    try:
        #GPIO.setmode(GPIO.BOARD)
       
        #time.sleep(2)
        #GPIO.setup(PINS, GPIO.OUT, initial=GPIO.HIGH)
        ledController = LEDController(PINS)
        #t = threading.Thread(target=ledMaster, args=(ledController,))
        # t.daemon = True
        # t.start()
        #ledController.cleanup()
        
        ledController.set('full_blue')
        time.sleep(2)
        ledController.set('full_green')
        time.sleep(2)
        ledController.set('slow_green')
        time.sleep(2)
        ledController.set('fast_green')
        time.sleep(2)
        ledController.set('fast_blue')
        time.sleep(2)
        ledController.set('slow_blue')
        time.sleep(2)





      
        
        
    except KeyboardInterrupt:
        pass
    finally:
        ledController.cleanup()
        #ledController.cleanup()
 
 
if __name__ == '__main__':
    main()



