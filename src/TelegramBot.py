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

import os,sys,ConfigParser,json
import telegram
from telegram.ext import Updater
from Parse import Parse
from GenericBot import GenericBot

class TelegramBot(GenericBot):
    def __init__(self, logger, chatnetwork, keyslocation, recipelocation, botmodulename, draw):
        GenericBot.__init__(self, logger, recipelocation, botmodulename, draw)
        self.brains = {}
        self.chatnetwork = chatnetwork
        self.keyslocation = keyslocation

        self.connect()
        self.loadrecipe()

    def connect(self):
        config = ConfigParser.ConfigParser()
        if self.chatnetwork == 'telegram':
            try:
                config.read(self.keyslocation)
                self.telegram_access_token = config.get('telegram','access_token')
                self.logger.debug("Successfully read access keys")
            except Exception,e:
                self.logger.error("Could not read access keys: %s"%e)
                sys.exit(1)
            try:
                self.telegram_bot = telegram.Bot(token=self.telegram_access_token)
                self.telegram_updater = Updater(token=self.telegram_access_token)
                self.telegram_dispatcher = self.telegram_updater.dispatcher
                self.telegram_dispatcher.addTelegramMessageHandler(self.respond)
            except Exception,e:
                self.logger.error("Telegram bot connect failed: %s"%e)
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
    
    def respond(self, bot, update):
        bot_brain = None
        if update.message.chat_id in self.brains:
            bot_brain = self.brains[update.message.chat_id]
        else:
            self.brains[update.message.chat_id] = Parse(self.recipe_dict, self.logger, self.botmodulename)
            bot_brain =  self.brains[update.message.chat_id]
            bot_brain.buildMachine()
        reply = []
        bot_brain.decide(update.message.text, reply)
        bot.sendMessage(chat_id=update.message.chat_id, text=reply[0])
        self.logger.debug("Message received from %s: %s \n Reply sent: %s"%(update.message.chat_id, update.message.text, reply[0]))
              
    def poll(self):
        self.logger.info("Starting telegram bot poll")
        self.telegram_updater.start_polling()
