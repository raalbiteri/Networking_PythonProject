# This program is meant to serve as the
# setup for the UDP client that will be run
# on the Raspberry Pi 3b+ with the pi hat in
# order to turn on LEDs on server pi
#
# Program: udpechoclient.py
# Author: Raunel Albiter <albiterri@msoe.edu>
# Date: 02/19/2021
# Revision: 1.0

import socket
import ledControl

mysocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ipaddr = '192.168.8.106'
port = 22222

while True:
    while ledControl.getConfirmedOption() == "-1":
        pass
    message = "Toggle LED: " + ledControl.getConfirmedOption()
    ledControl.resetConfirmedOption()
    mysocket.sendto(bytes(message,'utf-8'),(ipaddr,port))
    data, addr = mysocket.recvfrom(1024)
    parsedData = data.decode("utf-8").split(" ")
    toggleLEDs = parsedData[0]
    if toggleLEDs == "E-Check":
        ledControl.toggleMessage()
        toggleLEDs == ""
    print('Received: ' + data.decode("utf-8") + ' From: ' + addr[0] +
                ' Port: ' + str(addr[1]))
