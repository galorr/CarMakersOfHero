import zmq

class Sender(object):
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    def __init__(self):
        self.socket.bind("tcp://*:%s" % self.port)

    def send(self,message):
        self.socket.send(b(message))
        print('sender message - %s' % message) # For debug uses
