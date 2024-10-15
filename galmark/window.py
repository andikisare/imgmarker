from PyQt6.QtWidgets import ( QApplication, QMainWindow, QPushButton,
                              QLabel, QScrollArea, QGraphicsView,
                              QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, 
                              QSlider, QLineEdit, QFileDialog )
from PyQt6.QtGui import QAction, QIcon, QFont
from PyQt6.QtCore import Qt, QPoint, QPointF, QRectF
from galmark.mark import Mark
from galmark import __dirname__, ICON, HEART_SOLID, HEART_CLEAR
import galmark.io
import galmark.image
from galmark.widget import QHLine, PosWidget
import sys
import os
import datetime as dt
import textwrap
from math import floor, inf, nan
from functools import partial

class AdjustmentsWindow(QWidget):
    """
    Blur window
    """
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon(ICON))
        layout = QVBoxLayout()
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.setWindowTitle('Brightness and Contrast')
        self.setLayout(layout)

        # Brightness slider
        self.brightness_slider = QSlider()
        self._slider_setup(self.brightness_slider,self.brightness_moved)

        self.brightness_label = QLabel()
        self.brightness_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.brightness_label.setText(f'Brightness: {self.brightness_slider.value()}')

        # Contrast slider
        self.contrast_slider = QSlider()
        self._slider_setup(self.contrast_slider,self.contrast_moved)

        self.contrast_label = QLabel()
        self.contrast_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contrast_label.setText(f'Contrast: {self.contrast_slider.value()}')

        layout.addWidget(self.brightness_label)
        layout.addWidget(self.brightness_slider)
        layout.addWidget(self.contrast_label)
        layout.addWidget(self.contrast_slider)
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

    def brightness_moved(self,pos):
        self.brightness_slider.setValue(floor(pos))
        self.brightness_label.setText(f'Brightness: {floor(self.brightness_slider.value())/10}')
    
    def contrast_moved(self,pos):
        self.contrast_slider.setValue(floor(pos))
        self.contrast_label.setText(f'Contrast: {floor(self.contrast_slider.value())/10}')

    def show(self):
        super().show()
        self.activateWindow()   

