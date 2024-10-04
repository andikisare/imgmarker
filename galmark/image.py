from PyQt6.QtWidgets import ( QApplication, QMainWindow, QPushButton,
                              QLabel, QScrollArea, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
                              QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, 
                              QSlider, QFrame, QLineEdit, QSizePolicy, QStyle)
from PyQt6.QtGui import QPixmap, QCursor, QAction, QIcon, QFont, QPainter, QPen
from PyQt6.QtCore import Qt, QEvent, QPoint
from galmark.mark import Mark
from galmark import __dirname__, __icon__, __heart_solid__, __heart_clear__
import galmark.io
import sys
import os
import datetime as dt
import textwrap
from math import floor, inf
from functools import partial
from PIL import Image
from PIL.ImageQt import ImageQt
from PIL.ImageFilter import GaussianBlur
from PIL.ImageEnhance import Contrast, Brightness

class ImageFilter():
    def __init__(self,img:Image.Image,a=1,b=1,r=0):
        self.a = a
        self.b = b
        self.r = r
        self.img = img
    
    def setA(self,a): self.a = a
    def setB(self,b): self.a = b
    def setR(self,r): self.a = r

    def apply(self) -> Image.Image:
        def blur(img:Image.Image):
            return img.filter(GaussianBlur(self.r))
        def brighten(img:Image.Image):
            return Brightness(img).enhance(self.a)
        def contrast(img:Image.Image):
            return Contrast(img).enhance(self.b)
        return contrast(brighten(blur(self.img)))
    
class ImageScene(QGraphicsScene):
    def __init__(self,image:Image.Image):
        super().__init__()

        # Initial frame
        self.frame = 0

        self.image = image
        self.qimage = ImageQt(image)

        self.setBackgroundBrush(Qt.GlobalColor.black)
        self.pixmap = self._pixmap()
        self._pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.addItem(self._pixmap_item)

        # Initial adjustment values:
        self.r = 0
        self.a = 1
        self.b = 1
        self.blur_max = int((self.qimage.height()+self.qimage.width())/20)

        self.wcs = galmark.io.parseWCS(self.image)

        self.file = self.image.filename.split(os.sep)[-1]

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
    
    def blur(self,value):
        self.r = floor(value)/10
        imageFilter = ImageFilter(self.image,a=self.a,b=self.b,r=self.r)
        image_blurred = imageFilter.apply()
        
        self.qimage = ImageQt(image_blurred)
        self.pixmap = self._pixmap()
        self._pixmap_item.setPixmap(self.pixmap)

    def brighten(self,value):
        self.a = floor(value)/10 + 1
        imageFilter = ImageFilter(self.image,a=self.a,b=self.b,r=self.r)
        image_bright = imageFilter.apply()
        
        self.qimage = ImageQt(image_bright)
        self.pixmap = self._pixmap()
        self._pixmap_item.setPixmap(self.pixmap)

    def contrast(self,value):
        self.b = floor(value)/10 + 1
        imageFilter = ImageFilter(self.image,a=self.a,b=self.b,r=self.r)
        image_contrast = imageFilter.apply()
        
        self.qimage = ImageQt(image_contrast)
        self.pixmap = self._pixmap()
        self._pixmap_item.setPixmap(self.pixmap)

    def seek(self,value):
        self.frame = floor(value)
        if value > self.image.n_frames - 1: self.frame = 0
        elif value < 0: self.frame = self.image.n_frames -1
        
        self.image.seek(self.frame)
        self.qimage = ImageQt(self.image)
        self.pixmap = self._pixmap()
        self._pixmap_item.setPixmap(self.pixmap)

    def update(self,path):
        # Remove Marks
        for item in self.items(): 
            if isinstance(item,Mark): self.removeItem(item)

        # Update the pixmap
        self.image = Image.open(path)
        self.image.seek(min(self.frame,self.image.n_frames-1))
        
        self.file = self.image.filename.split(os.sep)[-1]
        self.qimage = ImageQt(self.image)
        self.pixmap = self._pixmap()
        self._pixmap_item.setPixmap(self.pixmap)

        self.wcs = galmark.io.parseWCS(self.image)

    def mark(self,x,y,group):
        mark = Mark(x,y,wcs=self.wcs,group=group)
        self.addItem(mark)
        return mark
