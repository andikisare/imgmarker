from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsRectItem, QAbstractGraphicsShapeItem 
from PyQt6.QtGui import QPen, QColor
from PyQt6.QtCore import Qt, QPoint, QPointF
from math import nan, ceil
from galmark.io import GROUP_NAMES
import typing

COLORS = [ QColor(255,255,255), QColor(255,0,0),QColor(255,128,0),QColor(255,255,0),
           QColor(0,255,0),QColor(0,255,255),QColor(0,128,128),
           QColor(0,0,255),QColor(128,0,255),QColor(255,0,255) ]

SHAPES = {'ellipse':QGraphicsEllipseItem, 'rect':QGraphicsRectItem}

class AbstractMark:
    @typing.overload
    def __init__(self,r:int,x:int,y:int,image=None) -> None: ...
    @typing.overload
    def __init__(self,r:int,ra:float=None,dec:float=None,image=None) -> None: ...
    def __init__(self,*args,**kwargs):
        self.image = kwargs['image']
        if 'ra' not in kwargs.keys(): 
            self.d, x, y = args
            self.center = QPointF(x,y)
            self.view_center = self.center + 4*QPointF(self.image.width,self.image.height) + QPointF(0.5,0.5)

            if (self.image.wcs != None):
                _x, _y = self.center.x(), self.image.height - self.center.y()
                self.wcs_center = self.image.wcs.all_pix2world([[_x, _y]], 0)[0]
            else: self.wcs_center = (nan, nan)
            
        else:
            self.d = args[0]
            self.wcs_center = (kwargs['ra'],kwargs['dec'])
            _x, _y = self.image.wcs.all_world2pix([[kwargs['ra'], kwargs['dec']]], 0)[0]
            self.center = QPointF(int(_x), self.image.height-int(_y))
            self.view_center = self.center + 4*QPointF(self.image.width,self.image.height) + QPointF(0.5,0.5)

class Mark(AbstractMark,QGraphicsEllipseItem,QGraphicsRectItem):
    @typing.overload
    def __init__(self,x:int,y:int,
                 shape:str='ellipse',
                 image=None,group:int=0,text:str=None,
                 
    ) -> None: ...
    @typing.overload
    def __init__(self,ra:float=None,dec:float=None,
                 shape:str='ellipse',
                 image=None,group:int=0,text:str=None,
    ) -> None: ...
    def __init__(self,*args,**kwargs) -> None:
        abstract_kwargs = kwargs.copy()
        keys = kwargs.keys()

        # Set up some default values
        if not 'image' in keys: raise ValueError('No image provided')
        else: image = kwargs['image']

        if not 'group' in keys: self.g = 0
        else: self.g = kwargs['group']

        if not 'text' in keys: self.text = GROUP_NAMES[self.g]
        else: self.text = kwargs['text']

        if not 'shape' in keys: shape = QGraphicsEllipseItem
        else: shape = SHAPES[kwargs['shape']]

        self.c = COLORS[self.g]
        d = ceil((image.width+image.height)/200)*2

        # Set up AbstractMark args
        if 'ra' not in kwargs.keys():
            x,y = args
            abstract_args = (d,x,y) 
        else: abstract_args = (d,)

        # Set up AbstractMark kwargs
        if 'group' in keys: del abstract_kwargs['group']
        if 'text' in keys: del abstract_kwargs['text']
        if 'shape' in keys: del abstract_kwargs['shape']

        # Initialize AbstractMark
        super().__init__(*abstract_args,**abstract_kwargs)

        # Initialize shape
        item_args = self.view_center.x()-self.d/2, self.view_center.y()-self.d/2, self.d, self.d
        super(shape,self).__init__(*item_args)
        shapeitem = shape(*item_args)
        shapeitem.setPen(QPen(self.c, int(self.d/10), Qt.PenStyle.SolidLine))
        self.paint = shapeitem.paint
        
        # Set up label
        self.label = QGraphicsTextItem()
        self.label.setPos(self.view_center)
        self.label.setDefaultTextColor(self.c)
        self.label.setPlainText(self.text)