# -*- coding: utf-8 -*-
"""Cmdline tests."""
from pyicloud import cmdline
from . import PyiCloudServiceMock
from .const import AUTHENTICATED_USER, REQUIRES_2FA_USER, VALID_PASSWORD, VALID_2FA_CODE
from .const_findmyiphone import FMI_FAMILY_WORKING

import os
from six import PY2
import pickle
import pytest
from unittest import TestCase

if PY2:
    from mock import patch
else:
    from unittest.mock import patch  # pylint: disable=no-name-in-module,import-error


class TestCmdline(TestCase):
    """Cmdline test cases."""

    main = None

    def setUp(self):
        cmdline.PyiCloudService = PyiCloudServiceMock
        self.main = cmdline.main

    def test_no_arg(self):
        """Test no args."""
        with pytest.raises(SystemExit, match="2"):
            self.main()

        with pytest.raises(SystemExit, match="2"):
            self.main(None)

        with pytest.raises(SystemExit, match="2"):
            self.main([])

    def test_help(self):
        """Test the help command."""
        with pytest.raises(SystemExit, match="0"):
            self.main(["--help"])

    def test_username(self):
        """Test the username command."""
        # No username supplied
        with pytest.raises(SystemExit, match="2"):
            self.main(["--username"])

    @patch("keyring.get_password", return_value=None)
    @patch("getpass.getpass")
    def test_username_password_invalid(
        self, mock_getpass, mock_get_password
    ):  # pylint: disable=unused-argument
        """Test username and password commands."""
        # No password supplied
        mock_getpass.return_value = None
        with pytest.raises(SystemExit, match="2"):
            self.main(["--username", "invalid_user"])

        # Bad username or password
        mock_getpass.return_value = "invalid_pass"
        with pytest.raises(
            RuntimeError, match="Bad username or password for invalid_user"
        ):
            self.main(["--username", "invalid_user"])

        # We should not use getpass for this one, but we reset the password at login fail
        with pytest.raises(
            RuntimeError, match="Bad username or password for invalid_user"
        ):
            self.main(["--username", "invalid_user", "--password", "invalid_pass"])

    @patch("keyring.get_password", return_value=None)
    @patch("pyicloud.cmdline.input")
    def test_username_password_requires_2fa(
        self, mock_input, mock_get_password
    ):  # pylint: disable=unused-argument
        """Test username and password commands."""
        # Valid connection for the first time
        mock_input.return_value = VALID_2FA_CODE
        with pytest.raises(SystemExit, match="0"):
            # fmt: off
            self.main([
                '--username', REQUIRES_2FA_USER,
                '--password', VALID_PASSWORD,
                '--non-interactive',
            ])
            # fmt: on

    @patch("keyring.get_password", return_value=None)
    def test_device_outputfile(
        self, mock_get_password
    ):  # pylint: disable=unused-argument
        """Test the outputfile command."""
        with pytest.raises(SystemExit, match="0"):
            # fmt: off
            self.main([
                '--username', AUTHENTICATED_USER,
                '--password', VALID_PASSWORD,
                '--non-interactive',
                '--outputfile'
            ])
            # fmt: on

        devices = FMI_FAMILY_WORKING.get("content")
        for device in devices:
            file_name = device.get("name").strip().lower() + ".fmip_snapshot"

            pickle_file = open(file_name, "rb")
            assert pickle_file

            contents = []
            with pickle_file as opened_file:
                while True:
                    try:
                        contents.append(pickle.load(opened_file))
                    except EOFError:
                        break
            assert contents == [device]

            pickle_file.close()
            os.remove(file_name)
