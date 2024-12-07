from .pyqt import QGraphicsScene, QGraphicsPixmapItem, QPixmap, QPainter, Qt
from . import mark as _mark
from . import io
import os
from math import floor
import PIL.Image
from PIL.ImageFilter import GaussianBlur
from math import nan
import numpy as np
from typing import overload, Union, List, Dict, TYPE_CHECKING
from astropy.visualization import ZScaleInterval, MinMaxInterval, BaseInterval, BaseStretch, ManualInterval, LinearStretch, LogStretch
from astropy.io import fits

if TYPE_CHECKING:
    from astropy.wcs import WCS

INTERVAL:Dict[str,BaseInterval] = {'zscale': ZScaleInterval(), 'min-max': MinMaxInterval()}
STRETCH:Dict[str,BaseStretch] = {'linear': LinearStretch(), 'log': LogStretch()}
FORMATS = ['TIFF','FITS','PNG','JPEG']
PIL.Image.MAX_IMAGE_PIXELS = None # change this if we want to limit the image size

def open(path:str) -> Union['Image',None]:
    """
    Opens the given image file.

    Parameters
    ----------
    path: str 
        Path to the image.
    
    Returns
    ----------
    img: `imgmarker.image.Image`
        Returns the image as a Image object.
    """
    return Image(path)

class Image(QGraphicsPixmapItem):
    """Image class based on the PyQt QGraphicsPixmapItem."""
    
    def __init__(self,path:str):
        """Initialize from parents."""
        
        super().__init__(QPixmap())

        self.path = path
        self.format = io.pathtoformat(path)

        if self.format in FORMATS:
            
            self.frame:int = 0
            self.imagefile = self.load()

            # Setup  __dict__
            self.width = self.imagefile.width
            self.height = self.imagefile.width

            try: self.n_frames = self.imagefile.n_frames
            except: self.n_frames = 1

            self.wcs:WCS = io.parse_wcs(self.imagefile)
            self.name = path.split(os.sep)[-1]

            self.r:float = 0.0
            self.a:float = 1.0
            self.b:float = 1.0
            self.stretch = 'linear'
            self.interval = 'min-max'
            
            self.comment = 'None'
            self.categories:List[str] = []
            self.marks:List['_mark.Mark'] = []
            self.cat_marks:List['_mark.Mark'] = []
            self.seen:bool = False
            self.catalogs:List[str] = []

            self.imagefile.close()
    
    @property
    def interval(self) -> ManualInterval: 
        interval = INTERVAL[self._interval_str]
        h,s,v = self.hsv()
        vlims = interval.get_limits(v)
        return ManualInterval(*vlims)
    @interval.setter
    def interval(self,value): self._interval_str = value

    @property
    def stretch(self) -> BaseStretch: return STRETCH[self._stretch_str]
    @stretch.setter
    def stretch(self,value): self._stretch_str = value

    @property
    def scaling(self): return self.stretch + self.interval

    @property
    def wcs_center(self) -> list:
        try: return self.wcs.all_pix2world([[self.width/2, self.height/2]], 0)[0]
        except: return nan, nan

    def load(self) -> PIL.Image.Image:
        if self.format == 'FITS':
            with fits.open(self.path) as f:
                arr = np.flipud(f[0].data).byteswap()
            file = PIL.Image.fromarray(arr, mode='F').convert('RGB')
            file.format = 'FITS'
            file.filename = self.path

        else: file = PIL.Image.open(self.path)

        file.seek(self.frame)
        return file
    
    def close(self):
        self.imagefile.close()
        self.setPixmap(QPixmap())
    
    def tell(self): return self.imagefile.tell()

    def seek(self,frame:int=0):
        """Switches to a new frame if it exists"""

        frame = floor(frame)
        
        if frame > self.n_frames - 1: frame = 0
        elif frame < 0: frame = self.n_frames - 1

        self.frame = frame
        self.imagefile = self.load()

        self.width = self.imagefile.width
        self.height = self.imagefile.width
        
        # reapply blur
        self.blur()

    def hsv(self):
        arr = np.array(self.load().convert('HSV'))
        h,s,v = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        return h,s,v
    
    def rescale(self):
        arr = np.array(self.imagefile.copy().convert('HSV'))
        h,s,v = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

        v = (self.scaling(v))*255
        arr[:, :, 0], arr[:, :, 1], arr[:, :, 2] = h,s,v

        image_scaled = PIL.Image.fromarray(arr.astype('uint8'),mode='HSV').convert('RGB')
        self.setPixmap(self.topixmap(image_scaled))
        
    def topixmap(self,image:PIL.Image.Image) -> QPixmap:
        """Creates a QPixmap with a pillows on each side to allow for fully zooming out."""

        qimage = image.toqimage()
        pixmap_base = QPixmap.fromImage(qimage)

        w, h = self.width, self.height
        _x, _y = int(w*4), int(h*4)

        pixmap = QPixmap(w*9,h*9)
        pixmap.fill(Qt.GlobalColor.black)

        painter = QPainter(pixmap)
        painter.drawPixmap(_x, _y, pixmap_base)
        painter.end()

        return pixmap
    
    @overload
    def blur(self) -> None: 
        """Applies the blur to the image"""
    @overload
    def blur(self,value) -> None:
        """Applies the blur to the image"""
    def blur(self,*args):
        if len(args) > 0: 
            value = args[0]
            if callable(value): r = value()
            else: r = value
            self.r = floor(r)/10

        newfile = self.load()
        newfile = newfile.filter(GaussianBlur(self.r))
        self.imagefile = newfile.copy()
        self.rescale()
            
class ImageScene(QGraphicsScene):
    """A class for storing and manipulating the information/image that is currently displayed."""
    def __init__(self,image:Image):
        super().__init__()
        self.image = image

        self.setBackgroundBrush(Qt.GlobalColor.black)
        self.addItem(self.image)

    def update(self,image:Image):
        """Updates the current image with a new image."""
        # Remove items
        for item in self.items(): self.removeItem(item)

        # Update the pixmap
        self.image = image
        self.addItem(self.image)
        self.setSceneRect(0,0,9*self.image.width,9*self.image.height)

    @overload
    def mark(self,x:float,y:float,shape='ellipse',text:Union[int,str]=0) -> '_mark.Mark': ...
    @overload
    def mark(self,ra:float=None,dec:float=None,shape='ellipse',text:Union[int,str]=0) -> '_mark.Mark': ...
    @overload
    def mark(self,mark:'_mark.Mark') -> '_mark.Mark': ... 

    def mark(self,*args,**kwargs) -> '_mark.Mark':
        """Creates a mark object and adds it to the image scene and returns the mark."""

        if len(args) == 1: mark = args[0]
        else: mark = _mark.Mark(*args,image=self.image,**kwargs)
        self.addItem(mark.label)
        self.addItem(mark)
        return mark
    
    def rmmark(self,mark:'_mark.Mark') -> None:
        """Removes the specified mark from the image scene."""

        self.removeItem(mark)
        self.removeItem(mark.label)
