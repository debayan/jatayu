#!/usr/bin/python

import os,sys,argparse,logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
from src.TelegramBot import TelegramBot
from src.FacebookBot import FacebookBot
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
from flask import Flask,request
app = Flask(__name__)


parser = argparse.ArgumentParser(description='Start your jatayu bot')
parser.add_argument('chatnetwork',  type=str, help='Options include facebook, telegram')
parser.add_argument('keyslocation', type=str, help='Path to file holding keys to authenticate with the chat network')
parser.add_argument('recipelocation', type=str, help='Path to file holding chat recipe')
parser.add_argument('botmodulename', type=str, help='Name of bot module class/file')
args = parser.parse_args()


logger.debug("Received arguments on command line: %s, %s, %s, %s "%(args.chatnetwork, args.keyslocation,args.recipelocation, args.botmodulename))

if args.chatnetwork == 'telegram':
    b = TelegramBot(logger, args.chatnetwork, args.keyslocation, args.recipelocation, args.botmodulename)
    b.poll()
elif args.chatnetwork == 'facebook':
    b = FacebookBot(logger, args.chatnetwork, args.keyslocation, args.recipelocation, args.botmodulename)
    @app.route('/', methods=['POST'])
    def handle():
        try:
            b.respond(request.data)
            return 'ok',200
        except Exception,e:
            logger.error("Facebook bot object error: %s"%e)
            return 'error',500
    app.run(port=8000)
else:
    logger.error('Chatnetwork name not correct, found %s'%args.chatnetwork)
