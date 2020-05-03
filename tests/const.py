# -*- coding: utf-8 -*-
"""Test constants."""
from .const_account_family import PRIMARY_EMAIL, APPLE_ID_EMAIL, ICLOUD_ID_EMAIL

# Base
AUTHENTICATED_USER = PRIMARY_EMAIL
REQUIRES_2SA_USER = "requires_2sa_user"
VALID_USERS = [AUTHENTICATED_USER, REQUIRES_2SA_USER, APPLE_ID_EMAIL, ICLOUD_ID_EMAIL]
VALID_PASSWORD = "valid_password"

CLIENT_ID = "client_id"
