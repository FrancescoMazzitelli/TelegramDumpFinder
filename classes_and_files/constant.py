import datetime


def date_format(date):
    """
    :param date:
    :return:
    """
    if type(date) is datetime:
        return date.strftime("%Y-%m-%d %H:%M:%S")
