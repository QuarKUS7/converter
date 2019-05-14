import datetime

def format_to_dot_date(date):
    yyyy, mm, dd = str(date).split("-")
    return f"{dd}.{mm}.{yyyy}"

def CNB_time():
    pass

def daterange(date1, date2):
    for n in range(int((date2 - date1).days) + 1):
        yield date1 + datetime.timedelta(n)
