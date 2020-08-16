# File Util.py
# Contains some helpful functions which don't inherently belong to any class

from math import sqrt, pow

FUNCTION_STRINGS = ['1', 'n', 'n\u00B2', 'n\u00B3']


def object_distance(object1, object2):
    """Returns the absolute Euclidean distance between two QObjects object1 and object2"""
    if not object1 or not object2:
        return None

    x_distance = object1.x() - object2.x()
    y_distance = object1.y() - object2.y()
    return sqrt(pow(x_distance, 2) + pow(y_distance, 2))


def movement_delta(source, destination, distance):
    """Returns the vector along which the source would need to move along in order to reach it's destination
       with the additional restriction of only moving distance """
    if not source or not destination:
        return 0, 0

    total_distance = object_distance(source, destination)

    # you are on the object, no movement required
    if total_distance == 0:
        return 0, 0
    fraction_of_total_distance = distance / total_distance
    delta_x = (destination.x() - source.x()) * fraction_of_total_distance
    delta_y = (destination.y() - source.y()) * fraction_of_total_distance
    return delta_x, delta_y


def close_enough(object1, object2, epsilon):
    """Determines if two object are closer than epsilon distance apart"""
    if object1 and object2:
        return object_distance(object1, object2) <= epsilon
    return False


def reverse_vector_2d(vector):
    """Takes in a 2-tuple and reverses the direction"""
    return vector[0] * -1, vector[1] * -1
