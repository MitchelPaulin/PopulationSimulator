#File Food.py 
#Holds a food instance 

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
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
            self.pixmap = QGraphicsPixmapItem(QPixmap('assets/'+random.choice(self.foodImages)))
        else:
            self.pixmap = QGraphicsPixmapItem(image)



