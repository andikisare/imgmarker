from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QScrollArea, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, QSlider
from PyQt6.QtGui import QPixmap, QCursor, QAction, QIcon, QFont, QImage
from PyQt6.QtCore import Qt
from galmark.mark import Mark
from galmark import __dirname__, __icon__ 
import galmark.io
import sys
import os
import datetime as dt
import textwrap
from math import ceil
import cv2

class AdjustmentsWindow(QWidget):
    """
    Blur window
    """
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon(__icon__))
        layout = QVBoxLayout()
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.setWindowTitle('Brightness and Contrast')
        self.setLayout(layout)
        
        # Set position of window
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(-qt_rectangle.topLeft().x() + self.fullw, qt_rectangle.topLeft().y())

        # Brightness slider
        self.brightnessSlider = QSlider()
        self.brightnessSlider.setMinimum(-100)
        self.brightnessSlider.setMaximum(100)
        self.brightnessSlider.setValue(0)
        self.brightnessSlider.setOrientation(Qt.Orientation.Horizontal)

        # Contrast slider
        self.contrastSlider = QSlider()
        self.contrastSlider.setMinimum(-100)
        self.contrastSlider.setMaximum(100)
        self.contrastSlider.setValue(0)
        self.contrastSlider.setOrientation(Qt.Orientation.Horizontal)

        layout.addWidget(self.brightnessSlider)
        layout.addWidget(self.contrastSlider)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

