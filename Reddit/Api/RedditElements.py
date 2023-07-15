from datetime import datetime, timedelta

def convert_to_datetime(text):
    if 'hours ago' in text:
        hours = int(text.split()[0])
        timedelta_obj = timedelta(hours=hours)
    elif 'days ago' in text:
        days = int(text.split()[0])
        timedelta_obj = timedelta(days=days)
    elif 'minutes ago' in text:
        minutes = int(text.split()[0])
        timedelta_obj = timedelta(minutes=minutes)
    elif 'hour ago' in text:
        hours = int(text.split()[0])
        timedelta_obj = timedelta(hours=hours)
    elif 'minute ago' in text:
        minutes = int(text.split()[0])
        timedelta_obj = timedelta(minutes=minutes)
    elif 'day ago' in text:
        days = 0
        timedelta_obj = timedelta(days=days)
    elif 'just now' in text:
        datetime_obj = datetime.now()
        return datetime_obj
    else:
        raise ValueError("Geçersiz zaman formatı: {}".format(text))

    datetime_obj = datetime.now() - timedelta_obj
    return datetime_obj