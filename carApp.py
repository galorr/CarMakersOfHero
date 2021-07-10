import zmq
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
        command.initFromJson(messag)
        running = False # only for debug uses
        # Activate the car controlers
        if command.type == CommandType.lock.value:
            print('lock') # Send lock PWM command
        if command.type == CommandType.gear.value:
            print('gear') # Send lock PWM command
        if command.type == CommandType.steering.value:
            print('steering') # Send lock PWM command
        if command.type == CommandType.throttle.value:
            print('throttle') # Send lock PWM command
    except:
        print('Error getting messages from server')
