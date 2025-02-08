"""This module contains the `Mark` class and related classes."""

from .pyqt import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsProxyWidget, QLineEdit, QPen, QColor, Qt, QPointF, QEvent
from math import nan, ceil
from astropy.wcs.utils import proj_plane_pixel_scales
from .. import config
from typing import TYPE_CHECKING, overload
import warnings

if TYPE_CHECKING:
    from imgmarker.image import Image
    from .pyqt import QAbstractGraphicsShapeItem as QAbstractItem

COLORS = [ QColor(255,255,255), QColor(255,0,0),QColor(255,128,0),QColor(255,255,0),
           QColor(0,255,0),QColor(0,255,255),QColor(0,128,128),
           QColor(0,0,255),QColor(128,0,255),QColor(255,0,255) ]

SHAPES = {'ellipse':QGraphicsEllipseItem, 'rect':QGraphicsRectItem}

class AbstractMark:
    """Abstract mark containing default mark properties created using Qt framework"""

    @overload
    def __init__(self,r:int,x:int,y:int,image:'Image'=None) -> None: ...
    @overload
    def __init__(self,r:int,ra:float=None,dec:float=None,image:'Image'=None) -> None: ...
    def __init__(self,*args,**kwargs):
        self.image:'Image' = kwargs['image']
        if 'ra' not in kwargs.keys(): 
            self.size, x, y = args
            self.center = QPointF(x,y)
            self.view_center = self.center + QPointF(0.5,0.5)

            if (self.image.wcs != None):
                _x, _y = self.center.x(), self.image.height - self.center.y()
                self.wcs_center = self.image.wcs.all_pix2world([[_x, _y]], 0)[0]
            else: self.wcs_center = (nan, nan)
        else:
            self.size = args[0]
            self.wcs_center = (kwargs['ra'],kwargs['dec'])
            _x, _y = self.image.wcs.all_world2pix([[kwargs['ra'], kwargs['dec']]], 0)[0]
            self.center = QPointF(_x, self.image.height-_y)
            self.view_center = self.center + QPointF(0.5,0.5)

class MarkLabel(QGraphicsProxyWidget):
    """Mark label and its attributes associated with a particular mark"""

    def __init__(self,mark:'Mark'):
        super().__init__()
        self.mark = mark
        self.lineedit = QLineEdit()
        self.lineedit.setReadOnly(True)
        f = self.lineedit.font()
        f.setPixelSize(int(self.mark.size))
        self.lineedit.setFont(f)

        # Using TabFocus because PyQt does not allow only focusing with left click
        self.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.lineedit.setFocusPolicy(Qt.FocusPolicy.TabFocus)

        self.lineedit.setText(self.mark.text)
        self.lineedit.setStyleSheet(f"""background-color: rgba(0,0,0,0);
                                     border: none; 
                                     color: rgba{self.mark.color.getRgb()}""")
        
        self.lineedit.textChanged.connect(self.autoresize)
        self.setWidget(self.lineedit)
        self.autoresize()
        self.installEventFilter(self)
        self.setPos(self.mark.view_center+QPointF(self.mark.size/2,self.mark.size/2))

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
    """Class for creating marks and associating label to mark"""

    @overload
    def __init__(self,x:int,y:int,
                 shape:str='ellipse',
                 image:'Image'=None,group:int=0,text:str=None,picked_color:QColor=None,size_unit:str=None,size:float=None,
    ) -> None: ...
    @overload
    def __init__(self,ra:float=None,dec:float=None,
                 shape:str='ellipse',
                 image:'Image'=None,group:int=0,text:str=None,picked_color:QColor=None,size_unit:str=None,size:float=None,
    ) -> None: ...
    def __init__(self,*args,**kwargs) -> None:
        abstract_kwargs = kwargs.copy()
        keys = kwargs.keys()

        # Set up some default values
        if not 'image' in keys: raise ValueError('No image provided')
        else: image:'Image' = kwargs['image']

        if not 'group' in keys: self.color = kwargs["picked_color"]
        else:
            self.g:int = kwargs['group']
            self.color = COLORS[self.g]

        if not 'text' in keys: self.text = config.GROUP_NAMES[self.g]
        else: self.text:str = kwargs['text']

        if not 'shape' in keys: shape = QGraphicsEllipseItem
        else: shape:str = SHAPES[kwargs['shape']]
        
        if not "size_unit" in keys: pixel_size = ceil((image.width+image.height)/200)*2
        else:
            if kwargs["size_unit"] == None: pixel_size = ceil((image.width+image.height)/200)*2
            else:
                size_unit = kwargs['size_unit']
                size = kwargs['size']
                if size_unit == "arcseconds":
                    pixel_scale = proj_plane_pixel_scales(image.wcs)[0] * 3600
                    pixel_size = size / pixel_scale
                elif size_unit == "pixels":
                    pixel_size = size
                else:
                    warnings.warn("Invalid size unit for catalog marks. Valid units: arcseconds, pixels")
                    return

        # Set up AbstractMark args
        if 'ra' not in kwargs.keys():
            x,y = args
            abstract_args = (pixel_size,x,y) 
        else: abstract_args = (pixel_size,)

        # Set up AbstractMark kwargs
        if 'group' in keys: del abstract_kwargs['group']
        if 'text' in keys: del abstract_kwargs['text']
        if 'shape' in keys: del abstract_kwargs['shape']

        # Initialize AbstractMark
        super().__init__(*abstract_args,**abstract_kwargs)

        # Initialize shape
        item_args = self.view_center.x()-self.size/2, self.view_center.y()-self.size/2, self.size, self.size
        super(shape,self).__init__(*item_args)
        shapeitem:QAbstractItem = shape(*item_args)
        shapeitem.setPen(QPen(self.color, int(self.size/14), Qt.PenStyle.SolidLine))
        self.paint = shapeitem.paint
        
        # Set up label
        self.label = MarkLabel(self)