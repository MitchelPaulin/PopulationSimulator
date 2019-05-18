#File SimulationView.py
#Handles the rendering of a simulation 

from PyQt5.QtWidgets import QGraphicsScene, QMessageBox
from PyQt5.QtCore import QTimer
from random import randint
import logging
import Simulation
from Food import Food 
from Creature import Creature
from Simulation import Simulation
from Util import closeEnough

class SimulationLoop():
    """
    A helper class for SimulationView which is responsible for 
    rendering the main simulation loop of the actors and managing 
    generation timing 
    """

    simulationView = None 
    timer = None 

    def __init__(self, simulationView):
        self.simulationView = simulationView
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextTimeStep)
        self.timer.setInterval(1000/30)# 60 Frames per second  

    def nextTimeStep(self):
        self.nextFrame()
        self.updateLcds()

    def nextFrame(self):
        """Render one time step"""
        creatureMoved = False 
        for creature in self.simulationView.simulation.creatures:
            if creature.currentEnergy <= 0 or creature.eatenFood >= 2:
                continue 
            closestFood = creature.findClosestFood(self.simulationView.simulation.food)
            if closestFood:
                creature.moveTowardsFood(closestFood, self.simulationView.simulation)
                creatureMoved = True
                if closeEnough(creature, closestFood, creature.speed):
                    creature.eat()
                    logging.info("I have been eaten " + str(closestFood))
                    self.simulationView.graphicsScene.removeItem(closestFood)
                    self.simulationView.simulation.food.remove(closestFood)      
        if not creatureMoved:
            self.pause()
            self.nextGeneration() 

    def updateLcds(self):
        """Update the LCD displays in the scene"""
        self.simulationView.mainWindow.generation_number_display.display(self.simulationView.simulation.generation)
        self.simulationView.mainWindow.creature_number_display.display(self.simulationView.simulation.populationSize())

    def nextGeneration(self): 
        logging.info("This generation had ended ")
        self.pause()
        self.simulationView.goToNextGeneration()
    
    def start(self):
        self.timer.start()
    
    def pause(self):
        self.timer.stop()
        
        
