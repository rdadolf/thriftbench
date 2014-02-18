import sys
sys.path.append('../../py_common/')

import common
from protocol import Null


transport = common.get_transport('localhost', 38003, framed = True)
protocol = common.get_protocol(transport, 'fast')
client = Null.Client(protocol)

WINDOW_SIZE = 1
NUM_REQUESTS = int(sys.argv[1])

i = 0 
while i < NUM_REQUESTS:
    for w in xrange(0, WINDOW_SIZE):
        client.send_identity(i + w)
    for w in xrange(0, WINDOW_SIZE):
        n = client.recv_identity()
        assert n == (i + w)
    i += WINDOW_SIZE

#print "finished %d requests" % NUM_REQUESTS

# Big messages
# buf = ' ' * 60000
# for i in xrange(0, NUM_REQUESTS):
#     client.a(buf)

transport.close()
