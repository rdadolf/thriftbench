import sys
sys.path.append('../../py_common/')

import common
from protocol import Null

class Handler:
    def identity(self, i):
        return i

    def oneway_test(self, i):
        pass


processor = Null.Processor(Handler())
port = 38003
prot_type = sys.argv[1] if len(sys.argv) > 1 else 'binary'

if __name__ == '__main__':
    print "Listening on %d" % port
    common.init_and_run_forever(processor, port, 'buffered', prot_type, 'threaded')