class BlurWindow(QWidget):
    """
    Blur window
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(QIcon(ICON))
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
        self.slider.sliderMoved.connect(self.slider_moved) 

        self.value_label = QLabel()
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setText(f'Radius: {self.slider.value()}')

        layout.addWidget(self.value_label)
        layout.addWidget(self.slider)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedWidth(int(self.fullw/6))
        self.setFixedHeight(layout.sizeHint().height())

        # Set position of window
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def slider_moved(self, pos):
        self.slider.setValue(floor(pos))
        self.value_label.setText(f'Radius: {floor(self.slider.value())/10}')

    def show(self):
        super().show()
        self.activateWindow()

class FrameWindow(QWidget):
    """
    Blur window
    """
    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(QIcon(ICON))
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
        self.slider.sliderMoved.connect(self.slider_moved) 

        self.value_label = QLabel()
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setText(f'Frame: {self.slider.value()}')

        layout.addWidget(self.value_label)
        layout.addWidget(self.slider)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedWidth(int(self.fullw/6))
        self.setFixedHeight(layout.sizeHint().height())

        # Set position of window
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def slider_moved(self, pos):
        self.slider.setValue(floor(pos))
        self.value_label.setText(f'Frame: {floor(self.slider.value())}')

    def show(self):
        super().show()
        self.activateWindow()

class InstructionsWindow(QWidget):
    """
    This window displays the instructions and keymappings
    """
    def __init__(self,groupNames):
        super().__init__()
        self.setWindowIcon(QIcon(ICON))
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
        self.setWindowIcon(QIcon(ICON))
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def getUser(self) -> None:
        # Make popup to get name
        text, OK = self.getText(self,"Startup", "Enter a username (no caps, no space, e.g. ryanwalker)")
        if not text.isalnum(): raise galmark.io.SAVE_ALPHANUM_ERR

        if not OK: sys.exit()
        elif not text.isalnum(): raise galmark.io.SAVE_ALPHANUM_ERR 
        else: return text

class MainWindow(QMainWindow):
    def __init__(self, username:str):
        super().__init__()
        self.setWindowTitle("Galaxy Marker")
        self.setWindowIcon(QIcon(ICON))
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.zoom_level = 1
        self.cursor_focus = False
    
        # Initialize data
        self.username = username
        self.date = dt.datetime.now(dt.UTC).date().isoformat()
        self.__init_data__()
        self.imageScene = galmark.image.ImageScene(self.image)

        # Setup child windows
        self.blur_window = BlurWindow()
        self.blur_window.slider.valueChanged.connect(self.image.blur)
        
        self.adjust_menu = AdjustmentsWindow()
        self.adjust_menu.contrast_slider.valueChanged.connect(self.image.contrast)
        self.adjust_menu.brightness_slider.valueChanged.connect(self.image.brighten)
        
        self.frame_window = FrameWindow()
        self.frame_window.slider.valueChanged.connect(self.image.seek)
        self.frame_window.slider.setMaximum(self.image.n_frames-1)

        # Set max blur based on size of image
        self.blur_max = int((self.image.height+self.image.width)/20)
        self.blur_window.slider.setMaximum(self.blur_max)

        # Current image widget
        self.image_label = QLabel(f'{self.image.name} ({self.idx+1} of {self.N})')
        self.image_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Mouse position widget
        self.pos_widget = PosWidget()

        # Create image view
        self.image_view = QGraphicsView(self.imageScene)
        self.fit_image()   
        
        ### Disable scrollbar
        self.image_view.verticalScrollBar().blockSignals(True)
        self.image_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.image_view.horizontalScrollBar().blockSignals(True)
        self.image_view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        ### Image view position setup and mouse tracking
        self.image_view.move(0, 0)
        self.image_view.setTransformationAnchor(self.image_view.ViewportAnchor(1))
        self.image_view.setMouseTracking(True)
        self.image_view.mouseMoveEvent = self.mouseMoveEvent

        ### Install event filters
        self.image_view.viewport().installEventFilter(self)

        # Back widget
        self.back_button = QPushButton(text='Back',parent=self)
        self.back_button.setFixedHeight(40)
        self.back_button.clicked.connect(partial(self.shift,-1))
        self.back_button.setShortcut('Shift+Tab')
        self.back_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Enter Button
        self.submit_button = QPushButton(text='Enter',parent=self)
        self.submit_button.setFixedHeight(40)
        self.submit_button.clicked.connect(self.enter)
        self.submit_button.setShortcut('Return')
        self.submit_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Next widget
        self.next_button = QPushButton(text='Next',parent=self)
        self.next_button.setFixedHeight(40)
        self.next_button.clicked.connect(partial(self.shift,1))
        self.next_button.setShortcut('Tab')
        self.next_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

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
        self.favorite_list = galmark.io.loadfav(username)
        self.favorite_box = QCheckBox(parent=self)
        self.favorite_box.setFixedHeight(20)
        self.favorite_box.setFixedWidth(40)
        self.favorite_box.setIcon(QIcon(HEART_CLEAR))
        self.favorite_box.setTristate(False)
        self.favorite_box.clicked.connect(self.favorite)
        self.favorite_box.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.categories_layout.addWidget(self.favorite_box)
        self.favorite_box.setShortcut('F')

        # Add widgets to main layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.image_label)
        layout.addWidget(self.image_view)
        layout.addWidget(self.pos_widget)
        layout.addWidget(QHLine())
        layout.addLayout(self.bottom_layout)
        layout.addLayout(self.categories_layout)
        self.setCentralWidget(central_widget)
        
        # Menu bar
        menu_bar = self.menuBar()

        ## File menu
        file_menu = menu_bar.addMenu("&File")

        ### Exit menu
        exit_menu = QAction('&Exit', self)
        exit_menu.setShortcuts(['Esc','q'])
        exit_menu.setStatusTip('Exit')
        exit_menu.triggered.connect(self.closeEvent)
        file_menu.addAction(exit_menu)

        ### Open file menu
        open_menu = QAction('&Open', self)
        open_menu.setShortcuts(['Ctrl+o'])
        open_menu.setStatusTip('Open save directory')
        open_menu.triggered.connect(self.open)
        file_menu.addAction(open_menu)

        ### Open image folder menu
        open_ims_menu = QAction('&Open image directory', self)
        open_ims_menu.setShortcuts(['Ctrl+Shift+o'])
        open_ims_menu.setStatusTip('Open image directory')
        open_ims_menu.triggered.connect(self.open_ims)
        file_menu.addAction(open_ims_menu)

        ## View menu
        view_menu = menu_bar.addMenu("&View")

        ### Frame menu
        frame_menu = QAction('&Frames...', self)
        frame_menu.setShortcuts(['Ctrl+f'])
        frame_menu.setStatusTip('Frames...')
        frame_menu.triggered.connect(self.frame_window.show)
        view_menu.addAction(frame_menu)

        ### Focus cursor menu
        cursor_focus_menu = QAction('&Focus cursor', self)
        cursor_focus_menu.setStatusTip('Focus cursor')
        cursor_focus_menu.setCheckable(True)
        cursor_focus_menu.triggered.connect(partial(setattr,self,'cursor_focus'))
        view_menu.addAction(cursor_focus_menu)

        ## Filter menu
        filter_menu = menu_bar.addMenu("&Filters")

        ### Blur
        blur_menu = QAction('&Gaussian Blur...',self)
        blur_menu.setStatusTip("Gaussian Blur")
        blur_menu.setShortcuts(['Ctrl+b'])
        blur_menu.triggered.connect(self.blur_window.show)
        filter_menu.addAction(blur_menu)

        ### Brightness and Contrast
        adjust_menu = QAction('&Brightness and Contrast...',self)
        adjust_menu.setStatusTip("Brightness and Contrast")
        adjust_menu.setShortcuts(['Ctrl+a'])
        adjust_menu.triggered.connect(self.adjust_menu.show)
        filter_menu.addAction(adjust_menu)

        ## Help menu
        help_menu = menu_bar.addMenu('&Help')

        ### Instructions and Keymapping window
        self.instructions_window = InstructionsWindow(galmark.io.GROUP_NAMES)
        instructions_menu = QAction('&Instructions', self)
        instructions_menu.setShortcuts(['F1'])
        instructions_menu.setStatusTip('Instructions')
        instructions_menu.triggered.connect(self.instructions_window.show)
        help_menu.addAction(instructions_menu)
        
        # Resize and center MainWindow; move instructions off to the right
        self.resize(int(self.fullw/2.5),int(self.fullw/2.5))

        center = QApplication.primaryScreen().geometry().center()
        center -= QPoint(self.width(),self.height())/2
        self.move(center)

        self.instructions_window.move(int(self.x()+self.width()*1.04),self.y())
        self.instructions_window.show()

        # Initialize some data
        self.get_comment()
        self.update_marks()
        self.update_categories()

    def __init_data__(self):
        # Initialize output dictionary
        self.images = galmark.io.load(self.username)
        
        self.favorite_list = galmark.io.loadfav(self.username)

        # Find all images in image directory

        try: self.image.clear_pixmap()
        except: pass
        
        try:
            self.images, self.idx = galmark.io.glob(edited_images=self.images)
            self.image = self.images[self.idx]
            self.image.__init_item__()
            self.image.seen = True
            self.N = len(self.images)
        except:
            # sys.exit(f"No images of type '{self.imtype}' found in directory: '{self.image_dir}'.\n"
            #          f"Please specify a different image directory in galmark.cfg and try again.")
            image_dir = os.path.join(QFileDialog.getExistingDirectory(self, "Open correct image directory", galmark.io.IMAGE_DIR),'')
            galmark.io.update_config(image_dir=image_dir)
            self.images, self.idx = galmark.io.glob(edited_images=self.images)
            self.image = self.images[self.idx]
            self.image.__init_item__()
            self.image.seen = True
            self.N = len(self.images)

    def inview(self,x,y): return (x>=0) and (x<=self.image.width-1) and (y>=0) and  (y<=self.image.height-1)

    # === Events ===

    def eventFilter(self, source, event):
        # Event filter for zooming without scrolling
        if (source == self.image_view.viewport()) and (event.type() == 31):
            x = event.angleDelta().y() / 120
            if x > 0:
                self.zoom(1/1.2)
            elif x < 0:
                self.zoom(1.2)
            return True

        return super().eventFilter(source, event)

    def keyPressEvent(self,event):
        # Check if key is bound with marking the image
        markButtons = galmark.io.check_marks(event)
        for i in range(0,9):
            if markButtons[i]: self.mark(group=i+1)

        if (event.key() == Qt.Key.Key_Backspace) or (event.key() == Qt.Key.Key_Delete):
            self.del_marks()

        if (event.key() == Qt.Key.Key_Space):
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.KeyboardModifier.ShiftModifier:
                self.image.seek(self.image.frame-1)
                self.image.frame = self.image.tell()
            else:
                self.image.seek(self.image.frame+1)
                self.image.frame = self.image.tell()

    def mousePressEvent(self,event):
        # Check if key is bound with marking the image
        markButtons = galmark.io.check_marks(event)
        for i in range(0,9):
            if markButtons[i]: self.mark(group=i+1)
        
        if (event.button() == Qt.MouseButton.MiddleButton):
            self.middle_mouse()

        if (event.button() == Qt.MouseButton.RightButton):
            self.del_marks()

    def mouseMoveEvent(self, event):
        # Mark if hovering over image
        pix_pos = self.mouse_pix_pos()
        x, y = pix_pos.x(), pix_pos.y()

        if self.inview(x,y):
            _x, _y = x, self.image.height - y

            try: ra, dec = self.image.wcs.all_pix2world([[_x, _y]], 0)[0]
            except: ra, dec = nan, nan

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
        self.update_comments()
        sys.exit()
    
    # === Actions ===
    def open(self):
        ### THIS IS WHERE YOU SELECT FILES, FILES ARE CURRENTLY LIMITED TO *.txt
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        fileName = dialog.getSaveFileName(self, 'Open save directory', os.getcwd())

        self.username = str(os.path.split(fileName[0])[1])
        if not self.username.isalnum(): raise galmark.io.SAVE_ALPHANUM_ERR
        
        self.__init_data__()
        self.update_images()
        self.update_marks()
        self.get_comment()
        self.update_categories()
        self.update_comments()
        self.update_favorites()

    def open_ims(self):
        image_dir = ''
        while (image_dir == ''):
            image_dir = os.path.join(QFileDialog.getExistingDirectory(self, "Select image directory", galmark.io.IMAGE_DIR),'')
        galmark.io.update_config(image_dir=image_dir)
        self.images, self.idx = galmark.io.glob(edited_images=[])
        try: self.image.clear_pixmap()
        except: pass
        self.image = self.images[self.idx]
        self.image.__init_item__()
        self.image.seen = True
        self.N = len(self.images)
    
        self.update_images()
        self.update_marks()
        self.get_comment()
        self.update_categories()
        self.update_comments()

    def favorite(self,state):
        state = Qt.CheckState(state)
        if state == Qt.CheckState.PartiallyChecked:
            self.favorite_box.setIcon(QIcon(HEART_SOLID))
            self.favorite_list.append(self.image.name)
            galmark.io.savefav(self.username,self.favorite_list)
        else:
            self.favorite_box.setIcon(QIcon(HEART_CLEAR))
            if self.image.name in self.favorite_list: 
                self.favorite_list.remove(self.image.name)
            galmark.io.savefav(self.username,self.favorite_list)

    def categorize(self,i:int) -> None:
        if (self.category_boxes[i-1].checkState() == Qt.CheckState.Checked) and (i not in self.image.categories):
            self.image.categories.append(i)
        elif (i in self.image.categories):
            self.image.categories.remove(i)
        galmark.io.save(self.username,self.date,self.images)
        galmark.io.savefav(self.username,self.favorite_list)

    def mark(self, group:int=0) -> None:
        '''
        Actions to complete when marking
        '''

        # get event position and position on image
        pix_pos = self.mouse_pix_pos()
        x, y = pix_pos.x(), pix_pos.y()
        
        # Mark if hovering over image
        if galmark.io.GROUP_MAX[group - 1] == 'None': limit = inf
        else: limit = int(galmark.io.GROUP_MAX[group - 1])

        marks_in_group = [m for m in self.image.marks if m.g == group]

        if self.inview(x,y):
            mark = self.imageScene.mark(x,y,group=group)
            
            if (limit == 1) and (len(marks_in_group) == 1):
                prev_mark = marks_in_group[0]
                self.imageScene.removeItem(prev_mark)
                self.image.marks.remove(prev_mark)
                self.image.marks.append(mark)

            elif len(marks_in_group) < limit:
                self.image.marks.append(mark)

            galmark.io.save(self.username,self.date,self.images)
            galmark.io.savefav(self.username,self.favorite_list)

    def shift(self,delta:int):
        # Increment the index
        self.idx += delta
        if self.idx > self.N-1:
            self.idx = 0
        elif self.idx < 0:
            self.idx = self.N-1

        self.update_comments()
        self.update_images()
        self.update_marks()
        self.get_comment()
        self.update_categories()
        self.update_favorites()
            
    def enter(self):
        self.update_comments()
        self.comment_box.clearFocus()
        galmark.io.save(self.username,self.date,self.images)
        galmark.io.savefav(self.username,self.favorite_list)

    def middle_mouse(self):
        # Center on cursor
        center = self.image_view.viewport().rect().center()
        scene_center = self.image_view.mapToScene(center)
        pix_pos = self.mouse_pix_pos(correction=False)

        delta = scene_center.toPoint() - pix_pos
        self.image_view.translate(delta.x(),delta.y())

        if self.cursor_focus:
            global_center = self.image_view.mapToGlobal(center)
            self.cursor().setPos(global_center)

    def zoom(self,scale:int=1,mode:str='mouse'):
        # Zoom in on cursor location
        self.zoom_level *= scale
        if mode == 'viewport': center = self.image_view.viewport().rect().center()
        if mode == 'mouse': center = self.mouse_view_pos()

        transform = self.image_view.transform()
        center = self.image_view.mapToScene(center)
        transform.translate(center.x(), center.y())
        transform.scale(scale, scale)
        transform.translate(-center.x(), -center.y())
        self.image_view.setTransform(transform)

    def fit_image(self):
        self.image_view.fitInView(self.image, Qt.AspectRatioMode.KeepAspectRatio)
        self.zoom(scale=9,mode='viewport')

    # === Update methods ===

    def update_favorites(self):
        if self.image.name in self.favorite_list:
            self.favorite_box.setChecked(True)
            self.favorite_box.setIcon(QIcon(HEART_SOLID))
        else:
            self.favorite_box.setIcon(QIcon(HEART_CLEAR))
            self.favorite_box.setChecked(False)

    def update_images(self):
        # Update scene
        _w, _h = self.image.width, self.image.height
        try: self.image.clear_pixmap()
        except: pass
        self.image = self.images[self.idx]
        self.image.__init_item__()
        self.image.seen = True
        self.imageScene.update(self.image)

        # Fit back to view if the image dimensions have changed
        if (self.image.width != _w) or (self.image.height != _h): self.fit_image()
            
        # Update sliders
        self.blur_window.slider.valueChanged.disconnect()
        self.adjust_menu.contrast_slider.valueChanged.disconnect()
        self.adjust_menu.brightness_slider.valueChanged.disconnect()
        self.frame_window.slider.valueChanged.disconnect()

        self.blur_window.slider.valueChanged.connect(self.image.blur)
        self.adjust_menu.contrast_slider.valueChanged.connect(self.image.contrast)
        self.adjust_menu.brightness_slider.valueChanged.connect(self.image.brighten)
        self.frame_window.slider.valueChanged.connect(self.image.seek)

        self.frame_window.slider.setMaximum(self.image.n_frames-1)
        self.blur_max = int((self.image.height+self.image.width)/20)
        self.blur_window.slider.setMaximum(self.blur_max)

        # Update image label
        self.image_label.setText(f'{self.image.name} ({self.idx+1} of {self.N})')
    
    def update_comments(self):
        # Update the comment in the dictionary
        comment = self.comment_box.text()
        if not comment: comment = 'None'

        self.image.comment = comment
        galmark.io.save(self.username,self.date,self.images)
        galmark.io.savefav(self.username,self.favorite_list)

    def get_comment(self):
        if (self.image.comment == 'None'):
            self.comment_box.setText('')
        else:
            comment = self.image.comment
            self.comment_box.setText(comment)

    def update_categories(self):
        # Initialize category and update checkboxes
        for box in self.category_boxes: box.setChecked(False)
        for i in self.image.categories:
            self.category_boxes[i-1].setChecked(True)

    def update_marks(self):
        # Redraws all marks in image
        for mark in self.image.marks: self.imageScene.addItem(mark)

    def del_marks(self):
        pix_pos = self.mouse_pix_pos(correction=False).toPointF()
        selected_items = [ item for item in self.imageScene.items() 
                           if isinstance(item,Mark) 
                           and (item is self.imageScene.itemAt(pix_pos, item.transform()))]
        
        for item in selected_items:
            self.imageScene.removeItem(item)
            self.image.marks.remove(item)
            galmark.io.save(self.username,self.date,self.images)
            galmark.io.savefav(self.username,self.favorite_list)

    # === Utils ===

    def mouse_view_pos(self):
        '''
        Gets mouse positions

        Returns:
            view_pos: position of mouse in the pixmap
        '''
        return self.image_view.mapFromGlobal(self.cursor().pos())
    
    def mouse_pix_pos(self,correction:bool=True):
        '''
        Gets mouse positions

        Returns:
            pix_pos: position of mouse in the pixmap
        '''
        view_pos = self.image_view.mapFromGlobal(self.cursor().pos())
        scene_pos = self.image_view.mapToScene(view_pos)

        # Get the pixel coordinates (including padding; half-pixel offset required)
        pix_pos = self.image.mapFromScene(scene_pos) - QPointF(0.5,0.5)

        # Get the true pixel coordinates (ignoring padding)
        if correction: pix_pos -= 4*QPointF(self.image.width,self.image.height)
        
        return pix_pos.toPoint()

    