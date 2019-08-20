# File SimulationView.py
# Handles the rendering of a simulation

from PyQt5.QtWidgets import QGraphicsScene, QMessageBox, QGraphicsPixmapItem
from PyQt5.QtCore import QTimer
from random import randint
import logging
import Simulation
from Food import Food
from Creature import Creature
from Simulation import Simulation
from Graph import Graph
from Util import closeEnough, objectDistance, reverseVector2D


class SimulationLoop():
    """
    A helper class for SimulationView which is responsible for
    rendering the main simulation loop of the actors and managing
    generation timing
    """

    FRAMES_PER_SECOND = 30

    simulationView = None
    timer = None
    frames = 0

    def __init__(self, simulationView):
        self.simulationView = simulationView
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextTimeStep)
        self.timer.setInterval(1000/self.FRAMES_PER_SECOND)

    def nextTimeStep(self):
        self.nextFrame()
        self.updateLcds()

    def findFood(self, creature):
        """See if the given creature can find food"""
        if creature.closestFood in self.simulationView.graphicsScene.items():
            return creature.closestFood

        return creature.findClosestFood(
            self.simulationView.simulation.food, [x for x in self.simulationView.simulation.creatures if x not in [creature]])

    def removeItemFromSim(self, item):
        self.simulationView.graphicsScene.removeItem(item)
        if isinstance(item, Food):
            self.simulationView.simulation.food.remove(item)
        else:
            self.simulationView.simulation.creatures.remove(
                item)

    def nextFrame(self):
        """Render one time step of the simulation"""
        self.frames += 1
        creatureMoved = False
        for creature in self.simulationView.simulation.creatures:

            closestFood = None

            # creature is out of energy, it cannot move
            if creature.isOutOfEnergy():
                continue

            # run away from larger creatures if they are too close
            if self.frames % self.FRAMES_PER_SECOND / 4 == 0:
                creature.hostile = creature.findHostile(
                    self.simulationView.simulation.creatures)

            hostile = creature.hostile
            if hostile and hostile.isActive():
                creature.moveAwayFromObject(hostile, self.simulationView)
                creature.hostile = hostile
                creature.closestFood = None
                logging.info(str(creature) + " running away from creature " + str(hostile))
                continue

            # if the creature is full and safe, continue
            if creature.isFull():
                continue

            closestFood = self.findFood(creature)
            creature.closestFood = closestFood

            if closestFood and objectDistance(creature, closestFood) < creature.seeingDistance():

                creature.moveTowardsObject(
                    closestFood, self.simulationView)

                # if creature could reach food in next time step
                if closeEnough(creature, closestFood, creature.movementSpeed() + self.simulationView.BUFFER):
                    creature.eat()
                    creature.closestFood = None
                    self.removeItemFromSim(closestFood)
                    logging.info("I have been eaten " + str(closestFood))

                creatureMoved = True

            elif not closeEnough(creature, self.simulationView.CENTER_OF_SIM, creature.movementSpeed()):
                # creature could not see food, move towards center
                creature.moveTowardsObject(
                    self.simulationView.CENTER_OF_SIM, self.simulationView)
                creatureMoved = True

        # no movement occurred, end of generation
        if not creatureMoved:
            self.pause()
            self.nextGeneration()

    def updateLcds(self):
        """Update the LCD displays in the scene"""
        self.simulationView.mainWindow.generation_number_display.display(
            self.simulationView.simulation.generation)
        self.simulationView.mainWindow.creature_number_display.display(
            self.simulationView.simulation.populationSize())

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
    and setting up/tearing down and reseting simulations.
    """

    CENTER_OF_SIM = None
    BUFFER = 20  # ensure we don't drop items too close to the extremes of the scene
    FOOD_BUFFER = 25  # don't let food spawn too close to the edges

    mainWindow = None
    graphicsScene = None
    simWindow = None
    simulation = None
    graphView = None
    isSimulating = False
    simulationStarted = False
    paused = False
    simulationLoop = None
    beginSimulationButton = None
    cancelSimulationButton = None
    toggleSimulationButton = None

    def __init__(self, mainWindow):
        self.mainWindow = mainWindow

        self.simWindow = mainWindow.simulation_window

        self.connectInputsToFunctions(self.mainWindow)

        self.graphView = Graph(self.mainWindow.graph_container)

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
        self.graphicsScene.setSceneRect(self.simWindow.x(), self.simWindow.y(
        ), self.simWindow.width() - self.BUFFER, self.simWindow.height() - self.BUFFER)
        self.simWindow.setScene(self.graphicsScene)

        # add an object to the center of the screen for path finding purposes
        self.CENTER_OF_SIM = QGraphicsPixmapItem()
        self.CENTER_OF_SIM.setPos(
            self.simWindow.width() / 2, self.simWindow.height() / 2)
        self.graphicsScene.addItem(self.CENTER_OF_SIM)

    def createFood(self, foodAmount):
        """Draw the food items to the screen and create new food objects"""
        for _ in range(foodAmount):
            food_x = randint(
                self.FOOD_BUFFER, self.graphicsScene.width() - self.FOOD_BUFFER)
            food_y = randint(
                self.FOOD_BUFFER, self.graphicsScene.height() - self.FOOD_BUFFER)
            newFood = Food()
            self.simulation.addFood(newFood)
            self.graphicsScene.addItem(newFood)
            newFood.setPos(food_x, food_y)

    def randomPerimeterPosition(self):
        """Retrun an (x,y) position along the perimeter of the scene.
           Helpful when drawing creatures"""
        direction = randint(1, 4)
        if direction == 1:  # North
            return (randint(self.BUFFER, self.graphicsScene.width() - self.BUFFER) - self.BUFFER, self.graphicsScene.height() - self.BUFFER)
        if direction == 2:  # East
            return (self.graphicsScene.width() - self.BUFFER, randint(self.BUFFER, self.graphicsScene.height() - self.BUFFER) - self.BUFFER)
        if direction == 3:  # South
            return(randint(self.BUFFER, self.graphicsScene.width() - self.BUFFER) - self.BUFFER, 0)
        else:  # West
            return(0, randint(self.BUFFER, self.graphicsScene.height() - self.BUFFER) - self.BUFFER)

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
        if self.isSimulating or self.paused:
            self.cancelSimulation()
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
        self.graphView.setSimulation(self.simulation)
        self.graphView.createAxis()
        self.simulationLoop.start()

    def toggleSimulation(self):
        """Toggle whether or not we are currently simulating"""
        if not self.simulationStarted:
            return

        if self.isSimulating:
            self.simulationLoop.pause()
            self.toggleSimulationButton.setText("Play Simulation")
            self.paused = True
        else:
            self.simulationLoop.start()
            self.toggleSimulationButton.setText("Pause Simulation")
            self.paused = False

        self.isSimulating = not self.isSimulating

    def deleteAssets(self):
        """
        Go through the scene/objects and delete assets.
        Normally you shouldn't have to do this but there seems to be an
        issue with the C++ bindings not causing the deconstructer to always
        run, so we need to delete the assets ourself
        """
        if not self.simulation:
            return

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
        if self.simulationLoop:
            self.simulationLoop.pause()
        if self.graphView:
            self.graphView.resetGraph()

        self.deleteAssets()
        self.isSimulating = False
        self.simulationStarted = False

    def cleanupFood(self):
        """Delete all food from the scene"""
        for food in list(self.simulation.food):
            self.simulation.food.remove(food)
            self.graphicsScene.removeItem(food)

    def resetCreatures(self):
        """Reset creature state as well as deal 
           with creature reproduction / survival"""

        for creature in list(self.simulation.creatures):

            if creature.eatenFood >= 1:  # creature survived to next generation
                newPos = self.randomPerimeterPosition()
                creature.setPos(newPos[0], newPos[1])
                if creature.isFull():  # create survived with enough food to reproduce
                    offspring = Creature(creature, self.simulation)
                    self.drawCreature(offspring)

            else:  # creature did not find enough food
                logging.info("Creature " + str(creature) + " has perished")
                self.simulation.creatures.remove(creature)
                self.graphicsScene.removeItem(creature)
                continue

            creature.resetState()

    def goToNextGeneration(self):
        """Set the simulation back to a starting state
           and deal with setting up next generation"""

        if not self.simulation:
            return

        self.cleanupFood()

        self.createFood(self.mainWindow.food_slider.sliderPosition())

        self.resetCreatures()

        self.simulation.generation += 1

        # update the graph with the population attributes
        self.graphView.updateGraph()

        if len(self.simulation.creatures) == 0:
            self.cancelSimulation()
            box = QMessageBox(self.mainWindow)
            box.setText("No creatures left")
            box.setWindowTitle("")
            box.open()
        else:
            self.simulationLoop.start()
