from __future__ import annotations
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem 
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt
import imgmarker.mark
from imgmarker import __dirname__, SUPPORTED_EXTS
import imgmarker.io
import os
from math import floor
from PIL import Image, ImageFile, ImageOps
from PIL.ImageFilter import GaussianBlur
from PIL.ImageEnhance import Contrast, Brightness
from astropy.wcs import WCS
from math import nan
from astropy.io import fits
import numpy as np
import time
import typing

def open(path:str) -> GImage | None:
    """
    Opens the given image file.

    :param path: Path to the image
    :returns gimage: An :py:class:`imgmarker.image.GImage` object.
    """
    Image.MAX_IMAGE_PIXELS = None # change this if we want to limit the image size
    ext = path.split('.')[-1]

    if ext in SUPPORTED_EXTS:
        gimage = GImage()

        if (ext == 'fits') or (ext == 'fit'):
            file = fits.open(path)
            img_array = np.flipud(file[0].data).byteswap()
            image = Image.fromarray(img_array, mode='F').convert('RGB')
            image.format = 'FITS'
            image.filename = path

        else: image = Image.open(path)

        # Setup  __dict__
        gimage.__dict__ =  image.__dict__
        try: gimage.n_frames = image.n_frames
        except: gimage.n_frames = 1
        gimage.wcs = imgmarker.io.parse_wcs(image)
        gimage.image_file = image
        gimage.name = path.split(os.sep)[-1] 

        gimage.r = 0.0
        gimage.a = 1.0
        gimage.b = 1.0

        gimage.comment = 'None'
        gimage.categories = []
        gimage.marks = []
        gimage.seen = False
        gimage.frame = 0

        # Get bytes from image (I dont think this does anything)
        gimage.frombytes(image.tobytes())

        super(QGraphicsPixmapItem,gimage).__init__(QPixmap())

        return gimage
    
class GImage(Image.Image,QGraphicsPixmapItem):
    def __init__(self):
        # Initialize from parents
        super().__init__()

        self.image_file:ImageFile.ImageFile
        self.wcs:WCS
        self.n_frames:int
        self.name:str
        self.r:float
        self.a:float
        self.b:float
        self.comment:str
        self.categories:list[str]
        self.marks:list[imgmarker.mark.Mark]
        self.ext_marks:list[imgmarker.mark.Mark]
        self.seen:bool
        self.frame:int

    def _new(self, im) -> GImage:
        new = GImage()
        new.im = im
        new._mode = im.mode
        new._size = im.size
        if im.mode in ("P", "PA"):
            if self.palette:
                new.palette = self.palette.copy()
            else:
                from PIL import ImagePalette

                new.palette = ImagePalette.ImagePalette()
        new.info = self.info.copy()
        return new
    
    def clear(self): self.setPixmap(QPixmap())
    
    def tell(self): return self.image_file.tell()

    def seek(self,frame:int=0):
        frame = floor(frame)
        
        if frame > self.n_frames - 1: frame = 0
        elif frame < 0: frame = self.n_frames - 1

        self.image_file.seek(frame)

        self.__dict__ = self.image_file.__dict__
        self.frombytes(self.image_file.tobytes())
        self.setPixmap(self.pixmap())
    
    def pixmap(self) -> QPixmap:
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
    
    def adjust(self) -> GImage:
        def _blur(img:GImage):
            return img.filter(GaussianBlur(self.r))
        def _brighten(img:GImage):
            return Brightness(img).enhance(self.a)
        def _contrast(img:GImage):
            return Contrast(img).enhance(self.b)
        
        img_filt = _contrast(_brighten(_blur(self)))
        gimg_filt = self.copy()
        gimg_filt.frombytes(img_filt.tobytes())

        return gimg_filt
    
    def blur(self,value):
        self.r = floor(value)/10
        pixmap_blurred = self.adjust().pixmap()
        self.setPixmap(pixmap_blurred)

    def brighten(self,value):
        self.a = floor(value)/10 + 1
        pixmap_bright = self.adjust().pixmap()
        self.setPixmap(pixmap_bright)

    def contrast(self,value):
        self.b = floor(value)/10 + 1
        pixmap_contrast = self.adjust().pixmap()
        self.setPixmap(pixmap_contrast)

    def wcs_center(self) -> list:
        try: return self.wcs.all_pix2world([[self.width/2, self.height/2]], 0)[0]
        except: return nan, nan
            
class ImageScene(QGraphicsScene):
    def __init__(self,image:GImage):
        super().__init__()
        self.image = image

        self.setBackgroundBrush(Qt.GlobalColor.black)
        self.addItem(self.image)

    def update(self,image:GImage):
        # Remove items
        for item in self.items(): self.removeItem(item)

        # Update the pixmap
        self.image = image
        self.addItem(self.image)
        self.setSceneRect(0,0,9*self.image.width,9*self.image.height)

    @typing.overload
    def mark(self,x:float,y:float,shape='ellipse',text:int|str=0) -> imgmarker.mark.Mark: ...
    @typing.overload
    def mark(self,ra:float=None,dec:float=None,shape='ellipse',text:int|str=0) -> imgmarker.mark.Mark: ...
    @typing.overload
    def mark(self,mark:imgmarker.mark.Mark) -> imgmarker.mark.Mark: ... 

    def mark(self,*args,**kwargs) -> imgmarker.mark.Mark:
        if len(args) == 1: mark = args[0]
        else: mark = imgmarker.mark.Mark(*args,image=self.image,**kwargs)
        self.addItem(mark.label)
        self.addItem(mark)
        return mark
    
    def rmmark(self,mark:imgmarker.mark.Mark) -> None:
        self.removeItem(mark)
        self.removeItem(mark.label)
