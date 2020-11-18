"""This module queries the MPC Battery Data Database and checks for missing values."""

# Openpyxl is chosen over xlsxwriter because of better functionality when writing to subdirectories
from datetime import date
import calendar

import xlsxwriter

import src.utils as df
import src.email_manager.email_lib as el
from src.worksheet import ExcelFile


def main():
   # reading_type_dict = {6: "Cell Impedance", 8: "Cell Voltage",
    #                     9: "Strap Impedance", 10: "Intertier Impedance"}

    reading_type_dict = {6: "Cell Impedance", 8: "Cell Voltage",
    9:"Strap Impedance"}

    stringrecordid_name_dict = df.get_stringrecordid_to_name_dict()

    excel_file = ExcelFile(df.workbook_name())

    for reading_type in reading_type_dict:
        for string_id in stringrecordid_name_dict:
            reading_count = 0

            for cell_number in range(1, 60):
                df.print_status(stringrecordid_name_dict.get(string_id), reading_type_dict.get(reading_type), cell_number)
                readings = df.query_database_cell_values(string_id, reading_type,
                                                         cell_number)

                reading_count += len(readings[0])


            if (reading_count <= 59):
                if (reading_type == 6):
                    excel_file.write_to_cell_impedance(stringrecordid_name_dict.get(string_id),
                                                                    reading_count, 59)
                if (reading_type == 8):
                    excel_file.write_to_cell_voltage(stringrecordid_name_dict.get(string_id),
                    reading_count, 59)

                if (reading_type == 9):
                    excel_file.write_to_strap_impedance(stringrecordid_name_dict.get(string_id),
                    reading_count, 59)


    excel_file.close()

    el.send_email(df.workbook_name())
