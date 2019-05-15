#File Simulation.py 
#Holds all the information about a particular instance of a simulation 

import Food, Creature 

class Simulation:

    food = []
    creatures = []

    def __init__(self, mainWindow):
        pass  

    def addFood(self, food):
        self.food.append(food)