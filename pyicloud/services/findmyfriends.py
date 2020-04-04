"""Find my Friends service."""
from __future__ import absolute_import
import json


class FindFriendsService(object):
    """
    The 'Find my Friends' iCloud service

    This connects to iCloud and returns friend data including the near-realtime
    latitude and longitude.
    """

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._friend_endpoint = "%s/fmipservice/client/fmfWeb/initClient" % (
            self._service_root,
        )
        self.response = {}

    def refresh_data(self):
        """
        Refreshes all data from Find my Friends endpoint,

        This ensures that the location data is up-to-date.

        """
        params = dict(self.params)
        # This is a request payload we mock to fetch the data
        mock_payload = json.dumps(
            {
                "clientContext": {
                    "appVersion": "1.0",
                    "contextApp": "com.icloud.web.fmf",
                    "mapkitAvailable": True,
                    "productType": "fmfWeb",
                    "tileServer": "Apple",
                    "userInactivityTimeInMS": 537,
                    "windowInFocus": False,
                    "windowVisible": True,
                },
                "dataContext": None,
                "serverContext": None,
            }
        )
        req = self.session.post(self._friend_endpoint, data=mock_payload, params=params)
        # Update the response for normal execution flow
        self.response = req.json()
        # FEAT: Return a value to support monkey-patching
        return self.response

    @property
    def data(self):
        """Memoized friends location data.

        Call `refresh_data()` before property access for latest data.

        """
        if not self.response:  # fetch once
            # FEAT: Support callees swizzling `refresh_data` method
            self.response = self.refresh_data()
        return self.response

    @property
    def locations(self):
        """Returns a list of your friends' locations"""
        return self.data.get("locations")

    @property
    def followers(self):
        """Returns a list of friends who follow you"""
        return self.data.get("followers")

    @property
    def friend_fences(self):
        """Returns friend geofences"""
        return self.data.get("friendFencesISet")

    @property
    def my_fences(self):
        """Returns my fences"""
        return self.data.get("myFencesISet")

    @property
    def details(self):
        """Returns a list of your friends contact details"""
        return self.data.get("contactDetails")
