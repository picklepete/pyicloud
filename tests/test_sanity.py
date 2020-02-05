from unittest2 import TestCase

from pyicloud.cmdline import main


class SanityTestCase(TestCase):
    def test_basic_sanity(self):
        with self.assertRaises(SystemExit):
            main(['--help'])
