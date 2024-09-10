from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsEllipseItem, QLineEdit, QMenuBar, QInputDialog
from PyQt6.QtGui import QPixmap, QPen, QCursor, QColor, QAction
from PyQt6.QtCore import Qt, QSize
import sys
import os
import numpy as np
import io
import glob
from PIL import Image
import argparse
import os
import sys
from PIL.TiffTags import TAGS
from astropy.wcs import WCS
from astropy.io import fits
from collections import defaultdict

class DataDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(DataDict, self).__init__(DataDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))
    
def markBindingCheck(event):
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

"""
# Use this function for correlating middle mouse button to a keyboard button, do later
def panBindingCheck(event):
    middleMouse = False
    try 
"""

class MainWindow(QMainWindow):
    def __init__(self, path = '', imtype = 'tif', overwrite = True, parent=None):
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

        self.imtype = imtype
        self.config = 'config'
        self.overwrite = overwrite
        self.readConfig()

        # Initialize images and WCS
        self.idx = 0
        self.images = self.findImages()
        self.N = len(self.images)

        # Initialize output dictionary
        self.data = DataDict()
        self.colors = [QColor(255,0,0),QColor(255,128,0),QColor(255,255,0),
                  QColor(0,255,0),QColor(0,255,255),QColor(0,128,128),
                  QColor(0,0,255),QColor(128,0,255),QColor(255,0,255)]

        # Useful attributes
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.windowsize = QSize(int(self.fullw/2), int(self.fullh/2))
        #self.zoomfrac = (self.fullh - 275) / 400
        self._go_back_one = False
        self.setWindowTitle("Galaxy Marker")
        
        self.username = ""
        self.username = str(self.getText())
        self.outfile = self.username + ".txt"
        # Create image view
        self.image_scene = QGraphicsScene(self)
        self.imageUpdate()
        self.image_view = QGraphicsView(self.image_scene)       
        self.image_view.verticalScrollBar().blockSignals(True)
        self.image_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.image_view.horizontalScrollBar().blockSignals(True)
        self.image_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.image_view.move(0, 0)
        self.image_view.setTransformationAnchor(self.image_view.ViewportAnchor(1))
        self.image_view.viewport().installEventFilter(self)

        # Current index widget
        self.idx_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Back widget
        self.back_button = QPushButton(text='Back',parent=self)
        self.back_button.setFixedHeight(40)
        self.back_button.clicked.connect(self.onBack)

        # Enter Button
        self.submit_button = QPushButton(text='Enter',parent=self)
        self.submit_button.setFixedHeight(40)
        self.submit_button.clicked.connect(self.onEnter)

        # Next widget
        self.next_button = QPushButton(text='Next',parent=self)
        self.next_button.setFixedHeight(40)
        self.next_button.clicked.connect(self.onNext)

        # Comment widget
        self.comment_box = QLineEdit(parent=self)
        self.comment_box.setFixedHeight(40)
        #self.commentUpdate()
    
        # Botton Bar layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.back_button)
        self.bottom_layout.addWidget(self.next_button)
        self.bottom_layout.addWidget(self.comment_box)
        self.bottom_layout.addWidget(self.submit_button)
        
        # Add widgets to main layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.image_view)
        layout.addWidget(self.idx_label)
        layout.addLayout(self.bottom_layout)
        self.setCentralWidget(central_widget)
        
        # Menu bar
        menuBar = self.menuBar()

        ## File menu
        fileMenu = menuBar.addMenu("&File")

        ### Save menu
        saveMenu = QAction("&Save", self)
        saveMenu.setShortcut("Ctrl+S")
        saveMenu.setStatusTip('Save')
        saveMenu.triggered.connect(self.onSave)
        fileMenu.addAction(saveMenu)

        ## Edit menu
        fileMenu = menuBar.addMenu("&Edit")

    def eventFilter(self, source, event):
        # Event filter for zooming without scrolling
        if (source == self.image_view.viewport()) and (event.type() == 31):
            x = event.angleDelta().y() / 120
            if x > 0:
                self.zoomOut()
            elif x < 0:
                self.zoomIn()
            return True
        return super().eventFilter(source, event)
    
    # Events

    def getText(self):
        # Make popup to get name
        text, OK = QInputDialog.getText(self,"Startup", "Your name: (no caps, no space, e.g. ryanwalker)")

        if OK:
            return text
        elif not OK:
            self.onEscape()

    def resizeEvent(self, event):
        '''
        Resize event; rescales image to fit in window, but keeps aspect ratio
        '''
        self.image_view.fitInView(self._pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        super().resizeEvent(event)

    def keyPressEvent(self,event):
        # Check if key is bound with marking the image
        markButtons = markBindingCheck(event)
        for i in range(0,9):
            if markButtons[i]: self.onMark(group=i)

        # Check if "Enter" was pressed
        if (event.key() == Qt.Key.Key_Return) or (event.key() == Qt.Key.Key_Enter):
            self.onEnter()

        if (event.key() == Qt.Key.Key_Escape) or (event.key() == Qt.Key.Key_Q):
            self.onEscape()

    def mousePressEvent(self,event):
        # Check if key is bound with marking the image
        markButtons = markBindingCheck(event)
        for i in range(0,9):
            if markButtons[i]: self.onMark(group=i)
        
        if (event.button() == Qt.MouseButton.MiddleButton):
            self.onMiddleMouse()

    # On-actions
    def onMark(self, group=0):
        '''
        Actions to complete when marking
        '''
        self.commentUpdate()
        # get event position and position on image
        ep, lp = self.mouseImagePos()
        
        # Mark if hovering over image  
        if self._pixmap_item is self.image_view.itemAt(ep):    
            x, y = lp.x(), self.pixmap.height() - lp.y()
            ra, dec = self.wcs.all_pix2world([[x, y]], 0)[0]

            self.drawCircle(lp.x(),lp.y(),c=self.colors[group])

            if not self.data[self.image_name][self.group_names[group]]['RA']:
                self.data[self.image_name][self.group_names[group]]['RA'] = []

            if not self.data[self.image_name][self.group_names[group]]['DEC']: 
                self.data[self.image_name][self.group_names[group]]['DEC'] = []

            self.data[self.image_name][self.group_names[group]]['RA'].append(ra)
            self.data[self.image_name][self.group_names[group]]['DEC'].append(dec)
            self.writeToTxt()

    def onNext(self):
        if self.idx+1 < self.N:
            # Increment the index
            self.idx += 1
            self.imageUpdate()
            self.redraw()
            self.commentUpdate()

    def onBack(self):
        if self.idx+1 > 1:
            # Increment the index
            self.idx -= 1
            self.imageUpdate()
            self.redraw()
            self.commentUpdate()

    def onEnter(self):
        self.commentUpdate()
        self.writeToTxt()
    
    def onEscape(self):
        self.writeToTxt()
        sys.exit()
    
    def onSave(self):
        pass

    def findImages(self):
        '''
        Finds and returns a list of images of self.imtype located at
            self.path.

        Returns:
            ims (list of strings): filenames
        '''
        images = glob.glob(self.images_path + '*.' + self.imtype)

        return images   
    
    def drawCircle(self,x,y,c=Qt.GlobalColor.black,r=10):
        ellipse = QGraphicsEllipseItem(x-r/2, y-r/2, r, r)
        ellipse.setPen(QPen(c, 1, Qt.PenStyle.SolidLine))
        self.image_scene.addItem(ellipse) 

    def imageUpdate(self):
        self.image_scene.clear()

        # Update idx label
        try: self.idx_label.setText(f'Image {self.idx+1} of {self.N}')
        except: 
            self.idx_label = QLabel(f'Image {self.idx+1} of {self.N}')
            self.idx_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Update the pixmap
        self.image = self.images[self.idx]
        self.image_name = self.image.split('/')[-1].split('.')[0]
        self.pixmap = QPixmap(self.image)
        self._pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.image_scene.addItem(self._pixmap_item)

        #Update WCS
        self.wcs = self.parseWCS(self.images[self.idx])
    
    def commentUpdate(self):
        # Update the comment in the dictionary
        comment = self.comment_box.text()
        if not comment: comment = 'None' # default comment to 'None'

        self.data[self.image_name]['comment'] = comment
        self.comment_box.setText('')

    def onMiddleMouse(self):
        # Center on cursor
        center = self.image_view.mapToScene(self.image_view.viewport().rect().center())
        view_pos, pix_pos = self.mouseImagePos()
        centerX = center.x()
        centerY = center.y()
        cursorX = pix_pos.x()
        cursorY = pix_pos.y()
        newX = int(centerX - cursorX)
        newY = int(centerY - cursorY)
        self.image_view.translate(newX, newY)

    def zoomIn(self):
        # Zoom in on cursor location
        view_pos, _ = self.mouseImagePos()
        transform = self.image_view.transform()
        center = self.image_view.mapToScene(view_pos)
        transform.translate(center.x(), center.y())
        transform.scale(1.2, 1.2)
        transform.translate(-center.x(), -center.y())
        self.image_view.setTransform(transform)

    def zoomOut(self):
        # Zoom out from cursor location
        view_pos, _ = self.mouseImagePos()
        transform = self.image_view.transform()
        center = self.image_view.mapToScene(view_pos)
        transform.translate(center.x(), center.y())
        transform.scale(1/1.2, 1/1.2)
        transform.translate(-center.x(), -center.y())
        self.image_view.setTransform(transform)

    def redraw(self):
        # Redraws circles if you go back or forward
        for i in range(0,9):
            RA_list = self.data[self.image_name][self.group_names[i]]['RA']
            DEC_list = self.data[self.image_name][self.group_names[i]]['DEC']

            if not RA_list or not DEC_list: pass  
            else:
                for j, _ in enumerate(RA_list):
   
                    x,y = self.wcs.all_world2pix([[RA_list[j], DEC_list[j]]], 0)[0]

                    y += self.pixmap.height() - 2*y

                    self.drawCircle(x,y,c=self.colors[i])
    
    def mouseImagePos(self):
        '''
        Gets mouse positions

        Returns:
            view_pos: position of mouse in image_view
            pix_pos: position of mouse in the pixmap
        '''
        view_pos = self.image_view.mapFromGlobal(QCursor.pos())
        scene_pos = self.image_view.mapToScene(view_pos)
        pix_pos = self._pixmap_item.mapFromScene(scene_pos).toPoint()

        return view_pos, pix_pos
    
    def parseWCS(self,image_tif):
        #tif_image_data = np.array(Image.open(image_tif))
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
        #shape = (meta_dict['ImageWidth'][0], meta_dict['ImageLength'][0])
        return wcs

    def checkUsername(self):
        if ((self.username != "None") and (self.username != "")):
            usernameExists = True
        else:
            usernameExists = False
        return usernameExists
    
    def writeToTxt(self):
        if self.checkUsername() and self.data:
            path_existed = os.path.exists(self.outfile)
            if path_existed and self.overwrite:
                os.remove(self.outfile)
            out = open(self.outfile,"a")

            lines = []
            name_lengths = []
            group_lengths = []
            ra_lengths = []
            dec_lengths = []
            comment_lengths = []

            for name in self.data:
                for level2 in self.data[name]:
                    if level2 == 'comment': pass
                    else: 
                        group = level2
                        comment = self.data[name]['comment']

                        RA_list = self.data[name][group]['RA']
                        DEC_list = self.data[name][group]['DEC']
                        for i, _ in enumerate(RA_list):
                            ra = RA_list[i]
                            dec = DEC_list[i]
                            l = [name,group,ra,dec,comment]

                            lines.append(l)
                            name_lengths.append(len(name))
                            group_lengths.append(len(group))
                            ra_lengths.append(len(f'{ra:.8f}'))
                            dec_lengths.append(len(f'{dec:.8f}'))
                            comment_lengths.append(len(comment))

            # Dynamically adjust column widths
            nameln = np.max(name_lengths) + 2
            groupln = max(np.max(group_lengths), 5) + 2
            raln = max(np.max(ra_lengths), 2) + 2
            decln = max(np.max(dec_lengths), 2) + 2
            commentln = max(np.max(comment_lengths), 7) + 2

            if not path_existed: out.write(f'{'name':^{nameln}}|{'group':^{groupln}}|{'RA':^{raln}}|{'DEC':^{decln}}|{'comment':^{commentln}}\n')

            for l in lines:
                outline = f'{l[0]:^{nameln}}|{l[1]:^{groupln}}|{l[2]:^{raln}.8f}|{l[3]:^{decln}.8f}|{l[4]:^{commentln}}\n'
                out.write(outline)

    def readConfig(self):
        for l in open(self.config):
            var, val = l.replace(' ','').split('=')
            if var == 'groups':
                self.group_names = val.split(',')
            if var == 'out_path':
                if var == './':
                    self.out_path = os.getcwd()
                else:
                    self.out_path = var
                if self.out_path[-1] != '/':
                    self.out_path = self.out_path + '/'
            if var == 'images_path':
                if val == './':
                    self.images_path = os.getcwd()
                else:
                    self.images_path = val
                if self.images_path[-1] != '/':
                    self.images_path = self.images_path + '/'


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__': main()