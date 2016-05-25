class TopupModel(object):
    dc = {}
    def __init__(self, logger):
        self.logger = logger
        self.name = 'Jack'
    
    def ifyesno(self, stt, text=None, reply=[]):
        if text.lower() == 'yes' or text.lower() == 'no':
            return True
        else:
            return False

    def ifyes(self, stt, text=None, reply=[]):
        if text.lower() == 'yes':
            return True
        else:
            return False

    def ifno(self, stt, text=None, reply=[]):
        if text.lower() == 'no':
            return True
        else:
            return False

    def ifhasnumber(self, stt, text=None, reply=[]):
        if text.isdigit():
            if len(text) == 10:
                self.mobilenumber = int(text)
                return True
        self.logger.debug("Did not find a number in %s"%text)
        return False

    def ifhasamount(self, stt, text=None, reply=[]):
        if text.isdigit():
           if len(text) > 0:
               self.topupamount = int(text)
               return True
        self.logger.debug("Did not find valid amount in %s"%text)
        return False

    def ifconfirm(self, stt, text=None, reply=[]):
        if text.lower() == 'yes' or text.lower() == 'no':
            return True
        else:
            self.logger.debug("Did not find confirmation in %s"%text)
            return False
   
    def testfunc(self, stt, text=None, reply=[]):
        print "Entered testfunc"
