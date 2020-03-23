"""Cmdline tests."""
from pyicloud import cmdline
from . import PyiCloudServiceMock, DEVICES

import os
import sys
import pickle
import pytest
from unittest import TestCase
if sys.version_info >= (3, 3):
    from unittest.mock import patch  # pylint: disable=no-name-in-module,import-error
else:
    from mock import patch

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
            self.main(['--help'])

    def test_username(self):
        """Test the username command."""
        # No username supplied
        with pytest.raises(SystemExit, match="2"):
            self.main(['--username'])

    @patch("getpass.getpass")
    def test_username_password(self, getpass):
        """Test username and password commands."""
        # No password supplied
        getpass.return_value = None
        with pytest.raises(SystemExit, match="2"):
            self.main(['--username', 'invalid_user'])

        # Bad username or password
        getpass.return_value = "invalid_pass"
        with pytest.raises(RuntimeError, match="Bad username or password for invalid_user"):
            self.main(['--username', 'invalid_user'])

        # We should not use getpass for this one, but we reset the password at login fail
        with pytest.raises(RuntimeError, match="Bad username or password for invalid_user"):
            self.main(['--username', 'invalid_user', '--password', 'invalid_pass'])

    def test_device_outputfile(self):
        """Test the username and password command."""
        self.main([
            '--username', 'valid_user',
            '--password', 'valid_pass',
            '--non-interactive',
            '--outputfile'
        ])

        for key in DEVICES:
            file_name = DEVICES[key].content['name'].strip().lower() + ".fmip_snapshot"

            pickle_file = open(file_name, "rb")
            assert pickle_file

            contents = []
            with pickle_file as opened_file:
                while True:
                    try:
                        contents.append(pickle.load(opened_file))
                    except EOFError:
                        break
            assert contents == [DEVICES[key].content]

            pickle_file.close()
            os.remove(file_name)