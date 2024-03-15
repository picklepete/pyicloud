"""Find my iPhone service."""
import json

from six import PY2, text_type

from pyicloud.exceptions import PyiCloudNoDevicesException

DEVICE_BATTERY_LEVEL = "batteryLevel"
DEVICE_BATTERY_STATUS = "batteryStatus"
DEVICE_CLASS = "deviceClass"
DEVICE_DISPLAY_NAME = "deviceDisplayName"
DEVICE_FROM_FAMILY = "fmlyShare"
DEVICE_ID = "id"
DEVICE_IS_MAC = "isMac"
DEVICE_LOCATION = "location"
DEVICE_LOCATION_HORIZONTAL_ACCURACY = "horizontalAccuracy"
DEVICE_LOCATION_LATITUDE = "latitude"
DEVICE_LOCATION_LONGITUDE = "longitude"
DEVICE_LOCATION_POSITION_TYPE = "positionType"
DEVICE_LOST_MODE_CAPABLE = "lostModeCapable"
DEVICE_LOW_POWER_MODE = "lowPowerMode"
DEVICE_MODEL = "deviceModel"
DEVICE_MODEL_RAW = "rawDeviceModel"
DEVICE_MSG_MAX_LENGTH = "maxMsgChar"
DEVICE_NAME = "name"
DEVICE_PERSON_ID = "prsId"
DEVICE_STATUS = "deviceStatus"
DEVICE_CAN_WIPE = "canWipeAfterLock"

class FindMyiPhoneServiceManager(object):
    """The 'Find my iPhone' iCloud service"""

DEVICE_STATUS_ONLINE = "online"
DEVICE_STATUS_OFFLINE = "offline"
DEVICE_STATUS_PENDING = "pending"
DEVICE_STATUS_UNREGISTERED = "unregistered"
DEVICE_STATUS_ERROR = "error"
DEVICE_STATUS_CODES = {
    "200": DEVICE_STATUS_ONLINE,
    "201": DEVICE_STATUS_OFFLINE,
    "203": DEVICE_STATUS_PENDING,
    "204": DEVICE_STATUS_UNREGISTERED,
}


class FindMyiPhoneService(object):
    """
    The 'Find my iPhone' iCloud service,
    connects to iCloud and returns devices,
    including battery state and location.
    """

    def __init__(self, service_root, session, params, with_family=False):
        self.session = session
        self.params = params
        self.with_family = with_family
        fmip_endpoint = "%s/fmipservice/client/web" % service_root
        self._fmip_refresh_url = "%s/refreshClient" % fmip_endpoint
        self._fmip_sound_url = "%s/playSound" % fmip_endpoint
        self._fmip_message_url = "%s/sendMessage" % fmip_endpoint
        self._fmip_lost_url = "%s/lostDevice" % fmip_endpoint
        self._fmip_erase_url = "%s/remoteWipeWithUserAuth" % fmip_endpoint
        self._devices = {}  # Need to call refresh_client() to fill/update it

    def refresh_client(self):
        """
        Refreshes devices to ensures that the data data is up-to-date.
        """
        req = self.session.post(
            self._fmip_refresh_url,
            params=self.params,
            data=json.dumps(
                {
                    "clientContext": {
                        "fmly": self.with_family,
                        "shouldLocate": True,
                        "selectedDevice": "all",
                        "deviceListVersion": 1,
                    }
                }
            ),
        )
        data = req.json()

        for device_info in data["content"]:
            device_id = device_info["id"]
            if device_id not in self._devices:
                self._devices[device_id] = AppleDevice(
                    device_info,
                    self.session,
                    self.params,
                    sound_url=self._fmip_sound_url,
                    lost_url=self._fmip_lost_url,
                    message_url=self._fmip_message_url,
                    erase_url=self._fmip_erase_url
                )
            else:
                self._devices[device_id].update(device_info)

        if not self._devices:
            raise PyiCloudNoDevicesException()

    @property
    def devices(self):
        """Return all devices."""
        return self._devices

    def device(self, key):
        """Return one device."""
        if isinstance(key, int):
            if PY2:
                key = self.keys()[key]
            else:
                key = list(self.keys())[key]
        return self._devices[key]

    def __getattr__(self, attr):
        return getattr(self._devices, attr)

    def __unicode__(self):
        return text_type(self._devices)

    def __str__(self):
        return f"{self._devices}"

    def __repr__(self):
        return "<%s: {with_family: %s, devices: %s}>" % (type(self).__name__, str(self))


