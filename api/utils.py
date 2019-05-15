import datetime
import pytz


def format_to_dot_date(date):
    # CNB uses dot date format
    yyyy, mm, dd = str(date).split("-")
    return f"{dd}.{mm}.{yyyy}"


def cnb_day():
    """
    Function return day from cnb view.
    This means that before 14:30 CNB uses rates from yesterday with yesterady date.
    """
    prague_time = pytz.timezone("Europe/Prague")
    now = datetime.datetime.now(prague_time)
    if datetime.time() < now.time() < datetime.time(14, 30):
        return datetime.date.today() - datetime.timedelta(days=1)
    return datetime.date.today()


def daterange(date1, date2):
    # Return day between two days
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + datetime.timedelta(n)
