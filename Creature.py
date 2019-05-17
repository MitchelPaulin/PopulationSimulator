#File Creature.py
#Holds all the information about an instance of a creature

from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap

class Creature(QGraphicsPixmapItem):
    xPos = None 
    yPos = None 

    def __init__(self, image=None):
        if not image:
            super().__init__(QPixmap('assets/Slime.png'))
        else:
            super().__init__QGraphicsPixmapItem(image)