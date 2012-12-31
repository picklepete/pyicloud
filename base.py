import time
import uuid
import hashlib
import json
import requests

from exceptions import PyiCloudFailedLoginException
from services import FindMyiPhoneService, CalendarService


class PyiCloudService(object):
    """
    A base authentication class for the iCloud service. Handles the
    validation and authentication required to access iCloud services.

    Usage:
        from pyicloud import PyiCloudService
        pyicloud = PyiCloudService('username@apple.com', 'password')
        pyicloud.iphone.location()
    """
    def __init__(self, apple_id, password):
        self.discovery = None
        self.client_id = str(uuid.uuid1()).upper()
        self.user = {'apple_id': apple_id, 'password': password}

        self._home_endpoint = 'https://www.icloud.com'
        self._setup_endpoint = 'https://p12-setup.icloud.com/setup/ws/1'
        self._push_endpoint = 'https://p12-pushws.icloud.com'

        self._base_login_url = '%s/login' % self._setup_endpoint
        self._base_validate_url = '%s/validate' % self._setup_endpoint
        self._base_system_url = '%s/system/version.json' % self._home_endpoint
        self._base_webauth_url = '%s/refreshWebAuth' % self._push_endpoint

        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'host': 'setup.icloud.com',
            'origin': self._home_endpoint,
            'referer': '%s/' % self._home_endpoint,
            'User-Agent': 'Opera/9.52 (X11; Linux i686; U; en)'
        })

        self.refresh_version()
        self.params = {
            'clientId': self.client_id,
            'clientBuildNumber': self.build_id
        }

        self.authenticate()

    def refresh_version(self):
        """
        Retrieves the buildNumber from the /version endpoint.
        This is used by almost all request query strings.
        """
        req = requests.get(self._base_system_url)
        self.build_id = req.json()['buildNumber']

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
        instance = resp['instance']
        sha = hashlib.sha1(self.user.get('apple_id') + instance)
        self.params.update({'id': sha.hexdigest().upper()})

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

        self.refresh_validate()

        self.discovery = req.json()
        self.webservices = self.discovery['webservices']

    @property
    def iphone(self):
        service_root = self.webservices['findme']['url']
        return FindMyiPhoneService(service_root, self.session, self.params)

    @property
    def calendar(self):
        service_root = self.webservices['calendar']['url']
        return CalendarService(service_root, self.session, self.params)
