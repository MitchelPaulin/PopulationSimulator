#File SimulationView.py
#Handles the rendering of a simulation 

from PySide2.QtWidgets import QGraphicsScene, QGraphicsView
import Simulation

class SimulationView():

    graphicsScene = None 
    isSimulating = False 
    beginSimulationButton = None 


    def __init__(self, mainWindow):
        #create new scene 
        self.graphicsScene = QGraphicsScene()
        mainWindow.simulation_window.setScene(self.graphicsScene)

        #connect buttons to functions 
        self.beginSimulationButton = mainWindow.begin_simulation_button
        self.beginSimulationButton.clicked.connect(self.simulate)
    
    #call the correct function based on the simulation state
    def simulate(self):

        text = "Begin Simulation" if self.isSimulating else "Pause Simulation"
        self.beginSimulationButton.setText(text)

        if self.isSimulating:
            self.resume()
        else:
            self.start()
        
        self.isSimulating = not self.isSimulating

    def drawFood(self, foodAmount):
        pass  

    def start(self):
        self.drawFood(10) 
    
    def pause(self):
        pass 

    def resume(self):
        pass 
    
    def nextGeneration(self):
        pass 