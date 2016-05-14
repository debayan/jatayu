#!/usr/bin/python

import json
import sys, os
from transitions import Machine
import logging
from types import MethodType
import inspect
from transitions import logger
from Model import Model
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

class Parse():
    def __init__(self, document, logger):
        self.document = document
        self.logger = logger
        self.model = None
        self.machine = None
        self.transitions = None
        self.text = {}
        
    def createVariables(self):
        for variable in self.document["variables"]:
            self.logger.debug("Setting variable %s"%variable)
            setattr(Model, variable, 0)

    def createStates(self):
        self.states = []
        for state in self.document["states"]:
            self.logger.debug("Setting state %s"%state["name"])
            self.states.append(state["name"])

    def instantiateModel(self):
        self.model = Model(self.logger)
        #print inspect.getmembers(self.model)
  
    def instantiateMachine(self):
         self.machine = Machine(self.model, self.states, initial=self.states[0],ignore_invalid_triggers=False, auto_transitions=False)

    def createTransitions(self):
        for transition in self.document["transitions"]:
            src = transition[0]
            dst = transition[1]
            conds = transition[2]
            self.logger.debug("Adding transition from %s to %s on condition %s"%(src,dst,conds))
            conditions_array = []
            unless_array = []
            for cond in conds:
                if '!' in cond:
                    unless_array.append(cond[1:])
                else:
                    conditions_array.append(cond)
            self.logger.debug("Adding conditions %s and unless %s"%(conditions_array, unless_array))
            self.machine.add_transition('condition_%s_%s'%(src,dst),src,dst,conditions=conditions_array, unless=unless_array)
        self.transitions = self.machine.get_transitions()

    def createModelFunctions(self):
        for state in self.document["states"]:
            if state.has_key('on_enter_say'):
                self.model.dc[state['name']] = state['on_enter_say']
                def f(cls, stt, text=None, reply=[]):
                    print "state = %s"%stt
                    reply.append(cls.dc[stt])
                setattr(Model, str('say_'+state['name']), classmethod(f))
                self.logger.debug("Adding %s() to Model"%('say_'+state['name']))
            if state.has_key('on_enter_call'):
                def f(cls, text=None,reply=[]):
                    pass
                setattr(Model, str(state['on_enter_call']), classmethod(f))
            if state.has_key('on_exit_call'):
                def f(cls, text=None,reply=[]):
                    pass
                setattr(Model, str(state['on_exit_call']), classmethod(f))
      
           
    def bindFunctions(self):
        for state in self.document["states"]:
            if state.has_key('on_enter_say'):
                self.logger.debug("Binding %s with %s"%('on_enter_%s'%state['name'], 'say_'+state['name']))
                getattr(self.machine, 'on_enter_%s'%state['name'])('say_'+state['name'])
            if state.has_key('on_enter_call'):
                self.logger.debug("Binding %s with %s"%('on_enter_%s'%state['name'], state['on_enter_call']))
                getattr(self.machine, 'on_enter_%s'%state['name'])(state['on_enter_call'])
            if state.has_key('on_exit_call'):
                self.logger.debug("Binding %s with %s"%('on_exit_%s'%state['name'], state['on_exit_call']))
                getattr(self.machine, 'on_exit_%s'%state['name'])(state['on_exit_call'])


    def printModel(self):
        print '''class Model(object):'''
        

    def buildMachine(self):
        self.createVariables()
        self.createStates()
        self.instantiateModel()
        self.createModelFunctions()
        self.instantiateMachine()
        self.createTransitions()
        self.bindFunctions()
        self.printModel()


    def try_all_transitions(self, text, reply):
        currentState = self.model.state
        for arr in self.transitions:
            if arr[1] == currentState:
                try:
                    print arr
                    print getattr(self.model, arr[0])(arr[2],text,reply)
                except Exception,e:
                    print e


    def decide(self, text, reply):
        if 'cancel' in text.lower():
            self.model.cancel()
        self.try_all_transitions(text, reply)
 

if __name__ == '__main__' :
    f = open(sys.argv[1])
    s = f.read()
    f.close()
    try:
        d = json.loads(s)
    except Exception,e:
        print "Could not parse json %s"%e
        sys.exit(1)
    p = Parse(d, logger)
    p.buildMachine()
    while True:
        text = raw_input(': ')
        reply = []
        p.decide(text, reply)
        print reply[0]
