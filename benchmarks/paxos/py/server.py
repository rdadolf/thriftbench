#!/usr/bin/env python
import sys
sys.path.append('../../py_common/')

import common
from paxos import Paxos

import socket

from paxos_machine import Paxos_Machine

if __name__=='__main__':
  assert len(sys.argv)>1, 'Usage: server.py <port>'
  fqdn = socket.getfqdn()
  port = sys.argv[1]

  processor = Paxos.Processor( Paxos_Machine(name='PaxMach:'+str(fqdn)+':'+str(port)) )
  common.init_and_run_forever(processor, port, 'framed', 'binary', 'threaded')
