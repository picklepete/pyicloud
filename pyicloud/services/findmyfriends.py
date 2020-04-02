import json
import sys
import six

from pyicloud.exceptions import PyiCloudNoDevicesException

class FindMyFriendsServiceManager(object):
    """
    The 'Find my Friends' iCloud service
    This connects to iCloud and returns friend data including contacts, friends,
    following and the near-realtime latitude and longitude.
    """
    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._friend_endpoint = '%s/fmipservice/client/fmfWeb/initClient' % (
            self._service_root,
        )
        self._data = {}


    def refresh_data(self):
        """
        Fetches all data from Find my Friends endpoint
        """
        params = dict(self.params)
        requested_data = json.dumps({
            'clientContext': {
                'appVersion': '1.0',
                'contextApp': 'com.icloud.web.fmf',
                'mapkitAvailable': True,
                'productType': 'fmfWeb',
                'tileServer': 'Apple',
                'userInactivityTimeInMS': 537,
                'windowInFocus': False,
                'windowVisible': True
            },
            'dataContext': None,
            'serverContext': None
        })
        req = self.session.post(
            self._friend_endpoint,
            data=requested_data,
            params=params
            )
        self.response = req.json()
        
        return self.response

    @property
    def data(self):
        if not self._data:
            self._data = self.refresh_data()
        return self._data

    @property
    def locations(self):
        return self.data.get('locations')

    @property
    def contacts(self):
        return self.data.get('contactDetails')

    @property
    def followers(self):
        return self.data.get('followers')

    @property
    def following(self):
        return self.data.get('following')

