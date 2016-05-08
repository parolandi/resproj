
import unittest
import common.io as testme

import numpy as np
import common.environment as coen


class TestIO(unittest.TestCase):


    def test_write_to_csv(self):
        vals = np.ones((4,5))
        testme.write_to_csv(vals, coen.get_src_location() + "/test/common/test_write_to_csv.csv")
        self.assertTrue(True)
        
        
    def test_read_from_csv(self):
        testme.read_from_csv(coen.get_src_location() + "/test/common/test_read_from_csv.csv")
        self.assertTrue(True)


    def test_write_to_txt(self):
        vals = np.ones((4,5))
        testme.write_to_txt(np.array_str(vals), coen.get_src_location() + "/test/common/test_write_to_txt.txt")
        self.assertTrue(True)
        
    def test_write_to_csv_is_none(self):
        testme.write_to_csv(None, coen.get_results_location() + "test_write_to_csv_none.csv")


if __name__ == "__main__":
    unittest.main()