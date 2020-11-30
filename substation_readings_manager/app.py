"""This module queries the MPC Battery Data Database and checks for missing values."""

from datetime import date
import calendar

import xlsxwriter

import substation_readings_manager.utils.utils as df
import substation_readings_manager.email_manager.email_lib as el
from substation_readings_manager.excel_file.ExcelFile import ExcelFile

def main():

    reading_type_dict = {6: "Cell Impedance", 8: "Cell Voltage",
    9:"Strap Impedance"}

    string_record_id_name_dict = df.get_string_record_id_to_name_dict()

    workbook_name = df.workbook_name()

    excel_file = ExcelFile(workbook_name)

    for reading_type in reading_type_dict:
        for string_record_id in string_record_id_name_dict:
            reading_count = 0

            for cell_number in range(1, 60):
                print(df.program_status(string_record_id_name_dict.get(string_record_id), reading_type_dict.get(reading_type), cell_number))

                readings = df.check_database_values(string_record_id, reading_type,
                                                         cell_number)

            if (reading_count <= 59):
                if (reading_type == 6):
                    excel_file.write_to_cell_impedance(string_record_id_name_dict.get(string_record_id),
                                                                    reading_count, 59)
                if (reading_type == 8):
                    excel_file.write_to_cell_voltage(string_record_id_name_dict.get(string_record_id),
                    reading_count, 59)

                if (reading_type == 9):
                    excel_file.write_to_strap_impedance(string_record_id_name_dict.get(string_record_id),
                    reading_count, 59)


    excel_file.close()

    el.send_email(df.workbook_name())
