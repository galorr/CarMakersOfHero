#!/usr/bin/env python3
import zmq
import RPi.GPIO as GPIO

from time import sleep
from robot import Robot
from command import Command
from enums import CommandType

port = "5556"
host = "127.0.0.1" # change to py host
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
        if command.type == CommandType.differentialRear.value:
            print('lock/unlock rear') # Send lock PWM command
            Robot.pwm_differentialRear(35,50)
        if command.type == CommandType.differentialFront.value:
            print('lock/unlock front') # Send lock PWM command
            Robot.pwm_differentialFront(35,50)
        if command.type == CommandType.steering.value:
            print('steering') # Send lock PWM command
            Robot.pwm_steering(35,50)
        if command.type == CommandType.throttle.value:
            print('throttle') # Send lock PWM command
            Robot.pwm_throttle(35,50)
    except:
        print('Error getting messages from server')
