from __future__ import annotations
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem 
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt
from galmark.mark import Mark
from galmark import __dirname__
import galmark.io
import os
from math import floor
from PIL import Image, ImageFile
from PIL.ImageFilter import GaussianBlur
from PIL.ImageEnhance import Contrast, Brightness
from astropy.wcs import WCS
from math import nan
from astropy.io import fits
import numpy as np

SUPPORTED_EXTS = ['tif','tiff','fits','fit','png','jpeg','jpg']

def open(path:str) -> GImage | None:
    """
    Opens the given image file.

    :param path: Path to the image
    :returns gimage: An :py:class:`galmark.image.GImage` object.
    """
    Image.MAX_IMAGE_PIXELS = None # change this if we want to limit the image size
    ext = path.split('.')[-1]

    if ext in SUPPORTED_EXTS:
        gimage = GImage()

        if (ext == 'fits') or (ext == 'fit'):
            file = fits.open(path)
            img_array = file[0].data
            img_array = np.flipud(img_array)
            img_array = img_array.byteswap()
            image = Image.fromarray(img_array, mode='F')
            filename = path.split(os.sep)[-1]
            print(filename)
            image = image.convert('RGB') 
        else:
            image = Image.open(path)
            filename = image.filename

        # Setup  __dict__
        gimage.__dict__ =  image.__dict__
        try: gimage.n_frames = image.n_frames
        except: gimage.n_frames = 1
        gimage.wcs = galmark.io.parseWCS(image)
        gimage.image_file = image
        gimage.name = filename.split(os.sep)[-1] 

        gimage.r = 0.0
        gimage.a = 1.0
        gimage.b = 1.0

        gimage.comment = 'None'
        gimage.categories = []
        gimage.marks = []
        gimage.seen = False

        # Get bytes from image (I dont think this does anything)
        gimage.frombytes(image.tobytes())
        
        # Initialize QGraphicsPixmapItem
        super(QGraphicsPixmapItem,gimage).__init__(gimage.pixmap())

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
        self.marks:list[Mark]
        self.seen:bool
 
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
    
    def tell(self) -> None: return self.image_file.tell()

    def seek(self,value) -> None:
        frame = floor(value)
        
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
        pixmap.fill(Qt.GlobalColor.red)

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

        self.frame = 0
        self.image = image

        self.setBackgroundBrush(Qt.GlobalColor.black)
        self.addItem(self.image)

    def update(self,image:GImage):
        # Remove items
        for item in self.items(): self.removeItem(item)

        # Update the pixmap
        self.image = image
        self.image.seek(min(self.frame,self.image.n_frames-1))
        self.addItem(self.image)
        self.setSceneRect(0,0,9*self.image.width,9*self.image.height)

    def mark(self,x,y,group):
        mark = Mark(x,y,image=self.image,group=group)
        self.addItem(mark)
        return mark  
