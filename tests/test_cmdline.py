"""Cmdline tests."""
import sys
import pytest
from unittest import TestCase
if sys.version_info >= (3, 3):
    from unittest.mock import patch
else:
    from mock import patch

from pyicloud import cmdline

from . import PyiCloudServiceMock

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
        """Test the username and password command."""
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

