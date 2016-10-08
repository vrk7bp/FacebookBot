# This file holds all the logic for dealing with payloads that come with message information. So this is where logic for the "Message Received" Facebook hanlder

import requests
import json
import constants

# Generic handler for "parsing" message and forwarding it to the necessary methods
def receivedMessage(messaging_event):
    sender_id = messaging_event["sender"]["id"]
    message = messaging_event["message"]
    print "Received message for user " + str(sender_id) + " from page " + str(messaging_event["recipient"]["id"]) + " at " + str(messaging_event["timestamp"]) + "; SEQ NUM: " + str(messaging_event["message"]["seq"]) #logging
    
    if message.get("attachments"):  #Deal with getting an attachment
        print "Got an attachment"
        parseAttachment(messaging_event)
 
    else:                           #Deal with a message you received
        print "Got a message"
        message_text = message["text"]
        if(message_text == "generic"):
            sendGenericMessage(sender_id)
        elif(message_text == "image"):
            sendImageMessage(sender_id)
        elif(message_text == "button"):
            sendButtonMessage(sender_id)
        elif(message_text == "receipt"):
            sendReceiptMessage(sender_id)
        else:
            sendTextMessage(sender_id, "Got your message :) :)")

# Method for dealing with attachments
def parseAttachment(messaging_event):
    sendTextMessage(sender_id, "I got your attachment, thanks :)")

# Generic message handler 1 (based on image example from Facebook)
def sendImageMessage(sender_id):
    print "Send Image Message"
    sendTextMessage(sender_id, "Got your image :)")

# Generic message handler 2 (based on button example from Facebook)
def sendButtonMessage(sender_id):
    print "Send Button Message"
    sendTextMessage(sender_id, "Got your button :)")

# Generic message handler 3 (based on template example from Facebook)
def sendGenericMessage(sender_id):
    print "Send Generic Message"
    data = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [{
                        "title": "rift",
                        "subtitle": "Next-generation virtual reality",
                        "item_url": "https://www.oculus.com/en-us/rift/",               
                        "image_url": "http://messengerdemo.parseapp.com/img/rift.png",
                        "buttons": [{
                            "type": "web_url",
                            "url": "https://www.oculus.com/en-us/rift/",
                            "title": "Open Web URL"
                        }, {
                            "type": "postback",
                            "title": "Call Postback",
                            "payload": "Payload for first bubble",
                        }],
                    }, {
                        "title": "touch",
                        "subtitle": "Your Hands, Now in VR",
                        "item_url": "https://www.oculus.com/en-us/touch/",               
                        "image_url": "http://messengerdemo.parseapp.com/img/touch.png",
                        "buttons": [{
                            "type": "web_url",
                            "url": "https://www.oculus.com/en-us/touch/",
                            "title": "Open Web URL"
                        }, {
                            "type": "postback",
                            "title": "Call Postback",
                            "payload": "Payload for second bubble",
                        }]
                    }]
                }
            }
        }
    })
    callSendAPI(data)

# Generic message handler 4 (based on receipt example from Facebook)
def sendReceiptMessage(sender_id):
    print "Send Receipt Message"
    sendTextMessage(sender_id, "Got your receipt")

# Generic message handler 5 (based on Facebook example)
def sendTextMessage(sender_id, message_text):
    print "Send Text Message"
    data = json.dumps({
        "recipient": {
            "id": sender_id
        },
        "message": {
            "text": message_text
        }
    })
    callSendAPI(data)

# Method that actually sends information back to user
def callSendAPI(messageData):
    params = {
        "access_token": constants.MY_TOKEN
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = messageData
    
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    
    if r.status_code == 200:
        print "Successfully sent message"
        print r.json()
    else:
        print "Error sending message"
        print r.json()
