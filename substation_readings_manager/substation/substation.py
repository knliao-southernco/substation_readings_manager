from enum import Enum
from datetime import date

from typing import List, Dict, Tuple
import substation_readings_manager.utils.database_functions as df
import substation_readings_manager.utils.date_functions as date_func

class DataReading():

    reading_type_dict = {6: "Cell Impedance", 8: "Cell Voltage",
    9:"Strap Impedance", 10: "Intertier Impedance"}

    def __init__(self, database_id):

        self.reading_type: tuple = (database_id, self.reading_type_dict.get(database_id))
        self.readings: list = None


    def set_readings(self, string_record_id: int, day: date)->None:

        ms_conn = df.connect_to_database()
        ms_cursor = ms_conn.cursor()


        first_day, last_day = date_func.get_date_range_one_month(day)

        query = F"""SELECT CellReadingsRecordID, ReadingDateTime,
            ReadingValue FROM BEEnterpriseHistory.dbo.CellReadingsHistory where
            StringRecordID = {string_record_id} and
            ReadingTypeRecordID = {self.reading_type[0]}  and
            ReadingDateTime between '{first_day}' and '{last_day}'"""

        ms_cursor.execute(query)

        reading_list = []

        for row in ms_cursor:
            reading_list.append(row)

        self.readings = reading_list

