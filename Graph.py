# File Graph.py
# The graph which shows the average creature attributes over time

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QSizePolicy


class Graph(FigureCanvas):
    """
    A matplotlib graph intended to show changes in the population over 
    generations. Works by averaging changes over the simulation instance 
    """

    speedHistory = []
    sizeHistory = []
    sightHistory = []
    ax = None
    figure = None
    simulation = None

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.style.use('dark_background')
        self.figure = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.figure)

        self.speedHistory = [1]
        self.sizeHistory = [1]
        self.sightHistory = [1]

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        parent.addWidget(self)

    def updateGraph(self):
        """Update the graph with any new information about the simulation"""

        if not self.simulation or len(self.simulation.creatures) == 0:
            return

        if self.simulation.enableSizeMutation:
            size = sum([creature.size for creature in self.simulation.creatures]
                       ) / len(self.simulation.creatures)

            self.sizeHistory.append(size)
            self.ax.plot(self.sizeHistory, 'r-', label="size")

        if self.simulation.enableSightMutation:
            sight = sum([creature.sight for creature in self.simulation.creatures]
                        ) / len(self.simulation.creatures)

            self.sightHistory.append(sight)
            self.ax.plot(self.sightHistory, 'c-', label="sight")

        if self.simulation.enableSpeedMutation:
            speed = sum([creature.speed for creature in self.simulation.creatures]
                        ) / len(self.simulation.creatures)

            self.speedHistory.append(speed)
            self.ax.plot(self.speedHistory, 'w-', label="speed")

        self.draw()

    def resetGraph(self):
        """Clear the history of the graph and recreate plot"""
        if self.figure:
            self.figure.clear()
        self.speedHistory = [1]
        self.sizeHistory = [1]
        self.sightHistory = [1]

    def setSimulation(self, simulation):
        """Set the simulation for instance of this graph"""
        self.simulation = simulation

    def createAxis(self):
        """Create the axis for the graph"""
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title('Average creature attributes')

        if not self.simulation:
            return

        if self.simulation.enableSpeedMutation:
            self.ax.plot(1, 'w-', label="speed")
        
        if self.simulation.enableSizeMutation:
            self.ax.plot(1, 'r-', label="size")
        
        if self.simulation.enableSightMutation:
            self.ax.plot(1, 'c-', label="sight")

        self.ax.legend(loc='upper left')

        self.draw()
