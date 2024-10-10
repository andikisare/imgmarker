from PyQt6.QtWidgets import ( QApplication, QMainWindow, QPushButton,
                              QLabel, QScrollArea, QGraphicsView,
                              QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, 
                              QSlider, QLineEdit, QFileDialog)
from PyQt6.QtGui import QCursor, QAction, QIcon, QFont
from PyQt6.QtCore import Qt, QPoint
from galmark.mark import Mark
from galmark import __dirname__, __icon__, __heart_solid__, __heart_clear__
import galmark.io
import galmark.image
from galmark.widget import QHLine, PosWidget
import sys
import os
import datetime as dt
import textwrap
from math import floor, inf
from functools import partial
from PIL import Image

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

        # Brightness slider
        self.brightnessSlider = QSlider()
        self._slider_setup(self.brightnessSlider,self.onBrightnessMoved)

        self.brightnessLabel = QLabel()
        self.brightnessLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.brightnessLabel.setText(f'Brightness: {self.brightnessSlider.value()}')

        # Contrast slider
        self.contrastSlider = QSlider()
        self._slider_setup(self.contrastSlider,self.onContrastMoved)

        self.contrastLabel = QLabel()
        self.contrastLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contrastLabel.setText(f'Contrast: {self.contrastSlider.value()}')

        layout.addWidget(self.brightnessLabel)
        layout.addWidget(self.brightnessSlider)
        layout.addWidget(self.contrastLabel)
        layout.addWidget(self.contrastSlider)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setFixedWidth(int(self.fullw/6))
        self.setFixedHeight(layout.sizeHint().height())

        # Set position of window
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def _slider_setup(self,slider:QSlider,connect):
        slider.setMinimum(-10)
        slider.setMaximum(10)
        slider.setValue(0)
        slider.setOrientation(Qt.Orientation.Horizontal)
        slider.sliderMoved.connect(connect)

    def onBrightnessMoved(self,pos):
        self.brightnessSlider.setValue(floor(pos))
        self.brightnessLabel.setText(f'Brightness: {floor(self.brightnessSlider.value())/10}')
    
    def onContrastMoved(self,pos):
        self.contrastSlider.setValue(floor(pos))
        self.contrastLabel.setText(f'Contrast: {floor(self.contrastSlider.value())/10}')

    def show(self):
        super().show()
        self.activateWindow()   

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

        self.slider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
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

        # Set position of window
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def onSliderMoved(self, pos):
        self.slider.setValue(floor(pos))
        self.valueLabel.setText(f'Radius: {floor(self.slider.value())/10}')

    def show(self):
        super().show()
        self.activateWindow()

