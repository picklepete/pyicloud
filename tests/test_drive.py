"""Drive service tests."""
from unittest import TestCase
from . import PyiCloudServiceMock
from .const import AUTHENTICATED_USER, VALID_PASSWORD
import pytest

# pylint: disable=pointless-statement
class DriveServiceTest(TestCase):
    """"Drive service tests"""

    service = None

    def setUp(self):
        self.service = PyiCloudServiceMock(AUTHENTICATED_USER, VALID_PASSWORD)

    def test_root(self):
        """Test the root folder."""
        drive = self.service.drive
        assert drive.name == ""
        assert drive.type == "folder"
        assert drive.size is None
        assert drive.date_changed is None
        assert drive.date_modified is None
        assert drive.date_last_open is None
        assert drive.dir() == ["Keynote", "Numbers", "Pages", "Preview", "pyiCloud"]

    def test_folder_app(self):
        """Test the /Preview folder."""
        folder = self.service.drive["Preview"]
        assert folder.name == "Preview"
        assert folder.type == "app_library"
        assert folder.size is None
        assert folder.date_changed is None
        assert folder.date_modified is None
        assert folder.date_last_open is None
        with pytest.raises(KeyError, match="No items in folder, status: ID_INVALID"):
            assert folder.dir()

    def test_folder_not_exists(self):
        """Test the /not_exists folder."""
        with pytest.raises(KeyError, match="No child named 'not_exists' exists"):
            self.service.drive["not_exists"]

    def test_folder(self):
        """Test the /pyiCloud folder."""
        folder = self.service.drive["pyiCloud"]
        assert folder.name == "pyiCloud"
        assert folder.type == "folder"
        assert folder.size is None
        assert folder.date_changed is None
        assert folder.date_modified is None
        assert folder.date_last_open is None
        assert folder.dir() == ["Test"]

    def test_subfolder(self):
        """Test the /pyiCloud/Test folder."""
        folder = self.service.drive["pyiCloud"]["Test"]
        assert folder.name == "Test"
        assert folder.type == "folder"
        assert folder.size is None
        assert folder.date_changed is None
        assert folder.date_modified is None
        assert folder.date_last_open is None
        assert folder.dir() == ["Document scanné 2.pdf", "Scanned document 1.pdf"]

    def test_subfolder_file(self):
        """Test the /pyiCloud/Test/Scanned document 1.pdf file."""
        folder = self.service.drive["pyiCloud"]["Test"]
        file = folder["Scanned document 1.pdf"]
        assert file.name == "Scanned document 1.pdf"
        assert file.type == "file"
        assert file.size == 21644358
        assert str(file.date_changed) == "2020-05-03 00:16:17"
        assert str(file.date_modified) == "2020-05-03 00:15:17"
        assert str(file.date_last_open) == "2020-05-03 00:24:25"
        assert file.dir() is None

    def test_file_open(self):
        """Test the /pyiCloud/Test/Scanned document 1.pdf file open."""
        file = self.service.drive["pyiCloud"]["Test"]["Scanned document 1.pdf"]
        with file.open(stream=True) as response:
            assert response.raw
