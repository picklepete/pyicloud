"""Account family test constants."""

# Fakers
FIRST_NAME = "Quentin"
LAST_NAME = "TARANTINO"
FULL_NAME = FIRST_NAME + " " + LAST_NAME
PERSON_ID = (FIRST_NAME + LAST_NAME).lower()
PRIMARY_EMAIL = PERSON_ID + "@hotmail.fr"
APPLE_ID_EMAIL = PERSON_ID + "@me.com"
ICLOUD_ID_EMAIL = PERSON_ID + "@icloud.com"

MEMBER_1_FIRST_NAME = "John"
MEMBER_1_LAST_NAME = "TRAVOLTA"
MEMBER_1_FULL_NAME = MEMBER_1_FIRST_NAME + " " + MEMBER_1_LAST_NAME
MEMBER_1_PERSON_ID = (MEMBER_1_FIRST_NAME + MEMBER_1_LAST_NAME).lower()
MEMBER_1_APPLE_ID = MEMBER_1_PERSON_ID + "@icloud.com"

MEMBER_2_FIRST_NAME = "Uma"
MEMBER_2_LAST_NAME = "THURMAN"
MEMBER_2_FULL_NAME = MEMBER_2_FIRST_NAME + " " + MEMBER_2_LAST_NAME
MEMBER_2_PERSON_ID = (MEMBER_2_FIRST_NAME + MEMBER_2_LAST_NAME).lower()
MEMBER_2_APPLE_ID = MEMBER_2_PERSON_ID + "@outlook.fr"

FAMILY_ID = "family_" + PERSON_ID

# Data
ACCOUNT_FAMILY_WORKING = {
    "status-message": "Member of a family.",
    "familyInvitations": [],
    "outgoingTransferRequests": [],
    "isMemberOfFamily": True,
    "family": {
        "familyId": FAMILY_ID,
        "transferRequests": [],
        "invitations": [],
        "organizer": PERSON_ID,
        "members": [PERSON_ID, MEMBER_2_PERSON_ID, MEMBER_1_PERSON_ID],
        "outgoingTransferRequests": [],
        "etag": "12",
    },
    "familyMembers": [
        {
            "lastName": LAST_NAME,
            "dsid": PERSON_ID,
            "originalInvitationEmail": PRIMARY_EMAIL,
            "fullName": FULL_NAME,
            "ageClassification": "ADULT",
            "appleIdForPurchases": PRIMARY_EMAIL,
            "appleId": PRIMARY_EMAIL,
            "familyId": FAMILY_ID,
            "firstName": FIRST_NAME,
            "hasParentalPrivileges": True,
            "hasScreenTimeEnabled": False,
            "hasAskToBuyEnabled": False,
            "hasSharePurchasesEnabled": True,
            "shareMyLocationEnabledFamilyMembers": [],
            "hasShareMyLocationEnabled": True,
            "dsidForPurchases": PERSON_ID,
        },
        {
            "lastName": MEMBER_2_LAST_NAME,
            "dsid": MEMBER_2_PERSON_ID,
            "originalInvitationEmail": MEMBER_2_APPLE_ID,
            "fullName": MEMBER_2_FULL_NAME,
            "ageClassification": "ADULT",
            "appleIdForPurchases": MEMBER_2_APPLE_ID,
            "appleId": MEMBER_2_APPLE_ID,
            "familyId": FAMILY_ID,
            "firstName": MEMBER_2_FIRST_NAME,
            "hasParentalPrivileges": False,
            "hasScreenTimeEnabled": False,
            "hasAskToBuyEnabled": False,
            "hasSharePurchasesEnabled": False,
            "hasShareMyLocationEnabled": False,
            "dsidForPurchases": MEMBER_2_PERSON_ID,
        },
        {
            "lastName": MEMBER_1_LAST_NAME,
            "dsid": MEMBER_1_PERSON_ID,
            "originalInvitationEmail": MEMBER_1_APPLE_ID,
            "fullName": MEMBER_1_FULL_NAME,
            "ageClassification": "ADULT",
            "appleIdForPurchases": MEMBER_1_APPLE_ID,
            "appleId": MEMBER_1_APPLE_ID,
            "familyId": FAMILY_ID,
            "firstName": MEMBER_1_FIRST_NAME,
            "hasParentalPrivileges": False,
            "hasScreenTimeEnabled": False,
            "hasAskToBuyEnabled": False,
            "hasSharePurchasesEnabled": True,
            "hasShareMyLocationEnabled": True,
            "dsidForPurchases": MEMBER_1_PERSON_ID,
        },
    ],
    "status": 0,
    "showAddMemberButton": True,
}
