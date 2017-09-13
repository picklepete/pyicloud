# -*- coding:utf-8 -*-

import base64
import json
import logging

import sys
from datetime import datetime

import pytz

from pyicloud.exceptions import (
    PyiCloudAPIResponseError
)

logger = logging.getLogger(__name__)

_SMART_ALBUMS = {
    "ALL": "All Photos",
    "FAVORITE": "Favorites",
    "VIDEO": "Videos",
    "LIVE": "Live Photos",
    "PANORAMA": "Panorama",
    "TIMELAPSE": "Timelapse",
    "SLOMO": "Slow Photos",
    "SCREENSHOT": "Screenshots"
}

_QUERY_DESIRED_KEYS = [
    "resJPEGFullWidth",
    "resJPEGFullHeight",
    "resJPEGFullFileType",
    "resJPEGFullFingerprint",
    "resJPEGFullRes",
    "resJPEGLargeWidth",
    "resJPEGLargeHeight",
    "resJPEGLargeFileType",
    "resJPEGLargeFingerprint",
    "resJPEGLargeRes",
    "resJPEGMedWidth",
    "resJPEGMedHeight",
    "resJPEGMedFileType",
    "resJPEGMedFingerprint",
    "resJPEGMedRes",
    "resJPEGThumbWidth",
    "resJPEGThumbHeight",
    "resJPEGThumbFileType",
    "resJPEGThumbFingerprint",
    "resJPEGThumbRes",
    "resVidFullWidth",
    "resVidFullHeight",
    "resVidFullFileType",
    "resVidFullFingerprint",
    "resVidFullRes",
    "resVidMedWidth",
    "resVidMedHeight",
    "resVidMedFileType",
    "resVidMedFingerprint",
    "resVidMedRes",
    "resVidSmallWidth",
    "resVidSmallHeight",
    "resVidSmallFileType",
    "resVidSmallFingerprint",
    "resVidSmallRes",
    "resSidecarWidth",
    "resSidecarHeight",
    "resSidecarFileType",
    "resSidecarFingerprint",
    "resSidecarRes",
    "itemType",
    "dataClassType",
    "mediaMetaDataType",
    "mediaMetaDataEnc",
    "filenameEnc",
    "originalOrientation",
    "resOriginalWidth",
    "resOriginalHeight",
    "resOriginalFileType",
    "resOriginalFingerprint",
    "resOriginalRes",
    "resOriginalAltWidth",
    "resOriginalAltHeight",
    "resOriginalAltFileType",
    "resOriginalAltFingerprint",
    "resOriginalAltRes",
    "resOriginalVidComplWidth",
    "resOriginalVidComplHeight",
    "resOriginalVidComplFileType",
    "resOriginalVidComplFingerprint",
    "resOriginalVidComplRes",
    "isDeleted",
    "isExpunged",
    "dateExpunged",
    "remappedRef",
    "recordName",
    "recordType",
    "recordChangeTag",
    "masterRef",
    "adjustmentRenderType",
    "assetDate",
    "addedDate",
    "isFavorite",
    "isHidden",
    "orientation",
    "duration",
    "assetSubtype",
    "assetSubtypeV2",
    "assetHDRType",
    "burstFlags",
    "burstFlagsExt",
    "burstId",
    "captionEnc",
    "locationEnc",
    "locationV2Enc",
    "locationLatitude",
    "locationLongitude",
    "adjustmentType",
    "timeZoneOffset",
    "vidComplDurValue",
    "vidComplDurScale",
    "vidComplDispValue",
    "vidComplDispScale",
    "vidComplVisibilityState",
    "customRenderedValue",
    "containerId",
    "itemId",
    "position",
    "isKeyAsset"
]


