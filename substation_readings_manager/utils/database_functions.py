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


def string_record_id_to_intertier_cells_monitor():
    """ Returns a dictionary { StringRecordID: ([intertier_cells], monitortype) }
    """

    ms_conn = connect_to_database()
    ms_cursor = ms_conn.cursor()

    query = """
    SELECT s.StringRecordID, dt.DeviceTypeName FROM BEEnterprise.dbo.strings s
    INNER JOIN
    BEEnterprise.dbo.deviceTypes dt
    on s.StringDeviceTypeRecordID = dt.DeviceTypeRecordID;
    """

    ms_cursor.execute(query)

    sr_dt_to_icm = dict()

    for row in ms_cursor:
        intertier_cell_list = get_intertier_cells(row[0])
        sr_dt_to_icm[row[0]] = (intertier_cell_list, row[1])

    return sr_dt_to_icm

def get_string_record_id_to_name_dict():
    """ Queries the database and returns a dictionary(mapping) of StringRecordID to name

    Returns:
        dict: Dictionary in the format {StringRecordID: ()}
    """

    ms_conn = connect_to_database()
    ms_cursor = ms_conn.cursor()

    query = """SELECT s.StringRecordID, s.name, dt.DeviceTypeName FROM BEEnterprise.dbo.strings s
INNER JOIN
BEEnterprise.dbo.deviceTypes dt
on s.StringDeviceTypeRecordID = dt.DeviceTypeRecordID;"""

    ms_cursor.execute(query)

    string_record_id_name_dict = {}

    for row in ms_cursor:
        string_record_id_name_dict.update({row[0]: (row[1], row[2])})

    return string_record_id_name_dict

def get_intertier_cells(string_record_id: int)->List[int]:
    """

    Returns:
        List[str]: List of the cells that are intertier cells
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