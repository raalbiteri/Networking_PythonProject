# Networking_PythonProject
Final Project for CE 4961 that uses UDP protocol to sent LED data between two raspberry pi devices.

ledControl.py: File that sets up the pi hat on raspberry pi 3b+ to use the LEDs and buttons

udpechoclient.py: File that is meant to run on the pi with the hat to send LED toggle data to server (Transmitter)
udpechoserver.py: File that is meant to run on the pi with 3 LEDs and 1 button setup to receive LED toggle data from client (Receiver)
