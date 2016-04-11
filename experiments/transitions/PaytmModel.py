class Model(object):
    def __init__(self):
        self._intent = None #topup, bus ticket, movie
        self._number = None #mobile number, dth id etc
        self._amount = None
        self.valid_intents = ['mobile', 'landline', 'dth', 'metro', 'electricity', 'datacard', 'gas', 'education', 'insurance']
    def ask_number(self, text=None,reply=[]):
        reply.append("Hi, what is your %s number?"%self._intent)

    def ask_number_clarify(self,text=None,reply=[]):
        reply.append("You need to enter a  valid %s number. Any number greater than 5 digits will do for this demonstration."%self._intent)

    def ask_amount(self,text=None,reply=[]):
        reply.append("What amount of topup do you want?")

    def ask_amount_clarify(self,text=None,reply=[]):
        reply.append("You need to enter a valid topup amount.")

    def ask_confirmation(self,text=None,reply=[]):
        reply.append("We are about to do a %s topup worth Rs %d for %d, please confirm (yes/no)."%(self._intent, self._amount, self._number))

    def ask_confirmation_clarify(self,text=None,reply=[]):
        reply.append("Please type yes or no.")

    def ask_intent(self, text=None,reply=[]):
        reply.append('Hi, what do you want to do today?')
   
    def ask_intent_clarify(self,text=None,reply=[]):
        reply.append("We currently allow following topups: %s"%(','.join(self.valid_intents)))

    def involve_human(self,text=None,reply=[]):
        reply.append("We failed to understand your request. In future versions we will involve a human agent. For now, try typing something again.")
        self.back_to_begin()

    def do_topup(self,text=None,reply=[]):
        reply.append("Topup is done")
        self.back_to_begin()


    def has_intent(self, text=None,reply=[]):
        for intent in self.valid_intents:
            if intent in text.lower():
                self._intent = intent
                return True
        return False
         

    def yes(self, text=None,reply=[]):
        if 'yes' in text.lower():
            print text
            return True
        else:
            return False

    def no(self, text=None,reply=[]):
        if 'no' in text.lower():
            return True
        else:
            return False

    def yesorno(self, text=None,reply=[]):
        if 'no' in text or 'yes' in text:
            return True
        else:
            return False

    def has_valid_number(self, text=None,reply=[]):
        for word in text.split(' '):
            if len(word) > 5 and word.isdigit():
                self._number = int(word)
                return True
        else:
            return False
    def has_topup_amount(self, text=None,reply=[]):
        for word in text.split(' '):
            if word.isdigit():
                if float(word) > 0 and float(word) < 1000:
                    self._amount = int(word)
                    return True
        return False
