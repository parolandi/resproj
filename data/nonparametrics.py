
import numpy

def cutoff_tail_by_count(data, count):
    assert(count < len(data))
    
    return numpy.sort(data)[0:-count]
