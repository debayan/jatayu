#!/usr/bin/python

import logging, sys
from transitions.extensions import MachineGraphSupport as Machine
from transitions import logger
logger.setLevel(logging.DEBUG)

class DecisionMaker():
    def __init__(self, model, machine):
        self.model = model
        self.transitions = machine.get_transitions()

    def try_all_transitions(self, text):
        currentState = self.model.state
        for arr in self.transitions:
            if arr[1] == currentState:
                try:
                    getattr(self.model, arr[0])(text)
                except Exception,e:
                    print e


    def decide(self, text):
        self.try_all_transitions(text)

class Model(object):
    def __init__(self):
        self._command = None #topup, bus ticket, movie
        self._topupnumber = None #mobile number, dth id etc
        self._userid = None 
        self._amount = None
        self._topuptype = None #mobile,dth,metro etc
        self._topupsubtype = None #prepaid/postpaid
    def ask_number(self,x=None):
        print "Hi, what is your number?"

    def ask_number_clarify(self,x=None):
        print "You need to enter a 10 digit valid Indian phone number."

    def ask_amount(self,x=None):
        print "What amount of topup do you want?"

    def ask_amount_clarify(self,x=None):
        print "You need to enter a valid topup amount."

    def ask_confirmation(self,x=None):
        print "We are about to do a %d topup of %d, please confirm (yes/no)."%(self._amount, self._number)

    def ask_confirmation_clarify(self,x=None):
        print "Please type yes or no."

    def involve_human(self,x=None):
        print "We failed to understand your request. Involving a human agent, please wait ...."

    def do_topup(self,x=None):
        print "Topup is done"

    def yes(self, text):
        if 'yes' in text.lower():
            print text
            return True
        else:
            return False

    def no(self, text):
        if 'no' in text.lower():
            return True
        else:
            return False

    def yesorno(self, text):
        if 'no' in text or 'yes' in text:
            return True
        else:
            return False

    def has_phone_number(self, text):
        for word in text.split(' '):
            if len(word) == 10 and word.isdigit():
                self._number = int(word)
                return True
        else:
            return False
    def has_topup_amount(self, text):
        for word in text.split(' '):
            if word.isdigit():
                if float(word) > 0 and float(word) < 1000:
                    self._amount = int(word)
                    return True
        return False 

states=['Begin', 'AskIntent', 'ExpectNumber', 'ExpectNumberClarify', 'ExpectTopupAmount', 'ExpectTopupAmountClarify', 'Confirm', 'ConfirmClarify', 'DoTopup', 'InvolveHuman', 'End']

model = Model()
machine = Machine(model, states, initial='Begin', ignore_invalid_triggers=True, auto_transitions=False)
machine.on_enter_ExpectNumber('ask_number')
machine.on_enter_ExpectNumberClarify('ask_number_clarify')
machine.on_enter_AskIntent('ask_intent')
machine.on_enter_ExpectTopupAmount('ask_amount')
machine.on_enter_ExpectTopupAmountClarify('ask_amount_clarify')
machine.on_enter_Confirm('ask_confirmation')
machine.on_enter_ConfirmClarify('ask_confirmation_clarify')
machine.on_enter_InvolveHuman('involve_human')
machine.on_enter_DoTopup('do_topup')

machine.add_transition('begin_to_confirmation_direct', 'Begin', 'Confirm', conditions=['has_intent','has_phone_number','has_topup_amount'])
machine.add_transition('start', 'Begin', 'ExpectNumber', unless=["has_phone_number"])
machine.add_transition('got_intent', 'AskIntent','ExpectNumber', conditions=['has_intent'])
machine.add_transition('confusing_intent', 'AskIntent', 'InvolveHuman', unless=['has_intent'])
machine.add_transition('got_phone_number', 'ExpectNumber', 'ExpectTopupAmount', conditions=['has_phone_number'])
machine.add_transition('repeat_ask_phonenumber', 'ExpectNumber','ExpectNumberClarify',unless=['has_phone_number'])
machine.add_transition('right_input_phonenumber', 'ExpectNumberClarify', 'ExpectTopupAmount', conditions=['has_phone_number'])
machine.add_transition('wrong_input_phonenumber', 'ExpectNumberClarify', 'InvolveHuman', unless=['has_phone_number'])
machine.add_transition('got_topup_amount', 'ExpectTopupAmount', 'Confirm', conditions=['has_topup_amount'])
machine.add_transition('repeat_topup_amount', 'ExpectTopupAmount', 'ExpectTopupAmountClarify', unless=['has_topup_amount'])
machine.add_transition('right_input_topup_amount', 'ExpectTopupAmountClarify', 'Confirm', conditions=['has_topup_amount'])
machine.add_transition('wrong_input_topup_amount', 'ExpectTopupAmountClarify', 'InvolveHuman', unless=['has_topup_amount'])

machine.add_transition('confirmation_yes', 'Confirm', 'DoTopup', conditions=['yes'])
machine.add_transition('confirmation_no', 'Confirm', 'ExpectNumber', conditions=['no'])
machine.add_transition('repeat_confirmation', 'Confirm', 'ConfirmClarify', unless=['yesorno'])
machine.add_transition('right_input_confirm', 'ConfirmClarify', 'DoTopup', conditions=['yesorno'])
machine.add_transition('wrong_input_confirm', 'ConfirmClarify', 'InvolveHuman', unless=['yesorno'])
machine.draw_graph_now()
machine.graph.draw('my_state_diagram.png', prog='dot')



d = DecisionMaker(model, machine)

while True:
    text = raw_input(': ')
    d.decide(text)
#    print machine.get_state(model.state).name
