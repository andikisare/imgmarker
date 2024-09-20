from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QHBoxLayout, QGraphicsEllipseItem, QLineEdit, QMenuBar, QInputDialog, QCheckBox, QTextEdit
from PyQt6.QtGui import QPixmap, QPen, QCursor, QColor, QAction, QIcon
from PyQt6.QtCore import Qt, QSize, QPoint
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

__dirname__ = os.path.dirname(os.path.realpath(__file__))
__icon__ = os.path.join(__dirname__,'icon.png')
COLORS = [ QColor(0,0,0), QColor(255,0,0),QColor(255,128,0),QColor(255,255,0),
           QColor(0,255,0),QColor(0,255,255),QColor(0,128,128),
           QColor(0,0,255),QColor(128,0,255),QColor(255,0,255) ]

class DataDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(DataDict, self).__init__(DataDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))

class Region(QGraphicsEllipseItem):
    def __init__(self,parent,x:int,y:int,r:int=5,wcs:WCS=None,group:int=0):
        super(Region, self).__init__(x-r,y-r,2*r,2*r)

        self.r = r
        self.wcs = wcs
        self.g = group
        self.c = COLORS[self.g]
        self.parent = parent
        
    def center(self):
        return QPoint(self.x()+self.r,self.y()+self.r)
    
    def x(self):
        return int(self.rect().x())
    
    def y(self):
        return int(self.rect().y())
    
    def centerWCS(self):
        if self.wcs != None:
            _x, _y = self.center().x(), self.wcs._naxis[0] - self.center().y()
            return self.wcs.all_pix2world([[_x, _y]], 0)[0]
        else: raise NameError('No WCS solution provided')

    def draw(self):
        self.setPen(QPen(self.c, 1, Qt.PenStyle.SolidLine))
        self.parent.image_scene.addItem(self)
    
    def setCenter(self,x:int,y:int):
        self.setPos(x-self.r,y-self.r)

    def setWCS(self,wcs:WCS):
        self.wcs = wcs

    def remove(self):
        self.parent.image_scene.removeItem(self)
        self.parent.data[self.parent.image_name][self.g]['Regions'].remove(self)

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

def parseWCS(image_tif):
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


