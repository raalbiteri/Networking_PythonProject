# This program is meant to serve as a
# setup for the Pi hat attached that will
# activate the LEDs and pushbuttons
#
# Program: ledControl.py
# Author: Raunel Albiter <albiterri@msoe.edu>
# Date: 02/19/2021
# Revision: 1.0

import RPi.GPIO as GPIO
import time
import threading

global ledOptions
ledOptions = [6,13,12]
global ledSelect
ledSelect = 0
global confirming
confirming = False
global confirmedLED
confirmedLED = "-1"
global toggleStatus
toggleStatus = False
e = threading.Event()


def initGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
def initThread():
    t = threading.Thread(name='non-block', target=flashLed, args=(e,))
    t.start()

def hatLEDSetup():
    leds = [6,13,12,26,20,21,4]
    GPIO.setup(leds,GPIO.OUT)
    ledOFF(leds)
    
def ledOFF(index):
    GPIO.output(index,GPIO.HIGH)

def ledON(index):
    GPIO.output(index,GPIO.LOW)
    
def toggleMessage():
    global toggleStatus
    leds = [20,21,4]
    if not toggleStatus:
        ledON(leds)
        toggleStatus = True
    else:
        ledOFF(leds)
        toggleStatus = False
    
def flashLed(event):
    flashInterval = 0.25
    while True:
        ledON(ledOptions[ledSelect])
        time.sleep(flashInterval)
        event_is_set = event.is_set()
        if event_is_set:
            ledOFF(ledOptions[ledSelect])
            time.sleep(flashInterval)
        else:
            ledON(ledOptions[ledSelect])
            

    
def hatButtonSetup():
    buttons = [16,19]
    GPIO.setup(buttons,GPIO.IN)
    GPIO.add_event_detect(buttons[0], GPIO.FALLING, callback=selectButton, bouncetime=300)  
    GPIO.add_event_detect(buttons[1], GPIO.FALLING, callback=confirmButton, bouncetime=300)

def selectButton(pin):
    global ledSelect, confirming
    if confirming:
        e.clear()
        confirming = False
    else:
        ledOFF(ledOptions[ledSelect])
        ledSelect += 1
        if ledSelect == 3:
            ledSelect = 0
    
def confirmButton(pin):
    global confirming, confirmedLED
    if not confirming:
        e.set()
        confirming = True
    else:
        e.clear()
        confirming = False
        confirmedLED = str(ledSelect)
#         print("You confirmed LED #" + str(ledSelect))
        
def getConfirmedOption():
    return str(confirmedLED)

def resetConfirmedOption():
    global confirmedLED
    confirmedLED = "-1"
    
initGPIO()
hatLEDSetup()
hatButtonSetup()
initThread()
    
