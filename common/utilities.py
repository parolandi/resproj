
import numpy

def sliceit(packed_vector):
    points = []
    for point in packed_vector:
        points.append(point[0])
    return points


def sliceit_asarray(packed_vector):
    points = sliceit(packed_vector)
    return numpy.asarray(points)
