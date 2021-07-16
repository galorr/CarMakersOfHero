from hashlib import new
import pygame
import json
from command import Command
from enums import ButtonKey
from enums import CommandType
from sender import Sender

################################# LOAD UP A BASIC SETTINGS ############################
pygame.init()
pygame.font.init()
running = True
clock = pygame.time.Clock()
commandDictionary = {}
oldCommandDictionary = {}
sender = Sender()
###########################################################################################

################################# LOAD UP A BASIC WINDOW #################################
DISPLAY_W, DISPLAY_H = 300, 60
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))
fontsize = 15
myfont = pygame.font.SysFont("times", fontsize)
OPEN = 'open'
LOCK = 'lock'
differentialFront = OPEN
differentialRear = OPEN
backSlowly = 'on'
###########################################################################################


# Initialize controller
joysticks = []
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
for joystick in joysticks:
    joystick.init()

# 0: Left analog horizontal, 1: Left Analog Vertical, 2: Right Analog Horizontal
# 3: Right Analog Vertical 4: Left Trigger, 5: Right Trigger
analog_keys = {0:0, 1:0, 2:0, 3:0, 4:-1, 5: -1 }

# Initialize command dictionary
for commandType in CommandType:
    commandDictionary[commandType] = None
    oldCommandDictionary[commandType] = None

# START OF GAME LOOP
while running:
    ################################# CHECK JOYSTICK INPUT #################################
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            ############### UPDATE SPRITE IF SPACE IS PRESSED #################################
            pass

        # HANDLES BUTTON RELEASES
        if event.type == pygame.JOYBUTTONUP:
            if event.button == ButtonKey.square.value:
                commandDictionary[CommandType.differentialFront] = Command(CommandType.differentialFront.value, 1000)
                differentialFront = OPEN
            if event.button == ButtonKey.circle.value:
                commandDictionary[CommandType.differentialFront] = Command(CommandType.differentialFront.value, 2000)
                differentialFront = LOCK
            if event.button == ButtonKey.x.value:
                commandDictionary[CommandType.differentialRear] = Command(CommandType.differentialRear.value, 1000)
                differentialRear = OPEN
            if event.button == ButtonKey.triangle.value:
                commandDictionary[CommandType.differentialRear] = Command(CommandType.differentialRear.value, 2000)
                differentialRear = LOCK
            if event.button == ButtonKey.down_arrow.value:
                commandDictionary[CommandType.throttle] = Command(CommandType.throttle.value, 1400)
                backSlowly = 'on'
            if event.button == ButtonKey.up_arrow.value:
                commandDictionary[CommandType.throttle] = Command(CommandType.throttle.value, 1500)
                backSlowly = 'off'

        #HANDLES ANALOG INPUTS
        if event.type == pygame.JOYAXISMOTION:         
            analog_keys[event.axis] = event.value
            
            if abs(analog_keys[0]) > .4 or abs(analog_keys[2]) > .4:
                 # Left Horizontal Analog
                if abs(analog_keys[0]) > .4:
                    commandDictionary[CommandType.steering] = Command(CommandType.steering.value, (analog_keys[0] + 3) * 500)
                # Right Horizontal Analog
                if abs(analog_keys[2]) > .4:
                    commandDictionary[CommandType.steering] = Command(CommandType.steering.value, (analog_keys[2] + 3) * 500)
            else:
                if event.axis == 0 or event.axis == 2:
                    commandDictionary[CommandType.steering] = Command(CommandType.steering.value, 1500)

            # Triggers
            if analog_keys[4] >= 0 or analog_keys[5] >= 0:
                if analog_keys[4] >= 0:  # Left trigger
                    commandDictionary[CommandType.throttle] = Command(CommandType.throttle.value, 1500 - 500 * analog_keys[4])               
                if analog_keys[5] >= 0:  # Right Trigger
                    commandDictionary[CommandType.throttle] = Command(CommandType.throttle.value, 1500 + 500 * analog_keys[5])
            else:
                if event.axis == 4 or event.axis == 5:
                    commandDictionary[CommandType.throttle] = Command(CommandType.throttle.value, 1500)
        else:
        ############### Clean the Queue ###############
            pass

    ################################# UPDATE WINDOW AND DISPLAY #################################
    # render text  
    canvas.fill((255,255,255))
    window.blit(canvas, (0,0)) 
    # Front differential Label 
    differentialFrontLabel = myfont.render('Front differential - %s' % differentialFront, 1, (0,0,0))
    window.blit(differentialFrontLabel,(5,0))
    # Rear differential Label 
    differentialRearLabel = myfont.render('Rear differential - %s' % differentialRear, 1, (0,0,0))
    window.blit(differentialRearLabel,(5,(fontsize)+(5)))
    # Back slowly Label 
    backSlowlyLabel = myfont.render('Back slowly - %s' % backSlowly, 1, (0,0,0))
    window.blit(backSlowlyLabel,(5,(2*fontsize)+(10)))
    # Send command to RaspberryPy
    for commandType in CommandType: 
        if commandDictionary[commandType] != None:
            if commandType == CommandType.throttle:
                if oldCommandDictionary[commandType] != None:                  
                    if commandDictionary[commandType].value == 1500 and oldCommandDictionary[commandType].value == 1500:
                        # Do nothing
                        pass
                    else:
                        message = json.dumps(commandDictionary[commandType].__dict__)
                        sender.send(message=message)           
                        if (commandDictionary[commandType].value > 1500 and oldCommandDictionary[commandType].value < 1500) or (oldCommandDictionary[commandType].value > 1500 and commandDictionary[commandType].value < 1500):
                            command = Command(CommandType.throttle.value, 1500)
                            message = json.dumps(command.__dict__)
                            sender.send(message=message) 
                        oldCommandDictionary[commandType] = commandDictionary[commandType]
                else:
                   oldCommandDictionary[commandType] = commandDictionary[commandType]
                   message = json.dumps(commandDictionary[commandType].__dict__) 
                   sender.send(message=message)     
            else:
                if not commandDictionary[commandType].equal(oldCommandDictionary[commandType]):
                    oldCommandDictionary[commandType] = commandDictionary[commandType]
                    message = json.dumps(commandDictionary[commandType].__dict__)
                    sender.send(message=message)                              
               
    pygame.display.update()
    clock.tick(60)