#File Food.py 
#Holds a food instance 

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
import random

class Food(QGraphicsPixmapItem):
    nutritionalValue = 1 
    foodImages = ('Cherry.png', 'Watermelon.png', 'Pear.png') #tuple so editing cannot occur 

    def __init__(self, image=None): 
        if not image:
            super().__init__(QPixmap('assets/'+random.choice(self.foodImages)))
        else:
            super().__init__QGraphicsPixmapItem(image)



