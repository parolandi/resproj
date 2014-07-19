
import unittest
import common.utilities

import numpy

class TestUtilities(unittest.TestCase):


    def test_sliceit(self):
        aslice = [1, 2, 3, 4, 5]
        whole = []
        whole.append(aslice)
        actual = common.utilities.sliceit(whole)
        expected = numpy.array(1)
        self.assertEquals(expected, actual)

    
    def test_sliceit_asarray(self):
        aslice = [1, 2, 3, 4, 5]
        whole = []
        whole.append(aslice)
        actual = common.utilities.sliceit_asarray(whole)
        expected = numpy.array(1)
        self.assertEquals(expected, actual)


if __name__ == "__main__":
    unittest.main()