class Substation:

    def __init__(self, string_record_id: int, intertier_cells: List[int], monitor_type:str):
        self.string_record_id: int = string_record_id
        self.intertier_cells: list = intertier_cells
        self.monitor_type: str = monitor_type

        self.cell_voltage_readings = DataReading(6)
        self.cell_impedance_readings = DataReading(8)
        self.strap_impedance_readings = DataReading(9)
        self.intertier_impedance_readings = DataReading(10)

        self.cell_voltage_readings.set_readings(string_record_id, date(2020,8,4))

        self.cell_impedance_readings.set_readings(string_record_id, date(2020,8,4))

        self.strap_impedance_readings.set_readings(string_record_id, date(2020,8,4))

        self.intertier_impedance_readings.set_readings(string_record_id, date(2020,8,4))

    def print_values(self):
        print(self.string_record_id, self.intertier_cells, self.monitor_type)

    def get_cell_voltage_readings(self, string_record_id: int, day: date):
        """
        Need to execute a sql statement here is what I suspect
        """

        query = F"""SELECT CellReadingsRecordID, ReadingDateTime,
            ReadingValue FROM BEEnterpriseHistory.dbo.CellReadingsHistory where
            StringRecordID = {string_record_id} and
            ReadingTypeRecordID = {reading_type} and cellNumber = {cell_number} and
            ReadingDateTime between '{first_day}' and '{last_day}' """




    # def check_cell_impedance(self):
    #     #Needs a reading once a month

    #     """ This funciton checks to make sure that a substation has at least one cell impedance reading for each of its cells

    #     Args:

    #     day (date, optional): Any day within the month that will be queried. Functions use this date
    #     to return the first of the month. Defaults to get_last_month_date().

    #     Returns:
    #         Tuple[int, int]:(The amount of readings in the database, the amount of readings that there should have been)
    #     """

    #     first_day, last_day = utils.get_date_range_one_month(day)

    #     db_conn = utils.connect_to_database()

    #     cursor = db_conn.cursor()

    #     query = F"""SELECT CellNumber, ReadingDateTime, ReadingValue FROM BEEnterpriseHistory.dbo.CellReadingsHistory
    #             where StringRecordID = {self.string_record_id}
    #             and ReadingTypeRecordID = 6
    #             and ReadingDateTime between {first_day} and {last_day}"""

    #     cursor.execute(query)

    #     #This is a simple check for now, it should be upgraded in the future so that it actually looks
    #     #at the cell readings. This is to catch scenarios like one cell being read more than once.
    #     if (len(self.intertier_cells) == len(cursor)):
    #         return(True, len(self.intertier_cells),len(cursor))

    #     return (False, len(self.intertier_cells), len(cursor))


    # def check_strap_impedance(self):
    #     #Needs a reading once a amonth

    #   #Needs a reading once a month
    #     """ This funciton checks to make sure that a substation has at least one intertier impedance reading for each of its cells
    #     in the intertier_cells attribute

    #     Args:

    #     day (date, optional): Any day within the month that will be queried. Functions use this date
    #     to return the first of the month. Defaults to get_last_month_date().

    #     Returns:
    #         Tuple[int, int]:(The amount of readings in the database, the amount of readings that there should have been)
    #     """

    #     first_day, last_day = utils.get_date_range_one_month(day)

    #     db_conn = utils.connect_to_database()

    #     cursor = db_conn.cursor()

    #     query = F"""SELECT CellNumber, ReadingDateTime, ReadingValue FROM BEEnterpriseHistory.dbo.CellReadingsHistory
    #             where StringRecordID = {self.string_record_id}
    #             and ReadingTypeRecordID = 9
    #             and ReadingDateTime between {first_day} and {last_day}"""

    #     cursor.execute(query)

    #     #This is a simple check for now, it should be upgraded in the future so that it actually looks
    #     #at the cell readings. This is to catch scenarios like one cell being read more than once.
    #     if (len(self.intertier_cells) == len(cursor)):
    #         return(True, len(self.intertier_cells),len(cursor))

    #     return (False, len(self.intertier_cells), len(cursor))



    # def check_intertier_impedance(self, day: date = utils.get_last_month_date())->Tuple[bool, int, int]:
    #     #Needs a reading once a month
    #     """ This funciton checks to make sure that a substation has at least one intertier impedance reading for each of its cells
    #     in the intertier_cells attribute

    #     Args:

    #     day (date, optional): Any day within the month that will be queried. Functions use this date
    #     to return the first of the month. Defaults to get_last_month_date().

    #     Returns:
    #         Tuple[int, int]:(The amount of readings in the database, the amount of readings that there should have been)
    #     """

    #     first_day, last_day = utils.get_date_range_one_month(day)

    #     db_conn = utils.connect_to_database()

    #     cursor = db_conn.cursor()

    #     query = F"""SELECT CellNumber, ReadingDateTime, ReadingValue FROM BEEnterpriseHistory.dbo.CellReadingsHistory
    #             where StringRecordID = {self.string_record_id}
    #             and ReadingTypeRecordID = 10
    #             and ReadingDateTime between {first_day} and {last_day}"""

    #     cursor.execute(query)

    #     #This is a simple check for now, it should be upgraded in the future so that it actually looks
    #     #at the cell readings. This is to catch scenarios like one cell being read more than once.
    #     if (len(self.intertier_cells) == len(cursor)):
    #         return(True, len(self.intertier_cells),len(cursor))

    #     return (False, len(self.intertier_cells), len(cursor))

    # def check_cell_voltage(self):
    #     #Needs a reading once a month
    #      """ This funciton checks to make sure that a substation has at least one intertier impedance reading for each of its cells
    #     in the intertier_cells attribute

    #     Args:

    #     day (date, optional): Any day within the month that will be queried. Functions use this date
    #     to return the first of the month. Defaults to get_last_month_date().

    #     Returns:
    #         Tuple[int, int]:(The amount of readings in the database, the amount of readings that there should have been)
    #     """

    #     first_day, last_day = utils.get_date_range_one_month(day)

    #     db_conn = utils.connect_to_database()

    #     cursor = db_conn.cursor()

    #     query = F"""SELECT CellNumber, ReadingDateTime, ReadingValue FROM BEEnterpriseHistory.dbo.CellReadingsHistory
    #             where StringRecordID = {self.string_record_id}
    #             and ReadingTypeRecordID = 8
    #             and ReadingDateTime between {first_day} and {last_day}"""

    #     cursor.execute(query)

    #     #This is a simple check for now, it should be upgraded in the future so that it actually looks
    #     #at the cell readings. This is to catch scenarios like one cell being read more than once.
    #     if (len(self.intertier_cells) == len(cursor)):
    #         return(True, len(self.intertier_cells),len(cursor))

    #     return (False, len(self.intertier_cells), len(cursor)

