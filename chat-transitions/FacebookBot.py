#!/usr/bin/python

import json, urllib, urllib2, ConfigParser
from Parse import Parse

class FacebookBot:
    def __init__(self, logger, chatnetwork, keyslocation, recipelocation):
        self.brains = {}
        self.logger = logger
        self.chatnetwork = chatnetwork
        self.keyslocation = keyslocation
        self.recipelocation = recipelocation
        self.loadtoken()
        self.loadrecipe()

    def loadtoken(self):
        config = ConfigParser.ConfigParser()
        if self.chatnetwork == 'facebook':
            try:
                config.read(self.keyslocation)
                self.facebook_access_token = config.get('facebook','access_token')
                self.logger.debug("Successfully read access keys")
            except Exception,e:
                self.logger.error("Could not read access keys: %s"%e)
                sys.exit(1)
        else:
            self.logger.error('Chatnetwork name not correct, found %s'%self.chatnetwork)
            return -1

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

    def respond(self, request_data):
        message_text = ''
        bot_brain = None
        sender_id = None
        try:
            data = json.loads(request_data)
            message_text = data["entry"][0]["messaging"][0]["message"]["text"]
            sender_id = data["entry"][0]["messaging"][0]["sender"]["id"]
            if sender_id in self.brains:
                bot_brain = self.brains[sender_id]
            else:
                self.brains[sender_id] = Parse(self.recipe_dict, self.logger)
                bot_brain =  self.brains[sender_id]
                bot_brain.buildMachine()
        except Exception,e:
            self.logger.error("Facebook bot error: %s"%e)
        self.logger.debug("Received: %s"%message_text)
        if len(message_text) > 0:
            reply = []
            bot_brain.decide(message_text, reply)
            self.send(sender_id, reply[0])

    def send(self, sender_id, reply):
        url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%self.facebook_access_token
        values = {
          "recipient": {"id": int(sender_id)},
          "message": {"text": reply},
        }
        self.logger.debug("Sending: %s"%values)
        data = urllib.urlencode(values)
        req = urllib2.Request(url, data)
        try:
            response = urllib2.urlopen(req)
        except Exception,e:
            self.logger.error("Facebook send error: %s"%e)
        
    


