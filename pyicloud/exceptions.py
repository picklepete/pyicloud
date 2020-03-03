
class PyiCloudException(Exception):
    pass


class PyiCloudNoDevicesException(PyiCloudException):
    pass


class PyiCloudAPIResponseError(PyiCloudException):
    def __init__(self, reason, code, retry=False):
        self.reason = reason
        self.code = code
        message = reason or ""
        if code:
            message += " (%s)" % code
        if retry:
            message += ". Retrying ..."

        super(PyiCloudAPIResponseError, self).__init__(message)


class PyiCloudFailedLoginException(PyiCloudException):
    pass


class PyiCloud2SARequiredError(PyiCloudException):
    def __init__(self, apple_id):
        message = "Two-step authentication required for account: %s" % apple_id
        super(PyiCloud2SARequiredError, self).__init__(message)


class PyiCloudNoDevicesException(Exception):
    pass


class NoStoredPasswordAvailable(PyiCloudException):
    pass


class PyiCloudServiceNotActivatedErrror(PyiCloudAPIResponseError):
    pass
