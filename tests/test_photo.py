"""Photo service tests

"""
import datetime
import json
import pytest
from pyicloud.services.photos import PhotoAlbum
from tests.date_util import DateTimeUtil, DateUtil


class CustomEncoder(json.JSONEncoder):
    """Custom Encoder"""

    # pylint: disable=method-hidden
    def default(self, o):
        """Default encode method

        :param o:
        :return:
        """
        if isinstance(o, datetime.date):
            return DateTimeUtil.get_datetime_from_date(o).timestamp()
        return super(CustomEncoder, self).default(o)


class DataException(Exception):
    """Exception for test

    """

    def __init__(self, data: dict):
        self.data = data
        super(DataException, self).__init__()

    def __str__(self):
        return json.dumps(self.data, sort_keys=True, cls=CustomEncoder)


MOCK_PHOTO_ASSET_DATA = [
    {
        "recordName": "asset1",
        "fields": {
            "assetDate": {
                "value": datetime.datetime(year=2020, month=1, day=1).timestamp() * 1000
            },
            "masterRef": {"value": {"recordName": "record1"}},
        },
    },
    {
        "recordName": "asset2",
        "fields": {
            "assetDate": {
                "value": datetime.datetime(year=2020, month=1, day=2).timestamp() * 1000
            },
            "masterRef": {"value": {"recordName": "record2"}},
        },
    },
    {
        "recordName": "asset3",
        "fields": {
            "assetDate": {
                "value": datetime.datetime(year=2020, month=1, day=3).timestamp() * 1000
            },
            "masterRef": {"value": {"recordName": "record3"}},
        },
    },
]

DUP_ASSET_DATA = {
    "recordName": "asset4",
    "fields": {
        "assetDate": {
            "value": datetime.datetime(year=2020, month=1, day=3).timestamp() * 1000
        },
        "masterRef": {"value": {"recordName": "record3"}},
    },
}


class MockResponse:
    """Mock Response for photo service

    """

    def __init__(self, idx, direction):
        """Init method

        :param idx:
        :param direction:
        """
        self.idx = int(idx)
        self.direction = direction

    def json(self):
        """Extract json info

        :return:
        """
        if self.idx < 0 or self.idx > MOCK_DATA_LEN:
            return {"records": []}

        if self.direction == "DESCENDING":  # pylint: disable=no-else-return,no-self-use
            return {"records": [one for one in MOCK_DATA[self.idx * 2 :] if one != []]}
        else:
            data = list(reversed(MOCK_DATA))
            return {"records": [one for one in data[self.idx * 2 :] if one != []]}


class MockPyiCloudSession:
    """Mock PyiCloudSession for photo service

    """

    def post(self, url, data, headers):  # pylint: disable=unused-argument,no-self-use
        """Mock post method of session

        :param url:
        :param data:
        :param headers:
        :return:
        """
        data = json.loads(data)
        idx = data[0]
        direction = data[1]
        return MockResponse(idx, direction)


class MockPyiCloudService:
    """Mock PyiCloudService for photo service

    """

    def __init__(self, username, password, client_id):
        """Init method

        :param username:
        :param password:
        :param client_id:
        """
        self.username = username
        self.password = password
        self.client_id = client_id

        self._service_endpoint = "mock_endpoint"
        self.params = {}
        self.session = MockPyiCloudSession()


MOCK_DATA = []

for one in MOCK_PHOTO_ASSET_DATA:
    MOCK_DATA.append(
        {
            "recordType": "CPLMaster",
            "recordName": one["fields"]["masterRef"]["value"]["recordName"],
        }
    )
    MOCK_DATA.append({"recordType": "CPLAsset", **one})
# add dup asset
MOCK_DATA.append([])
MOCK_DATA.append({"recordType": "CPLAsset", **DUP_ASSET_DATA})
MOCK_DATA_LEN = len(MOCK_DATA) // 2


