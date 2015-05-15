
import copy
import numpy


pseudo_experimental_dataset = {
    "time": [],
    # measurements subject to noise
    "meas": [],
    "true": [],
    "noise": [],
    }


calib_valid_data = {
    "id": "",
    "calib": dict(pseudo_experimental_dataset),
    "valid": dict(pseudo_experimental_dataset),
    }


def format_dataset_id(pattern, dim):
    return "-p-" + pattern + "-n-" + dim
    

# TODO: noise
# TODO: true
'''
returns data.data_splicing.calib_valid_data
'''
def splice_data_with_pattern(splicer_ones, splicer_zeros, times, meas, noise, true):
    datasets = dict(calib_valid_data)
    calib_meas = []
    for ii in range(len(meas)):
        calib_meas.append(splicer_ones(meas[ii]))
    datasets["calib"]["meas"] = calib_meas
    datasets["calib"]["time"] = splicer_ones(times)
    valid_meas = []
    for ii in range(len(meas)):
        valid_meas.append(splicer_zeros(meas[ii]))
    datasets["valid"]["meas"] = valid_meas
    datasets["valid"]["time"] = splicer_zeros(times)
    return datasets


# TODO: assert shapes
def splice_data_with_pattern_111000_get_ones(values):
    half = len(values) // 2
    remainder = len(values) % 2
    ones = values[slice(0, half+remainder, 1)]
    return ones


def splice_data_with_pattern_111000_get_zeros(values):
    half = len(values) // 2
    remainder = len(values) % 2
    zeros = numpy.concatenate(( \
        [copy.deepcopy(values[0])], \
        values[slice(half+remainder, len(values), 1)]))
    return zeros


'''
returns: calib_valid_data
'''
def splice_data_with_pattern_111000(times, meas, noise, true):
    datasets = splice_data_with_pattern(splice_data_with_pattern_111000_get_ones, \
        splice_data_with_pattern_111000_get_zeros, times, meas, noise, true)
    datasets["id"] = format_dataset_id("111000", str(len(times)))
    # WIP: add warning on diff len()
    return datasets
    

def splice_data_with_pattern_000111_get_ones(values):
    half = len(values) // 2
    remainder = len(values) % 2
    zeros = numpy.concatenate(( \
        [copy.deepcopy(values[0])], \
        values[slice(half+remainder, len(values), 1)]))
    return zeros


def splice_data_with_pattern_000111_get_zeros(values):
    half = len(values) // 2
    remainder = len(values) % 2
    ones = values[slice(0, half+remainder, 1)]
    return ones


def splice_data_with_pattern_000111(times, meas, noise, true):
    datasets = splice_data_with_pattern(splice_data_with_pattern_000111_get_ones, \
        splice_data_with_pattern_000111_get_zeros, times, meas, noise, true)
    datasets["id"] = format_dataset_id("000111", str(len(times)))
    return datasets


def splice_data_with_pattern_101010_get_ones(values):
    ones = numpy.delete(values, numpy.s_[1::2])
    return ones


def splice_data_with_pattern_101010_get_zeros(values):
    zeros = numpy.concatenate(( \
        [copy.deepcopy(values[0])],
        numpy.delete(values, numpy.s_[0::2])))
    return zeros


def splice_data_with_pattern_101010(times, meas, noise, true):
    datasets = splice_data_with_pattern(splice_data_with_pattern_101010_get_ones, \
        splice_data_with_pattern_101010_get_zeros, times, meas, noise, true)
    datasets["id"] = format_dataset_id("101010", str(len(times)))
    return datasets


def splice_data_with_pattern_110110_get_ones(values):
    ones = numpy.delete(values, numpy.s_[2::3])
    return ones


def splice_data_with_pattern_110110_get_zeros(values):
    vals = numpy.delete(values, numpy.s_[0::3])
    zeros = numpy.concatenate(( \
        [copy.deepcopy(values[0])],
        numpy.delete(vals, numpy.s_[0::2])))
    return zeros


