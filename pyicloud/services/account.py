"""Account service."""
from __future__ import division
from six import PY2, python_2_unicode_compatible
from collections import OrderedDict

from pyicloud.utils import underscore_to_camelcase


class AccountService(object):
    """The 'Account' iCloud service."""

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root

        self._devices = []
        self._family = []
        self._storage = None

        self._acc_endpoint = "%s/setup/web" % self._service_root
        self._acc_devices_url = "%s/device/getDevices" % self._acc_endpoint
        self._acc_family_details_url = "%s/family/getFamilyDetails" % self._acc_endpoint
        self._acc_family_member_photo_url = (
            "%s/family/getMemberPhoto" % self._acc_endpoint
        )
        self._acc_storage_url = "https://setup.icloud.com/setup/ws/1/storageUsageInfo"

    @property
    def devices(self):
        """Returns current paired devices."""
        if not self._devices:
            req = self.session.get(self._acc_devices_url, params=self.params)
            response = req.json()

            for device_info in response["devices"]:
                self._devices.append(AccountDevice(device_info))

        return self._devices

    @property
    def family(self):
        """Returns family members."""
        if not self._family:
            req = self.session.get(self._acc_family_details_url, params=self.params)
            response = req.json()

            for member_info in response["familyMembers"]:
                self._family.append(
                    FamilyMember(
                        member_info,
                        self.session,
                        self.params,
                        self._acc_family_member_photo_url,
                    )
                )

        return self._family

    @property
    def storage(self):
        """Returns storage infos."""
        if not self._storage:
            req = self.session.get(self._acc_storage_url, params=self.params)
            response = req.json()

            self._storage = AccountStorage(response)

        return self._storage

    def __unicode__(self):
        return "{devices: %s, family: %s, storage: %s bytes free}" % (
            len(self.devices),
            len(self.family),
            self.storage.usage.available_storage_in_bytes,
        )

    def __str__(self):
        as_unicode = self.__unicode__()
        if PY2:
            return as_unicode.encode("utf-8", "ignore")
        return as_unicode

    def __repr__(self):
        return "<%s: %s>" % (type(self).__name__, str(self))


@python_2_unicode_compatible
class AccountDevice(dict):
    """Account device."""

    def __getattr__(self, key):
        return self[underscore_to_camelcase(key)]

    def __unicode__(self):
        return "{model: %s, name: %s}" % (self.model_display_name, self.name)

    def __str__(self):
        as_unicode = self.__unicode__()
        if PY2:
            return as_unicode.encode("utf-8", "ignore")
        return as_unicode

    def __repr__(self):
        return "<%s: %s>" % (type(self).__name__, str(self))


class FamilyMember(object):
    """A family member."""

    def __init__(self, member_info, session, params, acc_family_member_photo_url):
        self._attrs = member_info
        self._session = session
        self._params = params
        self._acc_family_member_photo_url = acc_family_member_photo_url

    @property
    def last_name(self):
        """Gets the last name."""
        return self._attrs.get("lastName")

    @property
    def dsid(self):
        """Gets the dsid."""
        return self._attrs.get("dsid")

    @property
    def original_invitation_email(self):
        """Gets the original invitation."""
        return self._attrs.get("originalInvitationEmail")

    @property
    def full_name(self):
        """Gets the full name."""
        return self._attrs.get("fullName")

    @property
    def age_classification(self):
        """Gets the age classification."""
        return self._attrs.get("ageClassification")

    @property
    def apple_id_for_purchases(self):
        """Gets the apple id for purchases."""
        return self._attrs.get("appleIdForPurchases")

    @property
    def apple_id(self):
        """Gets the apple id."""
        return self._attrs.get("appleId")

    @property
    def family_id(self):
        """Gets the family id."""
        return self._attrs.get("familyId")

    @property
    def first_name(self):
        """Gets the first name."""
        return self._attrs.get("firstName")

    @property
    def has_parental_privileges(self):
        """Has parental privileges."""
        return self._attrs.get("hasParentalPrivileges")

    @property
    def has_screen_time_enabled(self):
        """Has screen time enabled."""
        return self._attrs.get("hasScreenTimeEnabled")

    @property
    def has_ask_to_buy_enabled(self):
        """Has to ask for buying."""
        return self._attrs.get("hasAskToBuyEnabled")

    @property
    def has_share_purchases_enabled(self):
        """Has share purshases."""
        return self._attrs.get("hasSharePurchasesEnabled")

    @property
    def share_my_location_enabled_family_members(self):
        """Has share my location with family."""
        return self._attrs.get("shareMyLocationEnabledFamilyMembers")

    @property
    def has_share_my_location_enabled(self):
        """Has share my location."""
        return self._attrs.get("hasShareMyLocationEnabled")

    @property
    def dsid_for_purchases(self):
        """Gets the dsid for purchases."""
        return self._attrs.get("dsidForPurchases")

    def get_photo(self):
        """Returns the photo."""
        params_photo = dict(self._params)
        params_photo.update({"memberId": self.dsid})
        return self._session.get(
            self._acc_family_member_photo_url, params=params_photo, stream=True
        )

    def __getitem__(self, key):
        if self._attrs.get(key):
            return self._attrs[key]
        return getattr(self, key)

    def __unicode__(self):
        return "{name: %s, age_classification: %s}" % (
            self.full_name,
            self.age_classification,
        )

    def __str__(self):
        as_unicode = self.__unicode__()
        if PY2:
            return as_unicode.encode("utf-8", "ignore")
        return as_unicode

    def __repr__(self):
        return "<%s: %s>" % (type(self).__name__, str(self))


