# -*- coding: utf-8 -*-
"""Login test constants."""
from .const_account_family import (
    FIRST_NAME,
    LAST_NAME,
    PERSON_ID,
    FULL_NAME,
    PRIMARY_EMAIL,
    APPLE_ID_EMAIL,
    ICLOUD_ID_EMAIL,
)

PERSON_ID = (FIRST_NAME + LAST_NAME).lower()
NOTIFICATION_ID = "12345678-1234-1234-1234-123456789012" + PERSON_ID
A_DS_ID = "123456-12-12345678-1234-1234-1234-123456789012" + PERSON_ID
WIDGET_KEY = "widget_key" + PERSON_ID

# Data
AUTH_OK = {
    "authType": "hsa2"
}

LOGIN_WORKING = {
    "dsInfo": {
        "lastName": LAST_NAME,
        "iCDPEnabled": False,
        "tantorMigrated": True,
        "dsid": PERSON_ID,
        "hsaEnabled": True,
        "ironcadeMigrated": True,
        "locale": "fr-fr_FR",
        "brZoneConsolidated": False,
        "isManagedAppleID": False,
        "gilligan-invited": "true",
        "appleIdAliases": [APPLE_ID_EMAIL, ICLOUD_ID_EMAIL],
        "hsaVersion": 2,
        "isPaidDeveloper": False,
        "countryCode": "FRA",
        "notificationId": NOTIFICATION_ID,
        "primaryEmailVerified": True,
        "aDsID": A_DS_ID,
        "locked": False,
        "hasICloudQualifyingDevice": True,
        "primaryEmail": PRIMARY_EMAIL,
        "appleIdEntries": [
            {"isPrimary": True, "type": "EMAIL", "value": PRIMARY_EMAIL},
            {"type": "EMAIL", "value": APPLE_ID_EMAIL},
            {"type": "EMAIL", "value": ICLOUD_ID_EMAIL},
        ],
        "gilligan-enabled": "true",
        "fullName": FULL_NAME,
        "languageCode": "fr-fr",
        "appleId": PRIMARY_EMAIL,
        "firstName": FIRST_NAME,
        "iCloudAppleIdAlias": ICLOUD_ID_EMAIL,
        "notesMigrated": True,
        "hasPaymentInfo": False,
        "pcsDeleted": False,
        "appleIdAlias": APPLE_ID_EMAIL,
        "brMigrated": True,
        "statusCode": 2,
        "familyEligible": True,
    },
    "hasMinimumDeviceForPhotosWeb": True,
    "iCDPEnabled": False,
    "webservices": {
        "reminders": {
            "url": "https://p31-remindersws.icloud.com:443",
            "status": "active",
        },
        "notes": {"url": "https://p38-notesws.icloud.com:443", "status": "active"},
        "mail": {"url": "https://p38-mailws.icloud.com:443", "status": "active"},
        "ckdatabasews": {
            "pcsRequired": True,
            "url": "https://p31-ckdatabasews.icloud.com:443",
            "status": "active",
        },
        "photosupload": {
            "pcsRequired": True,
            "url": "https://p31-uploadphotosws.icloud.com:443",
            "status": "active",
        },
        "photos": {
            "pcsRequired": True,
            "uploadUrl": "https://p31-uploadphotosws.icloud.com:443",
            "url": "https://p31-photosws.icloud.com:443",
            "status": "active",
        },
        "drivews": {
            "pcsRequired": True,
            "url": "https://p31-drivews.icloud.com:443",
            "status": "active",
        },
        "uploadimagews": {
            "url": "https://p31-uploadimagews.icloud.com:443",
            "status": "active",
        },
        "schoolwork": {},
        "cksharews": {"url": "https://p31-ckshare.icloud.com:443", "status": "active"},
        "findme": {"url": "https://p31-fmipweb.icloud.com:443", "status": "active"},
        "ckdeviceservice": {"url": "https://p31-ckdevice.icloud.com:443"},
        "iworkthumbnailws": {
            "url": "https://p31-iworkthumbnailws.icloud.com:443",
            "status": "active",
        },
        "calendar": {
            "url": "https://p31-calendarws.icloud.com:443",
            "status": "active",
        },
        "docws": {
            "pcsRequired": True,
            "url": "https://p31-docws.icloud.com:443",
            "status": "active",
        },
        "settings": {
            "url": "https://p31-settingsws.icloud.com:443",
            "status": "active",
        },
        "ubiquity": {
            "url": "https://p31-ubiquityws.icloud.com:443",
            "status": "active",
        },
        "streams": {"url": "https://p31-streams.icloud.com:443", "status": "active"},
        "keyvalue": {
            "url": "https://p31-keyvalueservice.icloud.com:443",
            "status": "active",
        },
        "archivews": {
            "url": "https://p31-archivews.icloud.com:443",
            "status": "active",
        },
        "push": {"url": "https://p31-pushws.icloud.com:443", "status": "active"},
        "iwmb": {"url": "https://p31-iwmb.icloud.com:443", "status": "active"},
        "iworkexportws": {
            "url": "https://p31-iworkexportws.icloud.com:443",
            "status": "active",
        },
        "geows": {"url": "https://p31-geows.icloud.com:443", "status": "active"},
        "account": {
            "iCloudEnv": {"shortId": "p", "vipSuffix": "prod"},
            "url": "https://p31-setup.icloud.com:443",
            "status": "active",
        },
        "fmf": {"url": "https://p31-fmfweb.icloud.com:443", "status": "active"},
        "contacts": {
            "url": "https://p31-contactsws.icloud.com:443",
            "status": "active",
        },
    },
    "pcsEnabled": True,
    "configBag": {
        "urls": {
            "accountCreateUI": "https://appleid.apple.com/widget/account/?widgetKey="
            + WIDGET_KEY
            + "#!create",
            "accountLoginUI": "https://idmsa.apple.com/appleauth/auth/signin?widgetKey="
            + WIDGET_KEY,
            "accountLogin": "https://setup.icloud.com/setup/ws/1/accountLogin",
            "accountRepairUI": "https://appleid.apple.com/widget/account/?widgetKey="
            + WIDGET_KEY
            + "#!repair",
            "downloadICloudTerms": "https://setup.icloud.com/setup/ws/1/downloadLiteTerms",
            "repairDone": "https://setup.icloud.com/setup/ws/1/repairDone",
            "accountAuthorizeUI": "https://idmsa.apple.com/appleauth/auth/authorize/signin?client_id="
            + WIDGET_KEY,
            "vettingUrlForEmail": "https://id.apple.com/IDMSEmailVetting/vetShareEmail",
            "accountCreate": "https://setup.icloud.com/setup/ws/1/createLiteAccount",
            "getICloudTerms": "https://setup.icloud.com/setup/ws/1/getTerms",
            "vettingUrlForPhone": "https://id.apple.com/IDMSEmailVetting/vetSharePhone",
        },
        "accountCreateEnabled": "true",
    },
    "hsaTrustedBrowser": True,
    "appsOrder": [
        "mail",
        "contacts",
        "calendar",
        "photos",
        "iclouddrive",
        "notes3",
        "reminders",
        "pages",
        "numbers",
        "keynote",
        "newspublisher",
        "fmf",
        "find",
        "settings",
    ],
    "version": 2,
    "isExtendedLogin": True,
    "pcsServiceIdentitiesIncluded": True,
    "hsaChallengeRequired": False,
    "requestInfo": {"country": "FR", "timeZone": "GMT+1", "region": "IDF"},
    "pcsDeleted": False,
    "iCloudInfo": {"SafariBookmarksHasMigratedToCloudKit": True},
    "apps": {
        "calendar": {},
        "reminders": {},
        "keynote": {"isQualifiedForBeta": True},
        "settings": {"canLaunchWithOneFactor": True},
        "mail": {},
        "numbers": {"isQualifiedForBeta": True},
        "photos": {},
        "pages": {"isQualifiedForBeta": True},
        "notes3": {},
        "find": {"canLaunchWithOneFactor": True},
        "iclouddrive": {},
        "newspublisher": {"isHidden": True},
        "fmf": {},
        "contacts": {},
    },
}

