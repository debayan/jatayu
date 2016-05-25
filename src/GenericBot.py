'''
    Copyright 2016 Debayan Banerjee, Shreyank Gupta    

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''


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