class SimulationView():
    """
    Main driver class responsible for handling UI interactions 
    and setting up,tearing down and reseting simulations.
    """

    mainWindow = None
    graphicsScene = None 
    simWindow = None
    simulation = None
    isSimulating = False  
    simulationStarted = False 
    simulationLoop = None 
    beginSimulationButton = None 
    cancelSimulationButton = None 
    toggleSimulationButton = None 
    BUFFER = 20 #ensure we don't drop items too close to the extremes of the scene 

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        self.simWindow = mainWindow.simulation_window

        self.connectInputsToFunctions(self.mainWindow)

    def connectInputsToFunctions(self, mainWindow):
        """Connect all user inputs to functions"""
        self.beginSimulationButton = mainWindow.begin_simulation_button
        self.beginSimulationButton.clicked.connect(self.simulate)
        
        self.cancelSimulationButton = mainWindow.cancel_simulation_button
        self.cancelSimulationButton.clicked.connect(self.cancelSimulation)

        self.toggleSimulationButton = mainWindow.toggle_simulation_button
        self.toggleSimulationButton.clicked.connect(self.toggleSimulation)
 
    def createGraphicsScene(self): 
        """Create new graphics scene inside the graphics view and set size"""
        self.graphicsScene = QGraphicsScene()
        self.graphicsScene.setSceneRect(self.simWindow.x(), self.simWindow.y(), self.simWindow.width() - self.BUFFER, self.simWindow.height() - self.BUFFER)
        self.simWindow.setScene(self.graphicsScene)
 
    def createFood(self, foodAmount):
        """Draw the food items to the screen and create new food objects"""
        for _ in range(foodAmount):
            food_x = randint(self.BUFFER, self.graphicsScene.width() - self.BUFFER)
            food_y = randint(self.BUFFER, self.graphicsScene.height() - self.BUFFER)
            newFood = Food()
            self.simulation.addFood(newFood)
            self.graphicsScene.addItem(newFood)
            newFood.setPos(food_x, food_y)

    def randomPerimeterPosition(self):
        """Retrun an (x,y) position along the perimeter of the scene.
           Helpful when drawing creatures"""
        direction = randint(1,4)
        if direction == 1: #North
            return (randint(self.BUFFER, self.graphicsScene.width() - self.BUFFER), self.graphicsScene.height() - self.BUFFER)
        if direction == 2: #East
            return (self.graphicsScene.width() - self.BUFFER, randint(self.BUFFER, self.graphicsScene.height() - self.BUFFER))
        if direction == 3: #South
            return(randint(self.BUFFER, self.graphicsScene.width() - self.BUFFER), 0)
        else: #West
            return(0, randint(self.BUFFER, self.graphicsScene.height() - self.BUFFER))

    def drawCreature(self, creature):
        """Draw an instance of a creature to the screen"""
        newPos = self.randomPerimeterPosition()
        self.simulation.addCreature(creature)
        self.graphicsScene.addItem(creature)
        creature.setPos(newPos[0], newPos[1])

    def createCreatures(self, creatureAmount=10):
        """Draw the creature items to the screen and create new creature objects"""
        for _ in range(creatureAmount):
            newCreature = Creature()
            self.drawCreature(newCreature)

    def simulate(self):
        """Call the correct function based on the simulation state"""
        if not self.isSimulating:
            self.start()
            self.isSimulating = True 
            self.simulationStarted = True
 
    def start(self):
        """Start the simulation"""
        self.createGraphicsScene()
        self.simulation = Simulation(self.mainWindow)
        self.simulationLoop = SimulationLoop(self)
        self.createFood(self.mainWindow.food_slider.sliderPosition())
        self.createCreatures()
        self.simulationLoop.start() 
     
    def toggleSimulation(self):
        """Toggle whether or not we are current simulating"""
        if not self.simulationStarted:
            return 

        if self.isSimulating:
            self.simulationLoop.pause()
            self.toggleSimulationButton.setText("Play Simulation")
        else:
            self.simulationLoop.start()
            self.toggleSimulationButton.setText("Pause Simulation")

        self.isSimulating = not self.isSimulating
     
    def deleteAssets(self):
        """
        Go through the scene/objects and delete assets. 
        Normally you shouldn't have to do this but there seems to be an
        issue with the C++ bindings not causing the deconstructor to always
        run so we need to delete the assets outself
        """
        foodList = list(self.simulation.food)
        for food in foodList:
            self.simulation.food.remove(food)

        creatureList = list(self.simulation.creatures)
        for creature in creatureList:
            self.simulation.creatures.remove(creature)

        itemsToRemove = list(self.graphicsScene.items())
        for item in itemsToRemove:
            self.graphicsScene.removeItem(item)

    def cancelSimulation(self):
        """Clear the simulation scene and reset variables"""
        self.simulationLoop.pause()
        self.deleteAssets()
        self.isSimulating = False 
        self.simulationStarted = False 

    def goToNextGeneration(self):
        """Set the simulation back to a starting state
           and deal with setting up next generation"""
        #delete all remaining food 
        foodList = list(self.simulation.food)
        for food in foodList:
            self.simulation.food.remove(food)
            self.graphicsScene.removeItem(food)

        self.createFood(self.mainWindow.food_slider.sliderPosition())
        self.simulation.generation += 1
        creatureList = list(self.simulation.creatures)
        for creature in creatureList:
            if creature.eatenFood >= 1: # creature survived to next generation 
                newPos = self.randomPerimeterPosition()
                creature.setPos(newPos[0], newPos[1])
                if creature.eatenFood >= 2: #create survived with enough food to reproduce  
                    offspring = Creature(creature)
                    self.drawCreature(offspring)
            else: #creature did not find enough food
                logging.info("Create " + str(creature) + " has perished")
                self.simulation.creatures.remove(creature)
                self.graphicsScene.removeItem(creature)
                continue 

            creature.resetState()

        if len(self.simulation.creatures) == 0:
            self.cancelSimulation()
            box = QMessageBox(self.mainWindow)
            box.setText("No creatures left")
            box.open()
        else:
            self.simulationLoop.start()
