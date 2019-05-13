def format_to_dot_date(date):
    yyyy, mm, dd = str(date).split("-")
    return f"{dd}.{mm}.{yyyy}"