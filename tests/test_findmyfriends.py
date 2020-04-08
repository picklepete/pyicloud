"""Find My Friends service tests."""
from unittest import TestCase
from . import PyiCloudServiceMock
from .const import AUTHENTICATED_USER, VALID_PASSWORD
from .const_findmyfriends import PERSON_ID_1, PERSON_ID_2, LOCATION_ID_1, LOCATION_ID_2


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

    def test_location_of_persons(self):
        """Tests locations."""
        friend_location = self.service.friends.location_of(PERSON_ID_1)
        location_id = friend_location.get("locationId")
        assert location_id == LOCATION_ID_1
        friend_location = self.service.friends.location_of(PERSON_ID_2)
        location_id = friend_location.get("locationId")
        assert location_id == LOCATION_ID_2
        friend_location = self.service.friends.location_of("NO_MATCH", {})
        location_id = friend_location.get("locationId")
        assert location_id is None
