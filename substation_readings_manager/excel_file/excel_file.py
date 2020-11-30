"""This class is responsible for creating the excel sheet and writing to it.
"""

import xlsxwriter

from substation_readings_manager.substation.substation import Substation

class ExcelFile:

    def __init__(self, workbook_name):
        self.workbook = xlsxwriter.Workbook(workbook_name)

        self.key = self.workbook.add_worksheet('Key')
        self.overall = self.workbook.add_worksheet('Overall')

        self.overall_row = 1

        self.format()

    def format(self):
        impedance_format = self.workbook.add_format()
        impedance_format.set_bg_color('red')

        voltage_format = self.workbook.add_format()
        voltage_format.set_bg_color('blue')

        both_format = self.workbook.add_format()
        both_format.set_bg_color('purple')

        self.key.write('A1', 'Key')
        self.key.write('A2','', impedance_format)
        self.key.write('A3', '', voltage_format)
        self.key.write('A4', '', both_format)

        self.key.write('B2', 'Indicates Impedance Value Missing')
        self.key.write('B3', 'Indicates a certain percentage of Voltage Values missing')
        self.key.write('B4', 'Both')

    def close(self):
        self.workbook.close()


    def analyze_substation(self, substation: Substation):

        if len(substation.cell_voltage_readings.readings < 30):