class PhotosService(object):
    """ The 'Photos' iCloud service."""

    def __init__(self, service_root, session, params):
        self.session = session
        self.params = dict(params)

        self.prepostfetch = 200

        self._service_root = service_root
        self._query_endpoint = \
            '%s/database/1/com.apple.photos.cloud/' \
            'production/private/records/query' \
            % self._service_root
        self._batch_endpoint = \
            '%s/database/1/com.apple.photos.cloud/' \
            'production/private/internal/records/query/batch' \
            % self._service_root
        self._photo_assets = {}

    def _batch(self, payload):
        '''
        Query count of photos
        List:
            "CPLAssetByAssetDateWithoutHiddenOrDeleted",
            "CPLAssetByAddedDate",
            "CPLAssetInSmartAlbumByAssetDate:Favorite",
            "CPLAssetInSmartAlbumByAssetDate:Video",
            "CPLAssetInSmartAlbumByAssetDate:Live",
            "CPLAssetInSmartAlbumByAssetDate:Panorama",
            "CPLAssetInSmartAlbumByAssetDate:Timelapse",
            "CPLAssetInSmartAlbumByAssetDate:Slomo",
            "CPLAssetBurstStackAssetByAssetDate",
            "CPLAssetInSmartAlbumByAssetDate:Screenshot",
            "CPLAssetHiddenByAssetDate",
            "CPLAssetDeletedByExpungedDate"
        :param payload:
        :return:
        '''
        params = dict(
            remapEnums='true',
            getCurrentSyncToken='true'
        )
        params.update(self.params)
        body = json.dumps(payload)
        request = self.session.request(
            'POST',
            self._batch_endpoint,
            params=params,
            data=body
        )
        response = request.json()
        return response
        pass

    def _query(self, payload):
        '''
        Query database
        List:
            `CPLAssetAndMaster`,
            `CPLAssetAndMasterByAddedDate`,
            `CPLAssetAndMasterByAssetDateWithoutHiddenOrDeleted`,
            `CPLAlbumByPositionLive`,
            `CPLContainerRelationLiveByAssetDate`,
            `CPLAssetAndMasterInSmartAlbumByAssetDate`
        :param payload: query data
        :return: response
        '''

        params = dict(
            remapEnums='true',
            getCurrentSyncToken='true'
        )
        params.update(self.params)
        body = json.dumps(payload)
        request = self.session.request(
            'POST',
            self._query_endpoint,
            params=params,
            data=body
        )
        response = request.json()
        return response

    @property
    def albums(self):
        albums = {}
        for k in _SMART_ALBUMS:
            data = dict(
                smartAlbum=True,
                recordName=k,
                albumName=_SMART_ALBUMS[k],
            )
            album = PhotoAlbum(data, self)
            albums[album.title] = album

        for folder in self._fetch_folders()['records']:
            if not folder['recordType'] == 'CPLAlbum':
                continue
            if folder['recordName'] == '----Root-Folder----':
                # Except root folder
                continue

            album = PhotoAlbum(folder, self)
            albums[album.title] = album
        return albums

    @property
    def all(self):
        return self.albums['All Photos']

    def _fetch_folders(self):
        payload = dict(
            query=dict(
                recordType='CPLAlbumByPositionLive'
            ),
            zoneID=dict(
                zoneName='PrimarySync'
            )
        )
        return self._query(payload)


