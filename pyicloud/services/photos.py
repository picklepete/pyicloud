import sys
import json
import urllib

from datetime import datetime
from base64 import b64decode
from bitstring import ConstBitStream
from pyicloud.exceptions import (
    PyiCloudAPIResponseError,
    PyiCloudBinaryFeedParseError,
    PyiCloudPhotoLibraryNotActivatedErrror
)


class PhotosService(object):
    """ The 'Photos' iCloud service."""

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = dict(params)

        self.prepostfetch = 200

        self._service_root = service_root
        self._service_endpoint = '%s/ph' % self._service_root

        try:
            request = self.session.get(
                '%s/startup' % self._service_endpoint,
                params=self.params
            )
            response = request.json()
            self.params.update({
                'syncToken': response['syncToken'],
                'clientInstanceId': self.params.pop('clientId')
            })
        except PyiCloudAPIResponseError as error:
            if error.code == 402:
                raise PyiCloudPhotoLibraryNotActivatedErrror(
                    "iCloud Photo Library has not been activated yet "
                    "for this user")

        self._photo_assets = {}

    @property
    def albums(self):
        request = self.session.get(
            '%s/folders' % self._service_endpoint,
            params=self.params
        )
        response = request.json()
        albums = {}
        for folder in response['folders']:
            if not folder['type'] == 'album':
                continue

            album = PhotoAlbum(folder, self)
            albums[album.title] = album

        return albums

    @property
    def all(self):
        return self.albums['All Photos']

    def _fetch_asset_data_for(self, client_ids):
        client_ids = [cid for cid in client_ids
                      if cid not in self._photo_assets]

        data = json.dumps({
            'syncToken': self.params.get('syncToken'),
            'methodOverride': 'GET',
            'clientIds': client_ids,
        })
        request = self.session.post(
            '%s/assets' % self._service_endpoint,
            params=self.params,
            data=data
        )

        response = request.json()

        for asset in response['assets']:
            self._photo_assets[asset['clientId']] = asset


