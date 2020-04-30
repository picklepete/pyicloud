"""Base service tests."""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created by magus0219[magus0219@gmail.com] on 2020/4/30
from unittest import TestCase
import pytest
from pyicloud.base import PyiCloudSession
from pyicloud.exceptions import PyiCloudAPIResponseException


class TestBase(TestCase):
    """Test pyicloud.base"""

    def test_raise_exception_gone(self):
        """Test raise exception of Gone"""
        # pylint: disable=R0201
        class MockService(object):
            """Mock service of this test"""

            # pylint: disable=no-init
            def requires_2sa(self):
                """Mock method"""
                # pylint: disable=R0201
                return True

        mock_session = PyiCloudSession(service=MockService())

        with pytest.raises(PyiCloudAPIResponseException) as excinfo:
            getattr(mock_session, "_raise_error")(code=410, reason="Gone")
        assert (
            str(excinfo.value)
            == "Gone. Please fetch Object(e.g. PhotoAsset) again to refresh download url. (410)"
        )
