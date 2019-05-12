#File SimulationView.py
#Handles the rendering of a simulation 

from PySide2.QtWidgets import QGraphicsScene, QGraphicsView

class SimulationView():

    graphicsScene = None 

    def __init__(self, graphicsView):
        #create new scene 
        self.graphicsScene = QGraphicsScene()
        graphicsView.setScene(self.graphicsScene)