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
        for creature in self.simulation.creatures:
            closestFood = creature.findClosestFood(self.simulation.food)
            creature.moveTowardsFood(closestFood)
    
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
    BUFFER = 20 #ensure we don't drop items too close to the extremes of the scene 


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

    #create new graphics scene inside the graphics view and set size 
    def createGraphicsScene(self): 
        self.graphicsScene = QGraphicsScene()
        self.graphicsScene.setSceneRect(self.simWindow.x(), self.simWindow.y(), self.simWindow.width() - self.BUFFER, self.simWindow.height() - self.BUFFER)
        self.simWindow.setScene(self.graphicsScene)

    #draw the food items to the screen and create new food objects 
    def createFood(self, foodAmount):
        for _ in range(foodAmount):
            food_x = randint(self.BUFFER, self.graphicsScene.width() - self.BUFFER)
            food_y = randint(self.BUFFER, self.graphicsScene.height() - self.BUFFER)
            newFood = Food()
            self.simulation.addFood(newFood)
            self.graphicsScene.addItem(newFood)
            newFood.setPos(food_x, food_y)

    #retrun an (x,y) position along the perimeter of the scene 
    def randomPerimeterPosition(self):
        direction = randint(1,4)
        if direction == 1: #North
            return (randint(self.BUFFER, self.graphicsScene.width() - self.BUFFER), self.graphicsScene.height() - self.BUFFER)
        if direction == 2: #East
            return (self.graphicsScene.width() - self.BUFFER, randint(self.BUFFER, self.graphicsScene.height() - self.BUFFER))
        if direction == 3: #South
            return(randint(self.BUFFER, self.graphicsScene.width() - self.BUFFER), 0)
        else: #West
            return(0, randint(self.BUFFER, self.graphicsScene.height() - self.BUFFER))

    #draw the creature items to the screen and create new creature objects 
    def createCreatures(self, creatureAmount=10):
        for _ in range(creatureAmount):
            newPos = self.randomPerimeterPosition()
            newCreature = Creature()
            self.simulation.addCreature(newCreature)
            self.graphicsScene.addItem(newCreature)
            newCreature.setPos(newPos[0], newPos[1])

    #call the correct function based on the simulation state
    def simulate(self):
        if not self.isSimulating:
            self.start()
            self.isSimulating = True 
            self.simulationStarted = True

    #start the simulation 
    def start(self):
        self.simulation = Simulation(self.mainWindow)
        self.frameRenderer = FrameRenderer(self.simulation, self.graphicsScene)
        self.createFood(self.foodSlider.sliderPosition())
        self.createCreatures()
        self.frameRenderer.start() 
    
    #toggle whether or not we are current simulating 
    def toggleSimulation(self):

        if not self.simulationStarted:
            return 

        if self.isSimulating:
            self.frameRenderer.pause()
            self.toggleSimulationButton.setText("Play Simulation")
        else:
            self.frameRenderer.start()
            self.toggleSimulationButton.setText("Pause Simulation")

        self.isSimulating = not self.isSimulating

    #clear sim window
    def cancelSimulation(self):
        # if items are not explicitly removed/deleted they will stick around, likely some issues with the PyQt bindings
        # not always calling the destructor properly 
        for item in self.graphicsScene.items():
            self.graphicsScene.removeItem(item)
        for food in self.simulation.food:
            self.simulation.food.remove(food)
            
        self.isSimulating = False 
        self.simulationStarted = False 