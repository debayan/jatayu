#!/usr/bin/python

import json
from Parse import Parse

class GenericBot:
    def __init__(self, logger, recipelocation, botmodulename):
        self.logger = logger
        self.recipelocation = recipelocation
        self.botmodulename = botmodulename
        self.loadrecipe()
        self.bot_brain = Parse(self.recipe_dict, self.logger, self.botmodulename)
        try:
            self.bot_brain.buildMachine()
        except Exception,e:
            self.logger.error("Generic bot error: %s"%e)
            return

    def loadrecipe(self):
        recipe_dict = {}
        try:
            f = open(self.recipelocation)
            s = f.read()
            f.close()
        except Exception,e:
            self.logger.error("Could not load recipe from %s"%self.recipelocation)
            sys.exit(1)
        try:
            self.recipe_dict = json.loads(s)
        except Exception,e:
            self.logger.error("Could not parse recipe json %s"%e)
            sys.exit(1)
    
    def respond(self, message_text, reply=[]):
        self.logger.debug("Received: %s"%message_text)
        if len(message_text) > 0:
            reply = []
            self.bot_brain.decide(message_text, reply)
            return reply[0]