class FrameWindow(QWidget):
    """
    Blur window
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(QIcon(__icon__))
        layout = QVBoxLayout()
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.setWindowTitle('Frames')
        self.setLayout(layout)

        self.slider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.sliderMoved.connect(self.onSliderMoved) 

        self.valueLabel = QLabel()
        self.valueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.valueLabel.setText(f'Frame: {self.slider.value()}')

        layout.addWidget(self.valueLabel)
        layout.addWidget(self.slider)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedWidth(int(self.fullw/6))
        self.setFixedHeight(layout.sizeHint().height())

        # Set position of window
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def onSliderMoved(self, pos):
        self.slider.setValue(floor(pos))
        self.valueLabel.setText(f'Frame: {floor(self.slider.value())}')

    def show(self):
        super().show()
        self.activateWindow()

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
        
        # Create the scroll area and label
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.label = QLabel()
        self.scroll_area.setWidget(self.label)
        self.scroll_area.setWidgetResizable(True)
        font = QFont('Courier')
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        # Lists for keybindings
        actions_list = ['Next','Back','Delete','Enter comment', 'Focus', 'Zoom in/out', 'Exit', 'Help']
        group_list = [f'Group \"{group}\"' for group in groupNames[1:]]
        actions_list = group_list + actions_list
        buttons_list = ['Left click OR 1', '2', '3', '4', '5', '6', '7', '8', '9', 'Tab', 'Shift+Tab', 'Right click OR Backspace', 'Enter', 'Middle click', 'Scroll wheel', 'Esc OR Q', 'F1', ]

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

    def show(self):
        super().show()
        self.activateWindow()

class StartupWindow(QInputDialog):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(__icon__))
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def getUser(self) -> None:
        # Make popup to get name
        text, OK = self.getText(self,"Startup", "Enter a username (no caps, no space, e.g. ryanwalker)")

        if OK: return text
        else: sys.exit()

class MainWindow(QMainWindow):
    def __init__(self, username:str, imtype:str = 'tif'):
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
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.zoomLevel = 1
        self.cursorFocus = False
    
        # Initialize config
        self.config = 'galmark.cfg'
        self.username = username
        self.date = dt.datetime.now(dt.UTC).date().isoformat()
        self.imtype = imtype

        # Initialize output dictionary
        self.__init_data__()

        self.imageScene = galmark.image.ImageScene(self.image)

        # Setup child windows
        self.blurWindow = BlurWindow()
        self.blurWindow.slider.valueChanged.connect(self.image.blur)
        
        self.adjustmentsWindow = AdjustmentsWindow()
        self.adjustmentsWindow.contrastSlider.valueChanged.connect(self.image.contrast)
        self.adjustmentsWindow.brightnessSlider.valueChanged.connect(self.image.brighten)
        
        self.frameWindow = FrameWindow()
        self.frameWindow.slider.valueChanged.connect(self.image.seek)
        self.frameWindow.slider.setMaximum(self.image.n_frames-1)

        

        # Set max blur based on size of image
        self.blur_max = int((self.image.height+self.image.width)/20)
        self.blurWindow.slider.setMaximum(self.blur_max)

        # Current image widget
        self.imageLabel = QLabel(f'{self.image.name} ({self.idx+1} of {self.N})')
        self.imageLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Mouse position widget
        self.pos_widget = PosWidget()

        # Create image view
        self.imageView = QGraphicsView(self.imageScene)       
        
        ### Disable scrollbar
        self.imageView.verticalScrollBar().blockSignals(True)
        self.imageView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.imageView.horizontalScrollBar().blockSignals(True)
        self.imageView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        ### Image view position setup and mouse tracking
        self.imageView.move(0, 0)
        self.imageView.setTransformationAnchor(self.imageView.ViewportAnchor(1))
        self.imageView.setMouseTracking(True)
        self.imageView.mouseMoveEvent = self.mouseMoveEvent

        ### Install event filters
        self.imageView.viewport().installEventFilter(self)

        # Back widget
        self.backButton = QPushButton(text='Back',parent=self)
        self.backButton.setFixedHeight(40)
        self.backButton.clicked.connect(partial(self.shift,-1))
        self.backButton.setShortcut('Shift+Tab')
        self.backButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Enter Button
        self.submitButton = QPushButton(text='Enter',parent=self)
        self.submitButton.setFixedHeight(40)
        self.submitButton.clicked.connect(self.enter)
        self.submitButton.setShortcut('Return')
        self.submitButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Next widget
        self.nextButton = QPushButton(text='Next',parent=self)
        self.nextButton.setFixedHeight(40)
        self.nextButton.clicked.connect(partial(self.shift,1))
        self.nextButton.setShortcut('Tab')
        self.nextButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Comment widget
        self.commentBox = QLineEdit(parent=self)
        self.commentBox.setFixedHeight(40)
    
        # Botton Bar layout
        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.addWidget(self.backButton)
        self.bottomLayout.addWidget(self.nextButton)
        self.bottomLayout.addWidget(self.commentBox)
        self.bottomLayout.addWidget(self.submitButton)
        
        ### Category widgets
        self.categories_layout = QHBoxLayout()

        # Category boxes
        self.category_boxes = [QCheckBox(text=galmark.io.CATEGORY_NAMES[i], parent=self) for i in range(1,6)]
        for i, box in enumerate(self.category_boxes):
            box.setFixedHeight(20)
            box.setStyleSheet("margin-left:30%; margin-right:30%;")
            box.clicked.connect(partial(self.categorize,i+1))
            box.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.categories_layout.addWidget(box)

        # Favorite box
        self.favorite_file_list = galmark.io.loadfav(username)
        self.favorite_box = QCheckBox(parent=self)
        self.favorite_box.setFixedHeight(20)
        self.favorite_box.setFixedWidth(40)
        self.favorite_box.setIcon(QIcon(__heart_clear__))
        self.favorite_box.setTristate(False)
        self.favorite_box.clicked.connect(self.favorite)
        self.favorite_box.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.categories_layout.addWidget(self.favorite_box)
        self.favorite_box.setShortcut('F')

        # Add widgets to main layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.imageLabel)
        layout.addWidget(self.imageView)
        layout.addWidget(self.pos_widget)
        layout.addWidget(QHLine())
        layout.addLayout(self.bottomLayout)
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

        ### Open file menu
        openMenu = QAction('&Open', self)
        openMenu.setShortcuts(['Ctrl+o'])
        openMenu.setStatusTip('Open save file')
        openMenu.triggered.connect(self.open)
        fileMenu.addAction(openMenu)

        ### Open image folder menu
        openDirMenu = QAction('&Open image directory', self)
        openDirMenu.setShortcuts(['Ctrl+Shift+o'])
        openDirMenu.setStatusTip('Open image directory')
        openDirMenu.triggered.connect(self.__init_data__)
        fileMenu.addAction(openDirMenu)

        ## View menu
        viewMenu = menuBar.addMenu("&View")

        ### Frame menu
        frameMenu = QAction('&Frames...', self)
        frameMenu.setShortcuts(['Ctrl+f'])
        frameMenu.setStatusTip('Frames...')
        frameMenu.triggered.connect(self.frameWindow.show)
        viewMenu.addAction(frameMenu)

        ### Focus cursor menu
        cursorFocusMenu = QAction('&Focus cursor', self)
        cursorFocusMenu.setStatusTip('Focus cursor')
        cursorFocusMenu.setCheckable(True)
        cursorFocusMenu.triggered.connect(partial(setattr,self,'cursorFocus'))
        viewMenu.addAction(cursorFocusMenu)

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
        self.instructionsWindow = InstructionsWindow(galmark.io.GROUP_NAMES)
        instructionsMenu = QAction('&Instructions', self)
        instructionsMenu.setShortcuts(['F1'])
        instructionsMenu.setStatusTip('Instructions')
        instructionsMenu.triggered.connect(self.instructionsWindow.show)
        helpMenu.addAction(instructionsMenu)
        
        # Resize and center MainWindow; move instructions off to the right
        self.resize(int(self.fullw/2.5),int(self.fullw/2.5))

        center = QApplication.primaryScreen().geometry().center()
        center -= QPoint(self.width(),self.height())/2
        self.move(center)

        self.instructionsWindow.move(int(self.x()+self.width()*1.04),self.y())
        self.instructionsWindow.show()

        # Initialize some data
        self.getComment()
        self.markUpdate()
        self.categoryUpdate()

    def __init_data__(self):
        # Initialize output dictionary
        self.images = galmark.io.load(self.username)
        
        self.favorite_file_list = galmark.io.loadfav(self.username)

        # Find all images in image directory
        
        try:
            self.images, self.idx = galmark.io.glob(self.imtype,edited_images=self.images)
            self.image = self.images[self.idx]
            self.image.seen = True
            self.N = len(self.images)
        except:
            # sys.exit(f"No images of type '{self.imtype}' found in directory: '{self.image_dir}'.\n"
            #          f"Please specify a different image directory in galmark.cfg and try again.")
            image_dir = os.path.join(QFileDialog.getExistingDirectory(self, "Select correct image directory", galmark.io.IMAGE_DIR),'')
            galmark.io.configUpdate(image_dir=image_dir)
            self.images, self.idx = galmark.io.glob(self.imtype,edited_images=self.images)
            self.image = self.images[self.idx]
            self.image.seen = True
            self.N = len(self.images)

    def eventFilter(self, source, event):
        # Event filter for zooming without scrolling
        if (source == self.imageView.viewport()) and (event.type() == 31):
            x = event.angleDelta().y() / 120
            if x > 0:
                self.zoom(-1)
            elif x < 0:
                self.zoom()
            return True

        return super().eventFilter(source, event)
    
    # === Events ===

    def resizeEvent(self, event):
        '''
        Resize event; rescales image to fit in window, but keeps aspect ratio
        '''
        transform = self.imageView.transform()
        self.imageView.fitInView(self.image, Qt.AspectRatioMode.KeepAspectRatio)
        self.imageView.setTransform(transform)
        super().resizeEvent(event)

    def keyPressEvent(self,event):
        # Check if key is bound with marking the image
        markButtons = galmark.io.markCheck(event)
        for i in range(0,9):
            if markButtons[i]: self.mark(group=i+1)

        if (event.key() == Qt.Key.Key_Backspace) or (event.key() == Qt.Key.Key_Delete):
            self.deleteMarks()

        if (event.key() == Qt.Key.Key_Space):
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.KeyboardModifier.ShiftModifier:
                self.image.seek(self.image.tell()-1)
            else:
                self.image.seek(self.image.tell()+1)

    def mousePressEvent(self,event):
        # Check if key is bound with marking the image
        markButtons = galmark.io.markCheck(event)
        for i in range(0,9):
            if markButtons[i]: self.mark(group=i+1)
        
        if (event.button() == Qt.MouseButton.MiddleButton):
            self.middleMouse()

        if (event.button() == Qt.MouseButton.RightButton):
            self.deleteMarks()

    def mouseMoveEvent(self, event):
        # Mark if hovering over image
        lp = self.mousePixPos()
        lp_true = lp - 4*QPoint(self.image.width,self.image.height)
        x, y = lp_true.x(), lp_true.y()
        w, h = self.image.width, self.image.height

        if (x>=0) and (x<=w) and (y>=0) and  (y<=h):
            _x, _y = x, h - y

            ra, dec = self.image.wcs.all_pix2world([[_x, _y]], 0)[0]

            self.pos_widget.x_text.setText(f'{x}')
            self.pos_widget.y_text.setText(f'{y}')

            self.pos_widget.ra_text.setText(f'{ra:.4f}°')
            self.pos_widget.dec_text.setText(f'{dec:.4f}°')

        else:
            self.pos_widget.x_text.setText('')
            self.pos_widget.y_text.setText('')

            self.pos_widget.ra_text.setText('')
            self.pos_widget.dec_text.setText('')

    def closeEvent(self, event):
        self.commentUpdate()
        sys.exit()
    
    # === Actions ===
    def open(self):
        ### THIS IS WHERE YOU SELECT FILES, FILES ARE CURRENTLY LIMITED TO *.txt
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        fileName = dialog.getSaveFileName(self, 'Open Save File', os.getcwd(), 'Text (*.txt)')

        self.username = str(os.path.split(fileName[0])[1]).removesuffix('.txt')
        
        self.__init_data__()
        self.imageUpdate()

        self.markUpdate()
        self.getComment()
        self.categoryUpdate()
        self.commentUpdate()
        self.favoriteUpdate()

    def openDir(self):
        image_dir = os.path.join(QFileDialog.getExistingDirectory(self, "Select image directory", galmark.io.IMAGE_DIR),'')
        galmark.io.configUpdate(image_dir=image_dir)
        self.images, self.idx = galmark.io.glob(self.imtype,edited_images=self.images)
        self.image = self.images[self.idx]
        self.image.seen = True
        self.N = len(self.images)
        self.imageLabel = QLabel(f'{self.image.name} ({self.idx+1} of {self.N})')

    def favorite(self,state):
        state = Qt.CheckState(state)
        if state == Qt.CheckState.PartiallyChecked:
            self.favorite_box.setIcon(QIcon(__heart_solid__))
            self.favorite_file_list.append(self.image.name)
            galmark.io.savefav(self.username,self.favorite_file_list)
        else:
            self.favorite_box.setIcon(QIcon(__heart_clear__))
            if self.image.name in self.favorite_file_list: 
                self.favorite_file_list.remove(self.image.name)
            galmark.io.savefav(self.username,self.favorite_file_list)

    def categorize(self,i:int) -> None:
        if (self.category_boxes[i-1].checkState() == Qt.CheckState.Checked) and (i not in self.image.categories):
            self.image.categories.append(i)
        elif (i in self.image.categories):
            self.image.categories.remove(i)
        galmark.io.save(self.username,self.date,self.images)
        galmark.io.savefav(self.username,self.favorite_file_list)

    def mark(self, group:int=0) -> None:
        '''
        Actions to complete when marking
        '''

        # get event position and position on image
        lp = self.mousePixPos()
        w, h = self.image.width, self.image.height
        lp_true = lp - 4*QPoint(w,h)
        x, y = lp_true.x(), lp_true.y()
        
        # Mark if hovering over image
        if galmark.io.GROUP_MAX[group - 1] == 'None': limit = inf
        else: limit = int(galmark.io.GROUP_MAX[group - 1])

        if (x>=0) and (x<=w) and (y>=0) and  (y<=h):
            mark = self.imageScene.mark(lp.x(),lp.y(),group=group)

            if (limit == 1) and (len(self.image.marks) == 1):
                prev_mark = self.image.marks[0]
                self.imageScene.removeItem(prev_mark)
                self.image.marks.remove(prev_mark)
                self.image.marks[0] = mark

            elif len(self.image.marks) < limit:
                self.image.marks.append(mark)

            galmark.io.save(self.username,self.date,self.images)
            galmark.io.savefav(self.username,self.favorite_file_list)

    def shift(self,delta:int):
        # Increment the index
        self.idx += delta
        if self.idx > self.N-1:
            self.idx = 0
        elif self.idx < 0:
            self.idx = self.N-1

        self.commentUpdate()
        self.imageUpdate()
        self.markUpdate()
        self.getComment()
        self.categoryUpdate()
        self.favoriteUpdate()
            
    def enter(self):
        self.commentUpdate()
        self.commentBox.clearFocus()
        galmark.io.save(self.username,self.date,self.images)
        galmark.io.savefav(self.username,self.favorite_file_list)

    def middleMouse(self):
        # Center on cursor
        center = self.imageView.viewport().rect().center()
        scene_center = self.imageView.mapToScene(center)
        pixPos = self.mousePixPos()

        delta = scene_center.toPoint() - pixPos
        self.imageView.translate(delta.x(),delta.y())

        if self.cursorFocus:
            global_center = self.imageView.mapToGlobal(center)
            self.cursor().setPos(global_center)

    def zoom(self,scale:int=1):
        # Zoom in on cursor location
        self.zoomLevel *= 1.2**scale

        viewPos = self.mouseViewPos()
        transform = self.imageView.transform()
        center = self.imageView.mapToScene(viewPos)
        transform.translate(center.x(), center.y())
        transform.scale(1.2**scale, 1.2**scale)
        transform.translate(-center.x(), -center.y())
        self.imageView.setTransform(transform)

    # === Update methods ===

    def favoriteUpdate(self):
        if self.image.name in self.favorite_file_list:
            self.favorite_box.setChecked(True)
            self.favorite_box.setIcon(QIcon(__heart_solid__))
        else:
            self.favorite_box.setIcon(QIcon(__heart_clear__))
            self.favorite_box.setChecked(False)

    def imageUpdate(self):
        # Update scene
        self.image = self.images[self.idx]
        self.image.seen = True
        self.imageScene.update(self.image)
        
        # Update sliders
        self.blurWindow.slider.valueChanged.disconnect()
        self.adjustmentsWindow.contrastSlider.valueChanged.disconnect()
        self.adjustmentsWindow.brightnessSlider.valueChanged.disconnect()
        self.frameWindow.slider.valueChanged.disconnect()

        self.blurWindow.slider.valueChanged.connect(self.image.blur)
        self.adjustmentsWindow.contrastSlider.valueChanged.connect(self.image.contrast)
        self.adjustmentsWindow.brightnessSlider.valueChanged.connect(self.image.brighten)
        self.frameWindow.slider.valueChanged.connect(self.image.seek)

        self.frameWindow.slider.setMaximum(self.image.n_frames-1)
        self.blur_max = int((self.image.height+self.image.width)/20)
        self.blurWindow.slider.setMaximum(self.blur_max)

        # Update image label
        self.imageLabel.setText(f'{self.image.name} ({self.idx+1} of {self.N})')
    
    def commentUpdate(self):
        # Update the comment in the dictionary
        comment = self.commentBox.text()
        if not comment:
            comment = 'None'

        self.image.comment = comment
        galmark.io.save(self.username,self.date,self.images)
        galmark.io.savefav(self.username,self.favorite_file_list)

    def getComment(self):
        if bool(self.image.comment):
            if (self.image.comment == 'None'):
                self.commentBox.setText('')
            else:
                comment = self.image.comment
                self.commentBox.setText(comment)
        else:
            comment = 'None'
            self.image.comment = comment
            self.commentBox.setText('')

    def categoryUpdate(self):
        # Initialize category and update checkboxes
        for box in self.category_boxes: box.setChecked(False)
        if not self.image.categories:
            self.image.categories = []
        else:
            category_list = self.image.categories
            for i in category_list:
                self.category_boxes[i-1].setChecked(True)

    def markUpdate(self):
        # Redraws all marks in image
        for mark in self.image.marks: self.imageScene.addItem(mark)

    def deleteMarks(self):
        pixPos = self.mousePixPos().toPointF()
        selected_items = [ item for item in self.imageScene.items() 
                           if isinstance(item,Mark) 
                           and (item is self.imageScene.itemAt(pixPos, item.transform()))]
        
        for item in selected_items:
            self.imageScene.removeItem(item)
            self.image.marks.remove(item)
            galmark.io.save(self.username,self.date,self.images)
            galmark.io.savefav(self.username,self.favorite_file_list)

    # === Utils ===

    def mouseViewPos(self):
        '''
        Gets mouse positions

        Returns:
            viewPos: position of mouse in the pixmap
        '''
        return self.imageView.mapFromGlobal(QCursor.pos())
    
    def mousePixPos(self):
        '''
        Gets mouse positions

        Returns:
            pixPos: position of mouse in the pixmap
        '''
        viewPos = self.imageView.mapFromGlobal(QCursor.pos())
        scenePos = self.imageView.mapToScene(viewPos)
        
        return self.image.mapFromScene(scenePos).toPoint()

    