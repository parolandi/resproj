
import unittest
import data.data_splicing

import numpy


class TestDataSplicing(unittest.TestCase):


    def test_splice_data_with_pattern_111000_even(self):
        values = numpy.arange(10)
        
        ones = data.data_splicing.splice_data_with_pattern_111000_get_ones(values)
        actual = numpy.asarray([0,1,2,3,4])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_111000_get_zeros(values)
        actual = numpy.asarray([0,5,6,7,8,9])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_111000_odd(self):
        values = numpy.arange(11)
        
        ones = data.data_splicing.splice_data_with_pattern_111000_get_ones(values)
        actual = numpy.asarray([0,1,2,3,4,5])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_111000_get_zeros(values)
        actual = numpy.asarray([0,6,7,8,9,10])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]

    
    def test_splice_data_with_pattern_000111_even(self):
        values = numpy.arange(10)
        
        ones = data.data_splicing.splice_data_with_pattern_000111_get_ones(values)
        actual = numpy.asarray([0,5,6,7,8,9])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_000111_get_zeros(values)
        actual = numpy.asarray([0,1,2,3,4])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_000111_odd(self):
        values = numpy.arange(11)
        
        ones = data.data_splicing.splice_data_with_pattern_000111_get_ones(values)
        actual = numpy.asarray([0,6,7,8,9,10])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_000111_get_zeros(values)
        actual = numpy.asarray([0,1,2,3,4,5])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]

    
    def test_splice_data_with_pattern_101010_even(self):
        values = numpy.arange(10)
        
        ones = data.data_splicing.splice_data_with_pattern_101010_get_ones(values)
        actual = numpy.asarray([0,2,4,6,8])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_101010_get_zeros(values)
        actual = numpy.asarray([0,1,3,5,7,9])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_101010_odd(self):
        values = numpy.arange(11)
        
        ones = data.data_splicing.splice_data_with_pattern_101010_get_ones(values)
        actual = numpy.asarray([0,2,4,6,8,10])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_101010_get_zeros(values)
        actual = numpy.asarray([0,1,3,5,7,9])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]

    
    def test_splice_data_with_pattern_110110_even(self):
        values = numpy.arange(10)
        
        ones = data.data_splicing.splice_data_with_pattern_110110_get_ones(values)
        actual = numpy.asarray([0,1,3,4,6,7,9])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_110110_get_zeros(values)
        actual = numpy.asarray([0,2,5,8])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_110110_odd(self):
        values = numpy.arange(11)
        
        ones = data.data_splicing.splice_data_with_pattern_110110_get_ones(values)
        actual = numpy.asarray([0,1,3,4,6,7,9,10])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_110110_get_zeros(values)
        actual = numpy.asarray([0,2,5,8])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_101101_even(self):
        values = numpy.arange(10)
        
        ones = data.data_splicing.splice_data_with_pattern_101101_get_ones(values)
        actual = numpy.asarray([0,2,3,5,6,8,9])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_101101_get_zeros(values)
        actual = numpy.asarray([0,1,4,7,10])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_101101_odd(self):
        values = numpy.arange(11)
        
        ones = data.data_splicing.splice_data_with_pattern_101101_get_ones(values)
        actual = numpy.asarray([0,2,3,5,6,8,9,11])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_101101_get_zeros(values)
        actual = numpy.asarray([0,1,4,7,10])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]

    
    def test_splice_data_with_pattern_011011_even(self):
        values = numpy.arange(10)
        
        ones = data.data_splicing.splice_data_with_pattern_011011_get_ones(values)
        actual = numpy.asarray([0,1,2,4,5,7,8,10])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_011011_get_zeros(values)
        actual = numpy.asarray([0,3,6,9])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_011011_odd(self):
        values = numpy.arange(11)
        
        ones = data.data_splicing.splice_data_with_pattern_011011_get_ones(values)
        actual = numpy.asarray([0,1,2,4,5,7,8,10,11])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = data.data_splicing.splice_data_with_pattern_011011_get_zeros(values)
        actual = numpy.asarray([0,3,6,9])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


if __name__ == "__main__":
    unittest.main()