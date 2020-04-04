"""Library tests."""
import json
from requests import Session, Response

from pyicloud import base
from pyicloud.exceptions import PyiCloudFailedLoginException
from pyicloud.services.findmyiphone import FindMyiPhoneServiceManager, AppleDevice

from .const import (
    AUTHENTICATED_USER,
    REQUIRES_2SA_USER,
    VALID_USERS,
    VALID_PASSWORD,
)
from .const_login import (
    LOGIN_WORKING,
    LOGIN_2SA,
    TRUSTED_DEVICES,
    TRUSTED_DEVICE_1,
    VERIFICATION_CODE_OK,
    VERIFICATION_CODE_KO,
)
from .const_account import ACCOUNT_DEVICES_WORKING, ACCOUNT_STORAGE_WORKING
from .const_account_family import ACCOUNT_FAMILY_WORKING
from .const_findmyiphone import FMI_FAMILY_WORKING


class ResponseMock(Response):
    """Mocked Response."""

    def __init__(self, result, status_code=200):
        Response.__init__(self)
        self.result = result
        self.status_code = status_code

    @property
    def text(self):
        return json.dumps(self.result)


class PyiCloudSessionMock(base.PyiCloudSession):
    """Mocked PyiCloudSession."""

    def request(self, method, url, **kwargs):
        data = json.loads(kwargs.get("data", "{}"))

        # Login
        if self.service.SETUP_ENDPOINT in url:
            if "login" in url and method == "POST":
                if (
                    data.get("apple_id") not in VALID_USERS
                    or data.get("password") != VALID_PASSWORD
                ):
                    self._raise_error(None, "Unknown reason")
                if (
                    data.get("apple_id") == REQUIRES_2SA_USER
                    and data.get("password") == VALID_PASSWORD
                ):
                    return ResponseMock(LOGIN_2SA)
                return ResponseMock(LOGIN_WORKING)

            if "listDevices" in url and method == "GET":
                return ResponseMock(TRUSTED_DEVICES)

            if "sendVerificationCode" in url and method == "POST":
                if data == TRUSTED_DEVICE_1:
                    return ResponseMock(VERIFICATION_CODE_OK)
                return ResponseMock(VERIFICATION_CODE_KO)

            if "validateVerificationCode" in url and method == "POST":
                TRUSTED_DEVICE_1.update({"verificationCode": "0", "trustBrowser": True})
                if data == TRUSTED_DEVICE_1:
                    self.service.user["apple_id"] = AUTHENTICATED_USER
                    return ResponseMock(VERIFICATION_CODE_OK)
                self._raise_error(None, "FOUND_CODE")

        # Account
        if "device/getDevices" in url and method == "GET":
            return ResponseMock(ACCOUNT_DEVICES_WORKING)
        if "family/getFamilyDetails" in url and method == "GET":
            return ResponseMock(ACCOUNT_FAMILY_WORKING)
        if "setup/ws/1/storageUsageInfo" in url and method == "GET":
            return ResponseMock(ACCOUNT_STORAGE_WORKING)

        # Find My iPhone
        if "fmi" in url and method == "POST":
            return ResponseMock(FMI_FAMILY_WORKING)

        return None


class PyiCloudServiceMock(base.PyiCloudService):
    """Mocked PyiCloudService."""

    def __init__(
        self,
        apple_id,
        password=None,
        cookie_directory=None,
        verify=True,
        client_id=None,
        with_family=True,
    ):
        base.PyiCloudSession = PyiCloudSessionMock
        base.PyiCloudService.__init__(
            self, apple_id, password, cookie_directory, verify, client_id, with_family
        )
