from datetime import datetime, timedelta
import json
import re
import sys


class DriveService(object):

    def __init__(self, service_root, document_root, session, params):
        self._service_root = service_root
        self._document_root = document_root
        self.session = session
        self.params = params
        self._root = None
        self.token = self.get_token_from_cookie()

    def get_node_data(self, id):
        request = self.session.post(
            self._service_root + '/retrieveItemDetailsInFolders',
            params=self.params,
            data=json.dumps([{
                "drivewsid": "FOLDER::com.apple.CloudDocs::%s" % id,
                "partialData": False,
            }])
        )
        return request.json()[0]

    def get_token_from_cookie(self):
        for cookie in self.session.cookies:
            if cookie.name == 'X-APPLE-WEBAUTH-TOKEN':
                match = re.search(r'\bt=([^:]+)', cookie.value)
                if not match:
                    raise Exception("Can't extract token from %r" % (
                        token_cookie,
                    ))
                return match.group(1)
        raise Exception("Token cookie not found")

    def get_file(self, id, **kwargs):
        meta = self.session.get(
            self._document_root + '/ws/com.apple.CloudDocs/download/by_id',
            params={
                'document_id': id,
                'token': self.token,
                'clientBuildNumber': self.params['clientBuildNumber'],
                'clientId': self.params['clientId'],
                'clientMasteringNumber': self.params['clientMasteringNumber'],
                'dsid': self.params['dsid'],
            }
        ).json()
        return self.session.get(
            meta['data_token']['url'],
            params=self.params,
            **kwargs
        )

    @property
    def root(self):
        if self._root is None:
            self._root = DriveNode(self, self.get_node_data('root'))
        return self._root

    def __getattr__(self, attr):
        return getattr(self.root, attr)

    def __getitem__(self, key):
        return self.root[key]


class DriveNode(object):
    def __init__(self, conn, data):
        self.data = data
        self.connection = conn

    @property
    def name(self):
        if self.type == 'file':
            return '%s.%s' % (self.data['name'], self.data['extension'])
        else:
            return self.data['name']

    @property
    def type(self):
        type = self.data.get('type')
        return type and type.lower()

    def get_children(self):
        if not hasattr(self, '_children'):
            if 'items' not in self.data:
                self.data.update(
                    self.connection.get_node_data(self.data['docwsid'])
                )
            self._children = [
                DriveNode(self.connection, item_data)
                for item_data in self.data['items']
            ]
        return self._children

    @property
    def size(self):
        try:
            return int(self.data.get('size'))
        except ValueError:
            return None

    @property
    def modified(self):
        # jump through hoops to return time in UTC rather than California time
        match = re.search(
            r'^(.+?)([\+\-]\d+):(\d\d)$',
            self.data.get('dateModified'),
        )
        if not match:
            raise ValueError(self.data.get('dateModified'))
        base = datetime.strptime(
            match.group(1),
            '%Y-%m-%dT%H:%M:%S'
        )
        diff = timedelta(
            hours=int(match.group(2)),
            minutes=int(match.group(3)),
        )
        return base - diff

    def dir(self):
        return [child.name for child in self.get_children()]

    def open(self, **kwargs):
        return self.connection.get_file(self.data['docwsid'], **kwargs)

    def get(self, name):
        return [
            child for child in self.get_children() if child.name == name
        ][0]

    def __getitem__(self, key):
        try:
            return self.get(key)
        except IndexError:
            raise KeyError('No child named %s exists' % key)

    def __unicode__(self):
        return self.name

    def __str__(self):
        as_unicode = self.__unicode__()
        if sys.version_info[0] >= 3:
            return as_unicode
        else:
            return as_unicode.encode('ascii', 'ignore')

    def __repr__(self):
        return "<%s: '%s'>" % (
            self.type.capitalize(),
            self
        )
