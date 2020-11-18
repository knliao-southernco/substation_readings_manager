"""[summary]

Returns:
    [type]: [description]
"""

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import calendar

import pyodbc
from typing import Dict, List, Tuple

def connect_to_database():
    """This function returns a connection to the database.

    Returns:
        pyodbc connection: A connection to the relevant battery database.
    """

    return pyodbc.connect('Driver={SQL Server};'
                          'Server=localhost\SQLEXPRESS;'
                          'Database=BEEnterprise;'
                          'Trusted_Connection=yes;')


def get_last_month_date() -> date:
    """ This function returns the date one month ago. This is for get_date_range_one_month
    which then takes the first of the month.

    Returns:
        date: One month ago from the current date
    """

    now = datetime.now()
    one_month_ago = now - relativedelta(months=1)
    return one_month_ago.date()


def get_string_record_id_to_name_dict() -> Dict[str, str]:
    """ Queries the database and returns a dictionary(mapping) of StringRecordID to name

    Returns:
        dict: Dictionary in the format {StringRecordID: name}
    """

    ms_conn = connect_to_database()
    ms_cursor = ms_conn.cursor()

    query = 'SELECT StringRecordID, name FROM BEEnterprise.dbo.strings;'
    ms_cursor.execute(query)

    string_record_id_name_dict = {}

    for row in ms_cursor:
        string_record_id_name_dict.update({row[0]: row[1]})

    return string_record_id_name_dict

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

#Each substation and each readingtype should have a certain number
# At a very high level, each substation should have a certain amount of readings

##for reading type and at the cell level
##  Maybe I could jsut extend my software?
# append to a list for each sheet, and then for each sheet I uhhhh,,,,,,,
#output the list, just one sheet, a lot of substations
#Just one sheet, uhhhhh,I can combine all the readings
#
#

def query_database_cell_values(string_record_id: str, reading_type: int, cell_number: int,
                               day: date = get_last_month_date()) -> List:
    """ This function queries the database for the readings for a specific StringID,
    reading type and cell number

    Args:
        string_record_id (str): The StringRecordID of the substation
        reading_type (int): The Reading Type being queried
        cell_number (int): The Cell Number being queried
        day (date, optional): Any day within the month that will be queried. Functions use this date
        to return the first of the month. Defaults to get_last_month_date().

    Returns:
        reading_list (List): reading_list is the list of readings from the database.
    """

    ms_conn = connect_to_database()

    ms_cursor = ms_conn.cursor()

    first_day, last_day = get_date_range_one_month(day)

    query = F"""SELECT CellReadingsRecordID, ReadingDateTime,
            ReadingValue FROM BEEnterpriseHistory.dbo.CellReadingsHistory where
            StringRecordID = {string_record_id} and
            ReadingTypeRecordID = {reading_type} and cellNumber = {cell_number} and
            ReadingDateTime between '{first_day}' and '{last_day}'"""

    ms_cursor.execute(query)

    reading_list = []

    for row in ms_cursor:
        reading_list.append(row[1].date())

    return reading_list

def check_database_values(string_record_id: str, reading_list: List[date],
        reading_type: int, cell_number: int, day: date) -> bool:
    """This function checks the results of query_database_cell_values to see if the correct
    number of readings is in the database for the specific reading type and string_record_id.

    Returns:
        bool(not_enough_readings) : True if not enough, False if enough readings
    """

    reading_type_dict = {6: "Cell Impedance", 8: "Cell Voltage",
                         9: "Strap Impedance", 10: "Intertier Impedance"}

    reading_list = query_database_cell_values(string_record_id, reading_type, cell_number)

    if (reading_type_dict.get(reading_type) == "Cell Impedance" or
        reading_type_dict.get(reading_type) == "Strap Impedance" or
            reading_type_dict.get(reading_type) == "Intertier Impedance"):
        return len(reading_list) < 1

    if reading_type_dict.get(reading_type) == "Cell Voltage":

        #check the reading_list
        #1. Get the a list of dates by iterating over the reading list
        #2. Get a the list of dates in that time range from get_all_days_between_two_days
        #3. Compare the two

        first_day, last_day = get_date_range_one_month(day)

        query_date_list = []

        for reading in reading_list:
            query_date_list.append(reading)

        days_between_two_dates = get_all_days_between_two_dates(
            first_day, last_day)

        return set(query_date_list) == set(days_between_two_dates)

def check_substation(string_record_id: int,
        reading_type: int,  day: date) -> bool:

#What do I want this function to tell me? I want given a (string_record_id, reading_type, and a dict of stuff) ,
# return a (bool, number it has, number its supposed to have)
# Data Structure
#


    reading_type_dict = {6: "Cell Impedance", 8: "Cell Voltage",
                         9: "Strap Impedance", 10: "Intertier Impedance"}

    if (reading_type_dict.get(reading_type) == "Cell Impedance" or
        reading_type_dict.get(reading_type) == "Strap Impedance" or
            reading_type_dict.get(reading_type) == "Intertier Impedance"):
        return len(reading_list) < 1

    if reading_type_dict.get(reading_type) == "Cell Voltage":

        #check the reading_list
        #1. Get the a list of dates by iterating over the reading list
        #2. Get a the list of dates in that time range from get_all_days_between_two_days
        #3. Compare the two

        first_day, last_day = get_date_range_one_month(day)

        query_date_list = []

        for reading in reading_list:
            query_date_list.append(reading)

        days_between_two_dates = get_all_days_between_two_dates(
            first_day, last_day)

        return set(query_date_list) == set(days_between_two_dates)


def get_intertier_cells(string_record_id: int)->Dict[int,List[int]]:
    """

    Returns:
        Dict[str,List[str]]: Dictionary that has string_record_id as the key
        and a list of the cells that are intertier cells
    """

    conn = connect_to_database()

    ms_cursor = conn.cursor()

    query = F"""SELECT CellNumber FROM BEEnterpriseHistory.dbo.CellReadingsHistory
    where ReadingTypeRecordID = 10 and StringRecordID = {string_record_id}"""

    ms_cursor.execute(query)

    intertier_cell_list = []

    for row in ms_cursor:
        if row[0] not in intertier_cell_list:
            intertier_cell_list.append(row[0])

    return intertier_cell_list

def workbook_name(day: date = get_last_month_date())->str:
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
