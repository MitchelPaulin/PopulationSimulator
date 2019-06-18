# File Simulation.py
# Holds all the information about a particular instance of a simulation

import Food
import Creature
from Util import FUNCTION_STRINGS


class Simulation:
    """
    Holds information about a current instance of a simulation this includes 
    actors and instance variables.
    In theory an entire simulation can be recreated from this instance which 
    makes it useful for data analyzation.
    """

    food = []
    creatures = []
    generation = 0
    enableSizeMutation = False
    enableSightMutation = False
    enableSpeedMutation = False
    speedCostExponent = 0
    sightCostExponenet = 0
    sizeCostExponenet = 0

    def __init__(self, mainWindow):
        self.enableSizeMutation = mainWindow.enable_size_mutation.isChecked()
        self.enableSightMutation = mainWindow.enable_sight_mutation.isChecked()
        self.enableSpeedMutation = mainWindow.enable_speed_mutation.isChecked()
        self.speedCostExponent = FUNCTION_STRINGS.index(mainWindow.speed_cost_function_comboBox.currentText())
        self.sightCostExponenet = FUNCTION_STRINGS.index(mainWindow.sight_cost_function_comboBox.currentText())
        self.sizeCostExponenet = FUNCTION_STRINGS.index(mainWindow.size_cost_function_comboBox.currentText())

    def addFood(self, food):
        self.food.append(food)

    def addCreature(self, creature):
        self.creatures.append(creature)

    def populationSize(self):
        return len(self.creatures)
