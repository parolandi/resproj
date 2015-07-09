
import unittest
import results.plot_3d as testme

import numpy as np


class TestPlot3d(unittest.TestCase):


    def test_plot_3d_from_file(self):
        region = np.loadtxt("C:/workspace/resproj/test/mock/multiplepoints.txt",delimiter=',')
        testme.plot_3d(region, [1,2,3])
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()