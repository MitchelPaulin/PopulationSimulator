# File Simulation.py
# Holds all the information about a particular instance of a simulation
from populationSimulator.Util import FUNCTION_STRINGS


class Simulation:
    """
    Holds information about a current instance of a simulation this includes 
    actors and instance variables.
    In theory an entire simulation can be recreated from this instance which 
    makes it useful for data analyzing.
    """

    def __init__(self, main_window):
        self.enableSizeMutation = main_window.enable_size_mutation.isChecked()
        self.enableSightMutation = main_window.enable_sight_mutation.isChecked()
        self.enableSpeedMutation = main_window.enable_speed_mutation.isChecked()
        self.speedCostExponent = FUNCTION_STRINGS.index(
            main_window.speed_cost_function_comboBox.currentText())
        self.sightCostExponent = FUNCTION_STRINGS.index(
            main_window.sight_cost_function_comboBox.currentText())
        self.sizeCostExponent = FUNCTION_STRINGS.index(
            main_window.size_cost_function_comboBox.currentText())

        self.food = []
        self.creatures = []
        self.generation = 0

    def add_food(self, food):
        self.food.append(food)

    def add_creature(self, creature):
        self.creatures.append(creature)

    def population_size(self):
        return len(self.creatures)
