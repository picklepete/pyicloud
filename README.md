## pyicloud

PyiCloud is a module which allows pythonistas to interact with iCloud webservices. It's powered by the fantastic [requests](https://github.com/kennethreitz/requests) HTTP library.

At its core, PyiCloud connects to iCloud using your username and password, then performs calendar and iPhone queries against their API.

### Authentication

Authentication is as simple as passing your username and password to the `PyiCloudService` class:

```python
>>> from pyicloud import PyiCloudService
>>> api = PyiCloudService('jappleseed@apple.com', 'password')
```

In the event that the username/password combination is invalid, a `PyiCloudFailedLoginException` exception is thrown.

### Find My iPhone

Once you have successfully authenticated, you can start querying your data!

#### Location

Returns the device's last known location. The Find My iPhone app must have been installed and initialized.

```python
>>> api.iphone.location()
{u'timeStamp': 1357753796553, u'locationFinished': True, u'longitude': -0.14189, u'positionType': u'GPS', u'locationType': None, u'latitude': 51.501364, u'isOld': False, u'horizontalAccuracy': 5.0}
```

#### Status

The Find My iPhone response is quite bloated, so for simplicity's sake this method will return a subset of the properties.

```python
>>> api.iphone.status()
{'deviceDisplayName': u'iPhone 5', 'deviceStatus': u'200', 'batteryLevel': 0.6166913, 'name': u"Peter's iPhone"}
```

If you wish to request further properties, you may do so by passing in a list of property names.

#### Play Sound

Sends a request to the device to play a sound, if you wish pass a custom message you can do so by changing the subject arg.

```python
>>> api.iphone.play_sound()
```

A few moments later, the device will play a ringtone, display the default notification ("Find My iPhone Alert") and a confirmation email will be sent to you.

#### Lost Mode

Lost mode is slightly different to the "Play Sound" functionality in that it allows the person who picks up the phone to call a specific phone number *without having to enter the passcode*. Just like "Play Sound" you may pass a custom message which the device will display, if it's not overriden the custom message of "This iPhone has been lost. Please call me." is used.

```python
>>> phone_number = '555-373-383'
>>> message = 'Thief! Return my phone immediately.'
>>> api.iphone.lost_device(phone_number, message)
```

### Calendar

The calendar webservice currently only supports fetching events.

#### Events

Returns this month's events:

```python
api.calendar.events()
```

Or, between a specific date range:

```python
from_dt = datetime(2012, 1, 1)
to_dt = datetime(2012, 1, 31)
api.calendar.events(from_dt, to_dt)
```
