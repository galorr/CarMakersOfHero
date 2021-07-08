from hashlib import new
import pygame
import json
import zmq
from command import Command
from enums import ButtonKey
from enums import CommandType
from sender import Sender

################################# LOAD UP A BASIC SETTINGS ############################
pygame.init()
pygame.font.init()
running = True
clock = pygame.time.Clock()
command = None
sender = Sender()
###########################################################################################

################################# LOAD UP A BASIC WINDOW #################################
DISPLAY_W, DISPLAY_H = 300, 100
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
player = pygame.Rect(DISPLAY_W/2, DISPLAY_H/2, 60,60)
fontsize = 15
myfont = pygame.font.SysFont("times", fontsize)
gear = 'low'
differential = 'open'
###########################################################################################


# Initialize controller
joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    joystick.init()

# 0: Left analog horizonal, 1: Left Analog Vertical, 2: Right Analog Horizontal
# 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }

# START OF GAME LOOP
while running:
    ################################# CHECK PLAYER INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ############### UPDATE SPRITE IF SPACE IS PRESSED #################################
            pass

        command = None

        # HANDLES BUTTON PRESSES
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == ButtonKey.square.value:
                command = Command(CommandType.lock.value, 1000)
                differential = 'open'
            if event.button == ButtonKey.circle.value:
                command = Command(CommandType.lock.value, 2000)
                differential = 'lock'
            if event.button == ButtonKey.x.value:
                command = Command(CommandType.gear.value, 1000)
                gear = 'low'
            if event.button == ButtonKey.triangle.value:
                command = Command(CommandType.gear.value, 2000)
                gear = 'high'
        # HANDLES BUTTON RELEASES
        if event.type == pygame.JOYBUTTONUP:
            if event.button == ButtonKey.square.value:
                command = Command(CommandType.lock.value, 1500)
            if event.button == ButtonKey.circle.value:
                command = Command(CommandType.lock.value, 1500)
            if event.button == ButtonKey.x.value:
                command = Command(CommandType.gear.value, 1500)
            if event.button == ButtonKey.triangle.value:
                command = Command(CommandType.gear.value, 1500)

        #HANDLES ANALOG INPUTS
        if event.type == pygame.JOYAXISMOTION:    
            # command = Command(CommandType.steering.value, 1500)       
            analog_keys[event.axis] = event.value
           
            if abs(analog_keys[0]) > .4 or abs(analog_keys[2]) > .4:
                 # Left Horizontal Analog
                if analog_keys[0] < -.4:
                    command = Command(CommandType.steering.value, 1500 + 500 * analog_keys[0])
                if analog_keys[0] > .4:
                    command = Command(CommandType.steering.value, 1500 + 500 * analog_keys[0])

                # Right Horizontal Analog
                if analog_keys[2] < -.4:
                    command = Command(CommandType.steering.value, 1500 + 500 * analog_keys[2])
                if analog_keys[2] > .4:
                    command = Command(CommandType.steering.value, 1500 + 500 * analog_keys[2])
            else:
                command = Command(CommandType.steering.value, 1500)

            # Triggers
            if analog_keys[4] >= 0:  # Left trigger
                command = Command(CommandType.throttle.value, 1500 - 500 * analog_keys[4])               
            if analog_keys[5] >= 0:  # Right Trigger
                command = Command(CommandType.throttle.value, 1500 + 500 * analog_keys[5])

    ################################# UPDATE WINDOW AND DISPLAY #################################
    # render text  
    canvas.fill((255,255,255))
    window.blit(canvas, (0,0))    
    differentialLabel = myfont.render('differential - %s' % differential, 1, (0,0,0))
    gearLabel = myfont.render('gear - %s' % gear, 1, (0,0,0))
    window.blit(differentialLabel,(0,0))
    window.blit(gearLabel,(0,(1*fontsize)+(5*1)))
    if command != None:
        commandLabel = myfont.render(command.toString(), 1, (0,0,0))
        window.blit(commandLabel,(0,(2*fontsize)+(15*2)))  
    pygame.display.update()

    # Send command to RaspberryPy
    if command != None:
        message = json.dumps(command.__dict__)
        #socket.send(b'message')
        sender.send(message=message)

    clock.tick(60)