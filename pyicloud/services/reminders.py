from __future__ import absolute_import
from datetime import datetime, timedelta
import time
import uuid
import pytz
import json


class RemindersService(object):
    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self.lists = {}
        self.collections = {}

        self.refresh()

    def get_all_possible_timezones_of_local_machine(self):
        """
        Return all possible timezones in Olson TZ notation
        This has been taken from
        http://stackoverflow.com/questions/7669938
        """
        local_names = []
        if time.daylight:
            local_offset = time.altzone
            localtz = time.tzname[1]
        else:
            local_offset = time.timezone
            localtz = time.tzname[0]

        local_offset = timedelta(seconds=-local_offset)

        for name in pytz.all_timezones:
            timezone = pytz.timezone(name)
            if not hasattr(timezone, '_tzinfos'):
                continue
            for (utcoffset, daylight, tzname), _ in timezone._tzinfos.items():
                if utcoffset == local_offset and tzname == localtz:
                    local_names.append(name)
        return local_names

    def get_system_tz(self):
        """
        Retrieves the system's timezone from a list of possible options.
        Just take the first one
        """
        return self.get_all_possible_timezones_of_local_machine()[0]

    def refresh(self):
        host = self._service_root.split('//')[1].split(':')[0]
        self.session.headers.update({'host': host})

        params_reminders = dict(self.params)
        params_reminders.update({
            'clientVersion': '4.0',
            'lang': 'en-us',
            'usertz': self.get_system_tz()
        })

        # Open reminders
        req = self.session.get(
            self._service_root + '/rd/startup',
            params=params_reminders
        )

        startup = req.json()

        self.lists = {}
        self.collections = {}
        for collection in startup['Collections']:
            temp = []
            self.collections[collection['title']] = {
                'guid': collection['guid'],
                'ctag': collection['ctag']
            }
            for reminder in startup['Reminders']:

                if reminder['pGuid'] != collection['guid']:
                    continue
                if 'dueDate' in reminder:
                    if reminder['dueDate']:
                        due = datetime(
                            reminder['dueDate'][1],
                            reminder['dueDate'][2], reminder['dueDate'][3],
                            reminder['dueDate'][4], reminder['dueDate'][5]
                        )
                    else:
                        due = None
                else:
                    due = None
                if reminder['description']:
                    desc = reminder['description']
                else:
                    desc = ""
                temp.append({
                    "title": reminder['title'],
                    "desc": desc,
                    "due": due
                })
            self.lists[collection['title']] = temp

    def post(self, title, description="", collection=None):
        pguid = 'tasks'
        if collection:
            if collection in self.collections:
                pguid = self.collections[collection]['guid']

        host = self._service_root.split('//')[1].split(':')[0]
        self.session.headers.update({'host': host})

        params_reminders = dict(self.params)
        params_reminders.update({
            'clientVersion': '4.0',
            'lang': 'en-us',
            'usertz': self.get_system_tz()
        })

        req = self.session.post(
            self._service_root + '/rd/reminders/tasks',
            data=json.dumps({
                "Reminders": {
                    'title': title,
                    "description": description,
                    "pGuid": pguid,
                    "etag": None,
                    "order": None,
                    "priority": 0,
                    "recurrence": None,
                    "alarms": [],
                    "startDate": None,
                    "startDateTz": None,
                    "startDateIsAllDay": False,
                    "completedDate": None,
                    "dueDate": None,
                    "dueDateIsAllDay": False,
                    "lastModifiedDate": None,
                    "createdDate": None,
                    "isFamily": None,
                    "createdDateExtended": int(time.time()*1000),
                    "guid": str(uuid.uuid4())
                },
                "ClientState": {"Collections": self.collections.values()}
            }),
            params=params_reminders)
        return req.ok
