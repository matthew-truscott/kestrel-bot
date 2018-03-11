# Importing required libraries
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
import threading
import time
import sortinghat
import os

'''
Script based off: https://github.com/abhishekchhibber/Gmail-Api-through-Python/blob/master/gmail_read.py
'''

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
UTIL_DIR = os.path.join(ROOT_DIR, 'cogs/utils')
CREDENTIALS_DIR = os.path.join(ROOT_DIR, '.credentials')

class SurveyResponseListenerThread(threading.Thread):

    # Creating a storage.JSON file with authentication details
    SCOPES = 'https://www.googleapis.com/auth/gmail.modify'  # we are using modify and not readonly, as we will be marking the messages Read
    store = file.Storage(os.path.join(DATA_DIR, 'storage.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(
            os.path.join(CREDENTIALS_DIR, 'client_secret_gmail.json'), SCOPES)
        creds = tools.run_flow(flow, store)
    GMAIL = discovery.build('gmail', 'v1', http=creds.authorize(Http()))

    user_id = 'me'
    label_id_one = 'INBOX'
    label_id_two = 'UNREAD'

    def __init__(self):
        super().__init__()
        pass

    def run(self):
        while True:
            time.sleep(2)
            unread_msgs = self.GMAIL.users().messages().list(userId='me',
                                                             labelIds=[self.label_id_one, self.label_id_two],
                                                             maxResults=3,
                                                             q="from:forms-receipts-noreply@google.com").execute()

            # We get a dictionary. Now reading values for the key 'messages'
            try:
                msg_list = unread_msgs['messages']
                print("Number of new responses: ", str(len(msg_list)))
                for msg in msg_list:
                    m_id = msg['id']  # get id of individual message
                    self.GMAIL.users().messages().modify(userId=self.user_id, # mark message as read
                                                         id=m_id,
                                                         body={'removeLabelIds': ['UNREAD']}).execute()
                sortinghat.main()

            except KeyError:
                print("No new responses.")


t = SurveyResponseListenerThread()
t.start()
