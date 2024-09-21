from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt, QPoint
from utils import COLORS
from astropy.wcs import WCS

class Region(QGraphicsEllipseItem):
    def __init__(self,parent,x:int,y:int,r:int=5,wcs:WCS=None,group:int=0):
        super(Region, self).__init__(x-r,y-r,2*r,2*r)

        self.r = r
        self.wcs = wcs
        self.g = group
        self.c = COLORS[self.g]
        self.parent = parent
        
    def center(self):
        return QPoint(self.x()+self.r,self.y()+self.r)
    
    def x(self):
        return int(self.rect().x())
    
    def y(self):
        return int(self.rect().y())
    
    def centerWCS(self):
        if self.wcs != None:
            _x, _y = self.center().x(), self.wcs._naxis[0] - self.center().y()
            return self.wcs.all_pix2world([[_x, _y]], 0)[0]
        else: raise NameError('No WCS solution provided')

    def draw(self):
        self.setPen(QPen(self.c, 1, Qt.PenStyle.SolidLine))
        self.parent.image_scene.addItem(self)
    
    def setCenter(self,x:int,y:int):
        self.setPos(x-self.r,y-self.r)

    def setWCS(self,wcs:WCS):
        self.wcs = wcs

    def remove(self):
        self.parent.image_scene.removeItem(self)
        self.parent.data[self.parent.image_name][self.g]['Regions'].remove(self)