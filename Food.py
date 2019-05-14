#File Food.py 
#Holds a food instance 

from PySide2.QtGui import QPixmap

class Food():
    xPos = None 
    yPos = None 
    nutritionalValue = 1
    pixmap = None 

    def __init__(self, xPos, yPos, image='../assets/food.png'):
        self.xPos = xPos
        self.yPos = yPos 
        self.pixmap = QPixmap(image)



