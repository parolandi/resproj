
import math

def exponential(parameters, independent, ordenate, step):
    values = []
    for abscisae in independent:
        values.append(step * (1 + ordenate - math.exp(-abscisae)))
    return values
