# we using gmail api now, fk sendgrid and mailgun and courier

# ------------ Dependencies to call the Gmail and Google API ------------------
from __future__ import print_function

import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage

# ------------ Dependencies for AMQP exchange and queue -----------------------
import json
import requests
import os
import amqp_setup

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

# PLEASE CHECK!! THE GOOGLE TOKEN NEEDS TO BE REFRESHED!! IT HAS A TIME FRAME BEFORE IT EXPIRES, WHICH MEANS YOU NEED TO GENERATE  A NEW TOKEN BEFORE YOU RUN THIS FILE!!
# TLDR: DELETE TOKEN.JSON BEFORE RUNNING SEND_EMAIL.PY!

monitor_binding_key = "#.email.#"
'''
Function: initiate the queue
'''
def receive_sms():
    amqp_setup.check_setup()
    queue_name = 'email'

    # set up queue and look for incoming messages
    amqp_setup.channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming()
    # need to terminate using Ctrl+C

'''
Function: callback function when receiving a message
Input: Input: JSON object -> {
    "food" : JSON object,
    "user" : JSON object
}
'''

def callback(channel, method, properties, body):
    print("\nReceived an email from " + __file__)
    sendClientUpdate(json.loads(body))
    print()

'''
Function: sending an SMS to related users
Input: JSON object -> {
    "food" : JSON object,
    "user" : JSON object
}
Output: SMS sent to users + a line printing the result of each SMS + success line when code completes
'''
def sendClientUpdate(body):
    food = body['food']
    user = body['user']

    # change accordingly for email
    recipient_email = user['email']
    recipient_name = user['name']
    food_location = food['address']
    food_name = food['post_name']
    food_description = food['description']
    food_allergens = food['allergens']
    food_end_time = food['end_time']
    
    # msg = f"Dear {recipient_name}, there's food nearby!\nBuffet name: {food_name}\nBuffet Address: {food_location}\nBuffet Lat, Long: {food_latitude}, {food_longitude}\nBuffet Description: {food_description}\nAllergens: {food_allergens}\nBuffet End Timing: {food_end_time}"

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()

        message.set_content(f'Hello {recipient_name}!\n\nThere is a new food offering near your default location!\nSee the posting details below,\nBuffet name: {food_name}\nBuffet Address: {food_location}\nBuffet Description: {food_description}\nAllergens: {food_allergens}\nBuffet End Timing: {food_end_time}\n\nThis is a automated message, please do not reply to this thread.\n\nHappy Eating,\nMakanBoleh Team')

        message['To'] = recipient_email
        message['From'] = 'contactmakanboleh@gmail.com'
        message['Subject'] = 'MakanBoleh: New Food Offer Near You!'

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(F'Message Id: {send_message["id"]}')
        print(f"Email to {recipient_name} has been sent to the following email : {recipient_email}")

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

    

if __name__ == "__main__":
    print("\nThis is " + os.path.basename(__file__), end='')
    print(f": monitoring routing key '{monitor_binding_key}' in exchange '{amqp_setup.exchangename}' ...".format(
        monitor_binding_key, amqp_setup.exchangename))
    receive_sms()