
import unittest
import common.utilities

import numpy


class TestUtilities(unittest.TestCase):


    def test_sliceit_1d(self):
        aslice = [1, 2, 3, 4, 5]
        whole = []
        whole.append(aslice)
        actual = common.utilities.sliceit_assnapshot(whole)
        expected = []
        expected.append(aslice)
        [self.assertEquals(exp, act) for exp, act in zip(expected[0], actual[0])]

    
    def test_sliceit_asarray_1d(self):
        aslice = [1, 2, 3, 4, 5]
        whole = []
        whole.append(aslice)
        actual = common.utilities.sliceit_assnapshot_asarray(whole)
        expected = []
        expected.append(numpy.asarray(aslice))
        [self.assertEquals(exp, act) for exp, act in zip(expected[0], actual[0])]


    def test_exclude_initial_point_array_1d(self):
        values = numpy.asarray([0, 1, 2, 3, 4])
        actual = common.utilities.exclude_initial_point(values)
        expected = numpy.asarray([1, 2, 3, 4])
        [self.assertEquals(exp, act) for exp, act in zip(expected, actual)]
        try:
            actual.shape
            self.assertTrue(True)
        except:
            self.assertTrue(False)


    def test_exclude_initial_point_array_2d(self):
        values = numpy.asarray([[0, 1, 2, 3, 4], [10, 11, 12, 13, 14]])
        actual = common.utilities.exclude_initial_point(values)
        expected = numpy.asarray([[1, 2, 3, 4], [11, 12, 13, 14]])
        [self.assertEquals(exp, act) for exp, act in zip(expected[0], actual[0])]
        [self.assertEquals(exp, act) for exp, act in zip(expected[1], actual[1])]
        try:
            actual.shape
            self.assertTrue(True)
        except:
            self.assertTrue(False)
        
        
    def test_exclude_initial_point_array_3d_raises_exception(self):
        try:
            values = numpy.asarray([[[0, 1, 2, 3, 4], [10, 11, 12, 13, 14]], [[0, 1, 2, 3, 4], [10, 11, 12, 13, 14]]])
            _ = common.utilities.exclude_initial_point(values)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    
    def test_exclude_initial_point_list_1d(self):
        values = [0, 1, 2, 3, 4]
        actual = common.utilities.exclude_initial_point(values)
        expected = numpy.asarray([1, 2, 3, 4])
        [self.assertEquals(exp, act) for exp, act in zip(expected, actual)]
        try:
            actual.shape
            self.assertTrue(True)
        except:
            self.assertTrue(False)
        
        
    def test_exclude_initial_point_list_2d(self):
        values = numpy.asarray([[0, 1, 2, 3, 4], [10, 11, 12, 13, 14]])
        actual = common.utilities.exclude_initial_point(values)
        expected = numpy.asarray([[1, 2, 3, 4], [11, 12, 13, 14]])
        [self.assertEquals(exp, act) for exp, act in zip(expected[0], actual[0])]
        [self.assertEquals(exp, act) for exp, act in zip(expected[1], actual[1])]
        try:
            actual.shape
            self.assertTrue(True)
        except:
            self.assertTrue(False)


    def test_exclude_initial_point_unknown_type_raises_exception(self):
        values = None
        try:
            _ = common.utilities.exclude_initial_point(values)
            self.assertTrue(False)
        except:
            self.assertTrue(True)
        

if __name__ == "__main__":
    unittest.main()
