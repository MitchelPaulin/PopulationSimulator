#!/usr/bin/python3
# File MainWindow.py
# Driver file for the application

import sys
import logging
import qdarkstyle
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi

from populationSimulator.SimulationView import SimulationView
from populationSimulator.Util import FUNCTION_STRINGS


class MainWindow(QMainWindow):
    """
    The Main panel of the application 
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("../assets/mainwindow.ui", self)
        self.populate_cost_combo_box()
        self.show()

    def populate_cost_combo_box(self):
        """Populate and set the initial values for the QComboBoxes"""
        speed_combo_box = self.speed_cost_function_comboBox
        sight_combo_box = self.sight_cost_function_comboBox
        size_combo_box = self.size_cost_function_comboBox

        for func in FUNCTION_STRINGS:
            speed_combo_box.addItem(func)
            sight_combo_box.addItem(func)
            size_combo_box.addItem(func)

        # recommended default starting values
        speed_combo_box.setCurrentIndex(2)
        sight_combo_box.setCurrentIndex(1)
        size_combo_box.setCurrentIndex(3)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    logging.basicConfig(filename='debug.log', filemode='w', level=logging.INFO)

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = MainWindow()

    # create a new simulation
    simulationView = SimulationView(window)

    sys.exit(app.exec_())
