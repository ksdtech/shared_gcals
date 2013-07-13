""" 
Copyright 2012 Peter Zingg <pzingg@kentfieldschools.org>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
from oauth import cache, simple_cli
import sys

def list_calendars(service):
    page_token = None
    while True:
      calendar_list = service.calendarList().list(pageToken=page_token).execute()
      for calendar in calendar_list['items']:
        print "%s\n   %s\n" % (calendar['summary'], calendar['id'])
      page_token = calendar_list.get('nextPageToken')
      if not page_token:
        break
        
def share_calendar(service, calendar_id, user_email, write_access=False):
    rule = {
        'scope': {
            'type': 'user',
            'value': user_email,
        },
        'role': 'writer' if write_access else 'reader' 
    }
    created_rule = service.acl().insert(calendarId=calendar_id, body=rule).execute()
    return created_rule   
    
def insert_calendar(service, calendar_id):
    body = {
        'id': calendar_id,
        'foregroundColor':  '#ffffff', # just testing the param stuff
        'backgroundColor':  '#0088aa'
    }
    param = {
        'colorRgbFormat': True # use the foreground and background colors
    }
    created_calendar = service.calendarList().insert(body=body, **param).execute()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Manipulate a user's calendars.")
    parser.add_argument('-a', '--authenticate', action='store_true',
                       help='(re-)authenticate via OAuth2')
    parser.add_argument('-c', '--calendar', type=str, help='calendar ID to share to this user')
    parser.add_argument('-u', '--user', type=str, help='email address of user to share calendar with')
    args = parser.parse_args()
    
    if args.authenticate:
        cache.authenticate('https://www.googleapis.com/auth/calendar')
    service = cache.get_service_object('calendar', 'v3')
    if args.calendar:
        if args.user:
            share_calendar(service, args.calendar, args.user)
        else:
            print "Calendar not shared: You must supply a user email address!"
    list_calendars(service)
