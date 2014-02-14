#!/usr/bin/env python

from evsim import ESEngine, ESAgent
import random

################################################################################
class Paxos(ESAgent,object):
  def __init__(self, name, engine):
    super(Paxos,self).__init__(name, engine)
    self.handle('prepare', self.prepare)
    self.handle('prepared', self.prepared)
    self.handle('accept', self.accept)
    self.handle('accepted', self.accepted)
    self.handle('decide', self.decide)

    self['n_p'] = 0
    self['n_l'] = 0
    self['n_a'] = 0
    self['v_a'] = None
    self['chosen'] = None
    self.persist( ['n_p','n_l','n_a','v_a','chosen'] )
  def __str__(self):
    return self.name

  def startup(self,src):
    self['n_o'] = 0
    self['v_o'] = None

  def propose(self,src):
    self['n_p'] = self['n_p'] + 1 + self.id()
    self['a'] = 0
    majority = random.sample( self.agents(), len(self.agents())/2+1 )
    [self.send(agent,'prepare',self['n_p']) for agent in majority]

  def prepare(self,src,n):
    self['n_l'] = max(self['n_l'],n)
    self.send(src,'prepared',self['n_a'],self['v_a'])

  def prepared(self,src,n,v):
    if n>self['n_o']:
      self['n_o'] = n
      self['v_o'] = v
    self['a'] = self['a'] + 1
    if self['a'] == len(self.agents())/2+1:
      if self['v_o'] is None:
        self['v_o'] = random.random()
      self['a'] = 0
      self['n_p'] = max(self['n_p'],self['n_o'])
      majority = random.sample( self.agents(), len(self.agents())/2+1 )
      [self.send(agent,'accept',self['n_p'],self['v_o']) for agent in majority]

  def accept(self,src,n,v):
    if n >= self['n_l']:
      self['n_l'] = self['n_a'] = n
      self['v_a'] = v
    self.send(src,'accepted',self['n_a'])

  def accepted(self,src,n):
    if n == self['n_p']:
      self['a'] = self['a'] + 1
    if self['a'] == len(self.agents())/2+1:
      [self.send(agent,'decide',self['v_o']) for agent in self.agents()]

  def decide(self,src,v):
    self['chosen'] = v

  def tick(self):
    self.send(self,'propose')

  def report(self,src):
    print str(self.name) + ' chose '+str(self['chosen'])

################################################################################
class BadPaxos(ESAgent,object):
  def __init__(self, name, engine):
    super(BadPaxos,self).__init__(name, engine)
    self.handle('prepare', self.prepare)
    self.handle('prepared', self.prepared)
    self.handle('accept', self.accept)
    self.handle('accepted', self.accepted)
    self.handle('decide', self.decide)

    self['n_p'] = 0
    #self['n_l'] = 0  #BADPAXOS
    self['n_a'] = 0
    self['v_a'] = None
    self['chosen'] = None
    self.persist( ['n_p','n_a','v_a','chosen'] ) #BADPAXOS
  def __str__(self):
    return self.name

  def startup(self,src):
    self['n_o'] = 0
    self['v_o'] = None

  def propose(self,src):
    self['n_p'] = self['n_p'] + 1 + self.id()
    self['a'] = 0
    self['n_o'] = 0
    majority = random.sample( self.agents(), len(self.agents())/2+1 )
    [self.send(agent,'prepare',self['n_p']) for agent in majority]

  def prepare(self,src,n):
    self['n_a'] = max(self['n_a'],n) #BADPAXOS
    self.send(src,'prepared',self['n_a'],self['v_a'])

  def prepared(self,src,n,v):
    self['n_o'] = max(self['n_o'],n) #BADPAXOS
    if n==self['n_o'] and v is not None: #BADPAXOS
      self['v_o'] = v
    self['a'] = self['a'] + 1
    if self['a'] == len(self.agents())/2+1:
      if self['v_o'] is None:
        self['v_o'] = random.random()
      self['a'] = 0
      #self['n_p'] = max(self['n_p'],self['n_o']) #BADPAXOS
      majority = random.sample( self.agents(), len(self.agents())/2+1 )
      [self.send(agent,'accept',self['n_p'],self['v_o']) for agent in majority]

  def accept(self,src,n,v):
    if n >= self['n_a']: #BADPAXOS
      self['n_a'] = n #BADPAXOS
      self['v_a'] = v
    self.send(src,'accepted',self['n_a'])

  def accepted(self,src,n):
    if n == self['n_o']: #BADPAXOS
      self['a'] = self['a'] + 1
    if self['a'] == len(self.agents())/2+1:
      [self.send(agent,'decide',self['v_o']) for agent in self.agents()]

  def decide(self,src,v):
    self['chosen'] = v

  def tick(self):
    self.send(self,'propose')

  def report(self,src):
    print str(self.name) + ' chose '+str(self['chosen'])



# Now run the experiment
for Protocol in [Paxos, BadPaxos]:
  random.seed(6)
  e = ESEngine()
  a = Protocol(e,'A')
  b = Protocol(e,'B')
  c = Protocol(e,'C')
  # c -> c/b
  e.schedule(1, None, c, 'propose')
  # delay c's accepts
  e.schedule_control(20, 'set_latency', c, b, 1000)
  e.schedule_control(20, 'set_latency', c, a, 1000)
  # a times out, a -> a/b
  e.schedule_control(100, 'tick', a)
  # a/b resolve, emit decides
  e.schedule(1500, None, a, 'report')
  e.schedule(1500, None, b, 'report')
  e.schedule(1500, None, c, 'report')
  # now c's accepts hit, collide with same ID, different value, emit decides
  e.schedule(2500, None, a, 'report')
  e.schedule(2500, None, b, 'report')
  e.schedule(2500, None, c, 'report')

  # Here, "chosen" means it received a "decide" message with a value.
  # Two constraints violated:
  #   "Only a single value is chosen"
  #   "A process never learns that a value has been chosen unless it actually has been"

  e.verbose=0
  e.run()
  #print ''
  #print 'EVENT LOG:'
  #e.print_event_log()
  print '#'*80
