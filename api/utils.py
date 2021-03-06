import datetime
import pytz
import holidays

# Get list of Czech public holidays
cz_holidays = holidays.Czech()

def format_to_dot_date(date):
    # CNB uses DDMMYYYY dot date format
    yyyy, mm, dd = str(date).split("-")
    return f"{dd}.{mm}.{yyyy}"

def format_from_dot_date(date):
    dd, mm, yyyy = date.split(".")
    return f"{yyyy}-{mm}-{dd}"

def prg_now():
    # Actual Prague time
    prague_time = pytz.timezone("Europe/Prague")
    return datetime.datetime.now(prague_time)

def cnb_day(dt=prg_now()):
    """
    Function returns date from cnb view.
    This means that before 14:30 CNB uses rates from yesterday with yesterady date.
    """
    # If holidays substract one day and try again
    if dt in cz_holidays:
        return cnb_day(dt - datetime.timedelta(days=1))
    # If date only arbibtrary default time
    if not isinstance(dt, datetime.datetime):
        dt = datetime.datetime.combine(dt, datetime.time(23, 59, 59))
    # If Saturday substract one day
    if dt.weekday() == 5:
        return (dt - datetime.timedelta(days=1)).date()
    # If Sunday substract two days
    if dt.weekday() == 6:
        return (dt - datetime.timedelta(days=2)).date()

    if datetime.time() < dt.time() < datetime.time(14, 30):
        # If weekend day substract one day and try again
        if (dt - datetime.timedelta(days=1)).weekday() in [5, 6]:
            return cnb_day(dt - datetime.timedelta(days=1))
        else:
            # Else substract one day
            return (dt - datetime.timedelta(days=1)).date()
    return dt.date()

def daterange(date1, date2):
    # Return day between two days
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + datetime.timedelta(n)
