import json

from pyicloud.exceptions import PyiCloudNoDevicesException


class FindMyiPhoneService(object):
    """
    The 'Find my iPhone' iCloud service, connects to iCloud and returns
    phone data including the near-realtime latitude and longitude.
    """
    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._fmip_endpoint = '%s/fmipservice/client/web' % self._service_root
        self._fmip_refresh_url = '%s/refreshClient' % self._fmip_endpoint
        self._fmip_sound_url = '%s/playSound' % self._fmip_endpoint
        self._fmip_lost_url = '%s/lostDevice' % self._fmip_endpoint

    def refresh_client(self):
        """
        Refreshes the FindMyiPhoneService endpoint,
        ensuring that the location data is up-to-date.
        """
        host = self._service_root.split('//')[1].split(':')[0]
        self.session.headers.update({'host': host})
        req = self.session.post(self._fmip_refresh_url, params=self.params)
        self.response = req.json()
        if self.response['content']:
            # TODO: Support multiple devices.
            self.content = self.response['content'][0]
        else:
            message = 'You do not have any active devices.'
            raise PyiCloudNoDevicesException(message)
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

    def play_sound(self, subject='Find My iPhone Alert'):
        """
        Send a request to the device to play a sound, it's possible to
        pass a custom message by changing the `subject`.
        """
        self.refresh_client()
        data = json.dumps({'device': self.content['id'], 'subject': subject})
        self.session.post(self._fmip_sound_url, params=self.params, data=data)

    def lost_device(self, number, text=None):
        """
        Send a request to the device to trigger 'lost mode'. The
        device will show the message in `text`, and if a number has
        been passed, then the person holding the device can call
        the number without entering the passcode.
        """
        self.refresh_client()
        if not text:
            text = 'This iPhone has been lost. Please call me.'
        data = json.dumps({
            'text': text,
            'userText': True,
            'ownerNbr': number,
            'lostModeEnabled': True,
            'trackingEnabled': True,
            'device': self.content['id'],
        })
        self.session.post(self._fmip_lost_url, params=self.params, data=data)
