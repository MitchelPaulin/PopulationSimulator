#File Util.py 
#Contains some helpful functions which don't inherently belong to any class 

from math import sqrt

#returns the absolute Euclidean distance between two QObjects object1 and object2
def objectDistance(object1, object2):
    xDistance = object1.x() - object2.x()
    yDistance = object1.y() - object2.y()
    return sqrt(xDistance**2 + yDistance**2)

#returns the vector along which the source would need to move along a target in order to reach it's destination
#with the additional restriction of only moving distance 
def movementDelta(source, destination, distance):
    totalDistance = objectDistance(source, destination)
    # you are on the object, no movement required 
    if totalDistance == 0:
        return (0,0)
    fractionOfTotalDistance = distance / totalDistance
    deltaX = (destination.x() - source.x()) * fractionOfTotalDistance
    deltaY = (destination.y() - source.y()) * fractionOfTotalDistance
    return (deltaX, deltaY) 