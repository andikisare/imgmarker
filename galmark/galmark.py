from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsEllipseItem
from PyQt6.QtGui import QPixmap, QPainter, QPen, QBrush, QCursor, QKeyEvent, QColor
from PyQt6.QtCore import Qt, QSize
import sys
import os
from PIL import Image, ImageShow
ImageShow.Viewer = "PNG"
import numpy as np
import pandas as pd
import io
import glob
import argparse
import os
import sys
from PIL.TiffTags import TAGS
from astropy.wcs import WCS as WCS
from astropy.io import fits
from collections import defaultdict

class MainWindow(QMainWindow):
    def __init__(self, path = '', imtype = 'tif',
        outfile = 'lensrankings.txt', overwrite = False, parent=None):
        '''
        Constructor

        Required Inputs:
            main (Tk): root to which the tkinter widgets are added

        Optional Inputs:
            path (string): path to directory containing candidate images
            imtype (string): file extension of images to be ranked
            outfile (string): filename of text file for saving data
        '''
        super().__init__()

        if path == '':
            self.path = os.getcwd()

        else:
            self.path = path

        if self.path[-1] != '/':
            self.path = self.path + '/'

        self.imtype = imtype
        self.outfile = outfile
        self.overwrite = overwrite

        # Initialize images and WCS
        self.idx = 0
        self.images = self._findImages()
        
        self.N = len(self.images)
        self.img = self.images[self.idx]
        
        self.wcs = self.parseWCS(self.img)

        # Initialize output dictionary
        data = defaultdict(dict)

        #sets useful attributes
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.windowsize = QSize(int(self.fullw/2), int(self.fullh/2))
        self.zoomfrac = (self.fullh - 275) / 400
        self._go_back_one = False
        self.setWindowTitle("Galaxy Marker")

        # Create image scene
        self.image_scene = QGraphicsScene(self)
        self.pixmap = QPixmap(self.img)
        self._pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.image_scene.addItem(self._pixmap_item)

        # Create image view
        self.image_view = QGraphicsView(self.image_scene)
        self.image_view.keyPressEvent = self.onImageClick
        self.image_view.mousePressEvent = self.onImageClick
        self.image_view.resizeEvent = self.onResize
        #self.image_view.mouseMoveEvent = self.mouseTracker

        # Current index widget
        self.idx_label = QLabel(f'Image {self.idx+1} of {self.N}')
        self.idx_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Back widget
        self.back_button = QPushButton(text='Back',parent=self)
        self.back_button.setFixedHeight(40)
        self.back_button.clicked.connect(self.onBack)

        '''# Submit Button
        self.submit_button = QPushButton(text='Submit',parent=self)
        self.submit_button.setFixedHeight(40)'''

        # Next widget
        self.next_button = QPushButton(text='Next',parent=self)
        self.next_button.setFixedHeight(40)
        self.next_button.clicked.connect(self.onNext)

        # Botton Bar layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.back_button)
        #self.bottom_layout.addWidget(self.submit_button)
        self.bottom_layout.addWidget(self.next_button)

        # Add widgets to main layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.image_view)
        layout.addWidget(self.idx_label)
        layout.addLayout(self.bottom_layout)
        self.setCentralWidget(central_widget)


    def _findImages(self):
        '''
        Finds and returns a list of images of self.imtype located at
            self.path.

        Returns:
            ims (list of strings): filenames
        '''
        images = glob.glob(self.path + '*.' + self.imtype)

        return images   
    
    def _buttonCheck(self,event):
        button1 = button2 = button3 = button4 = button5 = button6 = button7 = button8 = button9 = False

        try: button1 = event.button() == Qt.MouseButton.LeftButton
        except: button1 = event.key() == Qt.Key.Key_1

        try: button2 = event.button() == Qt.MouseButton.RightButton
        except: button2 = event.key() == Qt.Key.Key_2

        try:
            button3 = event.key() == Qt.Key.Key_3
            button4 = event.key() == Qt.Key.Key_4
            button5 = event.key() == Qt.Key.Key_5
            button6 = event.key() == Qt.Key.Key_6
            button7 = event.key() == Qt.Key.Key_7
            button8 = event.key() == Qt.Key.Key_8
            button9 = event.key() == Qt.Key.Key_9
        except: pass

        return [button1, button2, button3, button4, button5, button6, button7, button8, button9]

        
    def drawCircle(self,x,y,c=Qt.GlobalColor.black,r=10):
        ellipse = QGraphicsEllipseItem(x-r/2, y-r/2, r, r)
        ellipse.setPen(QPen(c, 1, Qt.PenStyle.SolidLine))
        self.image_scene.addItem(ellipse) 

    def imageUpdate(self):
        self.image_scene.clear()
        # Update idx label
        self.idx_label.setText(f'Current image: {self.idx+1} of {self.N}')

        # Update the pixmap
        next_image = QPixmap(self.images[self.idx])
        self.pixmap = QPixmap(next_image)
        self._pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.image_scene.addItem(self._pixmap_item)

        #Update WCS
        self.wcs = self.parseWCS(self.images[self.idx])


    def onResize(self, event):
        '''
        Resize event; rescales image to fit in window, but keeps aspect ratio
        '''
        self.image_view.fitInView(self._pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        super().resizeEvent(event)

    def onImageClick(self, event):
        '''
        Actions to complete on mouse-click
        '''
        # get event position and position on image
        ep, lp = self.mouseImagePos(event)
        
        # Check button presses
        buttons = self._buttonCheck(event)
        colors = [QColor(255,0,0),QColor(255,128,0),QColor(255,255,0),
                  QColor(0,255,0),QColor(0,255,255),QColor(0,128,128),
                  QColor(0,0,255),QColor(128,0,255),QColor(255,0,255)]

        # Used button1
        for i in range(0,9):

            if (self._pixmap_item is self.image_view.itemAt(ep)) and buttons[i]:
                
                x, y = lp.x(), self.pixmap.height() - lp.y()
                coords = self.wcs.all_pix2world([[x, y]], 0)[0]

                self.drawCircle(lp.x(),lp.y(),c=colors[i])

                print(lp)
                print(coords)
    
    def mouseImagePos(self,event):
        ep = self.image_view.mapFromGlobal(QCursor.pos())
        sp = self.image_view.mapToScene(ep)
        lp = self._pixmap_item.mapFromScene(sp).toPoint()

        return ep, lp
    
    def parseWCS(self,image_tif):
        tif_image_data = np.array(Image.open(image_tif))
        img = Image.open(image_tif)
        meta_dict = {TAGS[key] : img.tag[key] for key in img.tag_v2}
        
        long_header_str = meta_dict['ImageDescription'][0]

        line_length = 80

        # Splitting the string into lines of 80 characters
        lines = [long_header_str[i:i+line_length] for i in range(0, len(long_header_str), line_length)]
       
        # Join the lines with newline characters to form a properly formatted header string
        corrected_header_str = "\n".join(lines)

         # Use an IO stream to mimic a file
        header_stream = io.StringIO(corrected_header_str)

        # Read the header using astropy.io.fits
        header = fits.Header.fromtextfile(header_stream)

        # Create a WCS object from the header
        wcs = WCS(header)
        print(wcs)
        shape = (meta_dict['ImageWidth'][0], meta_dict['ImageLength'][0])
        return wcs
    
    def onNext(self):
        if self.idx+1 < self.N:
            # Increment the index
            self.idx += 1
            self.imageUpdate()

    def onBack(self):
        if self.idx+1 > 1:
            # Increment the index
            self.idx -= 1
            self.imageUpdate()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__': main()