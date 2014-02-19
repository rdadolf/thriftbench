#!/usr/bin/env python

import sys
sys.path.append('../../py_common')

from os import kill
from signal import SIGTERM
from subprocess import Popen
from time import time,sleep

from paxos import Paxos
from paxos_machine import Paxos_Machine

iterations = 100

# Sweep over 2m+1 clients
for m in xrange(1,9):
  enum_port = list(enumerate([str(38000+i) for i in xrange(0,2*m+1)]))
  agents=[Popen('./server.py '+p, shell=True) for (i,p) in enum_port]
  sleep(1)
  try: 
    PaxMach=Paxos_Machine(agent_list=[('localhost',int(p)) for (i,p) in enum_port],name='PaxMach:proposer')

    t0 = time()
    PaxMach.iterate(iterations)
    t1 = time()
    print '[%2d]: %f s' % (2*m+1, t1-t0)
  except Exception, e:
    [kill(agent.pid, SIGTERM) for agent in agents] # Term agents
    raise e, None, sys.exc_traceback # Preserve exception info

  [kill(agent.pid, SIGTERM) for agent in agents]

