
import unittest
import common.utilities

import numpy

class TestUtilities(unittest.TestCase):


    def test_sliceit_1d(self):
        aslice = [1, 2, 3, 4, 5]
        whole = []
        whole.append(aslice)
        actual = common.utilities.sliceit(whole)
        expected = []
        expected.append(aslice)
        [self.assertEquals(exp, act) for exp, act in zip(expected[0], actual[0])]

    
    def test_sliceit_asarray_1d(self):
        aslice = [1, 2, 3, 4, 5]
        whole = []
        whole.append(aslice)
        actual = common.utilities.sliceit_asarray(whole)
        expected = []
        expected.append(numpy.asarray(aslice))
        [self.assertEquals(exp, act) for exp, act in zip(expected[0], actual[0])]


if __name__ == "__main__":
    unittest.main()
