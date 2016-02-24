
class PyiCloudException(Exception):
    pass


class PyiCloudNoDevicesException(PyiCloudException):
    pass


class PyiCloudFailedLoginException(PyiCloudException):
    pass


class NoStoredPasswordAvailable(PyiCloudException):
    pass
