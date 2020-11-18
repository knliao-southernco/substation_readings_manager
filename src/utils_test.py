import unittest
from datetime import date

import pyodbc

import utils as df 

class LastMonthDate(unittest.TestCase):
    
    def test_connect_to_database(self): 
        self.assertIs(type(df.connect_to_database()), pyodbc.Connection)
    
    """Test that it returns a date 

    """

    def test_get_last_month_date(self):
        self.assertIs(type(df.get_last_month_date()), date)

    def test_get_stringrecordid_to_name_dict(self):
        #There is potentially an issue here, I've seen the database values 
        #change sometimes 

        self.assertIs(type(df.get_stringrecordid_to_name_dict()), dict)

    def test_check_substation(self):
        
#What do I need to assert on this funciton? I need to assert whether or not,for a known value in the database?
# Yes, I can call a query maybe on a known value
#
#

if __name__ == '__main__':
    unittest.main() 