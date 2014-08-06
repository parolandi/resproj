
import numpy

# size a multidimensional list 
def size_it(data):
    return sum(map(len, data)) 


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
