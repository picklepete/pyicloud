# Code samples

## From [@Quentame](https://github.com/Quentame)

pyicloud version: 0.9.6

### Configuration: 2SA + store cookie

https://github.com/home-assistant/core/blob/dev/homeassistant/components/icloud/config_flow.py

### Utilization: fetches

https://github.com/home-assistant/core/blob/dev/homeassistant/components/icloud/account.py


## From [@toothrobber](https://github.com/toothrobber)

pyicloud version: 0.9.1

```python

import os
import click
import datetime
from pyicloud import PyiCloudService


print("Setup Time Zone")
time.strftime("%X %x %Z")
os.environ["TZ"] = "America/New_York"


print("Py iCloud Services")
api = PyiCloudService("your@me.com", "password")

if api.requires_2fa:
    print("Two-factor authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print(
            "  %s: %s"
            % (i, device.get("deviceName", "SMS to %s" % device.get("phoneNumber")))
        )

    device = click.prompt("Which device would you like to use?", default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print("Failed to send verification code")
        sys.exit(1)

    code = click.prompt("Please enter validation code")
    if not api.validate_verification_code(device, code):
        print("Failed to verify verification code")
        sys.exit(1)

#
# Devices
#
print("Devices")
print(api.devices)
print(api.devices[0])
print(api.iphone)


#
# Location
#
print("Location")
print(api.iphone.location())


#
# Status
#
print("Status")
print(api.iphone.status())

#
# Play Sound
#
# api.iphone.play_sound()


#
# Events
#
print("Events")
print(api.calendar.events())
from_dt = datetime.date(2018, 1, 1)
to_dt = datetime.date(2018, 1, 31)
print(api.calendar.events(from_dt, to_dt))


# ========
# Contacts
# ========
print("Contacts")
for c in api.contacts.all():
    print(c.get("firstName"), c.get("phones"))


# =======================
# File Storage (Ubiquity)
# =======================

# You can access documents stored in your iCloud account by using the
# ``files`` property's ``dir`` method:
print("File Storage")
print(api.files.dir())
```

## From [@ixs](https://github.com/ixs)

### Debug build of pyicloud

This example allows to use tools like mitmproxy, fiddler, charles or similiar
things to debug the data sent on the wire.

In addition, the underlying requests module and the http.client are asked, to
output all data sent and received to stdout.

This uses code taken from [How do I disable the security certificate check in Python requests](https://stackoverflow.com/questions/15445981/how-do-i-disable-the-security-certificate-check-in-python-requests)
and [Log all requests from the python-requests module](https://stackoverflow.com/questions/16337511/log-all-requests-from-the-python-requests-module)


```python
#!/usr/bin/env python3

import contextlib
import http.client
import logging
import requests
import warnings
from pprint import pprint
from pyicloud import PyiCloudService
from urllib3.exceptions import InsecureRequestWarning

# Handle certificate warnings by ignoring them
old_merge_environment_settings = requests.Session.merge_environment_settings


@contextlib.contextmanager
def no_ssl_verification():
    opened_adapters = set()

    def merge_environment_settings(self, url, proxies, stream, verify, cert):
        # Verification happens only once per connection so we need to close
        # all the opened adapters once we're done. Otherwise, the effects of
        # verify=False persist beyond the end of this context manager.
        opened_adapters.add(self.get_adapter(url))

        settings = old_merge_environment_settings(
            self, url, proxies, stream, verify, cert
        )
        settings["verify"] = False

        return settings

    requests.Session.merge_environment_settings = merge_environment_settings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", InsecureRequestWarning)
            yield
    finally:
        requests.Session.merge_environment_settings = old_merge_environment_settings

        for adapter in opened_adapters:
            try:
                adapter.close()
            except:
                pass


# Monkeypatch the http client for full debugging output
httpclient_logger = logging.getLogger("http.client")


def httpclient_logging_patch(level=logging.DEBUG):
    """Enable HTTPConnection debug logging to the logging framework"""

    def httpclient_log(*args):
        httpclient_logger.log(level, " ".join(args))

    # mask the print() built-in in the http.client module to use
    # logging instead
    http.client.print = httpclient_log
    # enable debugging
    http.client.HTTPConnection.debuglevel = 1


# Enable general debug logging
logging.basicConfig(level=logging.DEBUG)

httpclient_logging_patch()

api = PyiCloudService(username, password)
if api.requires_2sa:
    print("Two-factor authentication required. Your trusted devices are:")

    devices = api.trusted_devices
    for i, device in enumerate(devices):
        print(
            "  %s: %s"
            % (i, device.get("deviceName", "SMS to %s") % device.get("phoneNumber"))
        )

    device = click.prompt("Which device would you like to use?", default=0)
    device = devices[device]
    if not api.send_verification_code(device):
        print("Failed to send verification code")
        sys.exit(1)

    code = click.prompt("Please enter validation code")
    if not api.validate_verification_code(device, code):
        print("Failed to verify verification code")
        sys.exit(1)

# This request will not fail, even if using intercepting proxies.
with no_ssl_verification():
    pprint(api.account)
```
