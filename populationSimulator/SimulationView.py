# File SimulationView.py
# Handles the rendering of a simulation

from PyQt5.QtWidgets import QGraphicsScene, QMessageBox, QGraphicsPixmapItem
from PyQt5.QtCore import QTimer
from random import randint
import logging

from populationSimulator.Creature import Creature
from populationSimulator.Food import Food
from populationSimulator.Graph import Graph
from populationSimulator.Simulation import Simulation
from populationSimulator.Util import object_distance, close_enough


class SimulationLoop:
    """
    A helper class for SimulationView which is responsible for
    rendering the main simulation loop of the actors and managing
    generation timing
    """

    FRAMES_PER_SECOND = 30

    frames = 0

    def __init__(self, simulation_view):
        self.simulationView = simulation_view
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_time_step)
        self.timer.setInterval(1000 / self.FRAMES_PER_SECOND)

    def next_time_step(self):
        self.next_frame()
        self.update_lcds()

    def find_food(self, creature):
        """See if the given creature can find food"""
        if creature.closest_food in self.simulationView.graphicsScene.items():
            return creature.closest_food

        return creature.find_closest_food(
            self.simulationView.simulation.food,
            [x for x in self.simulationView.simulation.creatures if x not in [creature]])

    def remove_item_from_sim(self, item):
        self.simulationView.graphicsScene.removeItem(item)
        if isinstance(item, Food):
            self.simulationView.simulation.food.remove(item)
        else:
            self.simulationView.simulation.creatures.remove(
                item)

    def next_frame(self):
        """Render one time step of the simulation"""
        self.frames += 1
        creature_moved = False
        for creature in self.simulationView.simulation.creatures:

            # creature is out of energy, it cannot move
            if creature.is_out_of_energy():
                continue

            # run away from larger creatures if they are too close
            if self.frames % self.FRAMES_PER_SECOND / 4 == 0:
                creature.hostile = creature.find_hostile(
                    self.simulationView.simulation.creatures)

            hostile = creature.hostile
            if hostile and hostile.isActive():
                creature.move_away_from_object(hostile, self.simulationView)
                creature.hostile = hostile
                creature.closest_food = None
                logging.info(str(creature) +
                             " running away from creature " + str(hostile))
                continue

            # if the creature is full and safe, continue
            if creature.is_full():
                continue

            closest_food = self.find_food(creature)
            creature.closest_food = closest_food

            if closest_food and object_distance(creature, closest_food) < creature.seeing_distance():

                creature.move_towards_object(
                    closest_food, self.simulationView)

                # if creature could reach food in next time step
                if close_enough(creature, closest_food, creature.movement_speed() + self.simulationView.BUFFER):
                    creature.eat()
                    creature.closest_food = None
                    self.remove_item_from_sim(closest_food)
                    logging.info("I have been eaten " + str(closest_food))

                creature_moved = True

            elif not close_enough(creature, self.simulationView.CENTER_OF_SIM, creature.movement_speed()):
                # creature could not see food, move towards center
                creature.move_towards_object(
                    self.simulationView.CENTER_OF_SIM, self.simulationView)
                creature_moved = True

        # no movement occurred, end of generation
        if not creature_moved:
            self.pause()
            self.next_generation()

    def update_lcds(self):
        """Update the LCD displays in the scene"""
        self.simulationView.mainWindow.generation_number_display.display(
            self.simulationView.simulation.generation)
        self.simulationView.mainWindow.creature_number_display.display(
            self.simulationView.simulation.population_size())

    def next_generation(self):
        logging.info("This generation had ended ")
        self.pause()
        self.simulationView.go_to_next_generation()

    def start(self):
        self.timer.start()

    def pause(self):
        self.timer.stop()


