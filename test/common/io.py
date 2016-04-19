
import unittest
import common.io as testme

import numpy as np


class TestIO(unittest.TestCase):


    def test_write_to_csv(self):
        vals = np.ones((4,5))
        testme.write_to_csv(vals, "C:/workspace/resproj/test/common/test_write_to_csv.csv")
        self.assertTrue(True)
        
        
    def test_read_from_csv(self):
        testme.read_from_csv("C:/workspace/resproj/test/common/test_read_from_csv.csv")
        self.assertTrue(True)


    def test_write_to_txt(self):
        vals = np.ones((4,5))
        testme.write_to_txt(np.array_str(vals), "C:/workspace/resproj/test/common/test_write_to_txt.txt")
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()