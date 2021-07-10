import zmq

port = "5556"
host = "127.0.0.1" # change to py host
running = True

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"")

socket.connect("tcp://%s:%s" % (host, port))

# Process the messages
total_value = 0
while running:
    try:
        print("Collecting updates from weather server...")
        string = socket.recv_string()
        print('messag %s' % string)
        running = False
    except:
        print('error')
