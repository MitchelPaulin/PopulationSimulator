# File Creature.py
# Holds all the information about an instance of a creature

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from Util import objectDistance, movementDelta, reverseVector2D, closeEnough
from sys import maxsize
from math import sqrt
from random import uniform
import logging


class Creature(QGraphicsPixmapItem):
    """
    Holds all the information relevant to a creature 
    Each creature can move, reproduce and mutate 
    """

    # how far a creature can move before it needs to stop
    CREATURE_STARTING_ENERGY = 5000
    # only run away if a creature is this close
    DANGER_ZONE = 100

    speed = 2
    MIN_SPEED = 0.5

    sight = 1
    MIN_SIGHT = 0.5
    SIGHT_MODIFER = 200

    size = 1
    MIN_SIZE = 0.5
    EAT_SIZE = 1.2  # creature must be 20% larger than another creature to eat it

    eatenFood = 0
    closestFood = None
    currentEnergy = CREATURE_STARTING_ENERGY
    MUTATION_RANGE = 0.5  # each attribute has a change to mutate up or down one on mutation

    def __init__(self, parent=None, simulation=None):
        if parent:
            # Create a new creature based on the parent allowing for natural mutations
            if simulation.enableSpeedMutation:
                self.speed = max(uniform(parent.speed - self.MUTATION_RANGE,
                                         parent.speed + self.MUTATION_RANGE), self.MIN_SPEED)
            if simulation.enableSightMutation:
                self.sight = max(uniform(parent.sight - self.MUTATION_RANGE,
                                         parent.sight + self.MUTATION_RANGE), self.MIN_SIGHT)
            if simulation.enableSizeMutation:
                self.size = max(uniform(parent.size - self.MUTATION_RANGE,
                                        parent.size + self.MUTATION_RANGE), self.MIN_SIZE)
        super().__init__(QPixmap('assets/Slime.png'))
        logging.info("I have been born! " + str(self) +
                     " from parent " + str(parent))

    def __str__(self):
        base = super().__str__()
        return base + ("(speed=%f size=%f sight=%f)" % (self.speed, self.size, self.sight))

    def moveTowardsObject(self, destObj, simulationView):
        """Moves this creature towards a given object"""
        delta = movementDelta(self, destObj, self.speed)
        newX = min(
            max(self.x() + delta[0], 0), simulationView.simWindow.width())
        newY = min(max(self.y() + delta[1], 0),
                   simulationView.simWindow.height())
        self.setPos(newX, newY)
        self.expendEnergy(delta[0], delta[1], simulationView.simulation)

    def moveAwayFromObject(self, otherObject, simulationView):
        """Move this creature awasy from a given object"""
        delta = reverseVector2D(movementDelta(self, otherObject, self.speed))
        newX = min(max(self.x() + delta[0], 0),
                   simulationView.simWindow.width())
        newY = min(max(self.y() + delta[1], 0),
                   simulationView.simWindow.height())
        self.setPos(newX, newY)
        self.expendEnergy(delta[0], delta[1], simulationView.simulation)

    def findClosestFood(self, foodList, creatureList):
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

        for creature in creatureList:
            distance = objectDistance(self, creature)
            if closestFoodDistance > distance and self.size / creature.size >= self.EAT_SIZE:
                closestFood = creature
                closestFoodDistance = distance

        return closestFood

    def findHostile(self, creatureList):
        """Run away from hostile creatures if they exist"""
        for otherCreature in creatureList:
            if self.EAT_SIZE * self.size < otherCreature.size and otherCreature.isActive():
                if closeEnough(self, otherCreature, min(self.seeingDistance(), self.DANGER_ZONE)):
                    return otherCreature
        return None

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

    def isActive(self):
        """returns whether or not this creature is currently active"""
        return self.currentEnergy > 0 and self.eatenFood < 2
