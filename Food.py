#File Food.py 
#Holds a food instance 

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
import random

class Food(QGraphicsPixmapItem):
    xPos = None 
    yPos = None 
    nutritionalValue = 1 
    foodImages = ['Cherry.png', 'Watermelon.png', 'Pear.png']

    def __init__(self, xPos, yPos, image=None):
        self.xPos = xPos
        self.yPos = yPos 
        if not image:
            super().__init__(QPixmap('assets/'+random.choice(self.foodImages)))
        else:
            super().__init__QGraphicsPixmapItem(image)



