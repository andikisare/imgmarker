"""
Copyright © 2025, UChicago Argonne, LLC

Full license found at _YOUR_INSTALLATION_DIRECTORY_/imgmarker/LICENSE
"""

"""This module contains the `Mark` class and related classes."""

from imgmarker.gui.pyqt import QGraphicsPathItem, QPainterPath, QGraphicsProxyWidget, QLineEdit, QPen, QColor, Qt, QPointF, QEvent
from imgmarker import config
from imgmarker.coordinates import PixCoord, WorldCoord
import os
from math import nan, ceil
from astropy.wcs.utils import proj_plane_pixel_scales
from typing import TYPE_CHECKING, overload, Literal
import warnings

if TYPE_CHECKING:
    from imgmarker.image import Image 

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
        h = fm.boundingRect('AA').height()
        self.lineedit.setFixedWidth(w)
        self.lineedit.setFixedHeight(h)

class Mark(QGraphicsPathItem):
    """Class for creating marks and associating label to mark"""

    @overload
    def __init__(self,x:int,y:int,
                 shape:str='ellipse',
                 image:'Image'=None,group:int=0,text:str=None,color:QColor=None,size_unit:Literal['px','arcsec']=None,size:float=None,
    ) -> None: ...
    @overload
    def __init__(self,ra:float=None,dec:float=None,
                 shape:str='ellipse',
                 image:'Image'=None,group:int=0,text:str=None,color:QColor=None,size_unit:Literal['px','arcsec']=None,size:float=None,
    ) -> None: ...
    def __init__(self,*args,**kwargs) -> None:
        # Set up some default values
        self.image = None
        self.g = 0
        self._shape = 'ellipse'
        self.size_unit = 'px'
        self.dst = os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')
        self.label:MarkLabel = QGraphicsProxyWidget()

        if 'image' in kwargs: 
            self.image:'Image' = kwargs['image']

        if ('group' in kwargs) and (kwargs['group'] != 0):
            self.g:int = kwargs['group']
            self._color = config.GROUP_COLORS[self.g]

        if 'color' in kwargs:
            self._color = kwargs["color"]

        if 'text' in kwargs:
            self.text:str = kwargs['text']
        else:
            self.text = config.GROUP_NAMES[self.g]

        if 'shape' in kwargs:
            self._shape = kwargs['shape']
        
        if "size" in kwargs:
            if 'size_unit' in kwargs:
                self.size_unit = kwargs['size_unit']
            self._size_value = kwargs['size']

        if 'ra' in kwargs:
            self._wcs_center = WorldCoord(kwargs['ra'],kwargs['dec'])            
        else:
            self._center = PixCoord(*args)
        
        super().__init__()
        
        self.setFlag(self.GraphicsItemFlag.ItemIsSelectable)

    @property
    def color(self):
        if hasattr(self,'_color'):
            return self._color
        else:
            return config.DEFAULT_COLORS[self.dst]

    @property
    def size_value(self):
        if hasattr(self,'_size_value'):
            return self._size_value
        elif self.image != None:
            return ceil((self.image.width+self.image.height)/200)*2
        else:
            return 10
    
    @property
    def size(self):
        if self.size_unit == "arcsec":
            pixel_scale = proj_plane_pixel_scales(self.image.wcs)[0] * 3600
            return self.size_value / pixel_scale
        elif self.size_unit == "px":
            return self.size_value
        else:
            warnings.warn("Invalid size unit for catalog marks. Valid units: arcsec, px")
            return
        
    @property
    def center(self) -> PixCoord:
        if not hasattr(self,'_center'):
            return self.wcs_center.topix(self.image.wcs)
        else:
            return self._center
    
    @property
    def view_center(self):
        return QPointF(*self.center) + QPointF(0.5,0.5)

    @property
    def wcs_center(self) -> WorldCoord:
        if not hasattr(self,'_wcs_center'):
            if (self.image.wcs != None):
                return self.center.toworld(self.image.wcs)
            else: 
                return (nan, nan)
        else:
            return self._wcs_center

    def draw(self):
        args = (self.view_center.x()-self.size/2,
                self.view_center.y()-self.size/2,
                self.size,
                self.size)
        
        path = QPainterPath()

        if self._shape == 'ellipse':
            path.addEllipse(*args)
        elif self._shape == 'rect':
            path.addRect(*args)
        
        self.setPath(path)
        pen = QPen(self.color, # brush
                int(self.size/10), # width
                Qt.PenStyle.SolidLine, # style
                Qt.PenCapStyle.RoundCap, # cap
                Qt.PenJoinStyle.MiterJoin) # join
        self.setPen(pen)

