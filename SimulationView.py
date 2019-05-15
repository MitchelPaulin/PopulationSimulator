#File SimulationView.py
#Handles the rendering of a simulation 

from PySide2.QtWidgets import QGraphicsScene, QGraphicsView
from random import randint
import Simulation
from Food import Food 
from Creature import Creature

class SimulationView():

    graphicsScene = None 
    isSimulating = False 
    beginSimulationButton = None 
    food = None 
    creatures = None
    BUFFER = 10 #ensure we don't drop items too close to the extremes of the scene


    def __init__(self, mainWindow):

        self.food = []
        self.creatures = []

        #create new scene 
        simWindow = mainWindow.simulation_window
        self.graphicsScene = QGraphicsScene()
        self.graphicsScene.setSceneRect(simWindow.x(), simWindow.y(), simWindow.width() - 10, simWindow.height() - 10)
        simWindow.setScene(self.graphicsScene)

        #connect buttons to functions 
        self.beginSimulationButton = mainWindow.begin_simulation_button
        self.beginSimulationButton.clicked.connect(self.simulate)
    
    #call the correct function based on the simulation state
    def simulate(self):
        if self.isSimulating:
            self.resume()
        else:
            self.start()
            self.isSimulating = True 

    #draw the food items to the screen and create new food objects 
    def drawFood(self, foodAmount):
        for _ in range(foodAmount):
            food_x = randint(self.BUFFER, self.graphicsScene.width() - self.BUFFER)
            food_y = randint(self.BUFFER, self.graphicsScene.height() - self.BUFFER)
            newFood = Food(food_x,food_y)
            self.food.append(newFood)
            self.graphicsScene.addItem(newFood.pixmap)
            newFood.pixmap.setPos(food_x, food_y)

    #start the simulation 
    def start(self):
        self.drawFood(10) 
    
    #pause the simulation
    def pause(self):
        pass 

    #resume the simulation 
    def resume(self):
        pass 
    
    #simulate to next generation only 
    def nextGeneration(self):
        pass 