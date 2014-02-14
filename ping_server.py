#!/usr/bin/env python

from ping import Ping
import sys

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

class PingServer:
  def __init__(self):
    pass

  def ping(self):
    pass


handler = PingServer()
processor = Ping.Processor(handler)
transport = TSocket.TServerSocket('localhost',9001)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print 'python ping server up'
try:
  server.serve()
except KeyboardInterrupt:
  print ''
  print 'python ping server down'
  sys.exit(0)