class HelpWindow(QWidget):
    """
    This window displays the instructions and keymappings
    """
    def __init__(self,groupNames):
        super().__init__()
        self.setWindowIcon(QIcon(__icon__))
        layout = QVBoxLayout()
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.resize(int(self.fullw/5), int(self.fullh/3))
        self.setWindowTitle('Instructions and Keymapping')
        self.setLayout(layout)

        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(-qt_rectangle.topLeft().x() + self.fullw, qt_rectangle.topLeft().y())

        self.help_text = QTextEdit()
        
        self.help_text.setPlainText(f'ALL data is saved when pressing "Next," "Back," or "Enter" in the window,\n'
                                                      f'as well as checking a problem, exiting, or making a mark.\n\n'
                                                      f'Action                                                     Button\n'
                                                      f'Group {groupNames[0]:<50} Left click OR 1\n'
                                                      f'Group {groupNames[1]:<50} Right click OR 2\n' 
                                                      f'Group {groupNames[2]:<50} 3\n'
                                                      f'Group {groupNames[3]:<50} 4\n'
                                                      f'Group {groupNames[4]:<50} 5\n'
                                                      f'Group {groupNames[5]:<50} 6\n'
                                                      f'Group {groupNames[6]:<50} 7\n'
                                                      f'Group {groupNames[7]:<50} 8\n'
                                                      f'Group {groupNames[8]:<50} 9\n\n'
                                                      f'Save                                                       Enter\n'
                                                      f'Pan                                                         Middle click\n'
                                                      f'Zoom in/out                                         Scroll wheel\n'
                                                      f'Save and close                                     Escape OR Q\n'
                                                      f'Open help window (this window)     F1\n\n'
                                                      f'To delete a mark, right click.'
        )
        self.help_text.setReadOnly(True)
        layout.addWidget(self.help_text)

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
        self.setWindowIcon(QIcon(__icon__))

        # Initialize config
        self.config = 'galmark.cfg'
        self.readConfig()

        # Initialize images and WCS
        self.imtype = imtype
        self.idx = 0
        self.images = glob.glob(self.images_path + '*.' + self.imtype)
        self.N = len(self.images)

        self.image = self.images[self.idx]
        self.image_name = self.image.split(os.sep)[-1].split('.')[0]
        self.wcs = parseWCS(self.image)

        # Initialize output dictionary
        self.data = DataDict()
        
        
        # Intiialize user
        self.username = ""
        self.username = self.getText()
        self.outfile = os.path.join(self.out_path, self.username + '.txt')
        self.date = dt.datetime.now(dt.UTC).date().isoformat()
        self.comment = 'None'

        # Useful attributes
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.windowsize = QSize(int(self.fullw/2), int(self.fullh/2))
        self._go_back_one = False
        self.setWindowTitle("Galaxy Marker")

        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

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
        self.getComment()
    
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
        exitMenu.triggered.connect(self.closeEvent)
        fileMenu.addAction(exitMenu)

        ## Edit menu
        fileMenu = menuBar.addMenu("&Edit")

        ## Help menu
        helpMenu = menuBar.addMenu('&Help')

        ### Instructions and Keymapping window
        instructionsMenu = QAction('&Instructions and Keymapping', self)
        instructionsMenu.setShortcuts(['F1'])
        instructionsMenu.setStatusTip('Instructions')
        instructionsMenu.triggered.connect(self.showInstructions)
        helpMenu.addAction(instructionsMenu)

        self.showInstructions()

    def showInstructions(self):
        self.helpWindow = HelpWindow(self.group_names)
        self.helpWindow.show()

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
        else: self.closeEvent()

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

        # if (event.key() == Qt.Key.Key_Right)

    def mousePressEvent(self,event):
        # Check if key is bound with marking the image
        markButtons = markBindingCheck(event)
        for i in range(0,9):
            if markButtons[i]: self.onMark(group=i+1)
        
        if (event.button() == Qt.MouseButton.MiddleButton):
            self.onMiddleMouse()

        if (event.button() == Qt.MouseButton.RightButton):
            self.getSelectedRegions()

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

            region = Region(self,lp.x(),lp.y(),wcs=self.wcs,group=group)
            region.draw()

            if not self.data[self.image_name][group]['Regions']:
                self.data[self.image_name][group]['Regions'] = []

            self.data[self.image_name][group]['Regions'].append(region)
            self.writeToTxt()

    def onNext(self):
        if self.idx+1 < self.N:
            # Increment the index
            self.idx += 1
            self.commentUpdate()
            self.imageUpdate()
            self.regionUpdate()
            self.getComment()
            self.problemUpdate()
            # self.writeToTxt()

    def onBack(self):
        if self.idx+1 > 1:
            # Increment the index
            self.idx -= 1
            self.commentUpdate()
            self.imageUpdate()
            self.regionUpdate()
            self.getComment()
            self.problemUpdate()
            # self.writeToTxt()
            
    def onEnter(self):
        self.commentUpdate()
        self.writeToTxt()
    
    def closeEvent(self, event):
        self.commentUpdate()
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
        for item in self.image_scene.items(): self.image_scene.removeItem(item)

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
        self.wcs = parseWCS(self.image)
    
    def commentUpdate(self):
        # Update the comment in the dictionary
        comment = self.comment_box.text()
        if not comment:
            comment = 'None'

        self.data[self.image_name]['comment'] = comment
        self.writeToTxt()

    def getComment(self):
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

    def regionUpdate(self):
        # Redraws all regions in image
        for i in range(0,10):
            region_list = self.data[self.image_name][i]['Regions']

            if bool(region_list):
                for region in region_list: region.draw()

    def getSelectedRegions(self):
        _, pix_pos = self.mouseImagePos()
        pix_pos = pix_pos.toPointF()
        selection_filt = [ item is self.image_scene.itemAt(pix_pos, item.transform()) 
                           for item in self.image_scene.items() 
                           if isinstance(item,Region) ]
        selected_items = [ item for item in self.image_scene.items() 
                           if isinstance(item,Region) 
                           and (item is self.image_scene.itemAt(pix_pos, item.transform()))]
        
        for item in selected_items:
            item.remove()
            self.writeToTxt()


    # === Transformations ===
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
    
    

    def checkUsername(self):
        return (self.username != "None") and (self.username != "")
    
    # === I/O ===

    def writeToTxt(self):
        lines = []
        name_lengths = []
        group_lengths = []
        ra_lengths = []
        dec_lengths = []
        problem_lengths = []
        comment_lengths = []

        # Create the file
        if os.path.exists(self.outfile): 
            os.remove(self.outfile)
        out = open(self.outfile,"a")
        
        if self.checkUsername() and self.data:
            names = list(self.data.keys())

            for name in names:
                comment = self.data[name]['comment']
                problem = self.problem_names[self.data[name]['problem']]

                # Get list of groups containing data
                level2_keys = list(self.data[name].keys())
                groups = [ key for key in level2_keys if isinstance(key,int) 
                          and self.data[name][key]['Regions'] ]

                # If there are no image problems, and there is data in groups, then add this data to lines
                if (problem == 'None') and (len(groups) != 0):
                    for group in groups:
                        group_name = self.group_names[group]
                        region_list = self.data[name][group]['Regions']

                        for region in region_list:
                            ra, dec = region.centerWCS()
                            l = [self.date,name,group_name,ra,dec,problem,comment]

                            lines.append(l)
                            name_lengths.append(len(name))
                            group_lengths.append(len(group_name))
                            ra_lengths.append(len(f'{ra:.8f}'))
                            dec_lengths.append(len(f'{dec:.8f}'))
                            problem_lengths.append(len(problem))
                            comment_lengths.append(len(comment))
                
                # Otherwise, if there is a problem or a comment, replace ra/dec with NaNs
                elif (problem != 'None') or (comment != 'None'):
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
                
                # Otherwise, (no comment, no problem, and no data) delete entry from dictionary
                else: pass

        # Print out lines if there are lines to print
        if len(lines) != 0:
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
            config_file.write(f'problems = {self.problem_names[1]},{self.problem_names[2]},{self.problem_names[3]},{self.problem_names[4]},{self.problem_names[5]}')


        else:
            for l in open(self.config):
                var, val = l.replace(' ','').replace('\n','').split('=')

                if var == 'groups':
                    self.group_names = val.split(',')
                    self.group_names.insert(0, 'None')

                if var == 'out_path':
                    if var == './': self.out_path = os.getcwd()
                    else: self.out_path = val
                    os.path.join(self.out_path,'')

                if var == 'images_path':
                    if val == './': self.images_path = os.getcwd()
                    else: self.images_path = val
                    self.images_path =  os.path.join(self.images_path,'')

                if var == 'problems':
                    self.problem_names = val.split(',')
                    self.problem_names.insert(0, 'None')


            
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__': main()

