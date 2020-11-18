import src.utils

class Substation:
    def __init__(self, string_record_id, intertier_cells):
        self.string_record_id = string_record_id
        self.intertier_cells = intertier_cells

    def check_values(self):

        write_bool,readings,needed_readings = self.check_intertier_impedance()

    def check_temperature(self):
        pass
    def check_voltage(self):
        pass

    def check_cell_impedance(self):
        #Needs a reading once a month

        """ This funciton checks to make sure that a substation has at least one cell impedance reading for each of its cells

        Args:

        day (date, optional): Any day within the month that will be queried. Functions use this date
        to return the first of the month. Defaults to get_last_month_date().

        Returns:
            Tuple[int, int]:(The amount of readings in the database, the amount of readings that there should have been)
        """

        first_day, last_day = utils.get_date_range_one_month(day)

        db_conn = utils.connect_to_database()

        cursor = db_conn.cursor()

        query = F"""SELECT CellNumber, ReadingDateTime, ReadingValue FROM BEEnterpriseHistory.dbo.CellReadingsHistory
                where StringRecordID = {self.string_record_id}
                and ReadingTypeRecordID = 6
                and ReadingDateTime between {first_day} and {last_day}"""

        cursor.execute(query)

        #This is a simple check for now, it should be upgraded in the future so that it actually looks
        #at the cell readings. This is to catch scenarios like one cell being read more than once.
        if (len(self.intertier_cells) == len(cursor)):
            return(True, len(self.intertier_cells),len(cursor))

        return (False, len(self.intertier_cells), len(cursor))


    def check_strap_impedance(self):
        #Needs a reading once a amonth

      #Needs a reading once a month
        """ This funciton checks to make sure that a substation has at least one intertier impedance reading for each of its cells
        in the intertier_cells attribute

        Args:

        day (date, optional): Any day within the month that will be queried. Functions use this date
        to return the first of the month. Defaults to get_last_month_date().

        Returns:
            Tuple[int, int]:(The amount of readings in the database, the amount of readings that there should have been)
        """

        first_day, last_day = utils.get_date_range_one_month(day)

        db_conn = utils.connect_to_database()

        cursor = db_conn.cursor()

        query = F"""SELECT CellNumber, ReadingDateTime, ReadingValue FROM BEEnterpriseHistory.dbo.CellReadingsHistory
                where StringRecordID = {self.string_record_id}
                and ReadingTypeRecordID = 9
                and ReadingDateTime between {first_day} and {last_day}"""

        cursor.execute(query)

        #This is a simple check for now, it should be upgraded in the future so that it actually looks
        #at the cell readings. This is to catch scenarios like one cell being read more than once.
        if (len(self.intertier_cells) == len(cursor)):
            return(True, len(self.intertier_cells),len(cursor))

        return (False, len(self.intertier_cells), len(cursor))



    def check_intertier_impedance(self, day: date = utils.get_last_month_date())->Tuple[bool, int, int]:
        #Needs a reading once a month
        """ This funciton checks to make sure that a substation has at least one intertier impedance reading for each of its cells
        in the intertier_cells attribute

        Args:

        day (date, optional): Any day within the month that will be queried. Functions use this date
        to return the first of the month. Defaults to get_last_month_date().

        Returns:
            Tuple[int, int]:(The amount of readings in the database, the amount of readings that there should have been)
        """

        first_day, last_day = utils.get_date_range_one_month(day)

        db_conn = utils.connect_to_database()

        cursor = db_conn.cursor()

        query = F"""SELECT CellNumber, ReadingDateTime, ReadingValue FROM BEEnterpriseHistory.dbo.CellReadingsHistory
                where StringRecordID = {self.string_record_id}
                and ReadingTypeRecordID = 10
                and ReadingDateTime between {first_day} and {last_day}"""

        cursor.execute(query)

        #This is a simple check for now, it should be upgraded in the future so that it actually looks
        #at the cell readings. This is to catch scenarios like one cell being read more than once.
        if (len(self.intertier_cells) == len(cursor)):
            return(True, len(self.intertier_cells),len(cursor))

        return (False, len(self.intertier_cells), len(cursor))

    def check_cell_voltage(self):
        #Needs a reading once a month
         """ This funciton checks to make sure that a substation has at least one intertier impedance reading for each of its cells
        in the intertier_cells attribute

        Args:

        day (date, optional): Any day within the month that will be queried. Functions use this date
        to return the first of the month. Defaults to get_last_month_date().

        Returns:
            Tuple[int, int]:(The amount of readings in the database, the amount of readings that there should have been)
        """

        first_day, last_day = utils.get_date_range_one_month(day)

        db_conn = utils.connect_to_database()

        cursor = db_conn.cursor()

        query = F"""SELECT CellNumber, ReadingDateTime, ReadingValue FROM BEEnterpriseHistory.dbo.CellReadingsHistory
                where StringRecordID = {self.string_record_id}
                and ReadingTypeRecordID = 8
                and ReadingDateTime between {first_day} and {last_day}"""

        cursor.execute(query)

        #This is a simple check for now, it should be upgraded in the future so that it actually looks
        #at the cell readings. This is to catch scenarios like one cell being read more than once.
        if (len(self.intertier_cells) == len(cursor)):
            return(True, len(self.intertier_cells),len(cursor))

        return (False, len(self.intertier_cells), len(cursor)
