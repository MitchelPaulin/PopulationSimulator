# File Util.py
# Contains some helpful functions which don't inherently belong to any class

from math import sqrt, pow


def objectDistance(object1, object2):
    """Returns the absolute Euclidean distance between two QObjects object1 and object2"""
    if not object1 or not object2:
        return None

    xDistance = object1.x() - object2.x()
    yDistance = object1.y() - object2.y()
    return sqrt(pow(xDistance, 2) + pow(yDistance, 2))


def movementDelta(source, destination, distance):
    """Returns the vector along which the source would need to move along a target in order to reach it's destination
       with the additional restriction of only moving distance """
    if not source or not destination:
        return (0, 0)

    totalDistance = objectDistance(source, destination)

    # you are on the object, no movement required
    if totalDistance == 0:
        return (0, 0)
    fractionOfTotalDistance = distance / totalDistance
    deltaX = (destination.x() - source.x()) * fractionOfTotalDistance
    deltaY = (destination.y() - source.y()) * fractionOfTotalDistance
    return (deltaX, deltaY)


def closeEnough(object1, object2, epsilon):
    """Determines if two object are closer than epsilon distance apart"""
    if object1 and object2:
        return objectDistance(object1, object2) <= epsilon
    return False


def reverseVector2D(vector):
    """Takes in a 2-tuple and reverses the direction"""
    return (vector[0] * -1, vector[1] * -1)
