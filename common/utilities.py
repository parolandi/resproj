
import numpy

import common.exceptions


# delete the initial point
# returns a numpy array
# fully unit-tested
def exclude_initial_point(points):
    try:
        values = numpy.asarray(points)
        # it is an array
        dims = len(values.shape)
        common.exceptions.assert_throw(dims > 0 and dims <3)
        if dims > 1:
            # multiple inner lists
            # efficiency: http://stackoverflow.com/questions/12299124/how-to-use-numpy-vstack
            values_excluding_initial = []
            for ii in range(len(values)):
                values_excluding_initial.append(numpy.delete(values[ii], 0))
            return numpy.asarray(values_excluding_initial)
        else:
            return numpy.delete(values, 0)
    except:
        common.exceptions.assert_throw(False) 


# size a multidimensional list 
def size_it(data):
    size = 0
    try:
        size = sum(map(len, data))
    except:
        size = len(data)
    return size


def sliceit_assnapshot(packed_vector):
    collection_of_points = []
    for points in packed_vector:
        stack_of_points = []
        for point in points:
            stack_of_points.append(point)
        collection_of_points.append(points)
    return collection_of_points


def sliceit_assnapshot_asarray(packed_vector):
    stack_of_points = sliceit_assnapshot(packed_vector)
    return numpy.asarray(stack_of_points)


def sliceit_astrajectory(packed_vector):
    snapshots = numpy.asarray(packed_vector)
    trajectories = numpy.transpose(snapshots)
    return trajectories


# TODO: unit-test
def get_maximum_absolute_sensitivity_value(sensitivity_trajectories, dim_states, dim_dv):
    max_sens = numpy.max(numpy.abs(sensitivity_trajectories), axis=1)
    sens_max = max_sens.reshape(dim_states, dim_dv).transpose()
    return sens_max


def get_maximum_absolute_ensemble_values(ensembles):
    assert(len(ensembles) > 0)
    max_ensn = numpy.max(numpy.abs(ensembles), axis=1)
    return max_ensn
