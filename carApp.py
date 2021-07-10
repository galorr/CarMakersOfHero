import sys
import zmq

port = "5556"

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

socket.connect("tcp://localhost:%s" % port)

    # Subscribe to zipcode, default is NYC, 10001
#topicfilter = 1
#socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

# Process 5 updates
total_value = 0
for update_nbr in range (5):
    print("Collecting updates from weather server...")
    string = socket.recv()
    print('messag %s' % string)
    #topic, messagedata = string.split()
    # total_value += int(messagedata)
    #print(topic, messagedata)

# print("Average messagedata value for topic '%s' was %dF" % (topicfilter, total_value / update_nbr))