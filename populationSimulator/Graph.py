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

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        plt.style.use('dark_background')
        self.figure = Figure(figsize=(width, height), dpi=dpi)

        FigureCanvas.__init__(self, self.figure)

        self.speed_history = [1]
        self.size_history = [1]
        self.sight_history = [1]
        self.ax = None
        self.simulation = None

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        parent.addWidget(self)

    def update_graph(self):
        """Update the graph with any new information about the simulation"""

        if not self.simulation or len(self.simulation.creatures) == 0:
            return

        if self.simulation.enableSizeMutation:
            size = sum([creature.size for creature in self.simulation.creatures]
                       ) / len(self.simulation.creatures)

            self.size_history.append(size)
            self.ax.plot(self.size_history, 'r-', label="size")

        if self.simulation.enableSightMutation:
            sight = sum([creature.sight for creature in self.simulation.creatures]
                        ) / len(self.simulation.creatures)

            self.sight_history.append(sight)
            self.ax.plot(self.sight_history, 'c-', label="sight")

        if self.simulation.enableSpeedMutation:
            speed = sum([creature.speed for creature in self.simulation.creatures]
                        ) / len(self.simulation.creatures)

            self.speed_history.append(speed)
            self.ax.plot(self.speed_history, 'w-', label="speed")

        self.draw()

    def reset_graph(self):
        """Clear the history of the graph and recreate plot"""
        if self.figure:
            self.figure.clear()
        self.speed_history = [1]
        self.size_history = [1]
        self.sight_history = [1]

    def set_simulation(self, simulation):
        """Set the simulation for the instance of this graph"""
        self.simulation = simulation

    def create_axis(self):
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
