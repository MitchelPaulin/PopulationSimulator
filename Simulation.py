#File Simulation.py 
#Holds all the information about a particular instance of a simulation 

import Food, Creature 

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

    def __init__(self, mainWindow):
        pass  

    def addFood(self, food):
        self.food.append(food)
    
    def addCreature(self, creature):
        self.creatures.append(creature)

    def populationSize(self):
        return len(self.creatures)