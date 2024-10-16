from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsRectItem
from PyQt6.QtGui import QPen, QColor
from PyQt6.QtCore import Qt, QPoint
from math import nan
from galmark.io import GROUP_NAMES

COLORS = [ QColor(0,0,0), QColor(255,0,0),QColor(255,128,0),QColor(255,255,0),
           QColor(0,255,0),QColor(0,255,255),QColor(0,128,128),
           QColor(0,0,255),QColor(128,0,255),QColor(255,0,255) ]

class Mark(QGraphicsEllipseItem):
    def __init__(self,x:int,y:int,image=None,group:int=0):
        self.image = image
        self.r = int((self.image.width+self.image.height)/200)
        self.g = group
        self.c = COLORS[self.g]
        _x, _y = x + 4*self.image.width + 0.5, y + 4*self.image.height + 0.5

        super(Mark, self).__init__(_x-self.r,_y-self.r,2*self.r,2*self.r)

        self.setPen(QPen(self.c, int(self.r/5), Qt.PenStyle.SolidLine))

        self.label = QGraphicsTextItem()
        self.label.setPos(_x,_y)
        self.label.setDefaultTextColor(self.c)
        self.label.setPlainText(GROUP_NAMES[self.g])

    def hide(self):
        super().hide()
        self.label.hide()
    
    def show(self):
        super().show()
        self.label.show()

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

class RectMark(QGraphicsRectItem):
    def __init__(self,label,x_ra_center,y_dec_center,image=None,input_wcs=False):
        self.image = image
        self.side_length = int((self.image.width+self.image.height)/200)
        self.c = QColor(238, 130, 238)

        if not input_wcs:
            x_center, y_center = x_ra_center + 4*self.image.width + 0.5, y_dec_center + 4*self.image.height + 0.5
        else:
            ra_center = x_ra_center
            dec_center = y_dec_center
            x_center, y_center = image.wcs.all_world2pix([[ra_center, dec_center]], 0)[0]
            y_center = self.image.height - y_center
            x_center, y_center = x_center + 4*self.image.width + 0.5, y_center + 4*self.image.height + 0.5

        super(RectMark, self).__init__(x_center-self.side_length/2, y_center-self.side_length/2, 1.5*self.side_length, 1.5*self.side_length)

        self.setPen(QPen(self.c, int(self.side_length/5), Qt.PenStyle.SolidLine))