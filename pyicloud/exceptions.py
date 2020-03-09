
class PyiCloudException(Exception):
    pass


# API
class PyiCloudAPIResponseException(PyiCloudException):
    def __init__(self, reason, code=None, retry=False):
        self.reason = reason
        self.code = code
        message = reason or ""
        if code:
            message += " (%s)" % code
        if retry:
            message += ". Retrying ..."

        super(PyiCloudAPIResponseException, self).__init__(message)


class PyiCloudServiceNotActivatedException(PyiCloudAPIResponseException):
    pass


# Login
class PyiCloudFailedLoginException(PyiCloudException):
    pass


class PyiCloud2SARequiredException(PyiCloudException):
    def __init__(self, apple_id):
        message = "Two-step authentication required for account: %s" % apple_id
        super(PyiCloud2SARequiredException, self).__init__(message)


class PyiCloudNoStoredPasswordAvailableException(PyiCloudException):
    pass


# Webservice specific
class PyiCloudNoDevicesException(PyiCloudException):
    pass
