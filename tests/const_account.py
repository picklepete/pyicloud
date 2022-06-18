"""Account test constants."""
from .const_login import FIRST_NAME

# Fakers
PAYMENT_METHOD_ID_1 = "PAYMENT_METHOD_ID_1"
PAYMENT_METHOD_ID_2 = "PAYMENT_METHOD_ID_2"
PAYMENT_METHOD_ID_3 = "PAYMENT_METHOD_ID_3"
PAYMENT_METHOD_ID_4 = "PAYMENT_METHOD_ID_4"

# Data
ACCOUNT_DEVICES_WORKING = {
    "devices": [
        {
            "serialNumber": "●●●●●●●NG123",
            "osVersion": "OSX;10.15.3",
            "modelLargePhotoURL2x": "https://statici.icloud.com/fmipmobile/deviceImages-4.0/MacBookPro/MacBookPro15,1-spacegray/online-infobox__2x.png",
            "modelLargePhotoURL1x": "https://statici.icloud.com/fmipmobile/deviceImages-4.0/MacBookPro/MacBookPro15,1-spacegray/online-infobox.png",
            "paymentMethods": [PAYMENT_METHOD_ID_3],
            "name": "MacBook Pro de " + FIRST_NAME,
            "imei": "",
            "model": "MacBookPro15,1",
            "udid": "MacBookPro15,1" + FIRST_NAME,
            "modelSmallPhotoURL2x": "https://statici.icloud.com/fmipmobile/deviceImages-4.0/MacBookPro/MacBookPro15,1-spacegray/online-sourcelist__2x.png",
            "modelSmallPhotoURL1x": "https://statici.icloud.com/fmipmobile/deviceImages-4.0/MacBookPro/MacBookPro15,1-spacegray/online-sourcelist.png",
            "modelDisplayName": 'MacBook Pro 15"',
        },
        {
            "serialNumber": "●●●●●●●UX123",
            "osVersion": "iOS;13.3",
            "modelLargePhotoURL2x": "https://statici.icloud.com/fmipmobile/deviceImages-4.0/iPhone/iPhone12,1-1-6-0/online-infobox__2x.png",
            "modelLargePhotoURL1x": "https://statici.icloud.com/fmipmobile/deviceImages-4.0/iPhone/iPhone12,1-1-6-0/online-infobox.png",
            "paymentMethods": [
                PAYMENT_METHOD_ID_4,
                PAYMENT_METHOD_ID_2,
                PAYMENT_METHOD_ID_1,
            ],
            "name": "iPhone de " + FIRST_NAME,
            "imei": "●●●●●●●●●●12345",
            "model": "iPhone12,1",
            "udid": "iPhone12,1" + FIRST_NAME,
            "modelSmallPhotoURL2x": "https://statici.icloud.com/fmipmobile/deviceImages-4.0/iPhone/iPhone12,1-1-6-0/online-sourcelist__2x.png",
            "modelSmallPhotoURL1x": "https://statici.icloud.com/fmipmobile/deviceImages-4.0/iPhone/iPhone12,1-1-6-0/online-sourcelist.png",
            "modelDisplayName": "iPhone 11",
        },
    ],
    "paymentMethods": [
        {
            "lastFourDigits": "333",
            "balanceStatus": "NOTAPPLICABLE",
            "suspensionReason": "ACTIVE",
            "id": PAYMENT_METHOD_ID_3,
            "type": "Boursorama Banque",
        },
        {
            "lastFourDigits": "444",
            "balanceStatus": "NOTAPPLICABLE",
            "suspensionReason": "ACTIVE",
            "id": PAYMENT_METHOD_ID_4,
            "type": "Carte Crédit Agricole",
        },
        {
            "lastFourDigits": "2222",
            "balanceStatus": "NOTAPPLICABLE",
            "suspensionReason": "ACTIVE",
            "id": PAYMENT_METHOD_ID_2,
            "type": "Lydia",
        },
        {
            "lastFourDigits": "111",
            "balanceStatus": "NOTAPPLICABLE",
            "suspensionReason": "ACTIVE",
            "id": PAYMENT_METHOD_ID_1,
            "type": "Boursorama Banque",
        },
    ],
}


ACCOUNT_STORAGE_WORKING = {
    "storageUsageByMedia": [
        {
            "mediaKey": "photos",
            "displayLabel": "Photos et vidéos",
            "displayColor": "ffcc00",
            "usageInBytes": 0,
        },
        {
            "mediaKey": "backup",
            "displayLabel": "Sauvegarde",
            "displayColor": "5856d6",
            "usageInBytes": 799008186,
        },
        {
            "mediaKey": "docs",
            "displayLabel": "Documents",
            "displayColor": "ff9500",
            "usageInBytes": 449092146,
        },
        {
            "mediaKey": "mail",
            "displayLabel": "Mail",
            "displayColor": "007aff",
            "usageInBytes": 1101522944,
        },
    ],
    "storageUsageInfo": {
        "compStorageInBytes": 0,
        "usedStorageInBytes": 2348632876,
        "totalStorageInBytes": 5368709120,
        "commerceStorageInBytes": 0,
    },
    "quotaStatus": {
        "overQuota": False,
        "haveMaxQuotaTier": False,
        "almost-full": False,
        "paidQuota": False,
    },
}
