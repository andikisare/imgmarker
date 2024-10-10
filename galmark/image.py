from __future__ import annotations
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem 
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt
from galmark.mark import Mark
from galmark import __dirname__, __icon__, __heart_solid__, __heart_clear__
import galmark.io
import os
from math import floor
from PIL import Image, ImageFile
from PIL.ImageQt import ImageQt
from PIL.ImageFilter import GaussianBlur
from PIL.ImageEnhance import Contrast, Brightness
from astropy.wcs import WCS

def open(path:str) -> GImage:
    """
    Opens the given image file.

    :param path: Path to the image
    :returns gimage: An :py:class:`galmark.image.GImage` object.
    """

    image = Image.open(path)
    gimage = GImage()

    # Setup  __dict__
    gimage.__dict__ =  image.__dict__
    gimage.n_frames = image.n_frames
    gimage.wcs = galmark.io.parseWCS(image)
    gimage.image_file = image
    gimage.name = image.filename.split(os.sep)[-1] 

    gimage.r = 0.0
    gimage.a = 1.0
    gimage.b = 1.0

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
    
    def seek(self,value) -> None:
        self.frame = floor(value)

        if value > self.n_frames - 1: self.frame = 0
        elif value < 0: self.frame = self.n_frames -1

        self.image_file.seek(self.frame)

        self.__dict__ = self.image_file.__dict__
        self.frombytes(self.image_file.tobytes())
        self.setPixmap(self.pixmap())
    
    def pixmap(self) -> QPixmap:
        qimage = self.toqimage()
        pixmap_base = QPixmap.fromImage(qimage)

        w, h = self.height, self.width
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
        return self.wcs.all_pix2world([[self.width/2, self.height/2]], 0)[0]
            
class ImageScene(QGraphicsScene):
    def __init__(self,image:GImage):
        super().__init__()

        # Initial frame
        self.frame = 0

        self.image = image
        self.qimage = ImageQt(self.image)

        self.setBackgroundBrush(Qt.GlobalColor.black)
        self._pixmap_item = self.image
        self.addItem(self.image)
        
    def _pixmap(self) -> QPixmap:
        pixmap_base = QPixmap.fromImage(self.qimage)

        w, h = pixmap_base.height(), pixmap_base.width()
        _x, _y = int(w*4), int(h*4)

        pixmap = QPixmap(w*9,h*9)
        pixmap.fill(Qt.GlobalColor.black)

        painter = QPainter(pixmap)
        painter.drawPixmap(_x, _y, pixmap_base)
        painter.end()

        return pixmap

    def update(self,image:GImage):
        # Remove items
        for item in self.items(): self.removeItem(item)

        # Update the pixmap
        self.image = image
        self.image.seek(min(self.frame,self.image.n_frames-1))
        
        self.addItem(self.image)

    def mark(self,x,y,group):
        mark = Mark(x,y,wcs=self.image.wcs,group=group)
        self.addItem(mark)
        return mark
