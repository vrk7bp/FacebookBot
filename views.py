# This is the "proxy" for the bot web server. This is where both verfication and post requests come in, and are then routed to other files/methods accordingly.

from flask import Flask
from datetime import datetime
from flask import render_template
from flask import redirect
from flask import request

import constants # constants.py, where your own verification and page_token should be defined
import messageHandler # messageHandler.py, where methods for dealing with "message" post requests are found

application = Flask(__name__)

# Endpoint for verification, and html result when people hit the URL
@application.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == constants.VERIFY_TOKEN:
            print "Bad Verification" #logging
            return "Verification token mismatch", 403
        print "Good Verification" #logging
        return request.args["hub.challenge"], 200

    # Code that runs if someone simply navigated to the URL via a browser
    print "Someone accessed the home page" #logging
    return "Hello world", 200

#Endpoint that is hit when Facebook sends a "request" to the bot
@application.route('/', methods=['POST'])
def webhook():

    data = request.get_json()

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("optin"):  # optin confirmation
                   receivedAuthentication()

                elif messaging_event.get("message"):  # someone sent us a message
                   receivedMessage(messaging_event)

                elif messaging_event.get("delivery"):  # delivery confirmation
                   receivedDeliveryConfirmation()

                elif messaging_event.get("read"):  # confirmation that someone sent us a message
                   receivedRead(messaging_event)

                elif messaging_event.get("postback"): # user clicked button that resulted in postback
                   receivedPostback(messaging_event)
                else:
                   print "Unknown messaging event received: " + str(messaging_event)

    return "ok", 200

# Authentication Handler
def receivedAuthentication():
    print "Received authentication" #logging

# Message Received Handler
def receivedMessage(messaging_event):
    messageHandler.receivedMessage(messaging_event)

# Delivery Confirmation Handler
def receivedDeliveryConfirmation():
    print "Received delivery confirmation" #logging

# Receive Handler
def receivedRead(message_event):
    print "Sequence number " + str(message_event["read"]["seq"]) + " was read by user " + str(message_event["sender"]["id"])  #logging 

# Postback Handler
def receivedPostback(message_event):
    print "Got back a postback, the payload was: " + str(message_event["postback"]["payload"]) #logging
    messageHandler.sendTextMessage(message_event["sender"]["id"], "Got your postback")

if __name__ == "__main__":
    application.run(host='0.0.0.0')
