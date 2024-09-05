from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsEllipseItem
from PyQt6.QtGui import QPixmap, QPainter, QPen, QBrush
from PyQt6.QtCore import Qt, QSize
import sys
import os
from PIL import ImageTk, Image, ImageShow, ImageFilter, ImageEnhance
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

        os.system('xset r off')
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

        #sets useful attributes
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.windowsize = QSize(int(self.fullw/2), int(self.fullh/2))
        self.zoomfrac = (self.fullh - 275) / 400
        self._go_back_one = False
        self.setWindowTitle("galnote")

        # Create image scene
        self.image_scene = QGraphicsScene(self)
        self.pixmap = QPixmap(self.img)
        self._pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.image_scene.addItem(self._pixmap_item)

        # Create image view
        self.image_view = QGraphicsView(self.image_scene)
        self.image_view.mousePressEvent = self.onClick
        self.image_view.resizeEvent = self.onResize

        # Current index widget
        self.idx_label = QLabel(f'Current image: {self.idx+1} of {self.N}')
        self.idx_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Back widget
        self.back_button = QPushButton(text='Back',parent=self)
        self.back_button.setFixedHeight(40)
        self.back_button.clicked.connect(self.onBack)

        # Submit Button
        self.submit_button = QPushButton(text='Submit',parent=self)
        self.submit_button.setFixedHeight(40)

        # Next widget
        self.next_button = QPushButton(text='Next',parent=self)
        self.next_button.setFixedHeight(40)
        self.next_button.clicked.connect(self.onNext)

        # Botton Bar layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.back_button)
        self.bottom_layout.addWidget(self.submit_button)
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
        
    def getPixel(self, event):
        x = self.event.pos().x()
        y = event.pos().y()
        print(x,y)

    def imageUpdate(self):
        # Update idx label
        self.idx_label.setText(f'Current image: {self.idx+1} of {self.N}')

        # Update the pixmap and WCS
        next_image = QPixmap(self.images[self.idx])
        self.wcs = self.parseWCS(self.images[self.idx])
        self._pixmap_item.setPixmap(next_image)


    def onResize(self, event):
        '''
        Resize event; rescales image to fit in window, but keeps aspect ratio
        '''
        self.image_view.fitInView(self._pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        super().resizeEvent(event)

    def onClick(self, event):
        '''
        Actions to complete on mouse-click
        '''
        # Left Click
        if (self._pixmap_item is self.image_view.itemAt(event.pos())) and (event.button() == Qt.MouseButton.LeftButton):
            sp = self.image_view.mapToScene(event.pos())
            lp = self._pixmap_item.mapFromScene(sp).toPoint()
            
            x, y = lp.x(), self.pixmap.height()-lp.y()
            coords = self.wcs.all_pix2world([[x, y]], 0)[0]

            r = 10
            ellipse = QGraphicsEllipseItem(lp.x()-r/2, lp.y()-r/2, r, r)
            ellipse.setPen(QPen(Qt.GlobalColor.red, 1, Qt.PenStyle.SolidLine))
            self.image_scene.addItem(ellipse) 
                        
            print(lp)
            print(coords)

        # Right Click
        if (self._pixmap_item is self.image_view.itemAt(event.pos())) and (event.button() == Qt.MouseButton.RightButton):
            pass
    

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