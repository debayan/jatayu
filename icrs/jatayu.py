#!/usr/bin/env python

import aiml
import sys

reload(sys)
sys.setdefaultencoding('utf8')

k = aiml.Kernel()
k.learn("./calendar.aiml")
while True: print k.respond(raw_input(">> "))
