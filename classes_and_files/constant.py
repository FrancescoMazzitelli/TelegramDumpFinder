import datetime


def date_format(date):

    """
    Metodo che consente di definire il formato della data desiderato

    :param date: la data il cui formato deve essere adattato
    :return: la data col formato desiderato
    """

    if type(date) is datetime:
        return date.strftime("%Y-%m-%d %H:%M:%S")
