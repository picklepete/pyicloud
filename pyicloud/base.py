"""Library base file."""
from six import PY2, string_types
from uuid import uuid1
import inspect
import json
import logging
from requests import Session
from tempfile import gettempdir
from os import path, mkdir
from re import match
import http.cookiejar as cookielib
import getpass

from pyicloud.exceptions import (
    PyiCloudFailedLoginException,
    PyiCloudAPIResponseException,
    PyiCloud2SARequiredException,
    PyiCloudServiceNotActivatedException,
)
from pyicloud.services import (
    FindMyiPhoneServiceManager,
    CalendarService,
    UbiquityService,
    ContactsService,
    RemindersService,
    PhotosService,
    AccountService,
    DriveService,
)
from pyicloud.utils import get_password_from_keyring


LOGGER = logging.getLogger(__name__)


class PyiCloudPasswordFilter(logging.Filter):
    """Password log hider."""

    def __init__(self, password):
        super(PyiCloudPasswordFilter, self).__init__(password)

    def filter(self, record):
        message = record.getMessage()
        if self.name in message:
            record.msg = message.replace(self.name, "*" * 8)
            record.args = []

        return True


class PyiCloudSession(Session):
    """iCloud session."""

    def __init__(self, service):
        self.service = service
        Session.__init__(self)

    def request(self, method, url, **kwargs):  # pylint: disable=arguments-differ

        # Charge logging to the right service endpoint
        callee = inspect.stack()[2]
        module = inspect.getmodule(callee[0])
        request_logger = logging.getLogger(module.__name__).getChild("http")
        if self.service.password_filter not in request_logger.filters:
            request_logger.addFilter(self.service.password_filter)

        request_logger.debug("%s %s %s", method, url, kwargs.get("data", ""))

        has_retried = kwargs.get("retried")
        kwargs.pop("retried", None)
        response = super(PyiCloudSession, self).request(method, url, **kwargs)

        content_type = response.headers.get("Content-Type", "").split(";")[0]
        json_mimetypes = ["application/json", "text/json"]

        if not response.ok and content_type not in json_mimetypes:
            if has_retried is None and response.status_code == 450:
                api_error = PyiCloudAPIResponseException(
                    response.reason, response.status_code, retry=True
                )
                request_logger.debug(api_error)
                kwargs["retried"] = True
                return self.request(method, url, **kwargs)
            self._raise_error(response.status_code, response.reason)

        if content_type not in json_mimetypes:
            return response

        try:
            data = response.json()
        except:  # pylint: disable=bare-except
            request_logger.warning("Failed to parse response with JSON mimetype")
            return response

        request_logger.debug(data)

        if isinstance(data, dict):
            reason = data.get("errorMessage")
            reason = reason or data.get("reason")
            reason = reason or data.get("errorReason")
            if not reason and isinstance(data.get("error"), string_types):
                reason = data.get("error")
            if not reason and data.get("error"):
                reason = "Unknown reason"

            code = data.get("errorCode")
            if not code and data.get("serverErrorCode"):
                code = data.get("serverErrorCode")

                if reason:
                    self._raise_error(code, reason)

        return response

    def _raise_error(self, code, reason):
        if (
            self.service.requires_2sa
            and reason == "Missing X-APPLE-WEBAUTH-TOKEN cookie"
        ):
            raise PyiCloud2SARequiredException(self.service.user["apple_id"])
        if code in ("ZONE_NOT_FOUND", "AUTHENTICATION_FAILED"):
            reason = (
                "Please log into https://icloud.com/ to manually "
                "finish setting up your iCloud service"
            )
            api_error = PyiCloudServiceNotActivatedException(reason, code)
            LOGGER.error(api_error)

            raise (api_error)
        if code == "ACCESS_DENIED":
            reason = (
                reason + ".  Please wait a few minutes then try again."
                "The remote servers might be trying to throttle requests."
            )

        api_error = PyiCloudAPIResponseException(reason, code)
        LOGGER.error(api_error)
        raise api_error


