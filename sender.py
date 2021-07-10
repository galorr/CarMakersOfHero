import zmq

class Sender(object):
    port = "5556"
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    def __init__(self):     
        self.socket.bind("tcp://*:%s" % self.port)

    def send(self,message):      
        self.socket.send_string(message)
        print('sender message - %s' % message)