class PhotoAlbum(object):
    def __init__(self, data, service):
        self.data = data
        self.service = service
        self._photo_assets = None

    @property
    def title(self):
        if self.data.get('smartAlbum', False):
            self._issmart = True
            self._record_name = self.data['recordName']
            self._album_name = self.data['albumName']
        else:
            self._album_type = self.data['fields']['albumType']['value']
            self._record_name = self.data['recordName']
            self._issmart = False

            if self.data['fields'].get('albumNameEnc', False):
                b64albumName = self.data['fields']['albumNameEnc']['value']
                albumName = base64.b64decode(b64albumName)
                self._album_name = str(albumName, encoding='utf8')
        return self._album_name

    def __iter__(self):
        return iter(self.photos)

    def __getitem__(self, index):
        return self.photos[index]

    @property
    def photos(self):
        index = 0
        max_query_num = 200
        photos_num = len(self)
        photos = {}
        while index < photos_num:
            fetch_photos = self._fetch_asset_data(index, max_query_num)
            photos.update(fetch_photos)
            index += len(fetch_photos)
        return photos

    def _fetch_asset_data(self, start, limit):
        if not self._photo_assets:
            if self._record_name == 'ALL':
                qtype = 'CPLAssetAndMasterByAssetDateWithoutHiddenOrDeleted'
                payload = dict(
                    query=dict(
                        filterBy=[],
                        recordType=qtype
                    )
                )
            elif self._issmart:
                payload = dict(
                    query=dict(
                        filterBy=[
                            dict(
                                comparator='EQUALS',
                                fieldName='smartAlbum',
                                fieldValue=dict(
                                    type='STRING',
                                    value=self._record_name
                                )
                            )
                        ],
                        recordType='CPLAssetAndMasterInSmartAlbumByAssetDate'
                    )
                )
                pass
            else:
                payload = dict(
                    query=dict(
                        filterBy=[
                            dict(
                                comparator='EQUALS',
                                fieldName='parentId',
                                fieldValue=dict(
                                    type='STRING',
                                    value=self._record_name
                                )
                            ),
                        ],
                        recordType='CPLContainerRelationLiveByAssetDate'
                    ),
                )

            payload['query']['filterBy'].append(
                dict(
                    comparator='EQUALS',
                    fieldName='startRank',
                    fieldValue=dict(type='INT64', value=start)
                )
            )
            payload['query']['filterBy'].append(
                dict(
                    comparator='EQUALS',
                    fieldName='direction',
                    fieldValue=dict(type='STRING', value='ASCENDING')
                )
            )
            payload['query'].update(desiredKeys=_QUERY_DESIRED_KEYS)
            payload.update(dict(
                resultsLimit=limit * 2,
                zoneID=dict(zoneName='PrimarySync')
            ))

            response = self.service._query(payload)
            records = response['records']

            photos = {}
            for record in records:
                if record['recordType'] == 'CPLMaster':
                    photo = PhotoAsset(
                        record['recordName'],
                        record['fields'],
                        self
                    )
                    photos[record['recordName']] = photo
                else:
                    continue

            for record in records:
                if record['recordType'] == 'CPLAsset':
                    fields = record['fields']
                    asset_name = fields['masterRef']['value']['recordName']
                    photo = photos.get(asset_name, False)
                    if photo:
                        photo.data.update(fields)
                        photo._record_name = record['recordName']
                        photos[photo.filename] = photos.pop(asset_name)
                    else:
                        logger.debug('Cannot find photo assets')
            return photos

    def __len__(self):
        if self._record_name == 'ALL':
            batch_value = 'CPLAssetByAssetDateWithoutHiddenOrDeleted'
        elif self._issmart:
            batch_value = 'CPLAssetInSmartAlbumByAssetDate:%s' \
                          % self._record_name
            pass
        else:
            batch_value = 'CPLContainerRelationNotDeletedByAssetDate:%s' \
                          % self._record_name
            pass

        batch_query = dict(
            query=dict(
                recordType="HyperionIndexCountLookup",
                filterBy=dict(
                    fieldName="indexCountID",
                    comparator="IN",
                    fieldValue=dict(
                        type="STRING_LIST",
                        value=[batch_value],
                    )
                )
            ),
            zoneID=dict(
                zoneName="PrimarySync"
            ),
            zoneWide=True,
            resultsLimit=1
        )
        response = self.service._batch({'batch': [batch_query]})
        if len(response['batch']) == 0:
            raise PyiCloudAPIResponseError(reason='Batch failed', code=0)
        fields = response['batch'][0]['records'][0]['fields']
        return fields['itemCount']['value']

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
    def __init__(self, recordName, data, album):
        self._record_name = recordName
        self.data = data
        self.album = album
        pass

    @property
    def filename(self):
        return str(
            base64.b64decode(self.data['filenameEnc'].get('value')),
            encoding='utf8'
        )

    @property
    def title(self):
        return self.filename

    @property
    def size(self):
        try:
            return int(self.data['resOriginalRes']['value'].get('size'))
        except ValueError:
            return None

    @property
    def created(self):
        return datetime.fromtimestamp(
            self.data['assetDate'].get('value') / 1000.0,
            tz=pytz.utc
        )

    @property
    def added(self):
        return datetime.fromtimestamp(
            self.data['addedDate'].get('value') / 1000.0,
            tz=pytz.utc
        )

    def download(self, **kwargs):
        return self.album.service.session.get(
            self.data['resOriginalRes']['value']['downloadURL'],
            stream=True,
            **kwargs
        )

    @property
    def dimensions(self):
        return [
            int(self.data['resOriginalWidth'].get('value')),
            int(self.data['resOriginalHeight'].get('value'))
        ]
