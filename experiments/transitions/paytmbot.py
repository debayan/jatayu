#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

import telegram
from telegram.ext import Updater
from PaytmBrain import PaytmBrain

paytmbrains = {} 
bot = telegram.Bot(token='219102194:AAGqRz7GPtCCZJRQtVaJkdVItzor5xNR9Zc')
updater = Updater(token='219102194:AAGqRz7GPtCCZJRQtVaJkdVItzor5xNR9Zc')
dispatcher = updater.dispatcher


def respond(bot, update):
  p = None
  if update.message.chat_id in paytmbrains:
      p = paytmbrains[update.message.chat_id]
  else:
      paytmbrains[update.message.chat_id] = PaytmBrain(update.message.chat.first_name)
      p =  paytmbrains[update.message.chat_id]
  reply = []
  p.process(update.message.text, reply)
  bot.sendMessage(chat_id=update.message.chat_id, text=reply[0])

def unknown(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

print bot.getMe()

dispatcher.addTelegramMessageHandler(respond)
dispatcher.addUnknownTelegramCommandHandler(unknown)

updater.start_polling()