class AppleDevice(object):
    """Apple device."""

    def __init__(
        self, attrs, session, params, sound_url=None, lost_url=None, message_url=None, erase_url=None
    ):
        self._attrs = attrs
        self._session = session
        self._params = params

        self.sound_url = sound_url
        self.lost_url = lost_url
        self.message_url = message_url
        self.erase_url = erase_url

    def update(self, attrs):
        self._attrs = attrs

    def play_sound(self, subject="Find My iPhone Alert"):
        """Send a request to the device to play a sound.
        It's possible to pass a custom message by changing the `subject`.
        """
        data = json.dumps(
            {"device": self.id, "subject": subject, "clientContext": {"fmly": True}}
        )
        self._session.post(self.sound_url, params=self._params, data=data)

    def display_message(
        self, subject="Find My iPhone Alert", message="This is a note", sounds=False
    ):
        """Send a request to the device to play a sound.

        It's possible to pass a custom message by changing the `subject`.
        """
        data = json.dumps(
            {
                "device": self.id,
                "subject": subject,
                "sound": sounds,
                "userText": True,
                "text": message,
            }
        )
        self._session.post(self.message_url, params=self._params, data=data)

    def lost_device(
        self, number, text="This iPhone has been lost. Please call me.", newpasscode=""
    ):
        """Send a request to the device to trigger 'lost mode'.

        The device will show the message in `text`, and if a number has
        been passed, then the person holding the device can call
        the number without entering the passcode.
        """
        data = json.dumps(
            {
                "text": text,
                "userText": True,
                "ownerNbr": number,
                "lostModeEnabled": True,
                "trackingEnabled": True,
                "device": self.id,
                "passcode": newpasscode,
            }
        )
        self._session.post(self.lost_url, params=self._params, data=data)

    def erase_device(
        self, text="This iPhone has been lost. Please call me.", newpasscode="", erasetoken=None
    ):
        if (erasetoken==None):
            print("This function requires an erase token. Obtain one by using the fmipWebAuthenticate() function")
            return
        
        """Send a request to the device to start a remote erase."""
        data = json.dumps(
            {
                "authToken": erasetoken,
                "text": text,
                "device": self.id,
                "passcode": newpasscode
            }
        )
        self._session.post(self.erase_url, params=self._params, data=data)
    @property
    def attrs(self):
        return self._attrs

    @property
    def batteryLevel(self):
        return self._attrs.get(DEVICE_BATTERY_LEVEL)

    @property
    def batteryStatus(self):
        return self._attrs[DEVICE_BATTERY_STATUS]

    @property
    def deviceClass(self):
        return self._attrs[DEVICE_CLASS]

    @property
    def deviceDisplayName(self):
        return self._attrs[DEVICE_DISPLAY_NAME]

    @property
    def deviceModel(self):
        return self._attrs.get(DEVICE_MODEL)

    @property
    def deviceStatus(self):
        return DEVICE_STATUS_CODES.get(
            self._attrs.get(DEVICE_STATUS), DEVICE_STATUS_ERROR
        )

    @property
    def fmlyShare(self):
        return self._attrs[DEVICE_FROM_FAMILY]

    @property
    def id(self):
        return self._attrs[DEVICE_ID]

    @property
    def isMac(self):
        return self._attrs[DEVICE_IS_MAC]

    @property
    def canWipe(self):
        return self._attrs[DEVICE_CAN_WIPE]

    @property
    def location(self):
        return self._attrs.get(DEVICE_LOCATION)

    @property
    def horizontalAccuracy(self):
        if self.location is None:
            return None
        return self.location.get(DEVICE_LOCATION_HORIZONTAL_ACCURACY)

    @property
    def latitude(self):
        if self.location is None:
            return None
        return self.location.get(DEVICE_LOCATION_LATITUDE)

    @property
    def longitude(self):
        if self.location is None:
            return None
        return self.location.get(DEVICE_LOCATION_LONGITUDE)

    @property
    def positionType(self):
        if self.location is None:
            return None
        return self.location.get(DEVICE_LOCATION_POSITION_TYPE)

    @property
    def lostModeCapable(self):
        return self._attrs.get(DEVICE_LOST_MODE_CAPABLE)

    @property
    def lowPowerMode(self):
        return self._attrs.get(DEVICE_LOW_POWER_MODE)

    @property
    def maxMsgChar(self):
        return self._attrs.get(DEVICE_MSG_MAX_LENGTH)

    @property
    def name(self):
        return self._attrs.get(DEVICE_NAME)

    @property
    def prsId(self):
        return self._attrs.get(DEVICE_PERSON_ID)

    @property
    def rawDeviceModel(self):
        return self._attrs.get(DEVICE_MODEL_RAW)

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        return self._attrs[key]

    def __getattr__(self, attr):
        return getattr(self._attrs, attr)

    def __unicode__(self):
        display_name = self["deviceDisplayName"]
        name = self["name"]
        return "%s: %s" % (display_name, name)

    def __str__(self):
        return f"{self['deviceDisplayName']}: {self['name']}"

    def __repr__(self):
        return "<AppleDevice(%s)>" % str(self)
