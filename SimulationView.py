#File SimulationView.py
#Handles the rendering of a simulation 

from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QTimer
from random import randint
import Simulation
from Food import Food 
from Creature import Creature
from Simulation import Simulation

class FrameRenderer():

    simulation = None 
    scene = None 
    timer = None 

    def __init__(self, simulation, scene):
        self.simulation = simulation
        self.scene = scene
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.timer.setInterval(1000/30)# 30 Frames per second  

    #Render one time step 
    def nextFrame(self):
        if self.simulation:
            for food in self.simulation.food:
                food.xPos = food.xPos + randint(-1,1)
                food.yPos = food.yPos + randint(-1,1)
                food.setPos(food.xPos, food.yPos)
    
    def start(self):
        self.timer.start()
    
    def pause(self):
        self.timer.stop()
        
        
class SimulationView():

    mainWindow = None
    graphicsScene = None 
    simWindow = None
    simulation = None
    isSimulating = False  
    simulationStarted = False 
    frameRenderer = None 
    beginSimulationButton = None 
    cancelSimulationButton = None 
    toggleSimulationButton = None 
    foodSlider = None 
    BUFFER = 10 #ensure we don't drop items too close to the extremes of the scene 


    def __init__(self, mainWindow):

        self.mainWindow = mainWindow

        self.simWindow = mainWindow.simulation_window

        self.createGraphicsScene()

        #connect QWidgets to functions 
        self.beginSimulationButton = mainWindow.begin_simulation_button
        self.beginSimulationButton.clicked.connect(self.simulate)
        
        self.cancelSimulationButton = mainWindow.cancel_simulation_button
        self.cancelSimulationButton.clicked.connect(self.cancelSimulation)

        self.toggleSimulationButton = mainWindow.toggle_simulation_button
        self.toggleSimulationButton.clicked.connect(self.toggleSimulation)

        self.foodSlider = mainWindow.food_slider

    def createGraphicsScene(self):
        #create new scene 
        self.graphicsScene = QGraphicsScene()
        self.graphicsScene.setSceneRect(self.simWindow.x(), self.simWindow.y(), self.simWindow.width() - self.BUFFER, self.simWindow.height() - self.BUFFER)
        self.simWindow.setScene(self.graphicsScene)

    #draw the food items to the screen and create new food objects 
    def drawFood(self, foodAmount):
        for _ in range(foodAmount):
            food_x = randint(self.BUFFER, self.graphicsScene.width() - self.BUFFER)
            food_y = randint(self.BUFFER, self.graphicsScene.height() - self.BUFFER)
            newFood = Food(food_x,food_y)
            self.simulation.addFood(newFood)
            self.graphicsScene.addItem(newFood)
            newFood.setPos(food_x, food_y)

    #call the correct function based on the simulation state
    def simulate(self):
        self.start()
        self.isSimulating = True 
        self.simulationStarted = True

    #start the simulation 
    def start(self):
        self.simulation = Simulation(self.mainWindow)
        self.frameRenderer = FrameRenderer(self.simulation, self.graphicsScene)
        self.drawFood(self.foodSlider.sliderPosition())
        self.frameRenderer.start() 
    
    #toggle whether or not we are current simulating 
    def toggleSimulation(self):

        if not self.simulationStarted:
            return 

        if self.isSimulating:
            self.frameRenderer.pause()
        else:
            self.frameRenderer.start()

        self.isSimulating = not self.isSimulating

    #clear sim window
    def cancelSimulation(self):
        for item in self.graphicsScene.items():
            self.graphicsScene.removeItem(item)
        self.isSimulating = False 
        self.simulationStarted = False 