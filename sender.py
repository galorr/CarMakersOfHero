import zmq

class Sender(object):
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    def __init__(self):     
        #self.socket.bind("tcp://*:%s" % self.port)
        self.socket.connect("tcp://localhost:%s" % self.port)

    def send(self,message):
        print('sender message - %s' % message)
        self.socket.send_string(message)
