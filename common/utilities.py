
import numpy

def sliceit(packed_vector):
    collection_of_points = []
    for points in packed_vector:
        stack_of_points = []
        for point in points:
            stack_of_points.append(point)
        collection_of_points.append(points)
    return collection_of_points


def sliceit_asarray(packed_vector):
    stack_of_points = sliceit(packed_vector)
    return numpy.asarray(stack_of_points)
