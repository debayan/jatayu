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

import os,sys,argparse,logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
from src.TelegramBot import TelegramBot
from src.FacebookBot import FacebookBot
from src.GenericBot import GenericBot
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.ERROR)
from flask import Flask,request
app = Flask(__name__)


parser = argparse.ArgumentParser(description='Start your jatayu bot')
parser.add_argument('-n', '--network',  type=str, help='Options include facebook, telegram')
parser.add_argument('-k', '--keys', type=str, help='Path to file holding keys to authenticate with the chat network')
parser.add_argument('-r', '--recipe', type=str, help='Path to file holding chat recipe')
parser.add_argument('-b', '--botmodule', type=str, help='Name of bot module class/file')
parser.add_argument('--cli', action='store_true')
parser.add_argument('--draw', action='store_true')
args = parser.parse_args()


logger.debug("Received arguments on command line: %s, %s, %s, %s, %s "%(args.network, args.keys,args.recipe, args.botmodule, args.cli))

if args.cli:
    b = GenericBot(logger, args.recipe, args.botmodule, args.draw)
    while True:
        text = raw_input(': ')
        reply = []
        print '>'+b.respond(text, reply)
    sys.exit(1)
elif args.network == 'telegram':
    b = TelegramBot(logger, args.network, args.keys, args.recipe, args.botmodule, args.draw)
    b.poll()
elif args.network == 'facebook':
    b = FacebookBot(logger, args.network, args.keys, args.recipe, args.botmodule, args.draw)
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
    logger.error('Chatnetwork name not correct, found %s'%args.network)
