class Model(object):
    def __init__(self):
        self._command = None #topup, bus ticket, movie
        self._topupnumber = None #mobile number, dth id etc
        self._userid = None
        self._amount = None
        self._topuptype = None #mobile,dth,metro etc
        self._topupsubtype = None #prepaid/postpaid
    def ask_number(self, text, reply):
        reply.append("Hi, what is your number?")

    def ask_number_clarify(self,text, reply):
        reply.append("You need to enter a 10 digit valid Indian phone number.")

    def ask_amount(self,text, reply):
        reply.append("What amount of topup do you want?")

    def ask_amount_clarify(self,text, reply):
        reply.append("You need to enter a valid topup amount.")

    def ask_confirmation(self,text, reply):
        reply.append("We are about to do a %d topup of %d, please confirm (yes/no)."%(self._amount, self._number))

    def ask_confirmation_clarify(self,text, reply):
        reply.append("Please type yes or no.")

    def involve_human(self,text, reply):
        reply.append("We failed to understand your request. Involving a human agent, please wait ....")
        self.back_to_begin()

    def do_topup(self,text, reply):
        reply.append("Topup is done")
        self.topup_back_to_begin()

    def yes(self, text, reply):
        if 'yes' in text.lower():
            print text
            return True
        else:
            return False

    def no(self, text, reply):
        if 'no' in text.lower():
            return True
        else:
            return False

    def yesorno(self, text, reply):
        if 'no' in text or 'yes' in text:
            return True
        else:
            return False

    def has_phone_number(self, text, reply):
        for word in text.split(' '):
            if len(word) == 10 and word.isdigit():
                self._number = int(word)
                return True
        else:
            return False
    def has_topup_amount(self, text, reply):
        for word in text.split(' '):
            if word.isdigit():
                if float(word) > 0 and float(word) < 1000:
                    self._amount = int(word)
                    return True
        return False
