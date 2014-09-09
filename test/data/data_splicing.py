
import unittest
import data.data_splicing

import numpy


class TestDataSplicing(unittest.TestCase):


    def test_splice_data_with_pattern_111000(self):
        values = numpy.arange(10)
        
        ones = data.data_splicing.splice_data_with_pattern_111000_get_ones(values)
        actual = numpy.asarray([0,1,2,3,4])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_111000_get_zeros(values)
        actual = numpy.asarray([0,5,6,7,8,9])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_000111(self):
        values = numpy.arange(10)
        
        ones = data.data_splicing.splice_data_with_pattern_000111_get_ones(values)
        actual = numpy.asarray([0,5,6,7,8,9])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_000111_get_zeros(values)
        actual = numpy.asarray([0,1,2,3,4])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_101010(self):
        values = numpy.arange(10)
        
        ones = data.data_splicing.splice_data_with_pattern_101010_get_ones(values)
        actual = numpy.asarray([0,2,4,6,8])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_101010_get_zeros(values)
        actual = numpy.asarray([0,1,3,5,7,9])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_110110(self):
        values = numpy.arange(10)
        
        ones = data.data_splicing.splice_data_with_pattern_110110_get_ones(values)
        actual = numpy.asarray([0,1,3,4,6,7,9])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_110110_get_zeros(values)
        actual = numpy.asarray([0,2,5,8])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


if __name__ == "__main__":
    unittest.main()