#File MainWindow.py
#Driver file for the application 

import sys
import qdarkstyle
from SimulationView import SimulationView
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile, QObject

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


def InitUI():

    #load ui file 
    ui_file = QFile("assets/mainwindow.ui")
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()

    #initialize values for drop downs
    populateCostComboBox(window)

    window.setFixedSize(window.size())
    window.show()
    return window 


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyside())

    window = InitUI()

    #Create a new simulation 
    simulationView = SimulationView(window)


    sys.exit(app.exec_())