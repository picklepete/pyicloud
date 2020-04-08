"""Find My Friends service tests."""
from unittest import TestCase
from . import PyiCloudServiceMock
from .const import AUTHENTICATED_USER, VALID_PASSWORD
from .const_findmyfriends import (
    PERSON_ID_1,
    PERSON_ID_2,
    LOCATION_ID_1,
    LOCATION_ID_2,
    PERSON_PHONE_1,
    PERSON_EMAIL_2,
)


class FindMyFriendsServiceTest(TestCase):
    """"Find My Friend service tests"""

    service = None

    def setUp(self):
        self.service = PyiCloudServiceMock(AUTHENTICATED_USER, VALID_PASSWORD)

    def test_contact_details(self):
        """Tests locations."""
        contact_details = self.service.friends.contact_details
        assert isinstance(contact_details, list)
        assert len(contact_details) == 2
        assert isinstance(contact_details[0], dict)
        assert isinstance(contact_details[1], dict)

    def test_locations(self):
        """Tests locations."""
        locations = self.service.friends.locations
        assert isinstance(locations, list)
        assert len(locations) == 2
        assert isinstance(locations[0], dict)
        assert isinstance(locations[1], dict)

    def test_contact_id_of_persons_by_identifier(self):
        """Tests lookup by identifier"""
        contact_id = self.service.friends.contact_id_for(PERSON_PHONE_1)
        assert contact_id == PERSON_ID_1
        contact_id = self.service.friends.contact_id_for(PERSON_EMAIL_2)
        assert contact_id == PERSON_ID_2
        contact_id = self.service.friends.contact_id_for("NOMATCH")
        assert contact_id is None

    def test_location_of_persons_by_contact_id(self):
        """Tests location_of by contact_id"""
        friend_location = self.service.friends.location_of(PERSON_ID_1)
        location_id = friend_location.get("locationId")
        assert location_id == LOCATION_ID_1
        friend_location = self.service.friends.location_of(PERSON_ID_2)
        location_id = friend_location.get("locationId")
        assert location_id == LOCATION_ID_2
        friend_location = self.service.friends.location_of("NOMATCH~~", {})
        location_id = friend_location.get("locationId")
        assert location_id is None
