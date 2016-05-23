#!/usr/bin/python

import os,sys,argparse,logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from TelegramBot import TelegramBot
#from Adapters import facebookadapter,telegramadapter
#from Parser import Parser
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


parser = argparse.ArgumentParser(description='Start your jatayu bot')
parser.add_argument('chatnetwork',  type=str, help='Options include facebook, telegram')
parser.add_argument('keyslocation', type=str, help='Path to file holding keys to authenticate with the chat network')
parser.add_argument('recipelocation', type=str, help='Path to file holding chat recipe')
args = parser.parse_args()


logger.debug("Received arguments on command line: %s, %s, %s "%(args.chatnetwork, args.keyslocation,args.recipelocation))

b = TelegramBot(logger, args.chatnetwork, args.keyslocation,args.recipelocation)
b.poll()
