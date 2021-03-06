from datetime import datetime


def date_converter(year, month=1, day=1):
    """Function converts date to timestamp
    """
    return round(datetime(year, month, day).timestamp())
