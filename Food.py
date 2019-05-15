#File Food.py 
#Holds a food instance 

from PySide2.QtWidgets import QGraphicsPixmapItem
import random

class Food():
    xPos = None 
    yPos = None 
    nutritionalValue = 1
    pixmap = None 
    foodImages = ['Cherry.png', 'Watermelon.png', 'Pear.png']

    def __init__(self, xPos, yPos, image=None):
        self.xPos = xPos
        self.yPos = yPos 
        if not image:
            self.pixmap = QGraphicsPixmapItem('assets/'+random.choice(self.foodImages))
        else:
            self.pixmap = QGraphicsPixmapItem(image)



