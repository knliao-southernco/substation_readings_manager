"""This module queries the MPC Battery Data Database and checks for missing values."""

# Openpyxl is chosen over xlsxwriter because of better functionality when writing to subdirectories
from datetime import date
import calendar

from openpyxl import Workbook

import substation_readings_manager.utils as df
import substation_readings_manager.email_manager.email_lib as el
from substation_readings_manager.substation import Substation
from substation_readings_manager.worksheet import Worksheet


def main():

    wb = ExcelFile()

    x = df.get_string_record_id_to_name_dict()

    for id in x:
        z = Substation(y, df.get_intertier_cells(y) )


