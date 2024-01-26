from logging.config import stopListening
from tokenize import StopTokenizing
from flask import Flask
import logging
import time
from leds import controls
from bouton.bouton import bouton
logging.basicConfig(level=logging.DEBUG)
import signal
import sys
from bt import scan
from play import play
import os




app = Flask(__name__)
led = controls.getLedController()
led.set('fast_green')
play()



app.logger.setLevel(logging.DEBUG)





current_state = {'state':'stopped'}


#werkzeug_logger = logging.getLogger('werkzeug')
#werkzeug_logger.setLevel(logging.DEBUG)

def play():
    current_directory = os.getcwd()
    app.logger.info(f'current player dir: {current_directory}')
    player.load('./test.wav')
    #full_green()
    fast_green()
    current_state['state'] = 'playing'
    player.play()
    

def stop():
    #full_green()
    slow_green()
    current_state['state'] = 'stopped'
    player.stop()

def pair():
    current_state['state'] = 'pairing'
    slow_blue()
    scan.scan_for_devices()
    fast_blue()
    time.sleep(2)
    stop()



@app.route('/')
def hello():
	return "Hello World! testrsdfghjgfdsrr"

@app.route('/full_green')
def full_green():
	led.set('full_green')
	return "led set to full green"

@app.route('/full_blue')
def full_blue():
	led.set('full_blue')
	return "led set to full blue"

@app.route('/slow_blue')
def slow_blue():
	led.set('slow_blue')
	return "led set to slow blue"

@app.route('/fast_blue')
def fast_blue():
	led.set('fast_blue')
	return "led set to fast blue"

@app.route('/slow_green')
def slow_green():
	led.set('slow_green')
	return "led set to slow green"

@app.route('/fast_green')
def fast_green():
	led.set('fast_green')
	return "led set to fast green"

@app.route('/clear')
def led_reset():
	led.set('None')
	return "led reset"

@app.route('/short_press')
def short_press():
    if current_state['state'] == 'stopped':
        play()
    elif current_state['state'] == 'playing':
        stop()
    return "short press"

@app.route('/long_press')
def long_press():
    if current_state['state'] == 'stopped' or current_state['state'] == 'playing':
        pair()
    return "long press"


bouton = bouton()




def graceful_exit(signum, frame):
    app.logger.info('EXITING.........')
    bouton.stop()
    bouton.join()
    led.stop()
    # Perform cleanup tasks
    # Then exit
    sys.exit(0)

signal.signal(signal.SIGTERM, graceful_exit)
signal.signal(signal.SIGINT, graceful_exit)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
    #app.run(host='0.0.0.0', port=8000, debug=True, use_reloader=False)
