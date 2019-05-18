#File Creature.py
#Holds all the information about an instance of a creature

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from Util import objectDistance, movementDelta
from sys import maxsize
from math import sqrt 
import logging 

class Creature(QGraphicsPixmapItem): 
    """
    Holds all the information relevant to a creature 
    Each creature can move, reproduce and mutate 
    """

    speed = 2
    eatenFood = 0
    energy = 1000 # how far a creature can move before it needs to stop
    MUTATION_RANGE = 1 # each attribute has a change to mutate up or down one on mutation 

    def __init__(self, image=None):
        if not image:
            super().__init__(QPixmap('assets/Slime.png'))
        else:
            super().__init__QGraphicsPixmapItem(image)

    def moveTowardsFood(self, food, simulation):
        """Moves this creature towards a given object"""
        delta = movementDelta(self, food, self.speed)
        self.setPos(self.x() + delta[0], self.y() + delta[1])
        self.expendEnergy(delta[0], delta[1], simulation)
 
    def findClosestFood(self, foodList):
        """Finds the closest food to this creature and returns it"""
        if not foodList or len(foodList) == 0:
            return None

        closestFood = None
        closestFoodDistance = maxsize
        for food in foodList: 
            distance = objectDistance(self, food)
            if closestFoodDistance > distance:
                closestFood = food 
                closestFoodDistance = distance

        return closestFood

    def expendEnergy(self, deltaX, deltaY, simulation):
        """Expend the amount of energy equal to the distance moved taking into account attributes"""
        self.energy -= sqrt(pow(deltaX,2) + pow(deltaY,2))

    def eat(self):
        self.eatenFood += 1
        logging.info("I have eaten " + str(self.eatenFood) + " " + str(self))

    def emptyStomach(self):
        self.eatenFood = 0
