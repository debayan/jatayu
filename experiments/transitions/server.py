from flask import Flask,request
import json
import urllib
import urllib2
from PaytmBrain import PaytmBrain
app = Flask(__name__)

paytmbrains = {}

def respond(sender_id, reply):
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=CAASZAZBFkr3g4BAC6ayWC131DgcykWltthWkx2r2WBTR2akWCzR3zuVvbK8LsTqZCzYNCsJOBuhik7umvrKIEhU8BT34TDXbohZAt3ZBvAxGJOdAp9i2QpOM8cat0QsXVSHazm46oT7f6DZBeZBanWg3lRMshIJIfj5xDxxZB7Qv9zWxcxTZAm9lAiAPcUSByWOYJGZA2hZCxpbLQZDZD'
    values = {
      "recipient": {"id": sender_id},
      "message": {"text": reply},
    }
    print "Sending: %s"%values
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

@app.route('/', methods=['POST'])
def handle():
    message_text = ''
    p = None
    sender_id = None
    try:
        data = json.loads(request.data)
        message_text = data["entry"][0]["messaging"][0]["message"]["text"]
        sender_id = data["entry"][0]["messaging"][0]["sender"]["id"]
        if sender_id in paytmbrains:
            p = paytmbrains[sender_id]
        else:
            paytmbrains[sender_id] = PaytmBrain('')
            p =  paytmbrains[sender_id]
    except Exception,e:
        print e
    print "Received: %s"%message_text
    if len(message_text) > 0:
        reply = []
        p.process(message_text, reply)
        respond(sender_id, reply[0])
    return 'ok',200

if __name__ == '__main__':
    app.run(port=8000)

