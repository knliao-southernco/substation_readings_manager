from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import calendar

import pyodbc
from typing import Dict, List, Tuple

def get_last_month_date() -> date:
    """ This function returns the date one month ago. This is for get_date_range_one_month
    which then takes the first of the month.

    Returns:
        date: One month ago from the current date
    """

    now = datetime.now()
    one_month_ago = now - relativedelta(months=1)
    return one_month_ago.date()


def get_all_days_between_two_dates(s_date: date, e_date: date) -> List[date]:
    """This function returns a list of days in between two days, inclusive of start and end


    Args:
        s_date (date): start date
        e_date (date): end date

    Returns:
        List[date]: List that contains a date object for every day in a month
    """
    delta = e_date - s_date

    date_list = []

    for i in range(delta.days):
        day = s_date + timedelta(days=i)
        date_list.append(day)
    return date_list


def get_month_and_year_string(day: date) -> Tuple[int, int]:
    """[summary]

    Args:
        day (date): Date that we want month and year of

    Returns:
        Tuple[int, int]: Month(1-12), Year(Int)
    """
    date_obj = datetime.strptime(day, "%m-%d-%Y")
    return (date_obj.month, date_obj.year)


def get_date_range_one_month(day_of_month: date = get_last_month_date()) -> Tuple[date, date]:
    """This function returns the first day of the month of day_of_month and
    the first of the next month in a tuple.
    The first day of the next month is chosen because when iterating through the date list,
    the last day is exclusive.

    This function by default in the code, just uses the current date but can use any date with
    the day_of_month argument.

    Args:
        day_of_month (date, optional): [description]. Defaults to get_last_month_date().

    Returns:
        tuple: tuple that contains first day of month and first day of next month
    """
    first_day = day_of_month.replace(day=1)

    last_day = first_day + relativedelta(months=1)

    return (first_day, last_day)