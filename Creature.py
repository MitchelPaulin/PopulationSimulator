#File Creature.py
#Holds all the information about an instance of a creature

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from Util import objectDistance, movementDelta
from sys import maxsize
from math import sqrt
from random import uniform
import logging 

class Creature(QGraphicsPixmapItem): 
    """
    Holds all the information relevant to a creature 
    Each creature can move, reproduce and mutate 
    """

    speed = 1
    MIN_SPEED = 0.5

    sight = 10
    MIN_SIGHT = 5
    SIGHT_MODIFER = 20

    size = 1
    MIN_SIZE = 0.5

    eatenFood = 0
    closestFood = None 
    currentEnergy = 3000 # how far a creature can move before it needs to stop
    CREATURE_STARTING_ENERGY = 3000
    MUTATION_RANGE = 0.5 # each attribute has a change to mutate up or down one on mutation 

    def __init__(self, parent=None):
        if parent:
            #Create a new creature based on the parent allowing for natural mutations 
            self.speed = max(uniform(parent.speed - self.MUTATION_RANGE, parent.speed + self.MUTATION_RANGE), self.MIN_SPEED)
            self.sight = max(uniform(parent.sight - self.MUTATION_RANGE, parent.speed + self.MUTATION_RANGE), self.MIN_SIGHT)
            self.size  = max(uniform(parent.size - self.MUTATION_RANGE, parent.size + self.MUTATION_RANGE), self.MIN_SIZE)
            self.size = 1
        super().__init__(QPixmap('assets/Slime.png'))
        logging.info("I have been born! " + str(self) + " from parent " + str(parent))

    def __str__(self):
        base = super().__str__() 
        return base + ("(speed=%f size=%f sight=%f)" % (self.speed, self.size, self.sight))
            
    def moveTowardsObject(self, destObj, simulation):
        """Moves this creature towards a given object"""
        delta = movementDelta(self, destObj, self.speed)
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
        self.currentEnergy -= pow(self.speed, 2)*pow(self.size, 3) + self.sight

    def eat(self):
        self.eatenFood += 1
        logging.info("I have eaten " + str(self.eatenFood) + " " + str(self))

    def resetState(self):
        """Set a creature back to its starting state"""
        self.eatenFood = 0
        self.currentEnergy = self.CREATURE_STARTING_ENERGY
        self.closestFood = None

    def seeingDistance(self):
        """Returns the distance a creature cant spot objects"""
        return self.sight * self.SIGHT_MODIFER
