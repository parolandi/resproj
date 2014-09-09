
import copy
import numpy

# TODO: assert shapes
def splice_data_with_pattern_111000_get_ones(values):
    half = len(values) // 2
    ones = values[slice(0, half, 1)]
    return ones


def splice_data_with_pattern_111000_get_zeros(values):
    half = len(values) // 2
    zeros = numpy.concatenate(( \
        [copy.deepcopy(values[0])], \
        values[slice(half, len(values), 1)]))
    return zeros


def splice_data_with_pattern_000111_get_ones(values):
    half = len(values) // 2
    zeros = numpy.concatenate(( \
        [copy.deepcopy(values[0])], \
        values[slice(half, len(values), 1)]))
    return zeros


def splice_data_with_pattern_000111_get_zeros(values):
    half = len(values) // 2
    ones = values[slice(0, half, 1)]
    return ones


def splice_data_with_pattern_101010_get_ones(values):
    ones = numpy.delete(values, numpy.s_[1::2])
    return ones


def splice_data_with_pattern_101010_get_zeros(values):
    zeros = numpy.concatenate(( \
        [copy.deepcopy(values[0])],
        numpy.delete(values, numpy.s_[0::2])))
    return zeros


def splice_data_with_pattern_110110_get_ones(values):
    ones = numpy.delete(values, numpy.s_[2::3])
    return ones


def splice_data_with_pattern_110110_get_zeros(values):
    vals = numpy.delete(values, numpy.s_[0::3])
    zeros = numpy.concatenate(( \
        [copy.deepcopy(values[0])],
        numpy.delete(vals, numpy.s_[0::2])))
    return zeros
