import sys
sys.path.append('../../py_common/')

import common
from protocol import Null


prot_type = sys.argv[1] if len(sys.argv) > 1 else 'binary'


transport = common.get_transport('localhost', 38003)
protocol = common.get_protocol(transport, prot_type)
client = Null.Client(protocol)

print client.identity(3)

transport.close()
