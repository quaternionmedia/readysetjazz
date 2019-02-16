
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import httplib2
import datetime
from os import path


SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = path.join('cred', 'client_id.json')
APPLICATION_NAME = 'RSJ calendar man'
#CALENDAR_ID = 'dellarteproductions.com_7ss0rggrpg59qgq7cr9um62n68@group.calendar.google.com'


def get_credentials():
	credential_path = path.join('cred', 'cred.json')
	store = Storage(credential_path)
	flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
	flow.user_agent = APPLICATION_NAME
	credentials = tools.run_flow(flow=flow, storage=store)
	return credentials

def get_events(credentials, calendar):
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	now = datetime.datetime.utcnow().isoformat() + 'Z'
	eventsResult = service.events().list(
		calendarId=calendar, timeMin=now, maxResults=10, singleEvents=True,
		orderBy='startTime').execute()
	events = eventsResult.get('items', [])
	if not events:
		eventsResult = service.events().list(
			calendarId=calendar, timeMax=now, singleEvents=True,
			orderBy='startTime').execute()
		events = eventsResult.get('items', [])
		events = [events[-1]]
	return [e for e in events if e.get('visibility', None) != 'private']
