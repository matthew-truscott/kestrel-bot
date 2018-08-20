import discord
from discord.ext import commands

import httplib2
import os

from googleapiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
CREDENTIALS_DIR = os.path.join(ROOT_DIR, '.credentials')
CLIENT_SECRET_FILE = os.path.join(CREDENTIALS_DIR, 'calendar_secret.json')
APPLICATION_NAME = 'Kestrel Bot Calendar'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    credential_path = os.path.join(CREDENTIALS_DIR,
                                   'kestrel_bot_calendar.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


class CalendarCog(object):
    def __init__(self, bot):
        self.bot = bot
        self.credentials = get_credentials()
        self.http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)
        self.now = datetime.datetime.utcnow().isoformat() + 'Z'

    def getNextEvents(self, number):
        pass


def main():
    """Basic usage of the Google Calendar API

    Creates a Google Calendar API service object and outputs a list of the
    next 10 events on the user's calendar.
    """

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()
