"""Library tests."""

from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException
class PyiCloudServiceMock(PyiCloudService):
    """Mocked PyiCloudService."""
    def __init__(
            self,
            apple_id,
            password=None,
            cookie_directory=None,
            verify=True,
            client_id=None,
            with_family=True
        ):
        PyiCloudService.__init__(self, apple_id, password, cookie_directory, verify, client_id, with_family)

    def authenticate(self):
        if not self.user.get("apple_id") or self.user.get("apple_id") != "valid_user":
            raise PyiCloudFailedLoginException("Invalid email/password combination.", None)
        if not self.user.get("password") or self.user.get("password") != "valid_pass":
            raise PyiCloudFailedLoginException("Invalid email/password combination.", None)
        
        self.params.update({'dsid': 'ID'})
        self._webservices = {
            'account': {
                'url': 'account_url',
            },
            'findme': {
                'url': 'findme_url',
            },
            'calendar': {
                'url': 'calendar_url',
            },
            'contacts': {
                'url': 'contacts_url',
            },
            'reminders': {
                'url': 'reminders_url',
            }
        }