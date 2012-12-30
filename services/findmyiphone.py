from pyicloud.exceptions import PyiCloudNoDevicesException


class FindMyiPhoneService(object):
    """
    The 'Find my iPhone' iCloud service, connects to iCloud and returns
    phone data including the near-realtime latitude and longitude.
    """
    def __init__(self, session, params):
        self.session = session
        self.params = params
        self._fmip_root = 'https://p12-fmipweb.icloud.com'
        self._fmip_endpoint = '%s/fmipservice/client/web' % self._fmip_root
        self._fmip_refresh_url = '%s/refreshClient' % self._fmip_endpoint

    def refresh_client(self):
        """
        Refreshes the FindMyiPhoneService endpoint,
        ensuring that the location data is up-to-date.
        """
        self.session.headers.update({'host': 'p12-fmipweb.icloud.com'})
        req = self.session.post(self._fmip_refresh_url, params=self.params)
        self.response = req.json()
        if self.response['content']:
	        # TODO: Support multiple devices.
        	self.content = self.response['content'][0]
        else:
	        raise PyiCloudNoDevicesException('You do not have any active devices.')
        self.user_info = self.response['userInfo']

    def location(self):
        self.refresh_client()
        return self.content['location']

    def status(self, additional=[]):
        """
        The FindMyiPhoneService response is quite bloated, this method
        will return a subset of the more useful properties.
        """
        self.refresh_client()
        fields = ['batteryLevel', 'deviceDisplayName', 'deviceStatus', 'name']
        fields += additional
        properties = {}
        for field in fields:
            properties[field] = self.content.get(field, 'Unknown')
        return properties
