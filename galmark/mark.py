from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QPen, QColor
from PyQt6.QtCore import Qt, QPoint
from astropy.wcs import WCS

COLORS = [ QColor(0,0,0), QColor(255,0,0),QColor(255,128,0),QColor(255,255,0),
           QColor(0,255,0),QColor(0,255,255),QColor(0,128,128),
           QColor(0,0,255),QColor(128,0,255),QColor(255,0,255) ]

class Mark(QGraphicsEllipseItem):
    def __init__(self,x:int,y:int,r:int=5,wcs:WCS=None,group:int=0):
        super(Mark, self).__init__(x-r,y-r,2*r,2*r)

        self.r = r
        self.wcs = wcs
        self.g = group
        self.c = COLORS[self.g]
        
    def center(self) -> QPoint:
        return QPoint(self.x()+self.r,self.y()+self.r)
    
    def x(self) -> int:
        return int(self.rect().x())
    
    def y(self) -> int:
        return int(self.rect().y())
    
    def img_center(self) -> QPoint:
        w, h = self.wcs._naxis[1], self.wcs._naxis[0]
        return self.center() - 4*QPoint(w,h)
    
    def wcs_center(self) -> list:
        if self.wcs != None:
            _x, _y = self.img_center().x(), self.wcs._naxis[0] - self.img_center().y()
            return self.wcs.all_pix2world([[_x, _y]], 0)[0]
        else: raise NameError('No WCS solution provided')

    def draw(self,scene) -> None:
        self.setPen(QPen(self.c, 1, Qt.PenStyle.SolidLine))
        scene.addItem(self)
    
    def setCenter(self,x:int,y:int) -> None:
        self.setRect(x-self.r,y-self.r,2*self.r,2*self.r)
        self.setPos(x-self.r,y-self.r)

    def setWCS(self,wcs:WCS) -> None:
        self.wcs = wcs