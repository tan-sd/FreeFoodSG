# we using gmail api now, fk sendgrid and mailgun and courier
from __future__ import print_function

import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def main():
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
        # Call the Gmail API to print mail labels
        # service = build('gmail', 'v1', credentials=creds)
        # results = service.users().labels().list(userId='me').execute()
        # labels = results.get('labels', [])

        # if not labels:
        #     print('No labels found.')
        #     return
        # print('Labels:')
        # for label in labels:
        #     print(label['name'])

        # THIS CODE IS TAKEN FROM send_email.py, THIS IS THE CODE THAT SENDS THE MAIL
        # ABOVE IS THE CODE THAT HANDLES THE CREDENTIALS AND AUTHORIZATION!!
        # ADJUST MAIL PARAMETERS BELOW
        # WE CAN EVEN CREATE A DRAFT MESSAGE TO SEND OUT.
        # WE NEED TO CREATE A FAKE GMAIL TO SEND OUT EMAILS FROM, CANNOT KEEP USING MY PERSONAL ONE!
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content('hm hope this sends from another email')

        message['To'] = 'sethyap.2021@scis.smu.edu.sg'
        message['From'] = 'contactmakanboleh@gmail.com'
        message['Subject'] = 'pls work'

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


    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()