#!/usr/bin/python

import logging, sys
from transitions.extensions import MachineGraphSupport as Machine
from transitions import logger
from PaytmModel import Model
logger.setLevel(logging.DEBUG)

class DecisionMaker():
    def __init__(self, model, machine):
        self.model = model
        self.transitions = machine.get_transitions()

    def try_all_transitions(self, text, reply):
        currentState = self.model.state
        for arr in self.transitions:
            if arr[1] == currentState:
                try:
                    getattr(self.model, arr[0])(text,reply)
                except Exception,e:
                    print e


    def decide(self, text, reply):
        self.try_all_transitions(text, reply)

class PaytmBrain():
    def __init__(self):
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
        
        machine.add_transition('begin_to_confirmation_direct', 'Begin', 'Confirm', conditions=['has_phone_number','has_topup_amount'])
        machine.add_transition('start', 'Begin', 'ExpectNumber', unless=["has_phone_number"])
        #machine.add_transition('got_intent', 'AskIntent','ExpectNumber', conditions=['has_intent'])
        #machine.add_transition('confusing_intent', 'AskIntent', 'InvolveHuman', unless=['has_intent'])
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
        machine.add_transition('back_to_begin', 'InvolveHuman', 'Begin')
        machine.add_transition('topup_back_to_begin', 'DoTopup', 'Begin')
        machine.draw_graph_now()
        machine.graph.draw('my_state_diagram.png', prog='dot')
        self.d = DecisionMaker(model,machine)
      
    def process(self, text, reply):
        return self.d.decide(text, reply)   


if __name__ == '__main__':
    p = PaytmBrain()
    while True:
        text = raw_input(': ')
        reply = []
        p.process(text, reply)
        print reply[0]
