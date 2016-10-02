from flask import Flask
from datetime import datetime
from flask import render_template
from flask import redirect
from flask import request

import requests
import json
import constants

application = Flask(__name__)

#Endpoint for verification, and html result when people hit the URL
@application.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == constants.VERIFY_TOKEN:
            return "Verification token mismatch", 403
            print "Bad Verification" #logging
        print "Good Verification" #logging
        return request.args["hub.challenge"], 200

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

                else:
                   print "Unknown messaging event received: " + str(messaging_event)

    return "ok", 200

def receivedMessage(messaging_event):
    print "Received message for user " + str(messaging_event["sender"]["id"]) + " from page " + str(messaging_event["recipient"]["id"]) + " at " + str(messaging_event["timestamp"]) + " with message: " + str(messaging_event["message"]["text"]) + "; SEQ NUM: " + str(messaging_event["message"]["seq"]) #logging
    
    params = {
        "access_token": constants.MY_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": messaging_event["sender"]["id"]
        },
        "message": {
            "text": "Thanks for the message :)"
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)

def receivedDeliveryConfirmation():
    print "Received delivery confirmation" #logging

def receivedAuthentication():
    print "Received authentication" #logging

def receivedRead(message_event):
    print "Sequence number " + str(message_event["read"]["seq"]) + " was read by user " + str(message_event["sender"]["id"])  #logging 

if __name__ == "__main__":
    application.run(host='0.0.0.0')
