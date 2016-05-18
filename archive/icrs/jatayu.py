#!/usr/bin/env python

import aiml
import sys

from preprocessors import recursively_remove_email

reload(sys)
sys.setdefaultencoding('utf8')

k = aiml.Kernel()
k.learn("./calendar.aiml")
k.setPredicate("user-id", "default")

while True:
    raw = raw_input("C: ")
    o, emails = recursively_remove_email(raw)
    if emails:
        k.setPredicate("emails", ",".join(emails))
    print "R:", k.respond(o)