class PhotoAlbum(object):
    def __init__(self, data, service):
        self.data = data
        self.service = service
        self._photo_assets = None

    @property
    def title(self):
        BUILTIN_ALBUMS = {
            'recently-added': "Recently Added",
            'time-lapse': "Time-lapse",
            'videos': "Videos",
            'slo-mo': 'Slo-mo',
            'all-photos': "All Photos",
            'selfies': "Selfies",
            'bursts': "Bursts",
            'favorites': "Favourites",
            'panoramas': "Panoramas",
            'deleted-photos': "Recently Deleted",
            'hidden': "Hidden",
            'screenshots': "Screenshots"
        }
        if self.data.get('isServerGenerated'):
            return BUILTIN_ALBUMS[self.data.get('serverId')]
        else:
            return self.data.get('title')

    def __iter__(self):
        return iter(self.photos)

    def __getitem__(self, index):
        return self.photos[index]

    @property
    def photos(self):
        if not self._photo_assets:
            child_assets = self.data.get('childAssetsBinaryFeed')
            if not child_assets:
                raise PyiCloudBinaryFeedParseError(
                    "Missing childAssetsBinaryFeed in photo album")
            self._photo_assets = self._parse_binary_feed(child_assets)

        return self._photo_assets

    def _parse_binary_feed(self, feed):
        binaryfeed = bytearray(b64decode(feed))
        bitstream = ConstBitStream(binaryfeed)

        payload_encoding = binaryfeed[0]
        if payload_encoding != bitstream.read("uint:8"):
            raise PyiCloudBinaryFeedParseError(
                "Missmatch betweeen binaryfeed and bistream payload encoding")

        ASSET_PAYLOAD = 255
        ASSET_WITH_ORIENTATION_PAYLOAD = 254
        ASPECT_RATIOS = [
            0.75,
            4.0 / 3.0 - 3.0 * (4.0 / 3.0 - 1.0) / 4.0,
            4.0 / 3.0 - 2.0 * (4.0 / 3.0 - 1.0) / 4.0,
            1.25,
            4.0 / 3.0, 1.5 - 2.0 * (1.5 - 4.0 / 3.0) / 3.0,
            1.5 - 1.0 * (1.5 - 4.0 / 3.0) / 3.0,
            1.5,
            1.5694444444444444,
            1.6388888888888888,
            1.7083333333333333,
            16.0 / 9.0,
            2.0 - 2.0 * (2.0 - 16.0 / 9.0) / 3.0,
            2.0 - 1.0 * (2.0 - 16.0 / 9.0) / 3.0,
            2,
            3
        ]

        valid_payloads = [ASSET_PAYLOAD, ASSET_WITH_ORIENTATION_PAYLOAD]
        if payload_encoding not in valid_payloads:
            raise PyiCloudBinaryFeedParseError(
                "Unknown payload encoding '%s'" % payload_encoding)

        assets = {}
        while len(bitstream) - bitstream.pos >= 48:
            range_start = bitstream.read("uint:24")
            range_length = bitstream.read("uint:24")
            range_end = range_start + range_length

            previous_asset_id = 0
            for index in range(range_start, range_end):
                aspect_ratio = ASPECT_RATIOS[bitstream.read("uint:4")]

                id_size = bitstream.read("uint:2")
                if id_size:
                    # A size has been reserved for the asset id
                    asset_id = bitstream.read("uint:%s" % (2 + 8 * id_size))
                else:
                    # The id is just an increment to a previous id
                    asset_id = previous_asset_id + bitstream.read("uint:2") + 1

                orientation = None
                if payload_encoding == ASSET_WITH_ORIENTATION_PAYLOAD:
                    orientation = bitstream.read("uint:3")

                assets[index] = PhotoAsset(index, asset_id, aspect_ratio,
                                           orientation, self)
                previous_asset_id = asset_id

        return assets.values()

    def _fetch_asset_data_for(self, asset):
        if asset.client_id in self.service._photo_assets:
            return self.service._photo_assets[asset.client_id]

        client_ids = []
        prefetch = postfetch = self.service.prepostfetch
        for index in range(
                max(asset.album_index - prefetch, 0),
                min(asset.album_index + postfetch + 1,
                    len(self._photo_assets))):
            client_ids.append(self._photo_assets[index].client_id)

        self.service._fetch_asset_data_for(client_ids)
        return self.service._photo_assets[asset.client_id]

    def __unicode__(self):
        return self.title

    def __str__(self):
        as_unicode = self.__unicode__()
        if sys.version_info[0] >= 3:
            return as_unicode
        else:
            return as_unicode.encode('ascii', 'ignore')

    def __repr__(self):
        return "<%s: '%s'>" % (
            type(self).__name__,
            self
        )


class PhotoAsset(object):
    def __init__(self, index, client_id, aspect_ratio, orientation, album):
        self.album_index = index
        self.client_id = client_id
        self.aspect_ratio = aspect_ratio
        self.orientation = orientation
        self.album = album
        self._data = None

    @property
    def data(self):
        if not self._data:
            self._data = self.album._fetch_asset_data_for(self)
        return self._data

    @property
    def filename(self):
        return self.data['details'].get('filename')

    @property
    def size(self):
        try:
            return int(self.data['details'].get('filesize'))
        except ValueError:
            return None

    @property
    def created(self):
        dt = datetime.fromtimestamp(self.data.get('createdDate') / 1000.0)
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    @property
    def dimensions(self):
        return self.data.get('dimensions')

    @property
    def versions(self):
        versions = {}
        for version in self.data.get('derivativeInfo'):
            (version, width, height, size, mimetype,
                u1, u2, u3, url, filename) = version.split(':')
            versions[version] = {
                'width': width,
                'height': height,
                'size': size,
                'mimetype': mimetype,
                'url': urllib.unquote(url),
                'filename': filename,
            }
        return versions

    def download(self, version='original', **kwargs):
        if version not in self.versions:
            return None

        return self.album.service.session.get(
            self.versions[version]['url'],
            stream=True,
            **kwargs
        )

    def __repr__(self):
        return "<%s: client_id=%s>" % (
            type(self).__name__,
            self.client_id
        )
