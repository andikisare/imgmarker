from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QPen, QColor
from PyQt6.QtCore import Qt, QPoint
from astropy.wcs import WCS
from math import nan

COLORS = [ QColor(0,0,0), QColor(255,0,0),QColor(255,128,0),QColor(255,255,0),
           QColor(0,255,0),QColor(0,255,255),QColor(0,128,128),
           QColor(0,0,255),QColor(128,0,255),QColor(255,0,255) ]

class Mark(QGraphicsEllipseItem):
    def __init__(self,x:int,y:int,r:int=5,image=None,group:int=0):
        self.r = r
        self.image = image
        self.g = group
        self.c = COLORS[self.g]
        _x, _y = x + 4*self.image.width, y + 4*self.image.width

        super(Mark, self).__init__(_x-r,_y-r,2*r,2*r)

        self.setPen(QPen(self.c, 1, Qt.PenStyle.SolidLine))
        
    def center(self) -> QPoint:
        return QPoint(self.x()+self.r,self.y()+self.r)
    
    def x(self) -> int:
        return int(self.rect().x())
    
    def y(self) -> int:
        return int(self.rect().y())
    
    def img_center(self) -> QPoint:
        w, h = self.image.width, self.image.height
        return self.center() - 4*QPoint(w,h)
    
    def wcs_center(self) -> list:
        if self.image.wcs != None:
            _x, _y = self.img_center().x(), self.image.height - self.img_center().y()
            return self.image.wcs.all_pix2world([[_x, _y]], 0)[0]
        else: return nan, nan
    
    def setCenter(self,x:int,y:int) -> None:
        self.setRect(x-self.r,y-self.r,2*self.r,2*self.r)
        self.setPos(x-self.r,y-self.r)