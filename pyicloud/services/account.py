import sys


class AccountService(object):
    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._devices = []

        self._acc_endpoint = '%s/setup/web/device' % self._service_root
        self._account_devices_url = '%s/getDevices' % self._acc_endpoint

        req = self.session.get(self._account_devices_url, params=self.params)
        self.response = req.json()

        for device_info in self.response['devices']:
            # device_id = device_info['udid']
            # self._devices[device_id] = AccountDevice(device_info)
            self._devices.append(AccountDevice(device_info))

    @property
    def devices(self):
        return self._devices


class AccountDevice(object):
    def __init__(self, device_info):
        self.serialNumber = device_info['serialNumber']
        self.osVersion = device_info['osVersion']
        self.modelLargePhotoURL2x = device_info['modelLargePhotoURL2x']
        self.modelLargePhotoURL1x = device_info['modelLargePhotoURL1x']
        self.name = device_info['name']
        self.imei = device_info['imei']
        self.model = device_info['model']
        self.udid = device_info['udid']
        self.modelSmallPhotoURL2x = device_info['modelSmallPhotoURL2x']
        self.modelSmallPhotoURL1x = device_info['modelSmallPhotoURL1x']
        self.modelDisplayName = device_info['modelDisplayName']
