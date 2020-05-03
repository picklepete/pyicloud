# -*- coding: utf-8 -*-
"""Find My iPhone service tests."""
from unittest import TestCase
from . import PyiCloudServiceMock
from .const import AUTHENTICATED_USER, VALID_PASSWORD

import logging

LOGGER = logging.getLogger(__name__)


class FindMyiPhoneServiceTest(TestCase):
    """"Find My iPhone service tests"""

    service = None

    def setUp(self):
        self.service = PyiCloudServiceMock(
            AUTHENTICATED_USER, VALID_PASSWORD
        ).find_my_iphone

    def test_repr(self):
        """Tests representations."""
        # fmt: off
        assert repr(self.service) == "<FindMyiPhoneService: {with_family: True, devices: 0}>"
        self.service.refresh_client()
        assert repr(self.service) == "<FindMyiPhoneService: {with_family: True, devices: 13}>"
        # fmt: on

    def test_init(self):
        """Tests init."""
        assert len(list(self.service.devices)) == 0

    def test_refresh_client(self):
        """Tests devices."""
        assert len(list(self.service.devices)) == 0

        self.service.refresh_client()

        assert len(self.service.devices) == 13

    def test_device(self):
        """Tests device."""
        with self.assertRaises(KeyError):
            self.service.device("iPhone12,1")
        with self.assertRaises(IndexError):
            self.service.device(0)

        self.service.refresh_client()

        assert self.service.device("iPhone12,1") is not None
        assert self.service.device(0) is not None
        # fmt: off
        assert repr(self.service.device(0)) == "<AppleDevice(iPhone 11: iPhone de Quentin)>"
        # fmt: on

        with self.assertRaises(IndexError):
            self.service.device(999)

    def test_devices(self):
        """Tests devices."""
        self.service.refresh_client()

        assert self.service.devices

        for device in self.service.devices.values():
            assert device.name
            assert device.deviceDisplayName
            # fmt: off
            assert repr(device) == "<AppleDevice("+device.deviceDisplayName+": "+device.name+")>"
            # fmt: on

            assert device["canWipeAfterLock"] is not None
            assert device["baUUID"] is not None
            assert device["wipeInProgress"] is not None
            assert device["lostModeEnabled"] is not None
            assert device["activationLocked"] is not None
            assert device["passcodeLength"] is not None
            assert device["deviceStatus"] is not None
            assert device["features"] is not None
            assert device["lowPowerMode"] is not None
            assert device["rawDeviceModel"] is not None
            assert device["id"] is not None
            assert device["isLocating"] is not None
            assert device["modelDisplayName"] is not None
            assert device["lostTimestamp"] is not None
            assert device["batteryLevel"] is not None
            assert device["locationEnabled"] is not None
            assert device["locFoundEnabled"] is not None
            assert device["fmlyShare"] is not None
            assert device["lostModeCapable"] is not None
            assert device["wipedTimestamp"] is None
            assert device["deviceDisplayName"] is not None
            assert device["audioChannels"] is not None
            assert device["locationCapable"] is not None
            assert device["batteryStatus"] is not None
            assert device["trackingInfo"] is None
            assert device["name"] is not None
            assert device["isMac"] is not None
            assert device["thisDevice"] is not None
            assert device["deviceClass"] is not None
            assert device["deviceModel"] is not None
            assert device["maxMsgChar"] is not None
            assert device["darkWake"] is not None
            assert device["remoteWipe"] is None

            assert device.attrs["canWipeAfterLock"] is not None
            assert device.attrs["baUUID"] is not None
            assert device.attrs["wipeInProgress"] is not None
            assert device.attrs["lostModeEnabled"] is not None
            assert device.attrs["activationLocked"] is not None
            assert device.attrs["passcodeLength"] is not None
            assert device.attrs["deviceStatus"] is not None
            assert device.attrs["features"] is not None
            assert device.attrs["lowPowerMode"] is not None
            assert device.attrs["rawDeviceModel"] is not None
            assert device.attrs["id"] is not None
            assert device.attrs["isLocating"] is not None
            assert device.attrs["modelDisplayName"] is not None
            assert device.attrs["lostTimestamp"] is not None
            assert device.attrs["batteryLevel"] is not None
            assert device.attrs["locationEnabled"] is not None
            assert device.attrs["locFoundEnabled"] is not None
            assert device.attrs["fmlyShare"] is not None
            assert device.attrs["lostModeCapable"] is not None
            assert device.attrs["wipedTimestamp"] is None
            assert device.attrs["deviceDisplayName"] is not None
            assert device.attrs["audioChannels"] is not None
            assert device.attrs["locationCapable"] is not None
            assert device.attrs["batteryStatus"] is not None
            assert device.attrs["trackingInfo"] is None
            assert device.attrs["name"] is not None
            assert device.attrs["isMac"] is not None
            assert device.attrs["thisDevice"] is not None
            assert device.attrs["deviceClass"] is not None
            assert device.attrs["deviceModel"] is not None
            assert device.attrs["maxMsgChar"] is not None
            assert device.attrs["darkWake"] is not None
            assert device.attrs["remoteWipe"] is None
