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
        assert self.service.devices
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

    def test_family(self):
        """Tests family members."""
        assert self.service.family
        assert len(self.service.family) == 3

        for member in self.service.family:
            assert member.last_name
            assert member.dsid
            assert member.original_invitation_email
            assert member.full_name
            assert member.age_classification
            assert member.apple_id_for_purchases
            assert member.apple_id
            assert member.first_name
            assert not member.has_screen_time_enabled
            assert not member.has_ask_to_buy_enabled
            assert not member.share_my_location_enabled_family_members
            assert member.dsid_for_purchases

    def test_storage(self):
        """Tests storage."""
        assert self.service.storage

        assert self.service.storage.usage
        assert (
            self.service.storage.usage.comp_storage_in_bytes
            or self.service.storage.usage.comp_storage_in_bytes == 0
        )
        assert self.service.storage.usage.used_storage_in_bytes
        assert self.service.storage.usage.used_storage_in_percent
        assert self.service.storage.usage.available_storage_in_bytes
        assert self.service.storage.usage.available_storage_in_percent
        assert self.service.storage.usage.total_storage_in_bytes
        assert (
            self.service.storage.usage.commerce_storage_in_bytes
            or self.service.storage.usage.commerce_storage_in_bytes == 0
        )
        assert not self.service.storage.usage.quota_over
        assert not self.service.storage.usage.quota_tier_max
        assert not self.service.storage.usage.quota_almost_full
        assert not self.service.storage.usage.quota_paid

        assert self.service.storage.usages_by_media

        for usage_media in self.service.storage.usages_by_media.values():
            assert usage_media.key
            assert usage_media.label
            assert usage_media.color
            assert usage_media.usage_in_bytes or usage_media.usage_in_bytes == 0
