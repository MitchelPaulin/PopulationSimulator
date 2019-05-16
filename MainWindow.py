#!/usr/bin/python3
#File MainWindow.py
#Driver file for the application 

import sys
import qdarkstyle
from SimulationView import SimulationView
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QFile
#from PyQt5.QtGui import QMainWindow
from PyQt5.uic import loadUi

class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("assets/mainwindow.ui", self)
        self.show()

#populate and set the initial values for the QComboBoxes
def populateCostComboBox(window):
    functions = ['1', 'n', 'n\u00B2', 'n\u00B3']
    speedComboBox = window.speed_cost_function_comboBox
    sightComboBox = window.sight_cost_function_comboBox 
    sizeComboBox = window.size_cost_function_comboBox 

    for func in functions: 
        speedComboBox.addItem(func)
        sightComboBox.addItem(func)
        sizeComboBox.addItem(func)

    #recommended default starting values 
    speedComboBox.setCurrentIndex(2)
    sightComboBox.setCurrentIndex(1)
    sizeComboBox.setCurrentIndex(3)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside())

    window = MainWindow()

    #Create a new simulation 
    simulationView = SimulationView(window)

    sys.exit(app.exec_())