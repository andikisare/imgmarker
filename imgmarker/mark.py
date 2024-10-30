from __future__ import annotations
from PyQt6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsProxyWidget,QLineEdit
from PyQt6.QtGui import QPen, QColor,QFocusEvent
from PyQt6.QtCore import Qt, QPointF, QEvent
from math import nan, ceil
from imgmarker.io import GROUP_NAMES
import typing

if typing.TYPE_CHECKING:
    from imgmarker.image import Image
    from PyQt6.QtWidgets import QAbstractGraphicsShapeItem as QAbstractItem

COLORS = [ QColor(255,255,255), QColor(255,0,0),QColor(255,128,0),QColor(255,255,0),
           QColor(0,255,0),QColor(0,255,255),QColor(0,128,128),
           QColor(0,0,255),QColor(128,0,255),QColor(255,0,255) ]

SHAPES = {'ellipse':QGraphicsEllipseItem, 'rect':QGraphicsRectItem}

class AbstractMark:
    @typing.overload
    def __init__(self,r:int,x:int,y:int,image:Image=None) -> None: ...
    @typing.overload
    def __init__(self,r:int,ra:float=None,dec:float=None,image:Image=None) -> None: ...
    def __init__(self,*args,**kwargs):
        self.image:Image = kwargs['image']
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
            self.center = QPointF(_x, self.image.height-_y)
            self.view_center = self.center + 4*QPointF(self.image.width,self.image.height) + QPointF(0.5,0.5)

class MarkLabel(QGraphicsProxyWidget):
    def __init__(self,mark:Mark):
        super().__init__()
        self.mark = mark
        self.lineedit = QLineEdit()
        self.lineedit.setReadOnly(True)
        f = self.lineedit.font()
        f.setPixelSize(int(self.mark.d))
        self.lineedit.setFont(f)

        # Using TabFocus because PyQt does not allow only focusing with left click
        self.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.lineedit.setFocusPolicy(Qt.FocusPolicy.TabFocus)

        self.lineedit.setText(self.mark.text)
        self.lineedit.setStyleSheet(f"""background-color: rgba(0,0,0,0);
                                     border: none; 
                                     color: rgba{self.mark.c.getRgb()}""")
        
        self.lineedit.textChanged.connect(self.autoresize)
        self.setWidget(self.lineedit)
        self.autoresize()
        self.installEventFilter(self)
        self.setPos(self.mark.view_center+QPointF(self.mark.d/2,self.mark.d/2))

    def enter(self):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.clearFocus()
        self.mark.text = self.lineedit.text()
        self.lineedit.setReadOnly(True)

    def focusInEvent(self, event):
        self.setCursor(Qt.CursorShape.IBeamCursor)
        self.lineedit.setReadOnly(False)
        return super().focusInEvent(event)
        
    def keyPressEvent(self, event):
        if (event.key() == Qt.Key.Key_Return): self.enter()
        else: return super().keyPressEvent(event)

    def eventFilter(self, source, event):
        if (event.type() == QEvent.Type.MouseButtonPress) or (event.type() == QEvent.Type.MouseButtonDblClick):
            if event.button() == Qt.MouseButton.LeftButton:
                # With TabFocusReason, tricks PyQt into doing proper focus events
                self.setFocus(Qt.FocusReason.TabFocusReason)
            return True
        return super().eventFilter(source,event)
        
    def autoresize(self):
        fm = self.lineedit.fontMetrics()
        w = fm.boundingRect(self.lineedit.text()).width()+fm.boundingRect('AA').width()
        self.lineedit.setFixedWidth(w)

class Mark(AbstractMark,QGraphicsEllipseItem,QGraphicsRectItem):
    @typing.overload
    def __init__(self,x:int,y:int,
                 shape:str='ellipse',
                 image:Image=None,group:int=0,text:str=None,        
    ) -> None: ...
    @typing.overload
    def __init__(self,ra:float=None,dec:float=None,
                 shape:str='ellipse',
                 image:Image=None,group:int=0,text:str=None,
    ) -> None: ...
    def __init__(self,*args,**kwargs) -> None:
        abstract_kwargs = kwargs.copy()
        keys = kwargs.keys()

        # Set up some default values
        if not 'image' in keys: raise ValueError('No image provided')
        else: image:Image = kwargs['image']

        if not 'group' in keys: self.g = 0
        else: self.g:int = kwargs['group']

        if not 'text' in keys: self.text = GROUP_NAMES[self.g]
        else: self.text:str = kwargs['text']

        if not 'shape' in keys: shape = QGraphicsEllipseItem
        else: shape:str = SHAPES[kwargs['shape']]

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
        shapeitem: QAbstractItem = shape(*item_args)
        shapeitem.setPen(QPen(self.c, int(self.d/10), Qt.PenStyle.SolidLine))
        self.paint = shapeitem.paint
        
        # Set up label
        self.label = MarkLabel(self)