class BlurWindow(QWidget):
    """
    Blur window
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(QIcon(__icon__))
        layout = QVBoxLayout()
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.setWindowTitle('Gaussian Blur')
        self.setLayout(layout)
        
        
        # Set position of window
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(-qt_rectangle.topLeft().x() + self.fullw, qt_rectangle.topLeft().y())

        max_blur = int((self.fullw+self.fullh)/20)
        self.slider = QSlider()
        self.slider.setMinimum(1)
        self.slider.setTickInterval(2)
        self.slider.setSingleStep(2)
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.sliderMoved.connect(self.onSliderMoved) 

        self.valueLabel = QLabel()
        self.valueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.valueLabel.setText(f'Radius: {self.slider.value()}')

        layout.addWidget(self.valueLabel)
        layout.addWidget(self.slider)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedWidth(int(self.fullw/6))
        self.setFixedHeight(layout.sizeHint().height())
        
    def onSliderMoved(self, pos):
        self.slider.setValue(ceil(pos) // 2 * 2 + 1)
        self.valueLabel.setText(f'Radius: {self.slider.value()}')

class InstructionsWindow(QWidget):
    """
    This window displays the instructions and keymappings
    """
    def __init__(self,groupNames):
        super().__init__()
        self.setWindowIcon(QIcon(__icon__))
        layout = QVBoxLayout()
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.setWindowTitle('Instructions')
        self.setLayout(layout)
        
        # Set position of window
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(-qt_rectangle.topLeft().x() + self.fullw, qt_rectangle.topLeft().y())

        # Create the scroll area and label
        self.scroll_area = QScrollArea()
        self.label = QLabel()
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setWidgetResizable(True)
        font = QFont('Courier')
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        # Lists for keybindings
        actions_list = ['Delete','Enter comment', 'Focus', 'Zoom in/out', 'Exit', 'Help']
        group_list = [f'Group \"{group}\"' for group in groupNames[1:]]
        actions_list = group_list + actions_list
        buttons_list = ['Left click OR 1', '2', '3', '4', '5', '6', '7', '8', '9', 'Right click', 'Enter', 'Middle click', 'Scroll wheel', 'Esc OR Q', 'F1', ]

        # Determing widths for keybindings list
        actions_width = max([len(a) for a in actions_list])
        buttons_width = max([len(b) for b in buttons_list]) + 10
        fullw_text = actions_width + buttons_width

        # Create text
        text = 'ALL data is saved when pressing "Next," "Back," or "Enter" in the window, as well as checking a category, exiting, or making a mark.'
        text = textwrap.wrap(text, width=fullw_text)
        text = '\n'.join([f'{l:<{fullw_text}}' for l in text]) + '\n'
        text += '-'*(fullw_text) + '\n'
        text += f'{'Keybindings':^{fullw_text}}\n'
        text += '-'*(fullw_text) + '\n'
        for i in range(0,len(actions_list)):
            text += f'{actions_list[i]:.<{actions_width}}{buttons_list[i]:.>{buttons_width}}\n'
        self.label.setText(text)
        text.removesuffix('\n')

        # Add scroll area to layout, get size of layout
        layout.addWidget(self.scroll_area)
        layout_width, layout_height = layout.sizeHint().width(), layout.sizeHint().height()

        # Resize window according to size of layout
        self.resize(int(layout_width*1.1),int(layout_height*1.1))

class StartupWindow(QInputDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(__icon__))

    def getUser(self):
        # Make popup to get name
        text, OK = self.getText(self,"Startup", "Enter a username (no caps, no space, e.g. ryanwalker)")

        if OK: return text
        else: sys.exit()

class MainWindow(QMainWindow):
    def __init__(self, username, out_path, images_path, group_names, category_names, group_max, imtype = 'tif'):
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
        self.setWindowTitle("Galaxy Marker")
        self.setWindowIcon(QIcon(__icon__))

        # Filter windows
        self.blurWindow = BlurWindow()
        self.blurWindow.slider.valueChanged.connect(self.onBlur)
        self.adjustmentsWindow = AdjustmentsWindow()

        # Initialize config
        self.config = 'galmark.cfg'
        self.username, self.group_names, self.category_names, self.group_max = username, group_names, category_names, group_max
        self.date = dt.datetime.now(dt.UTC).date().isoformat()

        # Initialize output dictionary
        self.data = galmark.io.load(username)

        # Find all images in image directory
        self.imtype = imtype
        self.images, self.idx = galmark.io.glob(images_path,self.imtype,data_filt=self.data)
        self.N = len(self.images)

        try: self.image = self.images[self.idx]
        except:
            print('No images found. Please specify image directory in configuration file (galmark.cfg) and try again.')
            sys.exit()

        self.matimage = cv2.imread(self.image)
        self.qimage = QImage(self.matimage.data, self.matimage.shape[1], self.matimage.shape[0], QImage.Format.Format_RGB888).rgbSwapped()

        # Set max blur based on size of image
        blur_max = ceil((self.qimage.height()+self.qimage.width())/20)// 2 * 2 + 1
        self.blurWindow.slider.setMaximum(blur_max)

        self.image_file = self.image.split(os.sep)[-1]
        self.wcs = galmark.io.parseWCS(self.image)

        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Current image widget
        self.image_label = QLabel(f'{self.image_file} ({self.idx+1} of {self.N})')
        self.image_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Mouse position widget
        self.position_label = QLabel()
        self.position_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.position_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

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
        self.image_view.setMouseTracking(True)
        self.image_view.mouseMoveEvent = self.mouseMoveEvent

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
    
        # Botton Bar layout
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addWidget(self.back_button)
        self.bottom_layout.addWidget(self.next_button)
        self.bottom_layout.addWidget(self.comment_box)
        self.bottom_layout.addWidget(self.submit_button)
        
        ### Category widgets

        # Category 1
        self.category_one_box = QCheckBox(text=self.category_names[1], parent=self)
        self.category_one_box.setFixedHeight(40)
        self.category_one_box.setStyleSheet("margin-left:50%; margin-right:50%;")
        self.category_one_box.clicked.connect(self.onCategoryOne)

        # Category 2
        self.category_two_box = QCheckBox(text=self.category_names[2], parent=self)
        self.category_two_box.setFixedHeight(40)
        self.category_two_box.setStyleSheet("margin-left:50%; margin-right:50%;")
        self.category_two_box.clicked.connect(self.onCategoryTwo)

        # Category 3
        self.category_three_box = QCheckBox(text=self.category_names[3], parent=self)
        self.category_three_box.setFixedHeight(40)
        self.category_three_box.setStyleSheet("margin-left:50%; margin-right:50%;")
        self.category_three_box.clicked.connect(self.onCategoryThree)

        # Category 4
        self.category_four_box = QCheckBox(text=self.category_names[4], parent=self)
        self.category_four_box.setFixedHeight(40)
        self.category_four_box.setStyleSheet("margin-left:50%; margin-right:50%;")
        self.category_four_box.clicked.connect(self.onCategoryFour)

        # Category 5/other
        self.category_five_box = QCheckBox(text=self.category_names[5], parent=self)
        self.category_five_box.setFixedHeight(40)
        self.category_five_box.setStyleSheet("margin-left:50%; margin-right:50%;")
        self.category_five_box.clicked.connect(self.onCategoryFive)

        # categories layout
        self.categories_layout = QHBoxLayout()
        self.categories_layout.addWidget(self.category_one_box)
        self.categories_layout.addWidget(self.category_two_box)
        self.categories_layout.addWidget(self.category_three_box)
        self.categories_layout.addWidget(self.category_four_box)
        self.categories_layout.addWidget(self.category_five_box)

        # Add widgets to main layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.image_label)
        layout.addWidget(self.image_view)
        layout.addWidget(self.position_label)
        layout.addLayout(self.bottom_layout)
        layout.addLayout(self.categories_layout)
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

        ## Filter menu
        filterMenu = menuBar.addMenu("&Filters")

        ### Blur
        blurMenu = QAction('&Gaussian Blur...',self)
        blurMenu.setStatusTip("Gaussian Blur")
        blurMenu.setShortcuts(['Ctrl+b'])
        blurMenu.triggered.connect(self.blurWindow.show)
        filterMenu.addAction(blurMenu)

        ### Brightness and Contrast
        adjustMenu = QAction('&Brightness and Contrast...',self)
        adjustMenu.setStatusTip("Brightness and Contrast")
        adjustMenu.setShortcuts(['Ctrl+a'])
        adjustMenu.triggered.connect(self.adjustmentsWindow.show)
        filterMenu.addAction(adjustMenu)

        ## Help menu
        helpMenu = menuBar.addMenu('&Help')

        ### Instructions and Keymapping window
        self.instructionsWindow = InstructionsWindow(self.group_names)
        instructionsMenu = QAction('&Instructions', self)
        instructionsMenu.setShortcuts(['F1'])
        instructionsMenu.setStatusTip('Instructions')
        instructionsMenu.triggered.connect(self.instructionsWindow.show)
        helpMenu.addAction(instructionsMenu)
        self.instructionsWindow.show()

        # Initialize some data
        self.getComment()
        self.markUpdate()
        self.categoryUpdate()

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

    def resizeEvent(self, event):
        '''
        Resize event; rescales image to fit in window, but keeps aspect ratio
        '''
        self.image_view.fitInView(self._pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        super().resizeEvent(event)

    def keyPressEvent(self,event):
        # Check if key is bound with marking the image
        markButtons = galmark.io.markBindingCheck(event)
        for i in range(0,9):
            if markButtons[i]: self.onMark(group=i+1)

        # Check if "Enter" was pressed
        if (event.key() == Qt.Key.Key_Return) or (event.key() == Qt.Key.Key_Enter):
            self.onEnter()

        # if (event.key() == Qt.Key.Key_Right)

    def mousePressEvent(self,event):
        # Check if key is bound with marking the image
        markButtons = galmark.io.markBindingCheck(event)
        for i in range(0,9):
            if markButtons[i]: self.onMark(group=i+1)
        
        if (event.button() == Qt.MouseButton.MiddleButton):
            self.onMiddleMouse()

        if (event.button() == Qt.MouseButton.RightButton):
            self.getSelectedMarks()

    def mouseMoveEvent(self, event):
        ep, lp = self.mouseImagePos()

        _x, _y = lp.x(), self.wcs._naxis[0] - lp.y()
        ra, dec = self.wcs.all_pix2world([[_x, _y]], 0)[0]
        
        # Mark if hovering over image
        if bool(self.image_view.itemAt(ep)):
            self.position_label.setText(f'Pixel: ({lp.x()} , {lp.y()})     WCS: ({ra:.4f}° , {dec:.4f}°)')
        else: 
            self.position_label.setText('')

    # === On-actions ===
    def onCategoryOne(self):
        if (self.category_one_box.checkState().value == 2) and (1 not in self.data[self.image_file]['category']):
            self.data[self.image_file]['category'].append(1)
        else:
            self.data[self.image_file]['category'].remove(1)
        galmark.io.save(self.data,self.username,self.date)
        self.imageUpdate()

    def onCategoryTwo(self):
        if (self.category_two_box.checkState().value == 2) and (2 not in self.data[self.image_file]['category']):
            self.data[self.image_file]['category'].append(2)
        else:
            self.data[self.image_file]['category'].remove(2)
        galmark.io.save(self.data,self.username,self.date)
        self.imageUpdate()

    def onCategoryThree(self):
        if (self.category_three_box.checkState().value == 2) and (3 not in self.data[self.image_file]['category']):
            self.data[self.image_file]['category'].append(3)
        else:
            self.data[self.image_file]['category'].remove(3)
        galmark.io.save(self.data,self.username,self.date)
        self.imageUpdate()

    def onCategoryFour(self):
        if (self.category_four_box.checkState().value == 2) and (4 not in self.data[self.image_file]['category']):
            self.data[self.image_file]['category'].append(4)
        else:
            self.data[self.image_file]['category'].remove(4)
        galmark.io.save(self.data,self.username,self.date)
        self.imageUpdate()

    def onCategoryFive(self):
        if (self.category_five_box.checkState().value == 2) and (5 not in self.data[self.image_file]['category']):
            self.data[self.image_file]['category'].append(5)
        else:
            self.data[self.image_file]['category'].remove(5)
        galmark.io.save(self.data,self.username,self.date)
        self.imageUpdate()

    def onMark(self, group=0):
        '''
        Actions to complete when marking
        '''

        # get event position and position on image
        ep, lp = self.mouseImagePos()
        
        # Mark if hovering over image
        
        if (self.group_max[group - 1] != 'None'):
            limit = int(self.group_max[group - 1])

            if (limit == 1) and (len(self.data[self.image_file][group]['Marks']) == 1):
                if self._pixmap_item is self.image_view.itemAt(ep):

                    mark = Mark(lp.x(),lp.y(),wcs=self.wcs,group=group)
                    mark.draw(self.image_scene)
                    
                    prev_mark = self.data[self.image_file][group]['Marks'][0]
                    self.image_scene.removeItem(prev_mark)
                    self.data[self.image_file][group]['Marks'][0] = mark
                    galmark.io.save(self.data,self.username,self.date)

            elif (len(self.data[self.image_file][group]['Marks']) < limit):
                if self._pixmap_item is self.image_view.itemAt(ep):

                    mark = Mark(lp.x(),lp.y(),wcs=self.wcs,group=group)
                    mark.draw(self.image_scene)

                    if not self.data[self.image_file][group]['Marks']:
                        self.data[self.image_file][group]['Marks'] = []

                    self.data[self.image_file][group]['Marks'].append(mark)
                    galmark.io.save(self.data,self.username,self.date)
        else:
            if self._pixmap_item is self.image_view.itemAt(ep):

                mark = Mark(lp.x(),lp.y(),wcs=self.wcs,group=group)
                mark.draw(self.image_scene)

                if not self.data[self.image_file][group]['Marks']:
                    self.data[self.image_file][group]['Marks'] = []

                self.data[self.image_file][group]['Marks'].append(mark)
                galmark.io.save(self.data,self.username,self.date)

    def onNext(self):
        if self.idx+1 < self.N:
            # Increment the index
            self.idx += 1
            self.commentUpdate()
            self.imageUpdate()
            self.markUpdate()
            self.getComment()
            self.categoryUpdate()
            # galmark.io.save(self.data,self.username,self.date)

    def onBack(self):
        if self.idx+1 > 1:
            # Increment the index
            self.idx -= 1
            self.commentUpdate()
            self.imageUpdate()
            self.markUpdate()
            self.getComment()
            self.categoryUpdate()
            # galmark.io.save(self.data,self.username,self.date)
            
    def onEnter(self):
        self.commentUpdate()
        galmark.io.save(self.data,self.username,self.date)
    
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

        _center = self.image_view.mapToGlobal(center)
        self.cursor().setPos(int(_center.x()),int(_center.x()))

    def onBlur(self,value):
        value = ceil(value) // 2 * 2 + 1
        self.matimage = cv2.imread(self.image)
        self.matimage = cv2.GaussianBlur(self.matimage,(value,value),0)
        self.qimage = QImage(self.matimage.data, self.matimage.shape[1], self.matimage.shape[0], QImage.Format.Format_RGB888).rgbSwapped()
        self.pixmap = QPixmap(self.qimage)
        self._pixmap_item.setPixmap(self.pixmap)

    # === Update methods ===

    def imageUpdate(self):
        for item in self.image_scene.items(): self.image_scene.removeItem(item)

        # Update the pixmap
        self.image = self.images[self.idx]
        self.image_file = self.image.split(os.sep)[-1]
        self.pixmap = QPixmap(self.image)
        self._pixmap_item = QGraphicsPixmapItem(self.pixmap)
        self.image_scene.addItem(self._pixmap_item)

        # Update image label
        self.image_label.setText(f'{self.image_file} ({self.idx+1} of {self.N})')

        #Update WCS
        self.wcs = galmark.io.parseWCS(self.image)
    
    def commentUpdate(self):
        # Update the comment in the dictionary
        comment = self.comment_box.text()
        if not comment:
            comment = 'None'

        self.data[self.image_file]['comment'] = comment
        galmark.io.save(self.data,self.username,self.date)

    def getComment(self):
        if bool(self.data[self.image_file]['comment']):
            if (self.data[self.image_file]['comment'] == 'None'):
                self.comment_box.setText('')
            else:
                comment = self.data[self.image_file]['comment']
                self.comment_box.setText(comment)
        else:
            comment = 'None'
            self.data[self.image_file]['comment'] = comment
            self.comment_box.setText('')

    def categoryUpdate(self):
        # Initialize category and update checkboxes
        self.category_one_box.setChecked(False)
        self.category_two_box.setChecked(False)
        self.category_three_box.setChecked(False)
        self.category_four_box.setChecked(False)
        self.category_five_box.setChecked(False)
        if not (self.data[self.image_file]['category']):
            self.data[self.image_file]['category'] = []
        else:
            category_list = self.data[self.image_file]['category']
            if (1 in category_list):
                self.category_one_box.setChecked(True)
            if (2 in category_list):
                self.category_two_box.setChecked(True)
            if (3 in category_list):
                self.category_three_box.setChecked(True)
            if (4 in category_list):
                self.category_four_box.setChecked(True)
            if (5 in category_list):
                self.category_five_box.setChecked(True)

    def markUpdate(self):
        # Redraws all marks in image
        for i in range(0,10):
            mark_list = self.data[self.image_file][i]['Marks']
                
            for mark in mark_list: mark.draw(self.image_scene)

    def getSelectedMarks(self):
        _, pix_pos = self.mouseImagePos()
        pix_pos = pix_pos.toPointF()
        selection_filt = [ item is self.image_scene.itemAt(pix_pos, item.transform()) 
                           for item in self.image_scene.items() 
                           if isinstance(item,Mark) ]
        selected_items = [ item for item in self.image_scene.items() 
                           if isinstance(item,Mark) 
                           and (item is self.image_scene.itemAt(pix_pos, item.transform()))]
        
        for item in selected_items:
            self.image_scene.removeItem(item)
            self.data[self.image_file][item.g]['Marks'].remove(item)
            galmark.io.save(self.data,self.username,self.date)

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


    