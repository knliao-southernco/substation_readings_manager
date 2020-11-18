"""This class is responsible for creating the excel sheet and writing to it.
"""

import xlsxwriter

class ExcelFile:
    """[summary]
    """
    def __init__(self, workbook_name):
        self.workbook = xlsxwriter.Workbook(workbook_name)

        self.key = self.workbook.add_worksheet('Key')
        self.overall = self.overall.add_worksheet('Overall')

        self.cell_impedance = self.workbook.add_worksheet('Cell Impedance')
        self.cell_voltage = self.workbook.add_worksheet('Cell Voltage')
        self.strap_impedance = self.workbook.add_worksheet('Strap Impedance')
        self.intertier_impedance = self.workbook.add_worksheet('Intertier Impedance')

        self.cell_impedance_row = 1
        self.cell_voltage_row = 1
        self.strap_impedance_row = 1
        self.intertier_impedance_row = 1

        self.cell_impedance.write(0, 0, "Substation Name")
        self.cell_impedance.write(0, 1, "Actual Number")
        self.cell_impedance.write(0, 2, "Expected Number")

        self.cell_voltage.write(0, 0, "Substation Name")
        self.cell_voltage.write(0, 1, "Actual Number")
        self.cell_voltage.write(0, 2, "Expected Number")

        self.strap_impedance.write(0, 0, "Substation Name")
        self.strap_impedance.write(0, 1, "Actual Readings")
        self.strap_impedance.write(0, 2, "Expected Number")

        self.intertier_impedance.write(0, 0, "Substation Name")
        self.intertier_impedance.write(0, 1, "Actual Readings")
        self.intertier_impedance.write(0, 2, "Expected Number")


    def write_to_cell_impedance(self, substation_name, num_readings: int,
                                     required_readings: int):

        if num_readings < required_readings:
            self.cell_impedance.write(self.cell_impedance_row, 0, substation_name)
            self.cell_impedance.write(self.cell_impedance_row, 1, num_readings)
            self.cell_impedance.write(self.cell_impedance_row, 2, required_readings)

        self.cell_impedance_row += 1

    def write_to_cell_voltage(self, substation_name, num_readings: int,
                                     required_readings: int):
        if num_readings < required_readings:
            self.cell_voltage.write(self.cell_voltage_row, 0, substation_name)
            self.cell_voltage.write(self.cell_voltage_row, 1, num_readings)
            self.cell_voltage.write(self.cell_voltage_row, 2, required_readings)

        self.cell_voltage_row += 1


    def write_to_strap_impedance(self, substation_name, num_readings: int,
                                     required_readings: int):

        if num_readings < required_readings:
            self.strap_impedance.write(self.strap_impedance_row, 0, substation_name)
            self.strap_impedance.write(self.strap_impedance_row, 1, num_readings)
            self.strap_impedance.write(self.strap_impedance_row, 2, required_readings)

        self.strap_impedance_row += 1


    def write_to_intertier_impedance(self, substation_name, num_readings: int,
                                     required_readings: int):


        if num_readings < required_readings:

            self.intertier_impedance.write(self.intertier_impedance_row, 0, substation_name)
            self.intertier_impedance.write(self.intertier_impedance_row, 1, num_readings)
            self.intertier_impedance.write(self.intertier_impedance_row, 2, required_readings)


        self.intertier_impedance_row += 1

    def close(self):
        self.workbook.close()

