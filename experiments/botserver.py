#!/usr/bin/python

import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

import telegram
from telegram.ext import Updater

bot = telegram.Bot(token='204971482:AAGmYTur90DJBtn-G_MUaMN1ugCUYBI8Mqs')
updater = Updater(token='204971482:AAGmYTur90DJBtn-G_MUaMN1ugCUYBI8Mqs')
dispatcher = updater.dispatcher


def echo(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text='Jatayu says '+update.message.text)

def unknown(bot, update):
  bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")



print bot.getMe()

dispatcher.addTelegramMessageHandler(echo)
dispatcher.addUnknownTelegramCommandHandler(unknown)

updater.start_polling()
