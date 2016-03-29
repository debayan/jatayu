#!/usr/bin/env python

import aiml
import sys

reload(sys)
sys.setdefaultencoding('utf8')

k = aiml.Kernel()
k.learn("./calendar.aiml")
#k._maxRecursionDepth = 1000
while True: print k.respond(raw_input(">> "))
