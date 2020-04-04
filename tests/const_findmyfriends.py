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
country_code = "US"
locality = "Cupertino"
country = "United States"
street_address = "10600 North Tantau Avenue"
administrative_area = "California"
state_code = "CA"
street_name = "North Tantau Avenue"
zipcode = "95014"
formatted_address_lines = [
    street_address,
    "{}, {} {}".format(locality, state_code, zipcode),
    country,
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
                "countryCode": country_code,
                "locality": locality,
                "formattedAddressLines": formatted_address_lines,
                "country": country,
                "streetAddress": street_address,
                "administrativeArea": administrative_area,
                "stateCode": state_code,
                "streetName": street_name,
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
                "countryCode": country_code,
                "locality": locality,
                "formattedAddressLines": formatted_address_lines,
                "country": country,
                "streetAddress": street_address,
                "administrativeArea": administrative_area,
                "stateCode": state_code,
                "streetName": street_name,
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