def splice_data_with_pattern_110110(times, meas, noise, true):
    datasets = splice_data_with_pattern(splice_data_with_pattern_110110_get_ones, \
        splice_data_with_pattern_110110_get_zeros, times, meas, noise, true)
    datasets["id"] = format_dataset_id("110110", str(len(times)))
    return datasets


def splice_data_with_pattern_101101_get_ones(values):
    ones = numpy.delete(values, numpy.s_[1::3])
    return ones


def splice_data_with_pattern_101101_get_zeros(values):
    vals = numpy.delete(values, numpy.s_[0::3])
    zeros = numpy.concatenate(( \
        [copy.deepcopy(values[0])],
        numpy.delete(vals, numpy.s_[1::2])))
    return zeros


def splice_data_with_pattern_101101(times, meas, noise, true):
    datasets = splice_data_with_pattern(splice_data_with_pattern_101101_get_ones, \
        splice_data_with_pattern_101101_get_zeros, times, meas, noise, true)
    datasets["id"] = format_dataset_id("101101", str(len(times)))
    return datasets


def splice_data_with_pattern_011011_get_ones(values):
    vals = numpy.delete(values, numpy.s_[0::3])
    ones = numpy.concatenate(( \
        [copy.deepcopy(values[0])],
        vals))
    return ones


def splice_data_with_pattern_011011_get_zeros(values):
    vals = numpy.delete(values, numpy.s_[1::3])
    zeros = numpy.delete(vals, numpy.s_[1::2])
    return zeros


def splice_data_with_pattern_011011(times, meas, noise, true):
    datasets = splice_data_with_pattern(splice_data_with_pattern_011011_get_ones, \
        splice_data_with_pattern_011011_get_zeros, times, meas, noise, true)
    datasets["id"] = format_dataset_id("011011", str(len(times)))
    return datasets


def convert_mask_to_index_expression(mask):
    end = 0
    slices = []
    for ii in range(len(mask)):
        start = end
        end = mask[ii]
        slc = slice(start, end, 1)
        slices.append(slc)
    start = end
    slc = slice(start, None, 1)
    slices.append(slc)
    return tuple(slices)


def splice_data_with_pattern_any_get_ones(mask, values):
    slices = convert_mask_to_index_expression(mask)
    slcs = []
    for ii in range(0, len(slices), 2):
        slcs.append(values[slices[ii]])
    ones = slcs[0]
    for ii in range(1, len(slcs)):
        ones = numpy.concatenate((ones, slcs[ii]))
    return ones


def splice_data_with_pattern_any_get_zeros(mask, values):
    slices = convert_mask_to_index_expression(mask)
    slcs = []
    for ii in range(1, len(slices), 2):
        slcs.append(values[slices[ii]])
    zeros = slcs[0]
    for ii in range(1, len(slcs)):
        zeros = numpy.concatenate((zeros, slcs[ii]))
    return zeros

def splice_data_with_pattern_any(mask, times, meas):
    """
    mask       list of splicing times
    times      time array
    meas       list of measurements array
    returns    calib_valid_data
    """
    datasets = dict(calib_valid_data)
    datasets["id"] = format_dataset_id("any", str(len(times)))
    calib_meas = []
    for ii in range(len(meas)):
        calib_meas.append(splice_data_with_pattern_any_get_ones(mask, meas[ii]))
    datasets["calib"]["meas"] = calib_meas
    datasets["calib"]["time"] = splice_data_with_pattern_any_get_ones(mask, times)
    valid_meas = []
    for ii in range(len(meas)):
        valid_meas.append(splice_data_with_pattern_any_get_zeros(mask, meas[ii]))
    datasets["valid"]["meas"] = valid_meas
    datasets["valid"]["time"] = splice_data_with_pattern_any_get_zeros(mask, times)
    return datasets