class SimulationView:
    """
    Main driver class responsible for handling UI interactions
    and setting up/tearing down and reseting simulations.
    """

    CENTER_OF_SIM = None
    BUFFER = 20  # ensure we don't drop items too close to the extremes of the scene
    FOOD_BUFFER = 25  # don't let food spawn too close to the edges

    def __init__(self, main_window):
        self.mainWindow = main_window

        self.simWindow = main_window.simulation_window

        self.connect_inputs_to_functions(self.mainWindow)

        self.graphView = Graph(self.mainWindow.graph_container)

        self.graphicsScene = None
        self.simulation = None
        self.isSimulating = False
        self.simulationStarted = False
        self.paused = False
        self.simulationLoop = None
        self.beginSimulationButton = None
        self.cancelSimulationButton = None
        self.toggleSimulationButton = None

    def connect_inputs_to_functions(self, main_window):
        """Connect all user inputs to functions"""
        self.beginSimulationButton = main_window.begin_simulation_button
        self.beginSimulationButton.clicked.connect(self.simulate)

        self.cancelSimulationButton = main_window.cancel_simulation_button
        self.cancelSimulationButton.clicked.connect(self.cancel_simulation)

        self.toggleSimulationButton = main_window.toggle_simulation_button
        self.toggleSimulationButton.clicked.connect(self.toggle_simulation)

    def create_graphics_scene(self):
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

    def create_food(self, food_amount):
        """Draw the food items to the screen and create new food objects"""
        for _ in range(food_amount):
            food_x = randint(
                self.FOOD_BUFFER, self.graphicsScene.width() - self.FOOD_BUFFER)
            food_y = randint(
                self.FOOD_BUFFER, self.graphicsScene.height() - self.FOOD_BUFFER)
            new_food = Food()
            self.simulation.add_food(new_food)
            self.graphicsScene.addItem(new_food)
            new_food.setPos(food_x, food_y)

    def random_perimeter_position(self):
        """Retrun an (x,y) position along the perimeter of the scene.
           Helpful when drawing creatures"""
        direction = randint(1, 4)
        if direction == 1:  # North
            return (randint(self.BUFFER, self.graphicsScene.width() - self.BUFFER) - self.BUFFER,
                    self.graphicsScene.height() - self.BUFFER)
        if direction == 2:  # East
            return (self.graphicsScene.width() - self.BUFFER,
                    randint(self.BUFFER, self.graphicsScene.height() - self.BUFFER) - self.BUFFER)
        if direction == 3:  # South
            return randint(self.BUFFER, self.graphicsScene.width() - self.BUFFER) - self.BUFFER, 0
        else:  # West
            return 0, randint(self.BUFFER, self.graphicsScene.height() - self.BUFFER) - self.BUFFER

    def draw_creature(self, creature):
        """Draw an instance of a creature to the screen"""
        new_pos = self.random_perimeter_position()
        self.simulation.add_creature(creature)
        self.graphicsScene.addItem(creature)
        creature.setPos(new_pos[0], new_pos[1])

    def create_creatures(self, creature_amount=10):
        """Draw the creature items to the screen and create new creature objects"""
        for _ in range(creature_amount):
            new_creature = Creature()
            self.draw_creature(new_creature)

    def simulate(self):
        """Call the correct function based on the simulation state"""
        if self.isSimulating or self.paused:
            self.cancel_simulation()
        self.start()
        self.isSimulating = True
        self.simulationStarted = True

    def start(self):
        """Start the simulation"""
        self.create_graphics_scene()
        self.simulation = Simulation(self.mainWindow)
        self.simulationLoop = SimulationLoop(self)
        self.create_food(self.mainWindow.food_slider.sliderPosition())
        self.create_creatures()
        self.graphView.set_simulation(self.simulation)
        self.graphView.create_axis()
        self.simulationLoop.start()

    def toggle_simulation(self):
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

    def delete_assets(self):
        """
        Go through the scene/objects and delete assets.
        Normally you shouldn't have to do this but there seems to be an
        issue with the C++ bindings not causing the de constructor to always
        run, so we need to delete the assets ourself
        """
        if not self.simulation:
            return

        food_list = list(self.simulation.food)
        for food in food_list:
            self.simulation.food.remove(food)

        creature_list = list(self.simulation.creatures)
        for creature in creature_list:
            self.simulation.creatures.remove(creature)

        items_to_remove = list(self.graphicsScene.items())
        for item in items_to_remove:
            self.graphicsScene.removeItem(item)

    def cancel_simulation(self):
        """Clear the simulation scene and reset variables"""
        if self.simulationLoop:
            self.simulationLoop.pause()
        if self.graphView:
            self.graphView.reset_graph()

        self.delete_assets()
        self.isSimulating = False
        self.simulationStarted = False

    def cleanup_food(self):
        """Delete all food from the scene"""
        for food in list(self.simulation.food):
            self.simulation.food.remove(food)
            self.graphicsScene.removeItem(food)

    def reset_creatures(self):
        """Reset creature state as well as deal 
           with creature reproduction / survival"""

        for creature in list(self.simulation.creatures):

            if creature.eaten_food >= 1:  # creature survived to next generation
                new_pos = self.random_perimeter_position()
                creature.setPos(new_pos[0], new_pos[1])
                if creature.is_full():  # create survived with enough food to reproduce
                    offspring = Creature(creature, self.simulation)
                    self.draw_creature(offspring)

            else:  # creature did not find enough food
                logging.info("Creature " + str(creature) + " has perished")
                self.simulation.creatures.remove(creature)
                self.graphicsScene.removeItem(creature)
                continue

            creature.reset_state()

    def go_to_next_generation(self):
        """Set the simulation back to a starting state
           and deal with setting up next generation"""

        if not self.simulation:
            return

        self.cleanup_food()

        self.create_food(self.mainWindow.food_slider.sliderPosition())

        self.reset_creatures()

        self.simulation.generation += 1

        # update the graph with the population attributes
        self.graphView.update_graph()

        if len(self.simulation.creatures) == 0:
            self.cancel_simulation()
            box = QMessageBox(self.mainWindow)
            box.setText("No creatures left")
            box.setWindowTitle("")
            box.open()
        else:
            self.simulationLoop.start()
