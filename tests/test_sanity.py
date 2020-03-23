"""Sanity test."""
from unittest2 import TestCase

from pyicloud.cmdline import main


class SanityTestCase(TestCase):
    """Sanity test."""
    def test_basic_sanity(self):
        """Sanity test."""
        with self.assertRaises(SystemExit):
            main(['--help'])
