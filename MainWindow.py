#!/usr/bin/python3
#File MainWindow.py
#Driver file for the application 

import sys, logging
import qdarkstyle
from SimulationView import SimulationView
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QFile
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    """
    The Main panel of the application 
    """
    
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("assets/mainwindow.ui", self)
        self.populateCostComboBox()
        self.show()

    
    def populateCostComboBox(self):
        """Populate and set the initial values for the QComboBoxes"""
        functions = ['1', 'n', 'n\u00B2', 'n\u00B3']
        speedComboBox = self.speed_cost_function_comboBox
        sightComboBox = self.sight_cost_function_comboBox 
        sizeComboBox = self.size_cost_function_comboBox 

        for func in functions: 
            speedComboBox.addItem(func)
            sightComboBox.addItem(func)
            sizeComboBox.addItem(func)

        #recommended default starting values 
        speedComboBox.setCurrentIndex(2)
        sightComboBox.setCurrentIndex(1)
        sizeComboBox.setCurrentIndex(3)

    def connectButtons(self, simulation):

        #connect QWidgets to functions 
        simulation.beginSimulationButton = self.begin_simulation_button
        simulation.beginSimulationButton.clicked.connect(simulation.simulate)
        
        simulation.cancelSimulationButton = self.cancel_simulation_button
        simulation.cancelSimulationButton.clicked.connect(simulation.cancelSimulation)

        simulation.toggleSimulationButton = self.toggle_simulation_button
        simulation.toggleSimulationButton.clicked.connect(simulation.toggleSimulation)

        simulation.foodSlider = self.food_slider


if __name__ == "__main__":
    app = QApplication(sys.argv)

    logging.basicConfig(filename='debug.log', filemode='w', level=logging.INFO)

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside())

    window = MainWindow()

    #Create a new simulation 
    simulationView = SimulationView(window)

    window.connectButtons(simulationView)

    sys.exit(app.exec_())