
import unittest
import data.data_splicing as testme

import numpy


class TestDataSplicing(unittest.TestCase):


    def test_splice_data_with_pattern_111000_even(self):
        values = numpy.arange(10)
        
        ones = testme.splice_data_with_pattern_111000_get_ones(values)
        actual = numpy.asarray([0,1,2,3,4])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = testme.splice_data_with_pattern_111000_get_zeros(values)
        actual = numpy.asarray([0,5,6,7,8,9])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_111000_odd(self):
        values = numpy.arange(11)
        
        ones = testme.splice_data_with_pattern_111000_get_ones(values)
        actual = numpy.asarray([0,1,2,3,4,5])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = testme.splice_data_with_pattern_111000_get_zeros(values)
        actual = numpy.asarray([0,6,7,8,9,10])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]

    
    def test_splice_data_with_pattern_000111_even(self):
        values = numpy.arange(10)
        
        ones = testme.splice_data_with_pattern_000111_get_ones(values)
        actual = numpy.asarray([0,5,6,7,8,9])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = testme.splice_data_with_pattern_000111_get_zeros(values)
        actual = numpy.asarray([0,1,2,3,4])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_000111_odd(self):
        values = numpy.arange(11)
        
        ones = testme.splice_data_with_pattern_000111_get_ones(values)
        actual = numpy.asarray([0,6,7,8,9,10])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = testme.splice_data_with_pattern_000111_get_zeros(values)
        actual = numpy.asarray([0,1,2,3,4,5])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]

    
    def test_splice_data_with_pattern_101010_even(self):
        values = numpy.arange(10)
        
        ones = testme.splice_data_with_pattern_101010_get_ones(values)
        actual = numpy.asarray([0,2,4,6,8])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = testme.splice_data_with_pattern_101010_get_zeros(values)
        actual = numpy.asarray([0,1,3,5,7,9])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_101010_odd(self):
        values = numpy.arange(11)
        
        ones = testme.splice_data_with_pattern_101010_get_ones(values)
        actual = numpy.asarray([0,2,4,6,8,10])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = testme.splice_data_with_pattern_101010_get_zeros(values)
        actual = numpy.asarray([0,1,3,5,7,9])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]

    
    def test_splice_data_with_pattern_110110_even(self):
        values = numpy.arange(10)
        
        ones = testme.splice_data_with_pattern_110110_get_ones(values)
        actual = numpy.asarray([0,1,3,4,6,7,9])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = testme.splice_data_with_pattern_110110_get_zeros(values)
        actual = numpy.asarray([0,2,5,8])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_110110_odd(self):
        values = numpy.arange(11)
        
        ones = testme.splice_data_with_pattern_110110_get_ones(values)
        actual = numpy.asarray([0,1,3,4,6,7,9,10])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = testme.splice_data_with_pattern_110110_get_zeros(values)
        actual = numpy.asarray([0,2,5,8])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_101101_even(self):
        values = numpy.arange(10)
        
        ones = testme.splice_data_with_pattern_101101_get_ones(values)
        actual = numpy.asarray([0,2,3,5,6,8,9])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = testme.splice_data_with_pattern_101101_get_zeros(values)
        actual = numpy.asarray([0,1,4,7,10])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_101101_odd(self):
        values = numpy.arange(11)
        
        ones = testme.splice_data_with_pattern_101101_get_ones(values)
        actual = numpy.asarray([0,2,3,5,6,8,9,11])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = testme.splice_data_with_pattern_101101_get_zeros(values)
        actual = numpy.asarray([0,1,4,7,10])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]

    
    def test_splice_data_with_pattern_011011_even(self):
        values = numpy.arange(10)
        
        ones = testme.splice_data_with_pattern_011011_get_ones(values)
        actual = numpy.asarray([0,1,2,4,5,7,8,10])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = testme.splice_data_with_pattern_011011_get_zeros(values)
        actual = numpy.asarray([0,3,6,9])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_splice_data_with_pattern_011011_odd(self):
        values = numpy.arange(11)
        
        ones = testme.splice_data_with_pattern_011011_get_ones(values)
        actual = numpy.asarray([0,1,2,4,5,7,8,10,11])
        [self.assertEquals(one, act) for one, act in zip(ones, actual)]
        
        zeros = testme.splice_data_with_pattern_011011_get_zeros(values)
        actual = numpy.asarray([0,3,6,9])
        [self.assertEquals(zero, act) for zero, act in zip(zeros, actual)]


    def test_convert_mask_to_index_expression(self):
        values = numpy.arange(10)
        
        mask = [4]
        actual = testme.convert_mask_to_index_expression(mask)
        ones = numpy.arange(4)
        zeroes = numpy.arange(4, 10)

        self.assertEqual(len(actual), 2)
        [self.assertEqual(val, act) for val, act in zip(values[actual[0]], ones)]
        [self.assertEqual(val, act) for val, act in zip(values[actual[1]], zeroes)]
        

    def test_splice_data_with_pattern_any_get_ones(self):
        values = numpy.arange(10)

        mask = [4]
        actual = testme.splice_data_with_pattern_any_get_ones(mask, values)
        ones = numpy.arange(4)
        [self.assertEqual(val, act) for val, act in zip(actual, ones)]
        
        mask = [3,6]
        actual = testme.splice_data_with_pattern_any_get_ones(mask, values)
        ones = numpy.concatenate((numpy.arange(3), numpy.arange(6, 10)))
        [self.assertEqual(val, act) for val, act in zip(actual, ones)]


    def test_splice_data_with_pattern_any_get_zeros(self):
        values = numpy.arange(10)
        
        mask = [4]
        actual = testme.splice_data_with_pattern_any_get_zeros(mask, values)
        ones = numpy.arange(4,10)
        [self.assertEqual(val, act) for val, act in zip(actual, ones)]

        mask = [2,5,7]
        actual = testme.splice_data_with_pattern_any_get_zeros(mask, values)
        ones = numpy.concatenate((numpy.arange(2,5), numpy.arange(7, 10)))
        [self.assertEqual(val, act) for val, act in zip(actual, ones)]


    def test_splice_data_with_pattern_any(self):
        mask = [5, 10]
        times = numpy.arange(15)
        meas = [numpy.arange(15,30)]
        
        actual = testme.splice_data_with_pattern_any(mask, times, meas)
        calib = numpy.concatenate((numpy.arange(0,5), numpy.arange(10,15)))
        [self.assertEqual(cal, act) for cal, act in zip(actual["calib"]["time"], calib)]
        calib = numpy.concatenate((numpy.arange(15,20), numpy.arange(25,30)))
        [self.assertEqual(cal, act) for cal, act in zip(actual["calib"]["meas"][0], calib)]
        
        actual = testme.splice_data_with_pattern_any(mask, times, meas)
        valid = numpy.arange(5,10)
        [self.assertEqual(val, act) for val, act in zip(actual["valid"]["time"], valid)]
        valid = numpy.arange(20,25)
        [self.assertEqual(val, act) for val, act in zip(actual["valid"]["meas"][0], valid)]


if __name__ == "__main__":
    unittest.main()