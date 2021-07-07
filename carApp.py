import sys
import zmq

port = "5556"
# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print('Collecting updates from weather server...')
socket.connect ("tcp://localhost:%s" % port)

string = socket.recv()
print(string)