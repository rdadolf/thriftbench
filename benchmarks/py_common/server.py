from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.server import TServer


from thrift.protocol import TBinaryProtocol
from thrift.protocol import TCompactProtocol
from thrift.protocol import TJSONProtocol

from thrift.transport import TTransport
from thrift.transport import TZlibTransportFactory

from thrift.server import TNonblockingServer
from thrift.server import TProcessPoolServer
from thrift.server import TServer


# These specify how data gets marshalled
PROTOCOLS = {
    'fast': TBinaryProtocol.TBinaryProtocolAcceleratedFactory,
    'binary': TBinaryProtocol.TBinaryProtocolFactory,
    'compact': TCompactProtocolFactory.TCompactProtocolFactory,
    'json': TJSONProtocol.TJSONProtocolFactory,
}

# These specify how data gets written and read from the socket
TRANSPORTS = {
    'buffered': TTransport.TBufferedTransportFactory,
    'framed': TTransport.TFramedTransportFactory,
    'compressed': TZlibTransport.TZlibTransportFactory,
    # TODO: twisted, tornado
}

# These specify how new connections are handled on the server
SERVERS = {
    'nonblocking': TNonblockingServer.TNonblockingServer,
    'process-pool': TProcessPoolServer.TProcessPoolServer,
    'simple': TServer.TSimpleServer,
    'threaded': TServer.TThreadedServer,
}


def initialize_server(processor, port, trans_type, prot_type, server_type):
    transport = TSocket.TServerSocket(port=port)
    tfactory = TRANSPORTS[trans_type]()
    pfactory = PROTOCOLS[prot_type]()
    server_c = SERVERS[server_type]
    return server_c(processor, transport, tfactory, tfactory, pfactory, pfactory)

