
class PyiCloudException(Exception):
    pass


class PyiCloudNoDevicesException(PyiCloudException):
    pass


class PyiCloudAPIResponseException(PyiCloudException):
    def __init__(self, reason, code, retry=False):
        self.reason = reason
        self.code = code
        message = reason or ""
        if code:
            message += " (%s)" % code
        if retry:
            message += ". Retrying ..."

        super(PyiCloudAPIResponseException, self).__init__(message)


class PyiCloudFailedLoginException(PyiCloudException):
    pass


class PyiCloud2SARequiredException(PyiCloudException):
    def __init__(self, apple_id):
        message = "Two-step authentication required for account: %s" % apple_id
        super(PyiCloud2SARequiredException, self).__init__(message)


class PyiCloudNoStoredPasswordAvailableException(PyiCloudException):
    pass


class PyiCloudServiceNotActivatedException(PyiCloudAPIResponseException):
    pass
