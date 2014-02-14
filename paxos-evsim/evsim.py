#!/usr/bin/env python

import operator
import random

class ESEngine(object):
  def __init__(self):
    self.t = -1
    self.Q = []
    self.log = []
    self.set_alarm_interval(10000)
    self.agents = []
    self.set_failures(0)
    self.verbose = 0
    self.links = dict() # added latency, -1 = infinite latency/fail, 

  def run(self):
    # Init links
    for agent in self.agents:
      self.links[agent.name] = dict([(a.name,10) for a in self.agents])

    # Init agents
    for agent in self.agents:
      agent.boot()

    watchdog = self.alarm_interval
    if self.verbose>1:
      print watchdog
      print '[Q@'+str(self.t)+'] ('+', '.join([str(t)+'|'+str(s)+'>'+str(d)+'|'+str(m) for (t,e,s,d,m,_) in self.Q])+')'
    # Run event loop
    while( len(self.Q)>0 ):
      if( self.Q[0][0] < watchdog ):
        if self.verbose>1:
          print watchdog
          print '[Q@'+str(self.Q[0][0])+'] ('+', '.join([str(t)+'|'+str(s)+'>'+str(d)+'|'+str(m) for (t,e,s,d,m,_) in self.Q])+')'
        self.step()
      else:
        print '[@'+str(watchdog)+'] Watchdog timer event'
        self.t = watchdog
        watchdog += self.alarm_interval
        for agent in self.agents:
          if agent.on:
            agent.tick()
    if self.verbose>1:
      print '[Q@'+str(self.t+1)+']'

    # Shutdown agents
    for agent in self.agents:
      agent.halt()

  def step(self):
    evtype = self.Q[0][1]
    self.t = t = self.Q[0][0]
    # Control event
    if evtype=='ctl':
      (t,e,action,args) = self.Q[0]
      if action=='agent_down':
        (agent,) = args
        assert agent.on==True, 'Attempted to halt a dead agent'
        agent.halt()
      elif action=='link_down':
        (src,dst) = args
        self.links[src.name][dst.name] = -abs(self.links[src.name][dst.name])
      elif action=='agent_up':
        (agent,) = args
        assert agent.on==False, 'Attempted to boot a live agent'
        agent.boot()
      elif action=='link_up':
        (src,dst) = args
        self.links[src.name][dst.name] = abs(self.links[src.name][dst.name])
      elif action=='tick':
        (agent,) = args
        if agent.on:
          agent.tick()
      elif action=='set_latency':
        (src,dst,val) = args
        self.links[src.name][dst.name] = val
    # Message event
    elif evtype=='msg':
      (t,e,src,dst,meth,args) = self.Q[0]
      log_message = '[@'+str(t)+']: '+str(src)+'>'+str(dst)+'|'+str(meth)+' ('+','.join(map(str,args))+')'
      # BADPAXOS DEBUG
      if False:
        for agent in self.agents:
          if 'n_a' in agent:
            print str(agent.name)+'[n_a]='+str(agent['n_a'])
          if 'n_l' in agent:
            print str(agent.name)+'[n_l]='+str(agent['n_l'])
      # END
      self.log.append( log_message )
      if self.verbose>0:
        print log_message
      assert meth in dir(dst)
      if dst.on:
        dst.__getattribute__(meth)(src,*args)
      else:
        print str(meth) + ' event missed while '+str(dst.name)+' halted.'
    self.Q = self.Q[1:]

  def schedule(self,time,src,dst,function,*args):
    self.Q.append( (time,'msg',src,dst,function,args) )
    self.Q.sort(key=operator.itemgetter(0))

  def schedule_control(self,time,action,*args):
    self.Q.append( (time,'ctl',action,args) )
    self.Q.sort(key=operator.itemgetter(0))

  def send(self,src,dst,method,*args):
    if self.links[src.name][dst.name]>=0:
      self.schedule(self.t+self.links[src.name][dst.name], src, dst, method, *args)
    else:
      if self.verbose>1:
        print 'Dropped '+str(method)+' message from '+str(src)+' to '+str(dst)

  def set_alarm_interval(self,ticks):
    self.alarm_interval = ticks
    return True
  def failures(self):
    self.f = value
  def set_failures(self,value):
    self.f = value

  def print_event_log(self):
    for ev in self.log:
      print ev
    pass


class ESAgent(dict):
  def __init__(self, engine, name):
    self.engine = engine
    self.name = name
    self.engine.agents.append(self)
    self.persistance = []
    self.on = False
  def id(self):
    return (hash(self.name)%100) # Bad. Just pray.
  def agents(self):
    return self.engine.agents
  def persist(self,names):
    self.persistance = names
  def boot(self):
    self.on = True
    self.startup(self) # from ourselves
  def halt(self):
    self.shutdown(self) # from ourselves
    for victim in [e for e in self if e not in self.persistance]:
      del self[victim]
    self.on = False
  def send(self, dest, mtype, *mdata):
    self.engine.send(self,dest,mtype,*mdata) # src==self, it's not a mistake
  def handle(self, mtype, handler):
    pass
  def __str__(self):
    return '<ESAgent '+self.name+'>'
  ### Override these if desired:
  def tick(self): # called every engine.alarm_interval ticks
    pass
  def startup(self,src):
    pass
  def shutdown(self,src):
    pass
