"""Find My Friends test constants."""

# 14 a-Z0-9 characters followed  by ~~
PERSON_ID_1 = "XY02jdsS9XYaNa~~"
PERSON_ID_2 = "XYc9jdFsDCXYNa~~"

# UUID V4 from https://www.uuidgenerator.net/version4
LOCATION_ID_1 = "fdcd2aa1-0141-4c78-b7fe-73595ed15bad"
LOCATION_ID_2 = "db0edef7-f5b7-4f7f-bd89-ce0a6a079e65"

# Apple Park Visitor Center data
LOCATION_LATITUDE = 37.33291413003810
LOCATION_LONGITUDE = -122.00520223179473
COUNTRY_CODE = "US"
LOCALITY = "Cupertino"
COUNTRY = "United States"
STREET_ADDRESS = "10600 North Tantau Avenue"
ADMINISTRATIVE_AREA = "California"
STATE_CODE = "CA"
STREET_NAME = "North Tantau Avenue"
ZIPCODE = "95014"
FORMATTED_ADDRESS_LINES = [
    STREET_ADDRESS,
    "{}, {} {}".format(LOCALITY, STATE_CODE, ZIPCODE),
    COUNTRY,
]

FRIENDS_LOCATION_WORKING = [
    {
        "id": PERSON_ID_1,
        "status": None,
        "locationStatus": None,
        "location": {
            "batteryStatus": None,
            "tempLangForAddrAndPremises": None,
            "locationTimestamp": 0,
            "timestamp": 1586034872142,
            "altitude": 0,
            "labels": [],
            "longitude": LOCATION_LONGITUDE,
            "locSource": None,
            "locationId": LOCATION_ID_1,
            "horizontalAccuracy": 5.0,
            "floorLevel": 0,
            "address": {
                "countryCode": COUNTRY_CODE,
                "LOCALITY": LOCALITY,
                "formattedAddressLines": FORMATTED_ADDRESS_LINES,
                "country": COUNTRY,
                "streetAddress": STREET_ADDRESS,
                "administrativeArea": ADMINISTRATIVE_AREA,
                "stateCode": STATE_CODE,
                "streetName": STREET_NAME,
            },
            "latitude": LOCATION_LATITUDE,
            "isInaccurate": False,
            "verticalAccuracy": 4.0,
        },
    },
    {
        "id": PERSON_ID_2,
        "status": None,
        "locationStatus": None,
        "location": {
            "batteryStatus": None,
            "tempLangForAddrAndPremises": None,
            "locationTimestamp": 0,
            "timestamp": 15860348720496,
            "altitude": 0.0,
            "labels": [],
            "longitude": LOCATION_LONGITUDE,
            "locSource": None,
            "locationId": LOCATION_ID_2,
            "horizontalAccuracy": 65.0,
            "floorLevel": 0,
            "address": {
                "countryCode": COUNTRY_CODE,
                "LOCALITY": LOCALITY,
                "formattedAddressLines": FORMATTED_ADDRESS_LINES,
                "country": COUNTRY,
                "streetAddress": STREET_ADDRESS,
                "administrativeArea": ADMINISTRATIVE_AREA,
                "stateCode": STATE_CODE,
                "streetName": STREET_NAME,
            },
            "latitude": LOCATION_LATITUDE,
            "isInaccurate": False,
            "verticalAccuracy": 10.0,
        },
    },
]

FRIENDS_SERVICE_WORKING = {
    "locations": FRIENDS_LOCATION_WORKING,
}
