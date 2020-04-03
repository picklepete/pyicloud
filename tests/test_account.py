"""Account service tests."""
from unittest import TestCase
from . import PyiCloudServiceMock
from .const import AUTHENTICATED_USER, VALID_PASSWORD


class AccountServiceTest(TestCase):
    """"Account service tests"""

    service = None

    def setUp(self):
        self.service = PyiCloudServiceMock(AUTHENTICATED_USER, VALID_PASSWORD).account

    def test_devices(self):
        """Tests devices."""
        assert len(self.service.devices) == 2

        for device in self.service.devices:
            assert device.name
            assert device.model
            assert device.udid
            assert device["serialNumber"]
            assert device["osVersion"]
            assert device["modelLargePhotoURL2x"]
            assert device["modelLargePhotoURL1x"]
            assert device["paymentMethods"]
            assert device["name"]
            assert device["model"]
            assert device["udid"]
            assert device["modelSmallPhotoURL2x"]
            assert device["modelSmallPhotoURL1x"]
            assert device["modelDisplayName"]
