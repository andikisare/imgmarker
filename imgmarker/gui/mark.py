"""This module contains the `Mark` class and related classes."""

from .pyqt import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsProxyWidget, QLineEdit, QPen, QColor, Qt, QPointF, QEvent
from .pyqt import QAbstractGraphicsShapeItem as QAbstractItem
from .. import config
import os
from math import nan, ceil
from astropy.wcs.utils import proj_plane_pixel_scales
from .. import config
from typing import TYPE_CHECKING, overload, Literal
import warnings

if TYPE_CHECKING:
    from imgmarker.image import Image 

COLORS = [ QColor(255,255,255), QColor(255,0,0),QColor(255,128,0),QColor(255,255,0),
           QColor(0,255,0),QColor(0,255,255),QColor(0,128,128),
           QColor(0,0,255),QColor(128,0,255),QColor(255,0,255) ]

SHAPES:dict[str,type[QAbstractItem]] = {'ellipse':QGraphicsEllipseItem, 'rect':QGraphicsRectItem}

'''class AbstractMark:
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
            self.view_center = self.center + QPointF(0.5,0.5)'''

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

class Mark:
    """Class for creating marks and associating label to mark"""

    @overload
    def __init__(self,x:int,y:int,
                 shape:str='ellipse',
                 image:'Image'=None,group:int=0,text:str=None,color:QColor=None,size_unit:str=None,size:float=None,
    ) -> None: ...
    @overload
    def __init__(self,ra:float=None,dec:float=None,
                 shape:str='ellipse',
                 image:'Image'=None,group:int=0,text:str=None,color:QColor=None,size_unit:str=None,size:float=None,
    ) -> None: ...
    def __init__(self,*args,**kwargs) -> None:
        
        # Set up image
        self.image = None
        if 'image' in kwargs: 
            self.image:'Image' = kwargs['image']

        try: w, h = self.image.width, self.image.height
        except: w, h = 512, 512  

        # Set up some default values
        self.g = 0
        self.color = COLORS[0]
        self.shape = SHAPES['ellipse']
        self.size = ceil((w+h)/200)*2
        size_unit = 'pixels'
        self.path = os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')

        if 'group' in kwargs:
            self.g:int = kwargs['group']
            self.color = COLORS[self.g]

        if 'picked_color' in kwargs:
            self.color = kwargs["picked_color"]

        if 'text' in kwargs:
            self.text:str = kwargs['text']
        else:
            self.text = config.GROUP_NAMES[self.g]

        if 'shape' in kwargs:
            self.shape = SHAPES[kwargs['shape']]
        
        if "size" in kwargs:
            if 'size_unit' in kwargs:
                size_unit = kwargs['size_unit']
            size = kwargs['size']
            if size_unit == "arcseconds":
                pixel_scale = proj_plane_pixel_scales(self.image.wcs)[0] * 3600
                self.size = size / pixel_scale
            elif size_unit == "pixels":
                self.size = size
            else:
                warnings.warn("Invalid size unit for catalog marks. Valid units: arcseconds, pixels")
                return

        if 'ra' in kwargs:
            self._wcs_center = (kwargs['ra'],kwargs['dec'])            
        else:
            self._center = QPointF(*args)

    @property
    def center(self):
        if not hasattr(self,'_center'):
            _x, _y = self.image.wcs.all_world2pix([list(self.wcs_center)], 0)[0]
            return QPointF(_x, self.image.height-_y)
        else:
            return self._center
    
    @property
    def view_center(self):
        return self.center + QPointF(0.5,0.5)

    @property
    def wcs_center(self):
        if not hasattr(self,'_wcs_center'):
            if (self.image.wcs != None):
                _x, _y = self.center.x(), self.image.height - self.center.y()
                return self.image.wcs.all_pix2world([[_x, _y]], 0)[0]
            else: 
                return (nan, nan)
        else:
            return self._wcs_center
    
    @property
    def shapeitem(self):
        if not hasattr(self,'_shapeitem'):
            args = self.view_center.x()-self.size/2, self.view_center.y()-self.size/2, self.size, self.size
            self._shapeitem = self.shape(*args)
            self._shapeitem.setPen(QPen(self.color, int(self.size/10), Qt.PenStyle.SolidLine))
        
        return self._shapeitem
    
    @property
    def label(self):
        if not hasattr(self,'_label'):
            self._label = MarkLabel(self)
        
        return self._label  