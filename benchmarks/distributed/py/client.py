import sys
sys.path.append('../../py_common/')

import common
from protocol import Distributed

WINDOW_SIZE = 5

IP = sys.argv[1] if (sys.argv) > 1 else 'localhost'
PORT = int(sys.argv[2]) if (sys.argv) > 2 else 38003
NUM_REQUESTS = int(sys.argv[3]) if (sys.argv) > 3 else 10000

transport = common.get_transport(IP, PORT, framed = True)
protocol = common.get_protocol(transport, 'binary')
client = Distributed.Client(protocol)

i = 0 
while i < NUM_REQUESTS:
    # send all requests in the window
    for w in xrange(0, WINDOW_SIZE):
        client.send_msg(str(i + w))

    # now block and process them
    for w in xrange(0, WINDOW_SIZE):
        resp = client.recv_msg()
        # make sure we got back what we sent in
        assert resp == str(i + w)

    i += WINDOW_SIZE

print "finished %d requests" % NUM_REQUESTS

transport.close()
