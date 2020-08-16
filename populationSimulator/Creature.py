# File Creature.py
# Holds all the information about an instance of a creature

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
from populationSimulator.Util import object_distance, movement_delta, reverse_vector_2d, close_enough
from sys import maxsize
from random import uniform
import logging


class Creature(QGraphicsPixmapItem):
    """
    Holds all the information relevant to a creature 
    Each creature can move, reproduce and mutate 
    """

    # how far a creature can move before it needs to stop
    CREATURE_STARTING_ENERGY = 1500
    # only run away if a creature is this close
    DANGER_ZONE = 150
    # the amount of food a creature needs to eat in order to reproduce
    FULL = 2
    # each attribute has a change to mutate up or down by the mutation value
    MUTATION_RANGE = 0.5

    MIN_SPEED = 0.5
    SPEED_MODIFIER = 2

    MIN_SIGHT = 0.5
    SIGHT_MODIFIER = 200

    MIN_SIZE = 0.5
    EAT_SIZE = 1.2  # creature must be 20% larger than another creature to eat it

    def __init__(self, parent=None, simulation=None):
        self.size = 1
        self.sight = 1
        self.speed = 1
        self.eaten_food = 0
        self.closest_food = None
        self.hostile = None
        self.current_energy = Creature.CREATURE_STARTING_ENERGY
        if parent:
            # create a new creature based on the parent, allowing for natural mutations
            if simulation.enableSpeedMutation:
                self.speed = max(uniform(parent.speed - self.MUTATION_RANGE,
                                         parent.speed + self.MUTATION_RANGE), self.MIN_SPEED)
            if simulation.enableSightMutation:
                self.sight = max(uniform(parent.sight - self.MUTATION_RANGE,
                                         parent.sight + self.MUTATION_RANGE), self.MIN_SIGHT)
            if simulation.enableSizeMutation:
                self.size = max(uniform(parent.size - self.MUTATION_RANGE,
                                        parent.size + self.MUTATION_RANGE), self.MIN_SIZE)
        super().__init__(QPixmap('../assets/Slime.png'))
        logging.info("I have been born! " + str(self) +
                     " from parent " + str(parent))

    def __str__(self):
        base = super().__str__()
        return base + ("(speed=%f size=%f sight=%f energy=%f food=%d)" % (
            self.speed, self.size, self.sight, self.current_energy, self.eaten_food))

    def move_towards_object(self, dest_obj, simulation_view):
        """Moves this creature towards a given object"""
        delta = movement_delta(self, dest_obj, self.movement_speed())
        new_x = min(
            max(self.x() + delta[0], 0), simulation_view.simWindow.width())
        new_y = min(max(self.y() + delta[1], 0),
                    simulation_view.simWindow.height())
        self.setPos(new_x, new_y)
        self.expend_energy(simulation_view.simulation)

    def move_away_from_object(self, other_object, simulation_view):
        """Move this creature away from a given object"""
        delta = reverse_vector_2d(movement_delta(
            self, other_object, self.movement_speed()))
        new_x = min(max(self.x() + delta[0], 0),
                    simulation_view.simWindow.width())
        new_y = min(max(self.y() + delta[1], 0),
                    simulation_view.simWindow.height())
        self.setPos(new_x, new_y)
        self.expend_energy(simulation_view.simulation)

    def find_closest_food(self, food_list, creature_list):
        """Finds the closest food to this creature and returns it"""
        if not food_list or len(food_list) == 0:
            return None

        closest_food_distance = maxsize
        closest_food = None
        for food in food_list:
            distance = object_distance(self, food)
            if closest_food_distance > distance:
                closest_food = food
                closest_food_distance = distance

        for creature in creature_list:
            distance = object_distance(self, creature)
            if closest_food_distance > distance and self.size / creature.size >= self.EAT_SIZE:
                closest_food = creature
                closest_food_distance = distance

        return closest_food

    def find_hostile(self, creature_list):
        """Run away from hostile creatures if they exist"""
        for otherCreature in creature_list:
            if otherCreature.size / self.size >= self.EAT_SIZE:
                if close_enough(self, otherCreature, min(self.seeing_distance(), self.DANGER_ZONE)):
                    return otherCreature
        return None

    def expend_energy(self, simulation):
        """Expend the amount of energy equal to the distance moved taking into account attributes"""
        speed_cost = pow(self.speed, simulation.speedCostExponent)
        size_cost = pow(self.size, simulation.sizeCostExponent)
        sight_cost = pow(self.sight, simulation.sightCostExponent)
        self.current_energy -= speed_cost * size_cost + sight_cost

    def eat(self):
        self.eaten_food += 1
        logging.info("I have eaten " + str(self.eaten_food) + " " + str(self))

    def reset_state(self):
        """Set a creature back to its starting state"""
        self.eaten_food = 0
        self.current_energy = self.CREATURE_STARTING_ENERGY
        self.closest_food = None

    def seeing_distance(self):
        """Returns the distance at which an object leaves a creatures view"""
        return self.sight * self.SIGHT_MODIFIER

    def movement_speed(self):
        """Returns the distance a creature can move"""
        return self.speed * self.SPEED_MODIFIER

    def isActive(self):
        """Returns whether or not this creature is currently active"""
        return not self.is_out_of_energy() and not self.is_full()

    def is_out_of_energy(self):
        return self.current_energy <= 0

    def is_full(self):
        return self.eaten_food >= self.FULL
