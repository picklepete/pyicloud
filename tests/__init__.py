"""Library tests."""

from pyicloud import base
from pyicloud.exceptions import PyiCloudFailedLoginException
from pyicloud.services.findmyiphone import FindMyiPhoneServiceManager, AppleDevice


AUTHENTICATED_USER = "authenticated_user"
REQUIRES_2SA_USER = "requires_2sa_user"
VALID_USERS = [AUTHENTICATED_USER, REQUIRES_2SA_USER]


class PyiCloudServiceMock(base.PyiCloudService):
    """Mocked PyiCloudService."""
    def __init__(
            self,
            apple_id,
            password=None,
            cookie_directory=None,
            verify=True,
            client_id=None,
            with_family=True
        ):
        base.PyiCloudService.__init__(self, apple_id, password, cookie_directory, verify, client_id, with_family)
        base.FindMyiPhoneServiceManager = FindMyiPhoneServiceManagerMock

    def authenticate(self):
        if not self.user.get("apple_id") or self.user.get("apple_id") not in VALID_USERS:
            raise PyiCloudFailedLoginException("Invalid email/password combination.", None)
        if not self.user.get("password") or self.user.get("password") != "valid_pass":
            raise PyiCloudFailedLoginException("Invalid email/password combination.", None)
        
        self.params.update({'dsid': 'ID'})
        self._webservices = {
            'account': {
                'url': 'account_url',
            },
            'findme': {
                'url': 'findme_url',
            },
            'calendar': {
                'url': 'calendar_url',
            },
            'contacts': {
                'url': 'contacts_url',
            },
            'reminders': {
                'url': 'reminders_url',
            }
        }

    @property
    def requires_2sa(self):
        return self.user["apple_id"] is REQUIRES_2SA_USER

    @property
    def trusted_devices(self):
        return  [
            {"deviceType": "SMS", "areaCode": "", "phoneNumber": "*******58", "deviceId": "1"}
        ]
    
    def send_verification_code(self, device):
        return device
    
    def validate_verification_code(self, device, code):
        if not device or code != 0:
            self.user["apple_id"] = AUTHENTICATED_USER
        self.authenticate()
        return not self.requires_2sa


IPHONE_DEVICE_ID = "X1x/X&x="
IPHONE_DEVICE = AppleDevice(
    {
        "msg": {
            "strobe": False,
            "userText": False,
            "playSound": True,
            "vibrate": True,
            "createTimestamp": 1568031021347,
            "statusCode": "200"
        },
        "canWipeAfterLock": True,
        "baUUID": "",
        "wipeInProgress": False,
        "lostModeEnabled": False,
        "activationLocked": True,
        "passcodeLength": 6,
        "deviceStatus": "200",
        "deviceColor": "1-6-0",
        "features": {
            "MSG": True,
            "LOC": True,
            "LLC": False,
            "CLK": False,
            "TEU": True,
            "LMG": False,
            "SND": True,
            "CLT": False,
            "LKL": False,
            "SVP": False,
            "LST": True,
            "LKM": False,
            "WMG": True,
            "SPN": False,
            "XRM": False,
            "PIN": False,
            "LCK": True,
            "REM": False,
            "MCS": False,
            "CWP": False,
            "KEY": False,
            "KPD": False,
            "WIP": True
        },
        "lowPowerMode": True,
        "rawDeviceModel": "iPhone11,8",
        "id": IPHONE_DEVICE_ID,
        "remoteLock": None,
        "isLocating": True,
        "modelDisplayName": "iPhone",
        "lostTimestamp": "",
        "batteryLevel": 0.47999998927116394,
        "mesg": None,
        "locationEnabled": True,
        "lockedTimestamp": None,
        "locFoundEnabled": False,
        "snd": {
            "createTimestamp": 1568031021347,
            "statusCode": "200"
        },
        "fmlyShare": False,
        "lostDevice": {
            "stopLostMode": False,
            "emailUpdates": False,
            "userText": True,
            "sound": False,
            "ownerNbr": "",
            "text": "",
            "createTimestamp": 1558383841233,
            "statusCode": "2204"
        },
        "lostModeCapable": True,
        "wipedTimestamp": None,
        "deviceDisplayName": "iPhone XR",
        "prsId": None,
        "audioChannels": [],
        "locationCapable": True,
        "batteryStatus": "NotCharging",
        "trackingInfo": None,
        "name": "Quentin's iPhone",
        "isMac": False,
        "thisDevice": False,
        "deviceClass": "iPhone",
        "location": {
            "isOld": False,
            "isInaccurate": False,
            "altitude": 0.0,
            "positionType": "GPS",
            "latitude": 46.012345678,
            "floorLevel": 0,
            "horizontalAccuracy": 12.012345678,
            "locationType": "",
            "timeStamp": 1568827039692,
            "locationFinished": False,
            "verticalAccuracy": 0.0,
            "longitude": 5.012345678
        },
        "deviceModel": "iphoneXR-1-6-0",
        "maxMsgChar": 160,
        "darkWake": False,
        "remoteWipe": None
    },
    None,
    None,
    None
)

DEVICES = {
    IPHONE_DEVICE_ID: IPHONE_DEVICE,
}


class FindMyiPhoneServiceManagerMock(FindMyiPhoneServiceManager):
    """Mocked FindMyiPhoneServiceManager."""
    def __init__(self, service_root, session, params, with_family=False):
        FindMyiPhoneServiceManager.__init__(self, service_root, session, params, with_family)

    def refresh_client(self):
        self._devices = DEVICES
