#!/usr/bin/env python3
import zmq
import RPi.GPIO as GPIO

from time import sleep
from robot import Robot
from command import Command
from enums import CommandType

port = "5556"
host = "192.168.68.35" # for debug the host is 127.0.0.1
running = True
command = Command('', '')

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")

socket.connect("tcp://%s:%s" % (host, port))

# Process the messages
total_value = 0
while running:
    try:
        print("Collecting messages from server...") # For debug uses
        messag = socket.recv_string()
        print(messag)
        sleep(1)
        command.initFromJson(messag)
        running = False # only for debug uses
        # Activate the car controlers
        if command.type == CommandType.steering.value:
            print("steering {}".format(command.value)) # Send lock PWM command
            Robot.pwm_steering(command.value)
        if command.type == CommandType.throttle.value:
            print("throttle {}".format(command.value)) # Send lock PWM command
            Robot.pwm_throttle(command.value)
    except:
        print('Error getting messages from server')