class PyiCloudService(object):
    """
    A base authentication class for the iCloud service. Handles the
    authentication required to access iCloud services.

    Usage:
        from pyicloud import PyiCloudService
        pyicloud = PyiCloudService('username@apple.com', 'password')
        pyicloud.iphone.location()
    """

    HOME_ENDPOINT = "https://www.icloud.com"
    SETUP_ENDPOINT = "https://setup.icloud.com/setup/ws/1"

    def __init__(
        self,
        apple_id,
        password=None,
        cookie_directory=None,
        verify=True,
        client_id=None,
        with_family=True,
    ):
        if password is None:
            password = get_password_from_keyring(apple_id)

        self.data = {}
        self.client_id = client_id or str(uuid1()).upper()
        self.with_family = with_family
        self.user = {"apple_id": apple_id, "password": password}

        self.password_filter = PyiCloudPasswordFilter(password)
        LOGGER.addFilter(self.password_filter)

        self._base_login_url = "%s/login" % self.SETUP_ENDPOINT

        if cookie_directory:
            self._cookie_directory = path.expanduser(path.normpath(cookie_directory))
        else:
            topdir = path.join(gettempdir(), "pyicloud")
            self._cookie_directory = path.join(topdir, getpass.getuser())
            if not path.exists(topdir):
                mkdir(topdir, 0o777)
            if not path.exists(self._cookie_directory):
                mkdir(self._cookie_directory, 0o700)

        self.session = PyiCloudSession(self)
        self.session.verify = verify
        self.session.headers.update(
            {
                "Origin": self.HOME_ENDPOINT,
                "Referer": "%s/" % self.HOME_ENDPOINT,
                "User-Agent": "Opera/9.52 (X11; Linux i686; U; en)",
            }
        )

        cookiejar_path = self._get_cookiejar_path()
        self.session.cookies = cookielib.LWPCookieJar(filename=cookiejar_path)
        if path.exists(cookiejar_path):
            try:
                self.session.cookies.load()
                LOGGER.debug("Read cookies from %s", cookiejar_path)
            except:  # pylint: disable=bare-except
                # Most likely a pickled cookiejar from earlier versions.
                # The cookiejar will get replaced with a valid one after
                # successful authentication.
                LOGGER.warning("Failed to read cookiejar %s", cookiejar_path)

        self.params = {
            "clientBuildNumber": "17DHotfix5",
            "clientMasteringNumber": "17DHotfix5",
            "ckjsBuildVersion": "17DProjectDev77",
            "ckjsVersion": "2.0.5",
            "clientId": self.client_id,
        }

        self.authenticate()

        self._drive = None
        self._files = None
        self._photos = None

    def authenticate(self):
        """
        Handles authentication, and persists the X-APPLE-WEB-KB cookie so that
        subsequent logins will not cause additional e-mails from Apple.
        """

        LOGGER.info("Authenticating as %s", self.user["apple_id"])

        data = dict(self.user)

        # We authenticate every time, so "remember me" is not needed
        data.update({"extended_login": False})

        try:
            req = self.session.post(
                self._base_login_url, params=self.params, data=json.dumps(data)
            )
        except PyiCloudAPIResponseException as error:
            msg = "Invalid email/password combination."
            raise PyiCloudFailedLoginException(msg, error)

        self.data = req.json()
        self.params.update({"dsid": self.data["dsInfo"]["dsid"]})
        self._webservices = self.data["webservices"]

        if not path.exists(self._cookie_directory):
            mkdir(self._cookie_directory)
        self.session.cookies.save()
        LOGGER.debug("Cookies saved to %s", self._get_cookiejar_path())

        LOGGER.info("Authentication completed successfully")
        LOGGER.debug(self.params)

    def _get_cookiejar_path(self):
        """Get path for cookiejar file."""
        return path.join(
            self._cookie_directory,
            "".join([c for c in self.user.get("apple_id") if match(r"\w", c)]),
        )

    @property
    def requires_2sa(self):
        """Returns True if two-step authentication is required."""
        return (
            self.data.get("hsaChallengeRequired", False)
            and self.data["dsInfo"].get("hsaVersion", 0) >= 1
        )
        # FIXME: Implement 2FA for hsaVersion == 2  # pylint: disable=fixme

    @property
    def trusted_devices(self):
        """Returns devices trusted for two-step authentication."""
        request = self.session.get(
            "%s/listDevices" % self.SETUP_ENDPOINT, params=self.params
        )
        return request.json().get("devices")

    def send_verification_code(self, device):
        """Requests that a verification code is sent to the given device."""
        data = json.dumps(device)
        request = self.session.post(
            "%s/sendVerificationCode" % self.SETUP_ENDPOINT,
            params=self.params,
            data=data,
        )
        return request.json().get("success", False)

    def validate_verification_code(self, device, code):
        """Verifies a verification code received on a trusted device."""
        device.update({"verificationCode": code, "trustBrowser": True})
        data = json.dumps(device)

        try:
            self.session.post(
                "%s/validateVerificationCode" % self.SETUP_ENDPOINT,
                params=self.params,
                data=data,
            )
        except PyiCloudAPIResponseException as error:
            if error.code == -21669:
                # Wrong verification code
                return False
            raise

        # Re-authenticate, which will both update the HSA data, and
        # ensure that we save the X-APPLE-WEBAUTH-HSA-TRUST cookie.
        self.authenticate()

        return not self.requires_2sa

    def _get_webservice_url(self, ws_key):
        """Get webservice URL, raise an exception if not exists."""
        if self._webservices.get(ws_key) is None:
            raise PyiCloudServiceNotActivatedException(
                "Webservice not available", ws_key
            )
        return self._webservices[ws_key]["url"]

    @property
    def devices(self):
        """Returns all devices."""
        service_root = self._get_webservice_url("findme")
        return FindMyiPhoneServiceManager(
            service_root, self.session, self.params, self.with_family
        )

    @property
    def iphone(self):
        """Returns the iPhone."""
        return self.devices[0]

    @property
    def account(self):
        """Gets the 'Account' service."""
        service_root = self._get_webservice_url("account")
        return AccountService(service_root, self.session, self.params)

    @property
    def files(self):
        """Gets the 'File' service."""
        if not self._files:
            service_root = self._get_webservice_url("ubiquity")
            self._files = UbiquityService(service_root, self.session, self.params)
        return self._files

    @property
    def photos(self):
        """Gets the 'Photo' service."""
        if not self._photos:
            service_root = self._get_webservice_url("ckdatabasews")
            self._photos = PhotosService(service_root, self.session, self.params)
        return self._photos

    @property
    def calendar(self):
        """Gets the 'Calendar' service."""
        service_root = self._get_webservice_url("calendar")
        return CalendarService(service_root, self.session, self.params)

    @property
    def contacts(self):
        """Gets the 'Contacts' service."""
        service_root = self._get_webservice_url("contacts")
        return ContactsService(service_root, self.session, self.params)

    @property
    def reminders(self):
        """Gets the 'Reminders' service."""
        service_root = self._get_webservice_url("reminders")
        return RemindersService(service_root, self.session, self.params)

    @property
    def drive(self):
        """Gets the 'Drive' service."""
        if not self._drive:
            self._drive = DriveService(
                service_root=self._get_webservice_url("drivews"),
                document_root=self._get_webservice_url("docws"),
                session=self.session,
                params=self.params,
            )
        return self._drive

    def __unicode__(self):
        return "iCloud API: %s" % self.user.get("apple_id")

    def __str__(self):
        as_unicode = self.__unicode__()
        if PY2:
            return as_unicode.encode("utf-8", "ignore")
        return as_unicode

    def __repr__(self):
        return "<%s>" % str(self)
