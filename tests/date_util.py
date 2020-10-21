"""Date Util Class

"""
import datetime


class DateUtil(object):
    """Date Util class

    """

    # pylint: disable=no-init
    @classmethod
    def get_date_from_str(cls, date_str):
        """get_date_from_str

        :param date_str:
        :return:
        """
        return datetime.datetime.strptime(date_str, "%Y%m%d").date()

    @classmethod
    def get_today(cls):
        """get_today

        :param cls:
        :return:
        """
        return datetime.date.today()

    @classmethod
    def get_yesterday(cls):
        """get_yesterday

        :return:
        """
        return datetime.date.today() - datetime.timedelta(days=1)

    @classmethod
    def get_str_from_date(cls, date_obj):
        """get_str_from_date

        :param date_obj:
        :return:
        """
        return date_obj.strftime("%Y-%m-%d")

    @classmethod
    def get_tomorrow(cls):
        """get_tomorrow

        :return:
        """
        return datetime.date.today() + datetime.timedelta(days=1)

    @classmethod
    def get_date_from_timestamp(cls, timestamp):
        """get_date_from_timestamp

        :param timestamp:
        :return:
        """
        return datetime.datetime.fromtimestamp(timestamp).date()


class DateTimeUtil(object):
    """DateTime Util class

    """

    # pylint: disable=no-init
    @classmethod
    def get_datetime_from_str(cls, date_str):
        """get_datetime_from_str

        :param date_str:
        :return:
        """
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    @classmethod
    def get_datetime_from_date_str(cls, date_str):
        """get_datetime_from_date_str

        :param date_str:
        :return:
        """
        return datetime.datetime.strptime(date_str, "%Y%m%d")

    @classmethod
    def get_str_from_datetime(cls, datetime_obj):
        """get_str_from_datetime

        :param datetime_obj:
        :return:
        """
        return datetime.datetime.strftime(datetime_obj, "%Y-%m-%d %H:%M:%S")

    @classmethod
    def get_now(cls):  # pragma: no cover
        """get_now

        :return:
        """
        return datetime.datetime.now()

    @classmethod
    def get_datetime_from_timestamp(cls, timestamp):
        """get_datetime_from_timestamp

        :param timestamp:
        :return:
        """
        return datetime.datetime.fromtimestamp(timestamp)

    @classmethod
    def get_datetime_from_date(cls, date):
        """get_datetime_from_date

        :param date:
        :return:
        """
        return datetime.datetime.fromordinal(date.toordinal())
