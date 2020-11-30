"""[summary]

Returns:
    [type]: [description]
"""

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import calendar

import pyodbc
from typing import Dict, List, Tuple

import database_functions as database_func
import date_functions as date_func

def check_substation(string_record_id: int,
        reading_type: int,  day: date) -> bool:

    reading_type_dict = {6: "Cell Impedance", 8: "Cell Voltage",
                         9: "Strap Impedance", 10: "Intertier Impedance"}

    if (reading_type_dict.get(reading_type) == "Cell Impedance" or
        reading_type_dict.get(reading_type) == "Strap Impedance" or
            reading_type_dict.get(reading_type) == "Intertier Impedance"):
        return len(reading_list) < 1

    if reading_type_dict.get(reading_type) == "Cell Voltage":

        first_day, last_day = date_func.get_date_range_one_month(day)

        query_date_list = []

        for reading in reading_list:
            query_date_list.append(reading)

        days_between_two_dates = date_func.get_all_days_between_two_dates(
            first_day, last_day)

        return set(query_date_list) == set(days_between_two_dates)

def workbook_name(day: date = date_func.get_last_month_date())->str:
    """This function returns a workbook name given a date

    Args:
        day (date): Date that the report is being run on

    Returns:
        string: Name in the format "October 2020 MPC Battery Report.xlsx"
    """

    month = str(calendar.month_name[day.month])

    year = str(day.year)
    workbook_name = month + " " +  year + ' MPC Battery Report' + '.xlsx'

    return workbook_name

def program_status(name: str, reading_type: str, cell_number: int)->str:
    """This functions prints the current value that the program is on

    Args:
        name (str): Name of the substation
        reading_type (str): Reading type that the substation is on
        cell_number (int): What Cell Number of the substation that the program is on

    Returns:
        string: "Substation x reading_type x Cell Number: x"
    """

    status = "Substation " + name + " " + reading_type + "Cell:" + cell_number

    return status
