#File Creature.py
#Holds all the information about an instance of a creature

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from Util import objectDistance, movementDelta
from sys import maxsize

class Creature(QGraphicsPixmapItem): 

    speed = 1

    def __init__(self, image=None):
        if not image:
            super().__init__(QPixmap('assets/Slime.png'))
        else:
            super().__init__QGraphicsPixmapItem(image)

    #moves this creature towards a given object
    def moveTowardsFood(self, food):
        delta = movementDelta(self, food, self.speed)
        self.setPos(self.x() + delta[0], self.y() + delta[1])

    #find the closest food to this creature and returns it 
    def findClosestFood(self, foodList):
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