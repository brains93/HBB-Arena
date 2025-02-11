from time import sleep
import RPi.GPIO as GPIO
import sys
import logging
import threading
import random

logging.basicConfig(filename='/var/log/arenaapi.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(levelname)-2s %(message)s',  datefmt='%Y-%m-%d %H:%M:%S')

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT) #Flipper pin
GPIO.setup(13, GPIO.OUT) #Spinner pin
GPIO.setup(15, GPIO.OUT) #Pit pin
GPIO.setup(19, GPIO.OUT) #LED mid pin
GPIO.setup(21, GPIO.OUT) #LED start pin
GPIO.setup(23, GPIO.OUT) #LED end pin
# GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Door sensor pin
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #flipper press sensor pin

active_flag = 'active_flag.txt' #file where weapon active flag is stored, 1=weapons active 0=weapons inactive, this is also used to break the match loop

def flipper():
    flagcheck()
    GPIO.output(11, 1)
    logging.info('flipper triggered')
    sleep(0.1)
    GPIO.output(11, 0)

def spinner(state):
    if state == True:
        flagcheck()
        logging.info('spinner turned on')
        GPIO.output(13, 1)
    else:
        logging.info('spinner turned off')
        GPIO.output(13, 0)

def pit():
    flagcheck()
    logging.info('pit triggered')
    GPIO.output(15, 1)
    sleep(1)
    GPIO.output(15, 0)

def lightstart():
    flagcheck()
    GPIO.output(19, 1)
    logging.info('light start')
    GPIO.output(19, 0)

def lightmid():
    flagcheck()
    GPIO.output(21, 1)
    logging.info('light mid started')
    GPIO.output(21, 0)

def lightend():
    flagcheck()
    GPIO.output(23, 1)
    logging.info('light end started')
    GPIO.output(23, 0)

def stopmatch():
    with open(active_flag, 'w') as file:
    # Write '0' to the file
        file.write('0')

def flagcheck():
    with open(active_flag, 'r') as file:
        # Read the content of the file
        content = file.read()

        # Check if the content is '0' or '1'
        if content == '0':
            logging.info("match end flag is set ending loop")
            sys.exit()
        elif content == '1':
            return
        

def matchtimer():
    logging.info('match started')
    with open(active_flag, 'w') as file:
        file.write('1')
    lightstart()
    sleep(60) #timer till pit opens and spinner turns on
    #middle of match, weapons activate
    lightmid()
    spinner(True)
    pit()
    sleep(120) #timer till the end of the match
    #end of the match
    lightend()
    spinner(False)
    stopmatch()
    logging.info('match ended')


def flipper_button_listener():
    logging.info('flipper button listener started')

    while True:
        if GPIO.input(40) == GPIO.HIGH:
            logging.info('flipper button pressed')
            random_num = random.randint(1, 100)
            if random_num >= 50:
                
                logging.info(f'flipper triggered with random number {random_num}')
                flipper()
                sleep(0.1)
            sleep(1)  # debounce delay

# Start the background thread
flipper_thread = threading.Thread(target=flipper_button_listener)
flipper_thread.daemon = True
flipper_thread.start()

