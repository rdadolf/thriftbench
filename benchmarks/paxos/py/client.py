#!/usr/bin/env python
import sys
sys.path.append('../../py_common')

import common
from paxos import Paxos

from paxos_machine import Paxos_Machine

import time

if __name__=='__main__':
  assert len(sys.argv)>1, 'Usage client.py <host:port> [ host2:port2, ...]'
  agent_list = [(host,int(port)) for (host,port) in map(lambda s:s.split(':'), sys.argv[1:]) ]
  PaxMach = Paxos_Machine(agent_list=agent_list, name='PaxMach:Proposer')

  n = 1000
  t0 = time.time()
  PaxMach.iterate(n)
  t1 = time.time()
  print 'Time for '+str(n)+' rounds of Paxos: '+str(t1-t0)
