"""This module queries the MPC Battery Data Database and checks for missing values."""

from datetime import date
import calendar

import substation_readings_manager.utils.database_functions as df
import substation_readings_manager.email_manager.email_lib as el
from substation_readings_manager.excel_file.excel_file import ExcelFile
from substation_readings_manager.substation.substation import Substation
import substation_readings_manager.utils.workbook as wb


def main():

    workbook_name = wb.workbook_name(date(2020,8,4))

    workbook = ExcelFile(workbook_name)

    x = df.string_record_id_to_intertier_cells_monitor()

    for string_record_id, value in x.items():

        sub = Substation(string_record_id, value[0], value[1])

        sub.print_values()
