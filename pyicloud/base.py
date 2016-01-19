import six
import copy
import uuid
import hashlib
import json
import logging
import pickle
import requests
import sys
import tempfile
import os
from re import match

from pyicloud.exceptions import PyiCloudFailedLoginException
from pyicloud.services import (
    FindMyiPhoneServiceManager,
    CalendarService,
    UbiquityService,
    ContactsService,
    RemindersService
)

if six.PY3:
    import http.cookiejar as cookielib
else:
    import cookielib


logger = logging.getLogger(__name__)


class PyiCloudService(object):
    """
    A base authentication class for the iCloud service. Handles the
    validation and authentication required to access iCloud services.

    Usage:
        from pyicloud import PyiCloudService
        pyicloud = PyiCloudService('username@apple.com', 'password')
        pyicloud.iphone.location()
    """
    def __init__(self, apple_id, password, cookie_directory=None, verify=True):
        self.discovery = None
        self.client_id = str(uuid.uuid1()).upper()
        self.user = {'apple_id': apple_id, 'password': password}

        self._home_endpoint = 'https://www.icloud.com'
        self._setup_endpoint = 'https://setup.icloud.com/setup/ws/1'

        self._base_login_url = '%s/login' % self._setup_endpoint
        self._base_validate_url = '%s/validate' % self._setup_endpoint

        if cookie_directory:
            self._cookie_directory = os.path.expanduser(
                os.path.normpath(cookie_directory)
            )
        else:
            self._cookie_directory = os.path.join(
                tempfile.gettempdir(),
                'pyicloud',
            )

        self.session = requests.Session()
        self.session.verify = verify
        self.session.headers.update({
            'Origin': self._home_endpoint,
            'Referer': '%s/' % self._home_endpoint,
            'User-Agent': 'Opera/9.52 (X11; Linux i686; U; en)'
        })

        cookiejar_path = self._get_cookiejar_path()
        self.session.cookies = cookielib.LWPCookieJar(filename=cookiejar_path)
        if os.path.exists(cookiejar_path):
            try:
                self.session.cookies.load()
            except cookielib.LoadError:
                # Most likely a pickled cookiejar from earlier versions
                pass

        self.params = {}

        self.authenticate()

    def refresh_validate(self):
        """
        Queries the /validate endpoint and fetches two key values we need:
        1. "dsInfo" is a nested object which contains the "dsid" integer.
            This object doesn't exist until *after* the login has taken place,
            the first request will compain about a X-APPLE-WEBAUTH-TOKEN cookie
        2. "instance" is an int which is used to build the "id" query string.
            This is, pseudo: sha1(email + "instance") to uppercase.
        """
        req = self.session.get(self._base_validate_url, params=self.params)
        resp = req.json()
        if 'dsInfo' in resp:
            dsid = resp['dsInfo']['dsid']
            self.params.update({'dsid': dsid})
        instance = resp.get(
            'instance',
            uuid.uuid4().hex.encode('utf-8')
        )
        sha = hashlib.sha1(
            self.user.get('apple_id').encode('utf-8') + instance
        )
        self.params.update({'id': sha.hexdigest().upper()})

        self.params.update({
            'clientBuildNumber': '14E45',
            'clientId': self.client_id,
        })

    def authenticate(self):
        """
        Handles the full authentication steps, validating,
        authenticating and then validating again.
        """
        self.refresh_validate()

        data = dict(self.user)
        data.update({'id': self.params['id'], 'extended_login': False})
        req = self.session.post(
            self._base_login_url,
            params=self.params,
            data=json.dumps(data)
        )

        if not req.ok:
            msg = 'Invalid email/password combination.'
            raise PyiCloudFailedLoginException(msg)

        if not os.path.exists(self._cookie_directory):
            os.mkdir(self._cookie_directory)
        self.session.cookies.save()

        self.refresh_validate()

        self.discovery = req.json()
        self.webservices = self.discovery['webservices']

    def _get_cookiejar_path(self):
        # Get path for cookiejar file
        return os.path.join(
            self._cookie_directory,
            ''.join([c for c in self.user.get('apple_id') if match(r'\w', c)])
        )

    @property
    def devices(self):
        """ Return all devices."""
        service_root = self.webservices['findme']['url']
        return FindMyiPhoneServiceManager(
            service_root,
            self.session,
            self.params
        )

    @property
    def iphone(self):
        return self.devices[0]

    @property
    def files(self):
        if not hasattr(self, '_files'):
            service_root = self.webservices['ubiquity']['url']
            self._files = UbiquityService(
                service_root,
                self.session,
                self.params
            )
        return self._files

    @property
    def calendar(self):
        service_root = self.webservices['calendar']['url']
        return CalendarService(service_root, self.session, self.params)

    @property
    def contacts(self):
        service_root = self.webservices['contacts']['url']
        return ContactsService(service_root, self.session, self.params)

    @property
    def reminders(self):
        service_root = self.webservices['reminders']['url']
        return RemindersService(service_root, self.session, self.params)

    def __unicode__(self):
        return 'iCloud API: %s' % self.user.get('apple_id')

    def __str__(self):
        as_unicode = self.__unicode__()
        if sys.version_info[0] >= 3:
            return as_unicode
        else:
            return as_unicode.encode('ascii', 'ignore')

    def __repr__(self):
        return '<%s>' % str(self)
