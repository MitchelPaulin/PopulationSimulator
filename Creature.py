#File Creature.py
#Holds all the information about an instance of a creature

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from Util import objectDistance, movementDelta
from sys import maxsize
import logging 

class Creature(QGraphicsPixmapItem): 
    """
    Holds all the information relevant to a creature 
    Each creature can move, reproduce and mutate 
    """

    speed = 2
    eatenFood = 0

    def __init__(self, image=None):
        if not image:
            super().__init__(QPixmap('assets/Slime.png'))
        else:
            super().__init__QGraphicsPixmapItem(image)

    def moveTowardsFood(self, food):
        """Moves this creature towards a given object"""
        delta = movementDelta(self, food, self.speed)
        self.setPos(self.x() + delta[0], self.y() + delta[1])
 
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

    def eat(self):
        self.eatenFood += 1
        logging.info("I have eaten " + str(self.eatenFood) + " " + str(self))

    def emptyStomach(self):
        self.eatenFood = 0
