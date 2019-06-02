# File Food.py

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap
import random


class Food(QGraphicsPixmapItem):
    """
    Food to be drawn to the simulation window 
    """

    # tuple so editing cannot occur
    foodImages = ('Cherry.png', 'Watermelon.png', 'Pear.png')

    def __init__(self, image=None):
        if not image:
            super().__init__(QPixmap('assets/'+random.choice(self.foodImages)))
        else:
            super().__init__QGraphicsPixmapItem(image)
