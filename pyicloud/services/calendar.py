from __future__ import absolute_import
import os
from datetime import datetime
from calendar import monthrange


class CalendarService(object):
    """
    The 'Calendar' iCloud service, connects to iCloud and returns events.
    """
    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._calendar_endpoint = '%s/ca' % self._service_root
        self._calendar_refresh_url = '%s/events' % self._calendar_endpoint

    def get_system_tz(self):
        """
        Retrieves the system's timezone.
        From: http://stackoverflow.com/a/7841417
        """
        return '/'.join(os.readlink('/etc/localtime').split('/')[-2:])

    def refresh_client(self, from_dt=None, to_dt=None):
        """
        Refreshes the CalendarService endpoint, ensuring that the
        event data is up-to-date. If no 'from_dt' or 'to_dt' datetimes
        have been given, the range becomes this month.
        """
        today = datetime.today()
        first_day, last_day = monthrange(today.year, today.month)
        if not from_dt:
            from_dt = datetime(today.year, today.month, first_day)
        if not to_dt:
            to_dt = datetime(today.year, today.month, last_day)
        host = self._service_root.split('//')[1].split(':')[0]
        self.session.headers.update({'host': host})
        params = dict(self.params)
        params.update({
            'lang': 'en-us',
            'usertz': self.get_system_tz(),
            'startDate': from_dt.strftime('%Y-%m-%d'),
            'endDate': to_dt.strftime('%Y-%m-%d')
        })
        req = self.session.get(self._calendar_refresh_url, params=params)
        self.response = req.json()

    def events(self, from_dt=None, to_dt=None):
        """
        Retrieves events for a given date range, by default, this month.
        """
        self.refresh_client(from_dt, to_dt)
        return self.response['Event']