# Setup data
LOGIN_2FA = {
    "dsInfo": {
        "lastName": LAST_NAME,
        "iCDPEnabled": False,
        "tantorMigrated": True,
        "dsid": PERSON_ID,
        "hsaEnabled": True,
        "ironcadeMigrated": True,
        "locale": "fr-fr_FR",
        "brZoneConsolidated": False,
        "isManagedAppleID": False,
        "gilligan-invited": "true",
        "appleIdAliases": [APPLE_ID_EMAIL, ICLOUD_ID_EMAIL],
        "hsaVersion": 2,
        "isPaidDeveloper": False,
        "countryCode": "FRA",
        "notificationId": NOTIFICATION_ID,
        "primaryEmailVerified": True,
        "aDsID": A_DS_ID,
        "locked": False,
        "hasICloudQualifyingDevice": True,
        "primaryEmail": PRIMARY_EMAIL,
        "appleIdEntries": [
            {"isPrimary": True, "type": "EMAIL", "value": PRIMARY_EMAIL},
            {"type": "EMAIL", "value": APPLE_ID_EMAIL},
            {"type": "EMAIL", "value": ICLOUD_ID_EMAIL},
        ],
        "gilligan-enabled": "true",
        "fullName": FULL_NAME,
        "languageCode": "fr-fr",
        "appleId": PRIMARY_EMAIL,
        "firstName": FIRST_NAME,
        "iCloudAppleIdAlias": ICLOUD_ID_EMAIL,
        "notesMigrated": True,
        "hasPaymentInfo": True,
        "pcsDeleted": False,
        "appleIdAlias": APPLE_ID_EMAIL,
        "brMigrated": True,
        "statusCode": 2,
        "familyEligible": True,
    },
    "hasMinimumDeviceForPhotosWeb": True,
    "iCDPEnabled": False,
    "webservices": {
        "reminders": {
            "url": "https://p31-remindersws.icloud.com:443",
            "status": "active",
        },
        "notes": {"url": "https://p38-notesws.icloud.com:443", "status": "active"},
        "mail": {"url": "https://p38-mailws.icloud.com:443", "status": "active"},
        "ckdatabasews": {
            "pcsRequired": True,
            "url": "https://p31-ckdatabasews.icloud.com:443",
            "status": "active",
        },
        "photosupload": {
            "pcsRequired": True,
            "url": "https://p31-uploadphotosws.icloud.com:443",
            "status": "active",
        },
        "photos": {
            "pcsRequired": True,
            "uploadUrl": "https://p31-uploadphotosws.icloud.com:443",
            "url": "https://p31-photosws.icloud.com:443",
            "status": "active",
        },
        "drivews": {
            "pcsRequired": True,
            "url": "https://p31-drivews.icloud.com:443",
            "status": "active",
        },
        "uploadimagews": {
            "url": "https://p31-uploadimagews.icloud.com:443",
            "status": "active",
        },
        "schoolwork": {},
        "cksharews": {"url": "https://p31-ckshare.icloud.com:443", "status": "active"},
        "findme": {"url": "https://p31-fmipweb.icloud.com:443", "status": "active"},
        "ckdeviceservice": {"url": "https://p31-ckdevice.icloud.com:443"},
        "iworkthumbnailws": {
            "url": "https://p31-iworkthumbnailws.icloud.com:443",
            "status": "active",
        },
        "calendar": {
            "url": "https://p31-calendarws.icloud.com:443",
            "status": "active",
        },
        "docws": {
            "pcsRequired": True,
            "url": "https://p31-docws.icloud.com:443",
            "status": "active",
        },
        "settings": {
            "url": "https://p31-settingsws.icloud.com:443",
            "status": "active",
        },
        "ubiquity": {
            "url": "https://p31-ubiquityws.icloud.com:443",
            "status": "active",
        },
        "streams": {"url": "https://p31-streams.icloud.com:443", "status": "active"},
        "keyvalue": {
            "url": "https://p31-keyvalueservice.icloud.com:443",
            "status": "active",
        },
        "archivews": {
            "url": "https://p31-archivews.icloud.com:443",
            "status": "active",
        },
        "push": {"url": "https://p31-pushws.icloud.com:443", "status": "active"},
        "iwmb": {"url": "https://p31-iwmb.icloud.com:443", "status": "active"},
        "iworkexportws": {
            "url": "https://p31-iworkexportws.icloud.com:443",
            "status": "active",
        },
        "geows": {"url": "https://p31-geows.icloud.com:443", "status": "active"},
        "account": {
            "iCloudEnv": {"shortId": "p", "vipSuffix": "prod"},
            "url": "https://p31-setup.icloud.com:443",
            "status": "active",
        },
        "fmf": {"url": "https://p31-fmfweb.icloud.com:443", "status": "active"},
        "contacts": {
            "url": "https://p31-contactsws.icloud.com:443",
            "status": "active",
        },
    },
    "pcsEnabled": True,
    "configBag": {
        "urls": {
            "accountCreateUI": "https://appleid.apple.com/widget/account/?widgetKey="
            + WIDGET_KEY
            + "#!create",
            "accountLoginUI": "https://idmsa.apple.com/appleauth/auth/signin?widgetKey="
            + WIDGET_KEY,
            "accountLogin": "https://setup.icloud.com/setup/ws/1/accountLogin",
            "accountRepairUI": "https://appleid.apple.com/widget/account/?widgetKey="
            + WIDGET_KEY
            + "#!repair",
            "downloadICloudTerms": "https://setup.icloud.com/setup/ws/1/downloadLiteTerms",
            "repairDone": "https://setup.icloud.com/setup/ws/1/repairDone",
            "accountAuthorizeUI": "https://idmsa.apple.com/appleauth/auth/authorize/signin?client_id="
            + WIDGET_KEY,
            "vettingUrlForEmail": "https://id.apple.com/IDMSEmailVetting/vetShareEmail",
            "accountCreate": "https://setup.icloud.com/setup/ws/1/createLiteAccount",
            "getICloudTerms": "https://setup.icloud.com/setup/ws/1/getTerms",
            "vettingUrlForPhone": "https://id.apple.com/IDMSEmailVetting/vetSharePhone",
        },
        "accountCreateEnabled": "true",
    },
    "hsaTrustedBrowser": False,
    "appsOrder": [
        "mail",
        "contacts",
        "calendar",
        "photos",
        "iclouddrive",
        "notes3",
        "reminders",
        "pages",
        "numbers",
        "keynote",
        "newspublisher",
        "fmf",
        "find",
        "settings",
    ],
    "version": 2,
    "isExtendedLogin": True,
    "pcsServiceIdentitiesIncluded": False,
    "hsaChallengeRequired": True,
    "requestInfo": {"country": "FR", "timeZone": "GMT+1", "region": "IDF"},
    "pcsDeleted": False,
    "iCloudInfo": {"SafariBookmarksHasMigratedToCloudKit": True},
    "apps": {
        "calendar": {},
        "reminders": {},
        "keynote": {"isQualifiedForBeta": True},
        "settings": {"canLaunchWithOneFactor": True},
        "mail": {},
        "numbers": {"isQualifiedForBeta": True},
        "photos": {},
        "pages": {"isQualifiedForBeta": True},
        "notes3": {},
        "find": {"canLaunchWithOneFactor": True},
        "iclouddrive": {},
        "newspublisher": {"isHidden": True},
        "fmf": {},
        "contacts": {},
    },
}

TRUSTED_DEVICE_1 = {
    "deviceType": "SMS",
    "areaCode": "",
    "phoneNumber": "*******58",
    "deviceId": "1",
}
TRUSTED_DEVICES = {"devices": [TRUSTED_DEVICE_1]}

VERIFICATION_CODE_OK = {"success": True}
VERIFICATION_CODE_KO = {"success": False}
