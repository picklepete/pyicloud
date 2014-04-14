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

### Devices

You can list which devices associated with your account by using the `devices` property:

```python
>>> api.devices
{
u'i9vbKRGIcLYqJnXMd1b257kUWnoyEBcEh6yM+IfmiMLh7BmOpALS+w==': <AppleDevice(iPhone 4S: Johnny Appleseed's iPhone)>,
u'reGYDh9XwqNWTGIhNBuEwP1ds0F/Lg5t/fxNbI4V939hhXawByErk+HYVNSUzmWV': <AppleDevice(MacBook Air 11": Johnny Appleseed's MacBook Air)>
}
```

and you can access individual devices by either their index, or their ID:

```python
>>> api.devices[0]
<AppleDevice(iPhone 4S: Johnny Appleseed's iPhone)>
>>> api.devices['i9vbKRGIcLYqJnXMd1b257kUWnoyEBcEh6yM+IfmiMLh7BmOpALS+w==']
<AppleDevice(iPhone 4S: Johnny Appleseed's iPhone)>
```

or, as a shorthand if you have only one associated apple device, you can simply use the `iphone` property to access the first device associated with your account:

```python
>>> api.iphone
<AppleDevice(iPhone 4S: Johnny Appleseed's iPhone)>
```

Note: the first device associated with your account may not necessarily be your iPhone.

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

### File Storage (Ubiquity)

You can access documents stored in your iCloud account by using the `files` property's `dir` method:

```python
>>> api.files.dir()
[u'.do-not-delete',
 u'.localized',
 u'com~apple~Notes',
 u'com~apple~Preview',
 u'com~apple~mail',
 u'com~apple~shoebox',
 u'com~apple~system~spotlight'
]
```

You can access children and their children's children using the filename as an index:

```python
>>> api.files['com~apple~Notes']
<Folder: u'com~apple~Notes'>
>>> api.files['com~apple~Notes'].type
u'folder'
>>> api.files['com~apple~Notes'].dir()
[u'Documents']
>>> api.files['com~apple~Notes']['Documents'].dir()
[u'Some Document']
>>> api.files['com~apple~Notes']['Documents']['Some Document'].name
u'Some Document'
>>> api.files['com~apple~Notes']['Documents']['Some Document'].modified
datetime.datetime(2012, 9, 13, 2, 26, 17)
>>> api.files['com~apple~Notes']['Documents']['Some Document'].size
1308134
>>> api.files['com~apple~Notes']['Documents']['Some Document'].type
u'file'
```

And when you have a file that you'd like to download, the `open` method will return a response object from which you can read the `content`.

```python
>>> api.files['com~apple~Notes']['Documents']['Some Document'].open().content
'Hello, these are the file contents'
```

Note: the object returned from the above `open` method is a [response object](http://www.python-requests.org/en/latest/api/#classes) and the `open` method can accept any parameters you might normally use in a request using [requests](https://github.com/kennethreitz/requests).

For example, if you know that the file you're opening has JSON content:

```python
>>> api.files['com~apple~Notes']['Documents']['information.json'].open().json()
{'How much we love you': 'lots'}
>>> api.files['com~apple~Notes']['Documents']['information.json'].open().json()['How much we love you']
'lots'
```

Or, if you're downloading a particularly large file, you may want to use the `stream` keyword argument, and read directly from the raw response object:

```python
>>> download = api.files['com~apple~Notes']['Documents']['big_file.zip'].open(stream=True)
>>> with open('downloaded_file.zip', 'wb') as opened_file:
        opened_file.write(download.raw.read())
```
