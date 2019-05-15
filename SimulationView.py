#File SimulationView.py
#Handles the rendering of a simulation 

from PySide2.QtWidgets import QGraphicsScene, QGraphicsView
from random import randint
import Simulation
from Food import Food 
from Creature import Creature
from Simulation import Simulation

class SimulationView():

    graphicsScene = None 
    simWindow = None
    simulation = None
    isSimulating = False 
    beginSimulationButton = None 
    cancelSimulationButton = None 
    foodSlider = None 
    BUFFER = 10 #ensure we don't drop items too close to the extremes of the scene 


    def __init__(self, mainWindow):

        self.simulation = Simulation(mainWindow)

        self.simWindow = mainWindow.simulation_window
        self.createGraphicsScene()

        #connect QWidgets to functions 
        self.beginSimulationButton = mainWindow.begin_simulation_button
        self.beginSimulationButton.clicked.connect(self.simulate)
        
        self.cancelSimulationButton = mainWindow.cancel_simulation_button
        self.cancelSimulationButton.clicked.connect(self.cancelSimulation)

        self.foodSlider = mainWindow.food_slider

    def createGraphicsScene(self):
        #create new scene 
        self.graphicsScene = QGraphicsScene()
        self.graphicsScene.setSceneRect(self.simWindow.x(), self.simWindow.y(), self.simWindow.width() - self.BUFFER, self.simWindow.height() - self.BUFFER)
        self.simWindow.setScene(self.graphicsScene)

    
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
            self.simulation.addFood(newFood)
            self.graphicsScene.addItem(newFood.pixmap)
            newFood.pixmap.setPos(food_x, food_y)

    #start the simulation 
    def start(self):
        self.drawFood(self.foodSlider.sliderPosition()) 
    
    #pause the simulation
    def pause(self):
        pass 

    #resume the simulation 
    def resume(self):
        pass 
    
    #simulate to next generation only 
    def nextGeneration(self):
        pass 

    #clear sim window
    def cancelSimulation(self):
        self.createGraphicsScene()
        self.isSimulating = False 