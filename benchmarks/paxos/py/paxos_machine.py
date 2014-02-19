# Paxos State Machine

import sys
sys.path.append('../../py_common')

import random

import common
import paxos
import paxos.ttypes

import struct

SENTINEL = -1

class Paxos_Machine:
  def __init__(self, persisted_state=None, agent_list=[], name=None, rounds=1):
    self.rounds = rounds
    if name is None:
      self.name = 'Paxos_Machine_'+str(random.randint(0,1000000))
    else:
      self.name = name

    # Must have an agent list if we're a proposer:
    # [ (hostname1,port1), (hostname2,port2), ... ]
    self.agents = map(self.rpc_init, agent_list)

    if persisted_state is not None:
      self.state = persisted_state
      # "volatile" state
      self.state['n_o'] = 0
      self.state['v_o'] = None
    else:
      self.state_init()

    #print name+' is alive'

  def state_init(self): # self.state
    self.target_value = SENTINEL
    self.state = dict()
    # "persistent" state
    self.state['n_p'] = 0
    self.state['n_l'] = 0
    self.state['n_a'] = 0
    self.state['v_a'] = SENTINEL
    self.state['chosen'] = None
    # "volatile" state
    self.state['n_o'] = 0
    self.state['v_o'] = SENTINEL

  def rpc_init(self,name_and_port):
    (name,port) = name_and_port
    # Setup RPC connection
    self.transport = common.get_transport(name,port,framed=True)
    self.protocol = common.get_protocol(self.transport, 'binary')
    return paxos.Paxos.Client(self.protocol)

  def iterate(self,n=None):
    if n is None:
      n = self.rounds
    self.state_init()
    for i in xrange(0,n):
      self.propose(100+i)
      self.state_init()
    #print 'Done'

  # STATE MACHINE METHODS
  def propose(self,target_value = SENTINEL):
    self.target_value = target_value
    #print '['+self.name+']: propose()'
    self.state['n_p'] = self.state['n_p'] + 1 + hash(self.name)&(2147483648-1)
    self.state['a'] = 0
    majority = random.sample( self.agents, len(self.agents)/2+1 )
    responses = [agent.prepare(self.state['n_p']) for agent in majority]
    map( self.prepared, responses )

  def prepare(self, args):
    n = args
    #print '['+self.name+']: prepare('+str(n)+')'
    self.state['n_l'] = max(self.state['n_l'], n)
    return paxos.ttypes.prepare_t(n=self.state['n_a'], v=self.state['v_a'])

  def prepared(self, args):
    n = args.n
    v = args.v
    #print '['+self.name+']: prepared('+str(n)+','+str(v)+')'
    # If we receive a newer proposal value, update it
    if n>self.state['n_o']:
      self.state['n_o'] = n
      self.state['v_o'] = v
    # Update our receiver counts
    self.state['a'] = self.state['a']+1
    # 
    if self.state['a'] == len(self.agents)/2+1:
      if self.state['v_o'] == SENTINEL:
        self.state['v_o'] = self.target_value
      self.state['a'] = 0 # Is this fragile? (must match sent PREPARE's with received PREPARED's or we can get really messed up)
      self.state['n_p'] = max(self.state['n_p'], self.state['n_o'])
      majority = random.sample( self.agents, len(self.agents)/2+1 )
      responses = [agent.accept(paxos.ttypes.accept_t(self.state['n_p'],self.state['v_o'])) for agent in majority]
      #print responses
      map( self.accepted, responses )

  def accept(self, args):
    n = args.n
    v = args.v
    #print '['+self.name+']: accept('+str(n)+','+str(v)+')'
    if n >= self.state['n_l']:
      self.state['n_l'] = self.state['n_a'] = n
      self.state['v_a'] = v
    return self.state['n_a'] # send accepted(n_a)

  def accepted(self, args):
    n = args
    #print '['+self.name+']: accepted('+str(n)+')'
    if n == self.state['n_p']:
      self.state['a'] = self.state['a']+1
    if self.state['a'] == len(self.agents)/2+1:
      #print 'DECIDING ON '+str(self.state['v_o'])
      self.chosen = self.state['v_o'] # We know we we're done.
      [agent.decide(self.state['v_o']) for agent in self.agents]
    return True

  def decide(self, args):
    v = args
    #print '['+self.name+']: decided('+str(v)+')'
    self.state['chosen'] = v
    self.state_init() # reset and prepare for next round
    
