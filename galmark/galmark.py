from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsEllipseItem, QLineEdit, QMenuBar, QInputDialog, QCheckBox
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
import platform
import sys
from PIL.TiffTags import TAGS
from astropy.wcs import WCS
from astropy.io import fits
from collections import defaultdict
import datetime as dt

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
    def __init__(self, path = '', imtype = 'tif', parent=None):
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

        if platform.system() == 'Windows': self._delim = '\\'
        else: self._delim = '/'

        # Initialize config
        self.config = 'galmark.cfg'
        self.readConfig()

        # Initialize images and WCS
        self.imtype = imtype
        self.idx = 0
        self.images = glob.glob(self.images_path + '*.' + self.imtype)
        self.N = len(self.images)

        self.image = self.images[self.idx]
        self.image_name = self.image.replace('\\','/').split('/')[-1].split('.')[0]
        self.wcs = self.parseWCS(self.image)

        # Initialize output dictionary
        self.data = DataDict()
        self.colors = [QColor(255,0,0),QColor(255,128,0),QColor(255,255,0),
                  QColor(0,255,0),QColor(0,255,255),QColor(0,128,128),
                  QColor(0,0,255),QColor(128,0,255),QColor(255,0,255)]
        
        # Intiialize user
        self.username = ""
        self.username = self.getText()
        self.outfile = self.username + ".txt"
        self.date = dt.datetime.now(dt.UTC).date().isoformat()
        self.comment = 'None'

        # Useful attributes
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.windowsize = QSize(int(self.fullw/2), int(self.fullh/2))
        self._go_back_one = False
        self.setWindowTitle("Galaxy Marker")

        # Current index widget
        self.idx_label = QLabel(f'Image {self.idx+1} of {self.N}')
        self.idx_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Current image name widget
        self.image_label = QLabel(f'{self.image_name}')
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Create image view
        self.image_scene = QGraphicsScene(self)
        self.pixmap = QPixmap(self.image)
        self._pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.image_scene.addItem(self._pixmap_item)
        self.image_view = QGraphicsView(self.image_scene)       
        self.image_view.verticalScrollBar().blockSignals(True)
        self.image_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.image_view.horizontalScrollBar().blockSignals(True)
        self.image_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.image_view.move(0, 0)
        self.image_view.setTransformationAnchor(self.image_view.ViewportAnchor(1))
        self.image_view.viewport().installEventFilter(self)

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
        self.commentUpdate(False)
    
        # Botton Bar layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.back_button)
        self.bottom_layout.addWidget(self.next_button)
        self.bottom_layout.addWidget(self.comment_box)
        self.bottom_layout.addWidget(self.submit_button)
        
        ### Problem widgets

        # Not centered on cluster
        self.problem_one_box = QCheckBox(text='Not Centered on Cluster', parent=self)
        self.problem_one_box.setFixedHeight(40)
        self.problem_one_box.clicked.connect(self.onProblemOne)

        # Bad image scaling
        self.problem_two_box = QCheckBox(text='Bad Image Scaling', parent=self)
        self.problem_two_box.setFixedHeight(40)
        self.problem_two_box.clicked.connect(self.onProblemTwo)

        # No cluster visible
        self.problem_three_box = QCheckBox(text='No Cluster Visible', parent=self)
        self.problem_three_box.setFixedHeight(40)
        self.problem_three_box.clicked.connect(self.onProblemThree)

        # High redshift/too red
        self.problem_four_box = QCheckBox(text='High Redshift Cluster', parent=self)
        self.problem_four_box.setFixedHeight(40)
        self.problem_four_box.clicked.connect(self.onProblemFour)

        # Other/leave comment prompt?
        self.problem_other_box = QCheckBox(text='Other', parent=self)
        self.problem_other_box.setFixedHeight(40)
        self.problem_other_box.clicked.connect(self.onProblemOther)

        self.problemUpdate()

        # Problems layout
        self.problems_layout = QHBoxLayout()
        self.problems_layout.addWidget(self.problem_one_box)
        self.problems_layout.addWidget(self.problem_two_box)
        self.problems_layout.addWidget(self.problem_three_box)
        self.problems_layout.addWidget(self.problem_four_box)
        self.problems_layout.addWidget(self.problem_other_box)

        # Add widgets to main layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.image_label)
        layout.addWidget(self.image_view)
        layout.addWidget(self.idx_label)
        layout.addLayout(self.bottom_layout)
        layout.addLayout(self.problems_layout)
        self.setCentralWidget(central_widget)
        
        # Menu bar
        menuBar = self.menuBar()

        ## File menu
        fileMenu = menuBar.addMenu("&File")

        ### Exit menu
        exitMenu = QAction('&Exit', self)
        exitMenu.setShortcuts(['Esc','q'])
        exitMenu.setStatusTip('Exit')
        exitMenu.triggered.connect(self.onExit)
        fileMenu.addAction(exitMenu)

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
    
    # === Events ===

    def getText(self):
        # Make popup to get name
        text, OK = QInputDialog.getText(self,"Startup", "Your name: (no caps, no space, e.g. ryanwalker)")

        if OK: return text
        else: self.onExit()

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
            if markButtons[i]: self.onMark(group=i+1)

        # Check if "Enter" was pressed
        if (event.key() == Qt.Key.Key_Return) or (event.key() == Qt.Key.Key_Enter):
            self.onEnter()

    def mousePressEvent(self,event):
        # Check if key is bound with marking the image
        markButtons = markBindingCheck(event)
        for i in range(0,9):
            if markButtons[i]: self.onMark(group=i+1)
        
        if (event.button() == Qt.MouseButton.MiddleButton):
            self.onMiddleMouse()

    # === On-actions ===
    def onProblemOne(self):
        if (self.problem_one_box.checkState().value == 2):
            self.data[self.image_name]['problem'] = 1
            for i in range(1,10):
                try: del self.data[self.image_name][i]
                except: pass
        else:
            self.data[self.image_name]['problem'] = 0
        self.writeToTxt()
        self.problem_two_box.setChecked(False)
        self.problem_three_box.setChecked(False)
        self.problem_four_box.setChecked(False)
        self.problem_other_box.setChecked(False)
        self.imageUpdate()

    def onProblemTwo(self):
        if (self.problem_two_box.checkState().value == 2):
            self.data[self.image_name]['problem'] = 2
            for i in range(1,10):
                try: del self.data[self.image_name][i]
                except: pass
        else:
            self.data[self.image_name]['problem'] = 0
        self.writeToTxt()
        self.problem_one_box.setChecked(False)
        self.problem_three_box.setChecked(False)
        self.problem_four_box.setChecked(False)
        self.problem_other_box.setChecked(False)
        self.imageUpdate()

    def onProblemThree(self):
        if (self.problem_three_box.checkState().value == 2):
            self.data[self.image_name]['problem'] = 3
            for i in range(1,10):
                try: del self.data[self.image_name][i]
                except: pass
        else:
            self.data[self.image_name]['problem'] = 0
        self.writeToTxt()
        self.problem_one_box.setChecked(False)
        self.problem_two_box.setChecked(False)
        self.problem_four_box.setChecked(False)
        self.problem_other_box.setChecked(False)
        self.imageUpdate()

    def onProblemFour(self):
        if (self.problem_four_box.checkState().value == 2):
            self.data[self.image_name]['problem'] = 4
            for i in range(1,10):
                try: del self.data[self.image_name][i]
                except: pass
        else:
            self.data[self.image_name]['problem'] = 0
        self.writeToTxt()
        self.problem_one_box.setChecked(False)
        self.problem_two_box.setChecked(False)
        self.problem_three_box.setChecked(False)
        self.problem_other_box.setChecked(False)
        self.imageUpdate()

    def onProblemOther(self):
        if (self.problem_other_box.checkState().value == 2):
            self.data[self.image_name]['problem'] = 5
            for i in range(1,10):
                try: del self.data[self.image_name][i]
                except: pass
        else:
            self.data[self.image_name]['problem'] = 0
        self.writeToTxt()
        self.problem_one_box.setChecked(False)
        self.problem_two_box.setChecked(False)
        self.problem_three_box.setChecked(False)
        self.problem_four_box.setChecked(False)
        self.imageUpdate()

    def onMark(self, group=0):
        '''
        Actions to complete when marking
        '''

        # get event position and position on image
        ep, lp = self.mouseImagePos()
        
        # Mark if hovering over image  
        if self._pixmap_item is self.image_view.itemAt(ep):    
            x, y = lp.x(), self.pixmap.height() - lp.y()
            ra, dec = self.wcs.all_pix2world([[x, y]], 0)[0]

            self.drawCircle(lp.x(),lp.y(),c=self.colors[group-1])

            if not self.data[self.image_name][group]['RA']:
                self.data[self.image_name][group]['RA'] = []

            if not self.data[self.image_name][group]['DEC']: 
                self.data[self.image_name][group]['DEC'] = []

            self.data[self.image_name][group]['RA'].append(ra)
            self.data[self.image_name][group]['DEC'].append(dec)
            self.writeToTxt()

    def onNext(self):
        if self.idx+1 < self.N:
            # Increment the index
            self.idx += 1
            self.commentUpdate(True)
            self.imageUpdate()
            self.redraw()
            self.commentUpdate(False)
            self.problemUpdate()
            # self.writeToTxt()

    def onBack(self):
        if self.idx+1 > 1:
            # Increment the index
            self.idx -= 1
            self.commentUpdate(True)
            self.imageUpdate()
            self.redraw()
            self.commentUpdate(False)
            self.problemUpdate()
            # self.writeToTxt()
            
    def onEnter(self):
        self.commentUpdate(True)
        self.writeToTxt()
    
    def onExit(self):
        sys.exit()

    def onMiddleMouse(self):
        # Center on cursor
        center = self.image_view.mapToScene(self.image_view.viewport().rect().center())
        _, pix_pos = self.mouseImagePos()
        centerX = center.x()
        centerY = center.y()
        cursorX = pix_pos.x()
        cursorY = pix_pos.y()
        newX = int(centerX - cursorX)
        newY = int(centerY - cursorY)
        self.image_view.translate(newX, newY)

    # === Update methods ===

    def imageUpdate(self):
        self.image_scene.clear()   

        # Update the pixmap
        self.image = self.images[self.idx]
        self.image_name = self.image.replace('\\','/').split('/')[-1].split('.')[0]
        self.pixmap = QPixmap(self.image)
        self._pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.image_scene.addItem(self._pixmap_item)

        # Update idx label
        self.idx_label.setText(f'Image {self.idx+1} of {self.N}')

        # Update image label
        self.image_label.setText(f'{self.image_name}')

        #Update WCS
        self.wcs = self.parseWCS(self.image)
    
    def commentUpdate(self, beforeImageUpdate):
        # Update the comment in the dictionary
        if beforeImageUpdate:
            comment = self.comment_box.text()
            if not comment:
                comment = 'None'

            self.data[self.image_name]['comment'] = comment
            self.writeToTxt()
        else:
            if bool(self.data[self.image_name]['comment']):
                if (self.data[self.image_name]['comment'] == 'None'):
                    self.comment_box.setText('')
                else:
                    comment = self.data[self.image_name]['comment']
                    self.comment_box.setText(comment)
            else:
                comment = 'None'
                self.data[self.image_name]['comment'] = comment
                self.comment_box.setText('')

    def problemUpdate(self):
        # Initialize problem and update checkboxes
        self.problem_one_box.setChecked(False)
        self.problem_two_box.setChecked(False)
        self.problem_three_box.setChecked(False)
        self.problem_four_box.setChecked(False)
        self.problem_other_box.setChecked(False)
        if not (self.data[self.image_name]['problem']):
            self.data[self.image_name]['problem'] = 0
        else:
            problem = self.data[self.image_name]['problem']
            if (problem == 1):
                self.problem_one_box.setChecked(True)
            if (problem == 2):
                self.problem_two_box.setChecked(True)
            if (problem == 3):
                self.problem_three_box.setChecked(True)
            if (problem == 4):
                self.problem_four_box.setChecked(True)
            if (problem == 5):
                self.problem_other_box.setChecked(True)

    def redraw(self):
        # Redraws circles if you go back or forward
        for i in range(0,9):
            RA_list = self.data[self.image_name][i+1]['RA']
            DEC_list = self.data[self.image_name][i+1]['DEC']

            if not RA_list or not DEC_list: pass
            else:
                for j, _ in enumerate(RA_list):
   
                    x,y = self.wcs.all_world2pix([[RA_list[j], DEC_list[j]]], 0)[0]

                    y += self.pixmap.height() - 2*y

                    self.drawCircle(x,y,c=self.colors[i])

    # === Interactions ===
    
    def drawCircle(self,x,y,c=Qt.GlobalColor.black,r=10):
        ellipse = QGraphicsEllipseItem(x-r/2, y-r/2, r, r)
        ellipse.setPen(QPen(c, 1, Qt.PenStyle.SolidLine))
        self.image_scene.addItem(ellipse) 

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

    # === Utils ===
    
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
        return wcs

    def checkUsername(self):
        return (self.username != "None") and (self.username != "")
    
    # === I/O ===

    def writeToTxt(self):
        if self.checkUsername() and self.data:
            
            if os.path.exists(self.outfile): os.remove(self.outfile)

            out = open(self.outfile,"a")

            lines = []
            name_lengths = []
            group_lengths = []
            ra_lengths = []
            dec_lengths = []
            problem_lengths = []
            comment_lengths = []

            for name in self.data:
                comment = self.data[name]['comment']
                problem = self.problem_names[self.data[name]['problem']]

                # Get list of groups containing data
                keys = [key for key in self.data[name]]
                groups = [g for g in keys if isinstance(g,int) 
                          and self.data[name][g]['RA'] 
                          and self.data[name][g]['DEC']]

                # If there are no image problems, and there is data in groups, then add this data to lines
                if (problem == 'None') and (len(groups) != 0):
                    for g in groups:
                        group_name = self.group_names[g-1]
                        RA_list = self.data[name][g]['RA']
                        DEC_list = self.data[name][g]['DEC']

                        for i, _ in enumerate(RA_list):
                            ra = RA_list[i]
                            dec = DEC_list[i]
                            l = [self.date,name,group_name,ra,dec,problem,comment]

                            lines.append(l)
                            name_lengths.append(len(name))
                            group_lengths.append(len(group_name))
                            ra_lengths.append(len(f'{ra:.8f}'))
                            dec_lengths.append(len(f'{dec:.8f}'))
                            problem_lengths.append(len(problem))
                            comment_lengths.append(len(comment))
                
                # Otherwise (i.e., there is an image problem, or there is no data in groups) delete any data, replace with NaNs
                else:
                    group_name = 'None'
                    ra = 'NaN'
                    dec = 'NaN'
                    l = [self.date,name,group_name,ra,dec,problem,comment]

                    lines.append(l)
                    name_lengths.append(len(name))
                    group_lengths.append(len(group_name))
                    ra_lengths.append(len(ra))
                    dec_lengths.append(len(dec))
                    problem_lengths.append(len(problem))
                    comment_lengths.append(len(comment))

            # Dynamically adjust column widths
            nameln = np.max(name_lengths) + 2
            groupln = max(np.max(group_lengths), 5) + 2
            raln = max(np.max(ra_lengths), 2) + 2
            decln = max(np.max(dec_lengths), 2) + 2
            problemln = max(np.max(problem_lengths), 9) + 2
            commentln = max(np.max(comment_lengths), 7) + 2
            dateln = 12

            out.write(f'{'date':^{dateln}}|{'name':^{nameln}}|{'group':^{groupln}}|{'RA':^{raln}}|{'DEC':^{decln}}|{'problem':^{problemln}}|{'comment':^{commentln}}\n')

            for l in lines:
                try: outline = f'{l[0]:^{dateln}}|{l[1]:^{nameln}}|{l[2]:^{groupln}}|{l[3]:^{raln}.8f}|{l[4]:^{decln}.8f}|{l[5]:^{problemln}}|{l[6]:^{commentln}}\n'
                except: outline = f'{l[0]:^{dateln}}|{l[1]:^{nameln}}|{l[2]:^{groupln}}|{l[3]:^{raln}}|{l[4]:^{decln}}|{l[5]:^{problemln}}|{l[6]:^{commentln}}\n'
                out.write(outline)

    def readConfig(self):
        '''
        Read each line from the config and parse it
        '''
        

        # If the config doesn't exist, create one
        if not os.path.exists(self.config):
            config_file = open(self.config,'w')
            self.group_names = ['1','2','3','4','5','6','7','8','9']
            self.out_path = os.path.join(os.getcwd(),'')
            self.images_path = os.path.join(os.getcwd(),'')
            self.problem_names = ['None','not_centered','bad_scaling','no_cluster','high_redshift','other']

            config_file.write('groups = 1,2,3,4,5,6,7,8,9\n')
            config_file.write(f'out_path = {self.out_path}\n')
            config_file.write(f'images_path = {self.images_path}\n')
            config_file.write(f'problem_names = {self.problem_names[0]},{self.problem_names[1]},{self.problem_names[2]},{self.problem_names[3]},{self.problem_names[4]},{self.problem_names[5]}')


        else:
            for l in open(self.config):
                var, val = l.replace(' ','').replace('\n','').split('=')

                if var == 'groups':
                    self.group_names = val.split(',')

                if var == 'out_path':
                    if var == './': self.out_path = os.getcwd()
                    else: self.out_path = var
                    os.path.join(self.out_path,'')

                if var == 'images_path':
                    if val == './': self.images_path = os.getcwd()
                    else: self.images_path = val
                    self.images_path =  os.path.join(self.images_path,'')

                if var == 'problem_names':
                    self.problem_names = val.split(',')
                    self.problem_names.insert(0, 'None')
            
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__': main()

