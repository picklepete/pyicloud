"""Find My Friends service tests."""
from unittest import TestCase
from . import PyiCloudServiceMock
from .const import AUTHENTICATED_USER, VALID_PASSWORD


class FindMyFriendsServiceTest(TestCase):
    """"Find My Friend service tests"""

    service = None

    def setUp(self):
        self.service = PyiCloudServiceMock(AUTHENTICATED_USER, VALID_PASSWORD)

    def test_locations(self):
        """Tests locations."""
        locations = self.service.friends.locations
        assert isinstance(locations, list)
        assert len(locations) == 2
        assert isinstance(locations[0], dict)
        assert isinstance(locations[1], dict)
