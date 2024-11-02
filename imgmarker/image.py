from .pyqt import QGraphicsScene, QGraphicsPixmapItem, QPixmap, QPainter, Qt
from . import mark as _mark
from . import SUPPORTED_EXTS
from . import io
import os
from math import floor
import PIL.Image, PIL.ImageFile
from PIL.ImageFilter import GaussianBlur
from astropy.wcs import WCS
from math import nan
from astropy.io import fits
import numpy as np
from typing import overload, Union, List, Dict
from astropy.visualization import ZScaleInterval, MinMaxInterval, BaseInterval, BaseStretch, ManualInterval, LinearStretch, LogStretch

INTERVAL:Dict[str,BaseInterval] = {'zscale': ZScaleInterval(), 'min-max': MinMaxInterval()}
STRETCH:Dict[str,BaseStretch] = {'linear': LinearStretch(), 'log': LogStretch()}

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

    PIL.Image.MAX_IMAGE_PIXELS = None # change this if we want to limit the image size
    ext = path.split('.')[-1]

    if ext in SUPPORTED_EXTS:
        img = Image()

        if (ext == 'fits') or (ext == 'fit'):
#            file = fits.open(path)
#            img_array = np.flipud(file[0].data).byteswap()
            with fits.open(path) as file:
                img_array = np.flipud(file[0].data).byteswap()
            img_pil = PIL.Image.fromarray(img_array, mode='F').convert('RGB')
            img_pil.format = 'FITS'
            img_pil.filename = path

        else: img_pil = PIL.Image.open(path)

        # Setup  __dict__
        img.__dict__ =  img_pil.__dict__
        try: img.n_frames = img_pil.n_frames
        except: img.n_frames = 1
        img.wcs = io.parse_wcs(img_pil)
        img.image_file = img_pil
        img.name = path.split(os.sep)[-1] 

        img.r = 0.0
        img.a = 1.0
        img.b = 1.0
        img.stretch = 'linear'
        img.interval = 'min-max'
        
        img.comment = 'None'
        img.categories = []
        img.marks = []
        img.ext_marks = []
        img.seen = False
        img.frame = 0

        # Get bytes from image (I dont think this does anything)
        img.frombytes(img_pil.tobytes())

        super(QGraphicsPixmapItem,img).__init__(QPixmap())

        #img_pil.close() #trying to close files
        return img

class Image(PIL.Image.Image,QGraphicsPixmapItem):
    """Image class based on the Python Pillow Image class and merged with the PyQt5 QGraphicsPixmapItem."""
    
    def __init__(self):
        """Initialize from parents."""
        
        super().__init__()

        self.image_file:PIL.ImageFile.ImageFile
        self.wcs:WCS
        self.n_frames:int
        self.name:str
        self.r:float
        self.a:float
        self.b:float
        self.comment:str
        self.categories:list[str]
        self.marks:list['_mark.Mark']
        self.ext_marks:list['_mark.Mark']
        self.seen:bool
        self.frame:int

    @property
    def interval(self) -> BaseInterval: 
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

    def copy(self) -> 'Image': return super().copy()

    def _new(self, im) -> 'Image':
        """Internal PIL.Image.Image method for making a copy of the image."""
        new = Image()
        new.im = im
        new._mode = im.mode
        try: new.mode = im.mode
        except: pass
        new._size = im.size
        if im.mode in ("P", "PA"):
            if self.palette:
                new.palette = self.palette.copy()
            else:
                from PIL import ImagePalette

                new.palette = ImagePalette.ImagePalette()
        new.info = self.info.copy()
        return new

    def frompillow(self,pil:PIL.Image.Image) -> 'Image':
        image = self.copy()
        image.__dict__.update(self.__dict__)
        image.frombytes(pil.tobytes())
        return image
    
    def hsv(self):
        arr = np.array(self.convert('HSV'))
        h,s,v = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
        return h,s,v
    
    def clear(self): self.setPixmap(QPixmap())
    
    def tell(self): return self.image_file.tell()

    def seek(self,frame:int=0):
        """Switches to a new frame if it exists"""

        frame = floor(frame)
        
        if frame > self.n_frames - 1: frame = 0
        elif frame < 0: frame = self.n_frames - 1

        self.image_file.seek(frame)

        self.__dict__ = self.image_file.__dict__
        self.frombytes(self.image_file.tobytes())

        # delete the adjustments layer
        if hasattr(self,'layer0'): del self.layer0
        
        # scale colors
        self.rescale()

    def rescale(self):
        if hasattr(self,'layer0'): image = self.layer0.copy()
        else: image = self.copy()

        arr = np.array(image.convert('HSV'))
        h,s,v = image.hsv()

        v = (self.scaling(v))*255

        arr[:, :, 0], arr[:, :, 1], arr[:, :, 2] = h, s, v

        image_scaled = image.frompillow(PIL.Image.fromarray(arr.astype('uint8'),mode='HSV').convert('RGB'))
        self.setPixmap(image_scaled.topixmap())

    def topixmap(self) -> QPixmap:
        """Creates a QPixmap with a pillows on each side to allow for fully zooming out."""

        qimage = self.toqimage()
        pixmap_base = QPixmap.fromImage(qimage)

        w, h = self.width, self.height
        _x, _y = int(w*4), int(h*4)

        pixmap = QPixmap(w*9,h*9)
        pixmap.fill(Qt.GlobalColor.black)

        painter = QPainter(pixmap)
        painter.drawPixmap(_x, _y, pixmap_base)
        painter.end()

        return pixmap
    
    def blur(self,value):
        """Applies the blur value to a filter and displays it."""
        if callable(value): r = value()
        else: r = value
        self.r = floor(r)/10

        pil = self.filter(GaussianBlur(self.r))
        self.layer0 = self.copy()
        self.layer0.frombytes(pil.tobytes())
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
