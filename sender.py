import zmq
import random
import sys

class Sender(object):
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    def __init__(self):     
        self.socket.bind("tcp://*:%s" % self.port)

    def send(self,message):
        topic = "10001"
        print("%d %d" % (topic, message))
        self.socket.send("%d %d" % (topic, message))
