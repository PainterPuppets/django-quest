from datetime import datetime, time, date, timedelta

from pytz import utc


def get_timestamp(date_time):
    second_timestamp = int(date_time.strftime('%s'))
    micro_timestamp = date_time.microsecond * 0.000001
    timestamp_str = str(int((second_timestamp + micro_timestamp) * 1000000))
    return timestamp_str


def get_utctime_from_timestamp_str(timestamp_str):
    micro_timestamp = float(timestamp_str) / 1000000
    return datetime.fromtimestamp(micro_timestamp).replace(tzinfo=utc)


def get_today_min_time():
    return datetime.combine(datetime.now(), time.min).replace(tzinfo=utc)


def get_first_day_of_month_min_time():
    return datetime.combine(date.today() - timedelta(days=datetime.now().day - 1), time.min).replace(tzinfo=utc)


def get_first_day_of_week_min_time():
    return datetime.combine(date.today() - timedelta(days=date.today().weekday()), time.min).replace(tzinfo=utc)


def get_current_timestamp():
    return int(datetime.now().timestamp())
