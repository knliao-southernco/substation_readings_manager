import os
import unittest

from ExcelFile import ExcelFile

class ExcelFileTest(unittest.TestCase):

    def test_create_excel_file(self):
        excel_file = ExcelFile("Excel_Test.xlsx")
        excel_file.close()
        self.assertTrue(os.path.exists("./Excel_Test.xlsx"))



if __name__ == '__main__':
    unittest.main()