"""Drive service."""
from datetime import datetime, timedelta
import json
from re import search
from six import PY2


class DriveService(object):
    """The 'Drive' iCloud service."""

    def __init__(self, service_root, document_root, session, params):
        self._service_root = service_root
        self._document_root = document_root
        self.session = session
        self.params = dict(params)
        self._root = None

    def _get_token_from_cookie(self):
        for cookie in self.session.cookies:
            if cookie.name == "X-APPLE-WEBAUTH-TOKEN":
                match = search(r"\bt=([^:]+)", cookie.value)
                if not match:
                    raise Exception("Can't extract token from %r" % cookie.value)
                self.params.update({"token": match.group(1)})
        raise Exception("Token cookie not found")

    def get_node_data(self, node_id):
        """Returns the node data."""
        request = self.session.post(
            self._service_root + "/retrieveItemDetailsInFolders",
            params=self.params,
            data=json.dumps(
                [
                    {
                        "drivewsid": "FOLDER::com.apple.CloudDocs::%s" % node_id,
                        "partialData": False,
                    }
                ]
            ),
        )
        return request.json()[0]

    def get_file(self, file_id, **kwargs):
        """Returns iCloud Drive file."""
        file_params = dict(self.params)
        file_params.update({"document_id": file_id})
        response = self.session.get(
            self._document_root + "/ws/com.apple.CloudDocs/download/by_id",
            params=file_params,
        )
        if not response.ok:
            return None
        url = response.json()["data_token"]["url"]
        return self.session.get(url, params=self.params, **kwargs)

    @property
    def root(self):
        """Returns the root node."""
        if not self._root:
            self._root = DriveNode(self, self.get_node_data("root"))
        return self._root

    def __getattr__(self, attr):
        return getattr(self.root, attr)

    def __getitem__(self, key):
        return self.root[key]


class DriveNode(object):
    """Drive node."""

    def __init__(self, conn, data):
        self.data = data
        self.connection = conn
        self._children = None

    @property
    def name(self):
        """Gets the node name."""
        if self.type == "file":
            return "%s.%s" % (self.data["name"], self.data["extension"])
        return self.data["name"]

    @property
    def type(self):
        """Gets the node type."""
        node_type = self.data.get("type")
        return node_type and node_type.lower()

    def get_children(self):
        """Gets the node children."""
        if not self._children:
            if "items" not in self.data:
                self.data.update(self.connection.get_node_data(self.data["docwsid"]))
            if "items" not in self.data:
                raise KeyError("No items in folder, status: %s" % self.data["status"])
            self._children = [
                DriveNode(self.connection, item_data)
                for item_data in self.data["items"]
            ]
        return self._children

    @property
    def size(self):
        """Gets the node size."""
        size = self.data.get("size")  # Folder does not have size
        if not size:
            return None
        return int(size)

    @property
    def date_changed(self):
        """Gets the node changed date (in UTC)."""
        return _date_to_utc(self.data.get("dateChanged"))  # Folder does not have date

    @property
    def date_modified(self):
        """Gets the node modified date (in UTC)."""
        return _date_to_utc(self.data.get("dateModified"))  # Folder does not have date

    @property
    def date_last_open(self):
        """Gets the node last open date (in UTC)."""
        return _date_to_utc(self.data.get("lastOpenTime"))  # Folder does not have date

    def open(self, **kwargs):
        """Gets the node file."""
        return self.connection.get_file(self.data["docwsid"], **kwargs)

    def dir(self):
        """Gets the node list of directories."""
        if self.type == "file":
            return None
        return [child.name for child in self.get_children()]

    def get(self, name):
        """Gets the node child."""
        if self.type == "file":
            return None
        return [child for child in self.get_children() if child.name == name][0]

    def __getitem__(self, key):
        try:
            return self.get(key)
        except IndexError:
            raise KeyError("No child named '%s' exists" % key)

    def __unicode__(self):
        return "{type: %s, name: %s}" % (self.type, self.name)

    def __str__(self):
        as_unicode = self.__unicode__()
        if PY2:
            return as_unicode.encode("utf-8", "ignore")
        return as_unicode

    def __repr__(self):
        return "<%s: %s>" % (type(self).__name__, str(self))


def _date_to_utc(date):
    if not date:
        return None
    # jump through hoops to return time in UTC rather than California time
    match = search(r"^(.+?)([\+\-]\d+):(\d\d)$", date)
    if not match:
        # Already in UTC
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    base = datetime.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S")
    diff = timedelta(hours=int(match.group(2)), minutes=int(match.group(3)))
    return base - diff
