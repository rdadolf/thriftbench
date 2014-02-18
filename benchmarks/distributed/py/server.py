import sys
sys.path.append('../../py_common/')

import common
from protocol import Distributed

class Handler:
    def msg(self, a):
        return a


processor = Distributed.Processor(Handler())
port = int(sys.argv[1]) if len(sys.argv) > 1 else 38003

if __name__ == '__main__':
    print "Listening on %d" % port
    common.init_and_run_forever(processor, port, 'framed', 'binary', 'threaded')
