#!/usr/bin/python3
# File MainWindow.py
# Driver file for the application

import sys
import logging
import qdarkstyle
from SimulationView import SimulationView
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QFile
from PyQt5.uic import loadUi
from Util import FUNCTION_STRINGS


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
        speedComboBox = self.speed_cost_function_comboBox
        sightComboBox = self.sight_cost_function_comboBox
        sizeComboBox = self.size_cost_function_comboBox

        for func in FUNCTION_STRINGS:
            speedComboBox.addItem(func)
            sightComboBox.addItem(func)
            sizeComboBox.addItem(func)

        # recommended default starting values
        speedComboBox.setCurrentIndex(2)
        sightComboBox.setCurrentIndex(1)
        sizeComboBox.setCurrentIndex(3)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    logging.basicConfig(filename='debug.log', filemode='w', level=logging.INFO)

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = MainWindow()

    # Create a new simulation
    simulationView = SimulationView(window)

    sys.exit(app.exec_())
