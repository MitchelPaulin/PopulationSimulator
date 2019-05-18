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
    eatenFood = 0
    currentEnergy = 2500 # how far a creature can move before it needs to stop
    CREATURE_STARTING_ENERGY = 2500
    MUTATION_RANGE = 1 # each attribute has a change to mutate up or down one on mutation 

    def __init__(self, parent=None):
        if parent:
            #Mutate the creature 
            self.speed += uniform(parent.speed - self.MUTATION_RANGE, parent.speed + self.MUTATION_RANGE)
        super().__init__(QPixmap('assets/Slime.png'))
            

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
        self.currentEnergy -= sqrt(pow(deltaX,2) + pow(deltaY,2)) + self.speed * self.speed

    def eat(self):
        self.eatenFood += 1
        logging.info("I have eaten " + str(self.eatenFood) + " " + str(self))

    def resetState(self):
        """Set a creature back to its starting state"""
        self.eatenFood = 0
        self.currentEnergy = self.CREATURE_STARTING_ENERGY

