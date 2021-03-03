# This program is meant to serve as the
# setup for the UDP server that will be run
# on the Raspberry Pi 1 with at least 2 LEDs
# that will be turned on by the client and a
# pushbutton that will be used to send client
# signal to turn on lower 3 LEDs on hat
#
# Program: udpechoserver.py
# Author: Raunel Albiter <albiterri@msoe.edu>
# Date: 02/19/2021
# Revision: 1.0

import socket
import time
import RPi.GPIO as GPIO

global buttonPressed
buttonPressed = False

ledOptions = [17,27,22]
ledStatus = [0,0,0] #all off default

def initGPIO():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
def LEDSetup():
    leds = [17,27,22]
    GPIO.setup(leds,GPIO.OUT)
    ledOFF(leds)
    
def ledOFF(index):
    GPIO.output(index,GPIO.LOW)

def ledON(index):
    GPIO.output(index,GPIO.HIGH)
    
def buttonSetup():
    GPIO.setup(4,GPIO.IN,pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(4, GPIO.FALLING, callback=checkLight, bouncetime=300)
    
def checkLight(pin):
    global buttonPressed
    print("Pressed")
    buttonPressed = True
    time.sleep(0.1)


initGPIO()
LEDSetup()
buttonSetup()

mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mysocket.bind(('',22222))

while True:
    data, addr = mysocket.recvfrom(1024)
    print('Received: ' + data.decode("utf-8") + ' From: ' + addr[0] +
              ' Port: ' + str(addr[1]))
    parsedData = data.decode("utf-8").split(" ")
    ledSelect = int(parsedData[2])
    if ledStatus[ledSelect]:
        ledOFF(ledOptions[ledSelect])
        ledStatus[ledSelect] = 0
    else:
        ledON(ledOptions[ledSelect])
        ledStatus[ledSelect] = 1 

    if buttonPressed:
        mysocket.sendto(bytes("E-Check",'utf-8'),addr)
        buttonPressed = False
    else:
        mysocket.sendto(data,addr)