class AccountStorageUsageForMedia(object):
    """Storage used for a specific media type into the account."""

    def __init__(self, usage_data):
        self.usage_data = usage_data

    @property
    def key(self):
        """Gets the key."""
        return self.usage_data["mediaKey"]

    @property
    def label(self):
        """Gets the label."""
        return self.usage_data["displayLabel"]

    @property
    def color(self):
        """Gets the HEX color."""
        return self.usage_data["displayColor"]

    @property
    def usage_in_bytes(self):
        """Gets the usage in bytes."""
        return self.usage_data["usageInBytes"]

    def __unicode__(self):
        return "{key: %s, usage: %s bytes}" % (self.key, self.usage_in_bytes)

    def __str__(self):
        as_unicode = self.__unicode__()
        if PY2:
            return as_unicode.encode("utf-8", "ignore")
        return as_unicode

    def __repr__(self):
        return "<%s: %s>" % (type(self).__name__, str(self))


class AccountStorageUsage(object):
    """Storage used for a specific media type into the account."""

    def __init__(self, usage_data, quota_data):
        self.usage_data = usage_data
        self.quota_data = quota_data

    @property
    def comp_storage_in_bytes(self):
        """Gets the comp storage in bytes."""
        return self.usage_data["compStorageInBytes"]

    @property
    def used_storage_in_bytes(self):
        """Gets the used storage in bytes."""
        return self.usage_data["usedStorageInBytes"]

    @property
    def used_storage_in_percent(self):
        """Gets the used storage in percent."""
        return round(self.used_storage_in_bytes * 100 / self.total_storage_in_bytes, 2)

    @property
    def available_storage_in_bytes(self):
        """Gets the available storage in bytes."""
        return self.total_storage_in_bytes - self.used_storage_in_bytes

    @property
    def available_storage_in_percent(self):
        """Gets the available storage in percent."""
        return round(
            self.available_storage_in_bytes * 100 / self.total_storage_in_bytes, 2
        )

    @property
    def total_storage_in_bytes(self):
        """Gets the total storage in bytes."""
        return self.usage_data["totalStorageInBytes"]

    @property
    def commerce_storage_in_bytes(self):
        """Gets the commerce storage in bytes."""
        return self.usage_data["commerceStorageInBytes"]

    @property
    def quota_over(self):
        """Gets the over quota."""
        return self.quota_data["overQuota"]

    @property
    def quota_tier_max(self):
        """Gets the max tier quota."""
        return self.quota_data["haveMaxQuotaTier"]

    @property
    def quota_almost_full(self):
        """Gets the almost full quota."""
        return self.quota_data["almost-full"]

    @property
    def quota_paid(self):
        """Gets the paid quota."""
        return self.quota_data["paidQuota"]

    def __unicode__(self):
        return "%s%% used of %s bytes" % (
            self.used_storage_in_percent,
            self.total_storage_in_bytes,
        )

    def __str__(self):
        as_unicode = self.__unicode__()
        if PY2:
            return as_unicode.encode("utf-8", "ignore")
        return as_unicode

    def __repr__(self):
        return "<%s: %s>" % (type(self).__name__, str(self))


class AccountStorage(object):
    """Storage of the account."""

    def __init__(self, storage_data):
        self.usage = AccountStorageUsage(
            storage_data.get("storageUsageInfo"), storage_data.get("quotaStatus")
        )
        self.usages_by_media = OrderedDict()

        for usage_media in storage_data.get("storageUsageByMedia"):
            self.usages_by_media[usage_media["mediaKey"]] = AccountStorageUsageForMedia(
                usage_media
            )

    def __unicode__(self):
        return "{usage: %s, usages_by_media: %s}" % (self.usage, self.usages_by_media)

    def __str__(self):
        as_unicode = self.__unicode__()
        if PY2:
            return as_unicode.encode("utf-8", "ignore")
        return as_unicode

    def __repr__(self):
        return "<%s: %s>" % (type(self).__name__, str(self))
