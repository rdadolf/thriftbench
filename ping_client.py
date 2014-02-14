#!/usr/bin/env python

from ping import Ping
#from ping.ttypes import * # Do I need this?

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:
  transport = TSocket.TSocket('localhost', 9001)
  transport = TTransport.TBufferedTransport(transport)
  protocol = TBinaryProtocol.TBinaryProtocol(transport)
  client = Ping.Client(protocol)

  transport.open()
 
  # Time N consecutive ping requests.
  for i in xrange(0,10):
    client.ping()
 
  transport.close()
 
except Thrift.TException, tx:
  print "%s" % (tx.message)
