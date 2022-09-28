"""Calendar service."""
from dataclasses import dataclass, asdict, field
from tzlocal import get_localzone_name
from calendar import monthrange
from datetime import datetime, timedelta
from random import randint
from uuid import uuid4
import json



class CalendarService:
    """
    The 'Calendar' iCloud service, connects to iCloud and returns events.
    """

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = params
        self._service_root = service_root
        self._calendar_endpoint = "%s/ca" % self._service_root
        self._calendar_refresh_url = "%s/events" % self._calendar_endpoint
        self._calendar_event_detail_url = f"{self._calendar_endpoint}/eventdetail"
        self._calendar_collections_url = f"{self._calendar_endpoint}/collections"
        self._calendars_url = "%s/startup" % self._calendar_endpoint

        self.response = {}

    @property
    def default_params(self) -> dict:
        today = datetime.today()
        first_day, last_day = monthrange(today.year, today.month)
        from_dt = datetime(today.year, today.month, first_day)
        to_dt = datetime(today.year, today.month, last_day)
        params = dict(self.params)
        params.update(
            {
                "lang": "en-us",
                "usertz": get_localzone_name(),
                "startDate": from_dt.strftime("%Y-%m-%d"),
                "endDate": to_dt.strftime("%Y-%m-%d"),
            }
        )

        return params

    def obj_from_dict(self, obj, _dict) -> object:
        for key, value in _dict.items():
            setattr(obj, key, value)
        
        return obj

    def get_ctag(self, guid) -> str:
        for cal in self.get_calendars(as_objs=False):
            if cal.get("guid") == guid:
                return cal.get("ctag")

    def refresh_client(self, from_dt=None, to_dt=None):
        """
        Refreshes the CalendarService endpoint, ensuring that the
        event data is up-to-date. If no 'from_dt' or 'to_dt' datetimes
        have been given, the range becomes this month.
        """
        today = datetime.today()
        first_day, last_day = monthrange(today.year, today.month)
        if not from_dt:
            from_dt = datetime(today.year, today.month, first_day)
        if not to_dt:
            to_dt = datetime(today.year, today.month, last_day)
        params = dict(self.params)
        params.update(
            {
                "lang": "en-us",
                "usertz": get_localzone_name(),
                "startDate": from_dt.strftime("%Y-%m-%d"),
                "endDate": to_dt.strftime("%Y-%m-%d"),
            }
        )
        req = self.session.get(self._calendar_refresh_url, params=params)
        self.response = req.json()

    @dataclass
    class CalendarObject:
        title: str = "Untitled"
        guid: str = ""
        shareType: str = None # can be (None, 'published', 'shared') where 'published' gens a public caldav link in the response.  Shared is not supported here as it is rather complex.
        symbolicColor: str = "__custom__"
        supportedType: str = "Event"
        objectType: str = "personal"
        shareTitle: str = ""
        sharedUrl: str = ""
        color: str = ""
        order: int = 7
        extendedDetailsAreIncluded: bool = True
        readOnly: bool = False
        enabled: bool = True
        ignoreEventUpdates = None
        emailNotification = None
        lastModifiedDate = None
        meAsParticipant = None
        prePublishedUrl = None
        participants = None
        deferLoading = None
        publishedUrl = None
        removeAlarms = None
        ignoreAlarms = None
        description = None
        removeTodos = None
        isDefault = None
        isFamily = None
        etag = None
        ctag = None

        def __post_init__(self) -> None:
            if not self.guid:
                self.guid = str(uuid4()).upper()

            if not self.color:
                self.color = self.gen_random_color()
                
        def gen_random_color(self) -> str:
            """
            Creates a random rgbhex color.
            """
            return "#%02x%02x%02x" % tuple([randint(0,255) for _ in range(3)])

        @property
        def request_data(self) -> dict:
            data = {
                "Collection": asdict(self),
                "ClientState": {
                    "Collection": [],
                    "fullState": False,
                    "userTime": 1234567890,
                    "alarmRange": 60
                }
            }
            return data

    def get_calendars(self, as_objs:bool=False) -> list:
        """
        Retrieves calendars of this month.
        """
        params = self.default_params
        req = self.session.get(self._calendars_url, params=params)
        self.response = req.json()
        calendars = self.response["Collection"]

        if as_objs and calendars:
            for idx, cal in enumerate(calendars):
                calendars[idx] = self.obj_from_dict(self.CalendarObject(), cal)
        
        return calendars
    
    def add_calendar(self, calendar:CalendarObject) -> None:
        """
        Adds a Calendar to the apple calendar.
        """
        data = calendar.request_data
        params = self.default_params

        req = self.session.post(self._calendar_collections_url + f"/{calendar.guid}",
                                 params=params, data=json.dumps(data))
        self.response = req.json()

    def remove_calendar(self, cal_guid:str) -> None:
        """
        Removes a Calendar from the apple calendar. 
        """
        params = self.default_params
        params["methodOverride"] = "DELETE"

        req = self.session.post(self._calendar_collections_url + f"/{cal_guid}",
                                 params=params, data=json.dumps({}))
        self.response = req.json()

    @dataclass
    class EventObject:
        pGuid: str 
        title: str = "New Event"
        startDate: datetime = datetime.today()
        endDate: datetime = datetime.today() + timedelta(minutes=60)
        localStartDate = None
        localEndDate = None
        duration: int = field(init=False)
        icon:int = 0
        changeRecurring: str = None
        tz: str = "US/Pacific"
        guid: str = "" # event identifier
        location: str = ""
        extendedDetailsAreIncluded: bool = True
        recurrenceException: bool = False
        recurrenceMaster: bool = False
        hasAttachments: bool = False
        allDay: bool = False
        isJunk: bool = False
        
        invitees:list[str] = field(init=False, default_factory=list)

        def __post_init__(self) -> None:
            if not self.localStartDate:
                self.localStartDate = self.startDate
            if not self.localEndDate:
                self.localEndDate = self.endDate

            if not self.guid:
                self.guid = str(uuid4()).upper()

            self.duration = int((self.endDate.timestamp() - self.startDate.timestamp()) / 60)

        @property
        def request_data(self) -> dict:
            event_dict = asdict(self)
            event_dict["startDate"] = self.dt_to_list(self.startDate)
            event_dict["endDate"] = self.dt_to_list(self.endDate, False)
            event_dict["localStartDate"] = self.dt_to_list(self.localStartDate)
            event_dict["localEndDate"] = self.dt_to_list(self.localEndDate, False)

            data = {
                "Event" : event_dict,
                "ClientState": {
                    "Collection": [{
                        "guid": self.guid,
                        "ctag": None
                        }],
                    "fullState": False,
                    "userTime": 1234567890,
                    "alarmRange": 60
                }
            }

            if self.invitees:
                data["Invitee"] = [
                    {
                        "guid": email_guid,
                        "pGuid": self.pGuid,
                        "role": "REQ-PARTICIPANT",
                        "isOrganizer": False,
                        "email": email_guid.split(":")[-1],
                        "inviteeStatus": "NEEDS-ACTION",
                        "commonName": "",
                        "isMyId": False
                    }
                    for email_guid in self.invitees
                ]

            return data
        
        def dt_to_list(self, dt:datetime, start:bool=True) -> list:
            """
            Converts python datetime object into a list format used
            by Apple's calendar.
            """
            if start:
                minutes = dt.hour * 60 + dt.minute
            else:
                minutes = (24 - dt.hour) * 60 + (60 - dt.minute)

            return [dt.strftime("%Y%m%d"), dt.year, dt.month, dt.day, dt.hour, dt.minute, minutes]
        
        def add_invitees(self, _invitees:list=[]) -> None:
            """
            Adds a list of emails to invitees in the correct format
            """
            self.invitees += ["{}:{}".format(self.guid, email) for email in _invitees]

        def get(self, var:str):
            return getattr(self, var, None)

    def get_events(self, from_dt:datetime=None, to_dt:datetime=None, period:str="month", as_objs:bool=False) -> list:
        """
        Retrieves events for a given date range, by default, this month.
        """
        if period != "month":
            if from_dt:
                today = datetime(from_dt.year, from_dt.month, from_dt.day)
            else:
                today = datetime.today()
            
            if period == "day":
                if not from_dt:
                    from_dt = datetime(today.year, today.month, today.day)
                to_dt = from_dt + timedelta(days=1)
            elif period == "week":
                from_dt = datetime(today.year, today.month, today.day) - timedelta(days=today.weekday() + 1 )
                to_dt = from_dt + timedelta(days=6)
        

        self.refresh_client(from_dt, to_dt)
        events = self.response.get("Event")

        if as_objs and events:
            for idx, event in enumerate(events):
                events[idx] = self.obj_from_dict(self.EventObject(), event)

        return events
    
    def get_event_detail(self, pguid, guid, as_obj:bool=False):
        """
        Fetches a single event's details by specifying a pguid
        (a calendar) and a guid (an event's ID).
        """
        params = dict(self.params)
        params.update({"lang": "en-us", "usertz": get_localzone_name()})
        url = f"{self._calendar_event_detail_url}/{pguid}/{guid}"
        req = self.session.get(url, params=params)
        self.response = req.json()
        event = self.response["Event"][0]

        if as_obj and event:
            event = self.obj_from_dict(self.EventObject(), event)

        return event

    def add_event(self, event:EventObject) -> None:
        """
        Adds an Event to a calendar.
        """
        data = event.request_data
        data["ClientState"]["Collection"][0]["ctag"] = self.get_ctag(event.guid)
        params = self.default_params

        req = self.session.post(self._calendar_refresh_url + f"/{event.pGuid}/{event.guid}",
                                 params=params, data=json.dumps(data))
        self.response = req.json()
    
    def remove_event(self, event:EventObject) -> None:
        """
        Removes an Event from a calendar. The calendar's guid corresponds to the EventObject's pGuid
        """
        data = event.request_data
        data["ClientState"]["Collection"][0]["ctag"] = self.get_ctag(event.guid)
        data["Event"] = {}

        params = self.default_params
        params["methodOverride"] = "DELETE"
        if not getattr(event, "etag", ""):
            event.etag = self.get_event_detail(event.pGuid, event.guid, as_obj=False).get("etag")
        params["ifMatch"] = event.etag

        req = self.session.post(self._calendar_refresh_url + f"/{event.pGuid}/{event.guid}",
                                 params=params, data=json.dumps(data))
        self.response = req.json()





