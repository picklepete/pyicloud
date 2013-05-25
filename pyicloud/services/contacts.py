from __future__ import absolute_import
import os
from datetime import datetime
from calendar import monthrange


class ContactsService(object):
    """
    The 'Contacts' iCloud service, connects to iCloud and returns contacts.
    """
    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._contacts_endpoint = '%s/co' % self._service_root
        self._contacts_refresh_url = '%s/startup' % self._contacts_endpoint

    def refresh_client(self, from_dt=None, to_dt=None):
        """
        Refreshes the ContactsService endpoint, ensuring that the
        contacts data is up-to-date.
        """
        host = self._service_root.split('//')[1].split(':')[0]
        self.session.headers.update({'host': host})
        params = dict(self.params)
        params.update({
            'locale': 'en_US',
            'order': 'last,first',
        })
        req = self.session.get(self._contacts_refresh_url, params=params)
        self.response = req.json()

    def all(self):
        """
        Retrieves all contacts.
        """
        self.refresh_client()
        return self.response['contacts']
