
import numpy


# delete the initial point
# returns a numpy array
def exclude_initial_point(values):
    if len(values) == 1:
        return numpy.delete(values, 0)

    values_excluding_initial = []
    for ii in range(len(values)):
        values_excluding_initial.append(numpy.delete(values[ii], 0))
    return values_excluding_initial


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