@pytest.fixture()
def mock_album(monkeypatch):
    """Fixture to mock PhotoAlbum

    :param monkeypatch:
    :return:
    """

    def mock__len__(self):  # pylint: disable=unused-argument
        return MOCK_DATA_LEN

    def mock_list_query_gen(
        self,
        offset: int,
        list_type: str,
        direction: str,
        query_filter=None,
        simple=False,
    ):  # pylint: disable=unused-argument
        """Mock _list_query_gen

        :param self:
        :param offset:
        :param list_type:
        :param direction:
        :param query_filter:
        :param simple:
        :return:
        """
        if direction == "DESCENDING":  # pylint: disable=no-else-return
            return [MOCK_DATA_LEN - 1 - offset, direction]
        else:
            return [offset, direction]

    monkeypatch.setattr(PhotoAlbum, "__len__", mock__len__)
    monkeypatch.setattr(PhotoAlbum, "_list_query_gen", mock_list_query_gen)

    album = PhotoAlbum(
        service=MockPyiCloudService(
            username="username", password="password", client_id="client_id"
        ),
        name="",
        list_type="",
        obj_type="",
        direction="DESCENDING",
    )
    return album


class TestPhotoAlbum:
    """Testcases of PhotoAlbum

    """

    def test_get_photos_by_date_desc(
        self, mock_album
    ):  # pylint: disable=redefined-outer-name,no-self-use
        """test get_photos_by_date_desc

        :param mock_album:
        :return:
        """
        method = getattr(mock_album, "_PhotoAlbum__get_photos_by_date")
        photos = [
            photo for photo in method()
        ]  # pylint: disable=unnecessary-comprehension
        assert len(photos) == MOCK_DATA_LEN
        assert (
            photos[0].id
            == MOCK_PHOTO_ASSET_DATA[0]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[1].id
            == MOCK_PHOTO_ASSET_DATA[1]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[2].id
            == MOCK_PHOTO_ASSET_DATA[2]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[3].id
            == MOCK_PHOTO_ASSET_DATA[2]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert photos[0].asset_id == MOCK_PHOTO_ASSET_DATA[0]["recordName"]
        assert photos[1].asset_id == MOCK_PHOTO_ASSET_DATA[1]["recordName"]
        assert photos[2].asset_id == MOCK_PHOTO_ASSET_DATA[2]["recordName"]
        assert photos[3].asset_id == DUP_ASSET_DATA["recordName"]

    def test_get_photos_by_date_asc(
        self, mock_album
    ):  # pylint: disable=redefined-outer-name,no-self-use
        """test get_photos_by_date_asc

        :param mock_album:
        :return:
        """
        mock_album.direction = "ASCENDING"
        method = getattr(mock_album, "_PhotoAlbum__get_photos_by_date")
        photos = [
            photo for photo in method()
        ]  # pylint: disable=unnecessary-comprehension
        assert len(photos) == MOCK_DATA_LEN
        assert (
            photos[0].id
            == MOCK_PHOTO_ASSET_DATA[2]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[1].id
            == MOCK_PHOTO_ASSET_DATA[2]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[2].id
            == MOCK_PHOTO_ASSET_DATA[1]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[3].id
            == MOCK_PHOTO_ASSET_DATA[0]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert photos[0].asset_id == DUP_ASSET_DATA["recordName"]
        assert photos[1].asset_id == MOCK_PHOTO_ASSET_DATA[2]["recordName"]
        assert photos[2].asset_id == MOCK_PHOTO_ASSET_DATA[1]["recordName"]
        assert photos[3].asset_id == MOCK_PHOTO_ASSET_DATA[0]["recordName"]

    def test_get_offset_and_cnt_by_date_desc(
        self, mock_album
    ):  # pylint: disable=redefined-outer-name,no-self-use
        """test get_offset_and_cnt_by_date_desc

        :param mock_album:
        :return:
        """
        method = getattr(mock_album, "_PhotoAlbum__get_offset_and_cnt_by_date")
        assert method(
            album_len=4,
            date_start=datetime.date(year=2019, month=12, day=30),
            date_end=datetime.date(year=2019, month=12, day=31),
        ) == (0, 0)
        assert method(
            album_len=4,
            date_start=datetime.date(year=2020, month=1, day=4),
            date_end=datetime.date(year=2020, month=1, day=6),
        ) == (0, 0)

        assert method(
            album_len=4,
            date_start=datetime.date(year=2020, month=1, day=1),
            date_end=datetime.date(year=2020, month=1, day=2),
        ) == (3, 2)

        assert method(
            album_len=4,
            date_start=datetime.date(year=2019, month=12, day=31),
            date_end=datetime.date(year=2020, month=1, day=2),
        ) == (3, 2)

        assert method(
            album_len=4,
            date_start=datetime.date(year=2020, month=1, day=2),
            date_end=datetime.date(year=2020, month=1, day=4),
        ) == (2, 3)

    def test_get_offset_and_cnt_by_date_asc(
        self, mock_album
    ):  # pylint: disable=redefined-outer-name,no-self-use
        """test get_offset_and_cnt_by_date_asc

        :param mock_album:
        :return:
        """
        mock_album.direction = "ASCENDING"
        method = getattr(mock_album, "_PhotoAlbum__get_offset_and_cnt_by_date")
        assert method(
            album_len=4,
            date_start=datetime.date(year=2019, month=12, day=30),
            date_end=datetime.date(year=2019, month=12, day=31),
        ) == (0, 0)
        assert method(
            album_len=4,
            date_start=datetime.date(year=2020, month=1, day=4),
            date_end=datetime.date(year=2020, month=1, day=6),
        ) == (0, 0)

        assert method(
            album_len=4,
            date_start=datetime.date(year=2020, month=1, day=1),
            date_end=datetime.date(year=2020, month=1, day=2),
        ) == (2, 2)

        assert method(
            album_len=4,
            date_start=datetime.date(year=2019, month=12, day=31),
            date_end=datetime.date(year=2020, month=1, day=2),
        ) == (2, 2)

        assert method(
            album_len=4,
            date_start=datetime.date(year=2020, month=1, day=2),
            date_end=datetime.date(year=2020, month=1, day=4),
        ) == (0, 3)

    def test_calculate_offset_and_cnt_desc(
        self, mock_album, monkeypatch
    ):  # pylint: disable=redefined-outer-name,no-self-use
        """test calculate_offset_and_cnt_desc

        :param mock_album:
        :param monkeypatch:
        :return:
        """

        def mock_get_offset_and_cnt_by_date(self, album_len, date_start, date_end):
            raise DataException(
                {"album_len": album_len, "date_start": date_start, "date_end": date_end}
            )

        monkeypatch.setattr(
            mock_album,
            "_PhotoAlbum__get_offset_and_cnt_by_date",
            mock_get_offset_and_cnt_by_date.__get__(
                mock_album
            ),  # pylint: disable=no-value-for-parameter
        )

        # without arguments
        offset, cnt = mock_album.calculate_offset_and_cnt()
        assert (offset, cnt) == (3, 4)
        # only date_start
        data = {
            "album_len": MOCK_DATA_LEN,
            "date_start": DateUtil.get_today(),
            "date_end": DateUtil.get_tomorrow(),
        }
        with pytest.raises(DataException) as exc_info:
            mock_album.calculate_offset_and_cnt(date_start=DateUtil.get_today())
        assert json.dumps(data, sort_keys=True, cls=CustomEncoder) in str(
            exc_info.value
        )

        # only date_start and date_end
        data = {
            "album_len": MOCK_DATA_LEN,
            "date_start": DateUtil.get_date_from_str("20190101"),
            "date_end": DateUtil.get_date_from_str("20190201"),
        }
        with pytest.raises(DataException) as exc_info:
            mock_album.calculate_offset_and_cnt(
                date_start=DateUtil.get_date_from_str("20190101"),
                date_end=DateUtil.get_date_from_str("20190201"),
            )
        assert json.dumps(data, sort_keys=True, cls=CustomEncoder) in str(
            exc_info.value
        )

        # only last
        offset, cnt = mock_album.calculate_offset_and_cnt(last=2)
        assert (offset, cnt) == (1, 2)

        # only last larger than album len
        offset, cnt = mock_album.calculate_offset_and_cnt(last=5)
        assert (offset, cnt) == (3, 4)

    def test_calculate_offset_and_cnt_asc(
        self, mock_album, monkeypatch
    ):  # pylint: disable=redefined-outer-name,no-self-use
        """test calculate_offset_and_cnt_asc
        """
        mock_album.direction = "ASCENDING"

        def mock_get_offset_and_cnt_by_date(self, album_len, date_start, date_end):
            raise DataException(
                {"album_len": album_len, "date_start": date_start, "date_end": date_end}
            )

        monkeypatch.setattr(
            mock_album,
            "_PhotoAlbum__get_offset_and_cnt_by_date",
            mock_get_offset_and_cnt_by_date.__get__(
                mock_album
            ),  # pylint: disable=no-value-for-parameter
        )

        # without arguments
        offset, cnt = mock_album.calculate_offset_and_cnt()
        assert (offset, cnt) == (0, 4)
        # only date_start
        data = {
            "album_len": MOCK_DATA_LEN,
            "date_start": DateUtil.get_today(),
            "date_end": DateUtil.get_tomorrow(),
        }
        with pytest.raises(DataException) as exc_info:
            mock_album.calculate_offset_and_cnt(date_start=DateUtil.get_today())
        assert json.dumps(data, sort_keys=True, cls=CustomEncoder) in str(
            exc_info.value
        )

        # only date_start and date_end
        data = {
            "album_len": MOCK_DATA_LEN,
            "date_start": DateUtil.get_date_from_str("20190101"),
            "date_end": DateUtil.get_date_from_str("20190201"),
        }
        with pytest.raises(DataException) as exc_info:
            mock_album.calculate_offset_and_cnt(
                date_start=DateUtil.get_date_from_str("20190101"),
                date_end=DateUtil.get_date_from_str("20190201"),
            )
        assert json.dumps(data, sort_keys=True, cls=CustomEncoder) in str(
            exc_info.value
        )

        # only last
        offset, cnt = mock_album.calculate_offset_and_cnt(last=2)
        assert (offset, cnt) == (0, 2)

        # only last larger than album len
        offset, cnt = mock_album.calculate_offset_and_cnt(last=5)
        assert (offset, cnt) == (0, 4)

    def test_fetch_photos_all(
        self, mock_album
    ):  # pylint: disable=redefined-outer-name,no-self-use
        """test fetch_photos_all

        :param mock_album:
        :return:
        """
        photos = [
            photo for photo in mock_album.fetch_photos()
        ]  # pylint: disable=unnecessary-comprehension
        assert len(photos) == 4
        assert (
            photos[0].id
            == MOCK_PHOTO_ASSET_DATA[0]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[1].id
            == MOCK_PHOTO_ASSET_DATA[1]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[2].id
            == MOCK_PHOTO_ASSET_DATA[2]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[2].id == DUP_ASSET_DATA["fields"]["masterRef"]["value"]["recordName"]
        )

    def test_fetch_photos_last(
        self, mock_album
    ):  # pylint: disable=redefined-outer-name,no-self-use
        """test fetch_photos_last

        :param mock_album:
        :return:
        """
        photos = [
            photo for photo in mock_album.fetch_photos(last=3)
        ]  # pylint: disable=unnecessary-comprehension
        assert len(photos) == 3
        assert (
            photos[0].id
            == MOCK_PHOTO_ASSET_DATA[1]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[1].id
            == MOCK_PHOTO_ASSET_DATA[2]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[2].id == DUP_ASSET_DATA["fields"]["masterRef"]["value"]["recordName"]
        )

    def test_fetch_photos_by_date_desc(
        self, mock_album
    ):  # pylint: disable=redefined-outer-name,no-self-use
        """test fetch_photos_by_date_desc

        :param mock_album:
        :return:
        """
        mock_album.direction = "ASCENDING"
        # pylint: disable=unnecessary-comprehension
        photos = [
            photo
            for photo in mock_album.fetch_photos(
                date_start=DateUtil.get_date_from_str("20200102"),
                date_end=DateUtil.get_date_from_str("20200103"),
            )
        ]

        assert len(photos) == 3
        assert (
            photos[0].id == DUP_ASSET_DATA["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[1].id
            == MOCK_PHOTO_ASSET_DATA[2]["fields"]["masterRef"]["value"]["recordName"]
        )
        assert (
            photos[2].id
            == MOCK_PHOTO_ASSET_DATA[1]["fields"]["masterRef"]["value"]["recordName"]
        )
