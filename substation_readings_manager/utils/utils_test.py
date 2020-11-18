import unittest
from datetime import date

import pyodbc

import utils as df

class LastMonthDate(unittest.testCase):

    def test_connect_to_database(self):
        self.assertIs(type(df.connect_to_database()), pyodbc.Connection)

    def test_get_last_month_date(self):
        self.assertIs(type(df.get_last_month_date()), date)

    def test_get_string_record_id_to_name_dict(self):
        #There is potentially an issue here, I've seen the database values
        #change sometimes

        self.assertIs(type(df.get_string_record_id_to_name_dict()), dict)

    def test_check_substation(self):

        pass

    def test_workbook_name(self):
        self.assertEqual(df.workbook_name(date(2020, 10, 29)), "October 2020 MPC Battery Report.xlsx")

    def test_program_status(self):
        self.assertIs(df.program_status("Malborn", "Cell Voltage",6),
                       "Substation Malborn Cell Voltage Cell: 6")

    def test_query_database_cell_values(self):

#What do I need to assert on this funciton? I need to assert whether or not,for a known value in the database?
# Yes, I can call a query maybe on a known value
#
#

if __name__ == '__main__':
    unittest.main()