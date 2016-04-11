#!/usr/bin/python

import logging, sys
from transitions.extensions import MachineGraphSupport as Machine
#from transitions import Machine
from transitions import logger
from PaytmModel import Model
logger.setLevel(logging.DEBUG)

class DecisionMaker():
    def __init__(self, model_, machine):
        self.model_ = model_
        self.transitions = machine.get_transitions()

    def try_all_transitions(self, text, reply):
        currentState = self.model_.state
        for arr in self.transitions:
            if arr[1] == currentState:
                try:
                    getattr(self.model_, arr[0])(text,reply)
                except Exception,e:
                    print e


    def decide(self, text, reply):
        self.try_all_transitions(text, reply)

class PaytmBrain():
    def __init__(self):
        states=['Begin', 'AskIntent', 'AskIntentClarify', 'ExpectNumber', 'ExpectNumberClarify', 'ExpectTopupAmount', 'ExpectTopupAmountClarify', 'Confirm', 'ConfirmClarify', 'DoTopup', 'InvolveHuman']

        self.model = Model()
        machine = Machine(self.model, states, initial='Begin', ignore_invalid_triggers=True, auto_transitions=False)
        machine.on_enter_ExpectNumber('ask_number')
        machine.on_enter_ExpectNumberClarify('ask_number_clarify')
        machine.on_enter_AskIntent('ask_intent')
        machine.on_enter_ExpectTopupAmount('ask_amount')
        machine.on_enter_ExpectTopupAmountClarify('ask_amount_clarify')
        machine.on_enter_Confirm('ask_confirmation')
        machine.on_enter_ConfirmClarify('ask_confirmation_clarify')
        machine.on_enter_InvolveHuman('involve_human')
        machine.on_enter_DoTopup('do_topup')
        machine.on_enter_AskIntent('ask_intent')
        machine.on_enter_AskIntentClarify('ask_intent_clarify')
       
        machine.add_transition('start', 'Begin', 'AskIntent') 
        machine.add_transition('_ask_intent_to_confirmation_direct', 'AskIntent', 'Confirm', conditions=['has_intent','has_valid_number','has_topup_amount'])
        machine.add_transition('_ask_intent_confirm', 'AskIntent', 'AskIntentClarify', unless=['has_intent'])
        machine.add_transition('_has_intent', 'AskIntent', 'ExpectNumber', conditions=['has_intent'])
        machine.add_transition('_has_intent_', 'AskIntentClarify', 'ExpectNumber', conditions=['has_intent']) 
        machine.add_transition('no_intent', 'AskIntentClarify', 'InvolveHuman', unless=['has_intent'])
        machine.add_transition('got_phone_number', 'ExpectNumber', 'ExpectTopupAmount', conditions=['has_valid_number'])
        machine.add_transition('repeat_ask_phonenumber', 'ExpectNumber','ExpectNumberClarify',unless=['has_valid_number'])
        machine.add_transition('right_input_phonenumber', 'ExpectNumberClarify', 'ExpectTopupAmount', conditions=['has_valid_number'])
        machine.add_transition('wrong_input_phonenumber', 'ExpectNumberClarify', 'InvolveHuman', unless=['has_valid_number'])
        machine.add_transition('got_topup_amount', 'ExpectTopupAmount', 'Confirm', conditions=['has_topup_amount'])
        machine.add_transition('repeat_topup_amount', 'ExpectTopupAmount', 'ExpectTopupAmountClarify', unless=['has_topup_amount'])
        machine.add_transition('right_input_topup_amount', 'ExpectTopupAmountClarify', 'Confirm', conditions=['has_topup_amount'])
        machine.add_transition('wrong_input_topup_amount', 'ExpectTopupAmountClarify', 'InvolveHuman', unless=['has_topup_amount'])
        
        machine.add_transition('confirmation_yes', 'Confirm', 'DoTopup', conditions=['yes'])
        machine.add_transition('confirmation_no', 'Confirm', 'AskIntent', conditions=['no'])
        machine.add_transition('repeat_confirmation', 'Confirm', 'ConfirmClarify', unless=['yesorno'])
        machine.add_transition('right_input_confirm', 'ConfirmClarify', 'DoTopup', conditions=['yesorno'])
        machine.add_transition('wrong_input_confirm', 'ConfirmClarify', 'Begin', unless=['yesorno'])
        machine.add_transition('back_to_begin', 'InvolveHuman', 'Begin')
        machine.add_transition('back_to_begin', 'DoTopup', 'Begin')
        machine.add_transition('cancel','*','AskIntent')
        machine.draw_graph_now()
        machine.graph.draw('my_state_diagram.png', prog='dot')
        self.d = DecisionMaker(self.model, machine)
      
    def process(self, text, reply):
        if 'cancel' in text.lower():
            self.model.cancel()
        return self.d.decide(text, reply)   


if __name__ == '__main__':
    p = PaytmBrain()
    while True:
        text = raw_input(': ')
        reply = []
        p.process(text, reply)
        print reply[0]
