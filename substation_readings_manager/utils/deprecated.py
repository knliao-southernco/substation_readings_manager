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

        first_day, last_day = get_date_range_one_month(day)

        query_date_list = []

        for reading in reading_list:
            query_date_list.append(reading)

        days_between_two_dates = get_all_days_between_two_dates(
            first_day, last_day)

        return set(query_date_list) == set(days_between_two_dates)