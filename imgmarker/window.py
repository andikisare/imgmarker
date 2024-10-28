from PyQt6.QtWidgets import ( QApplication, QMainWindow, QPushButton,
                              QLabel, QScrollArea, QGraphicsView,
                              QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, 
                              QSlider, QLineEdit, QFileDialog )
from PyQt6.QtGui import QAction, QIcon, QFont
from PyQt6.QtCore import Qt, QPoint, QPointF
from imgmarker.mark import Mark
from imgmarker import __dirname__, ICON, HEART_SOLID, HEART_CLEAR
import imgmarker.io
import imgmarker.image
from imgmarker.widget import QHLine, PosWidget
import sys
import os
import datetime as dt
import textwrap
from math import floor, inf, nan
from functools import partial

class AdjustmentsWindow(QWidget):
    """Class for the brightness and contrast window."""
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
        self._slider_setup(self.brightness_slider,self.brightness_moved,self.brightness_changed)

        self.brightness_label = QLabel()
        self.brightness_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.brightness_label.setText(f'Brightness: {self.brightness_slider.value()}')
        
        # Contrast slider
        self.contrast_slider = QSlider()
        self._slider_setup(self.contrast_slider,self.contrast_moved,self.contrast_changed)

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

    def _slider_setup(self,slider:QSlider,moved_connect,value_connect):
        slider.setMinimum(-10)
        slider.setMaximum(10)
        slider.setValue(0)
        slider.setOrientation(Qt.Orientation.Horizontal)
        slider.sliderMoved.connect(moved_connect)
        slider.valueChanged.connect(value_connect)

    def brightness_moved(self,pos):
        self.brightness_slider.setValue(floor(pos))

    def contrast_moved(self,pos):
        self.contrast_slider.setValue(floor(pos))

    def brightness_changed(self,value):
        self.brightness_label.setText(f'Brightness: {floor(self.brightness_slider.value())/10}')

    def contrast_changed(self,value):
        self.contrast_label.setText(f'Contrast: {floor(self.contrast_slider.value())/10}')

    def show(self):
        super().show()
        self.activateWindow()   

class BlurWindow(QWidget):
    """Class for the blur adjustment window."""
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
        self.slider.valueChanged.connect(self.value_changed) 

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

    def value_changed(self,value):
        self.value_label.setText(f'Radius: {floor(self.slider.value())/10}')

    def show(self):
        super().show()
        self.activateWindow()

class FrameWindow(QWidget):
    """Class for the window for switching between frames in an image."""
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
        self.slider.valueChanged.connect(self.value_changed)

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

    def value_changed(self,value):
        self.value_label.setText(f'Frame: {self.slider.value()}')

    def show(self):
        super().show()
        self.activateWindow()

class InstructionsWindow(QWidget):
    """Class for the window that displays the instructions and keymappings."""
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
        actions_list = ['Next','Back','Change frame','Delete','Enter comment', 'Focus', 'Zoom in/out', 'Exit', 'Help']
        group_list = [f'Group \"{group}\"' for group in groupNames[1:]]
        actions_list = group_list + actions_list
        buttons_list = ['Left click OR 1', '2', '3', '4', '5', '6', '7', '8', '9', 'Tab', 'Shift+Tab', 'Spacebar', 'Right click OR Backspace', 'Enter', 'Middle click', 'Scroll wheel', 'Esc OR Q', 'F1', ]

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
    """Class for the startup window"""
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(ICON))
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def getUser(self) -> None:
        # Make popup to get name
        text, OK = self.getText(self,"Startup", "Enter a username (no caps, no space, e.g. ryanwalker)")

        if not OK: sys.exit()
        elif not text.isalnum(): raise imgmarker.io.SAVE_ALPHANUM_ERR 
        else: return text

class MainWindow(QMainWindow):
    """Class for the main window"""
    def __init__(self, username:str):
        super().__init__()
        self.setWindowTitle("Image Marker")
        self.setWindowIcon(QIcon(ICON))
        self.fullw = self.screen().size().width()
        self.fullh = self.screen().size().height()
        self.zoom_level = 1
        self.cursor_focus = False
        self.frame = 0
    
        # Initialize data
        self.username = username
        self.date = dt.datetime.now(dt.UTC).date().isoformat()
        self.__init_data__()
        self.image_scene = imgmarker.image.ImageScene(self.image)

        # Setup child windows
        self.blur_window = BlurWindow()
        self.blur_window.slider.valueChanged.connect(self.image.blur)
        
        self.adjust_window = AdjustmentsWindow()
        self.adjust_window.contrast_slider.valueChanged.connect(self.image.contrast)
        self.adjust_window.brightness_slider.valueChanged.connect(self.image.brighten)
        
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
        if self.image.wcs == None: 
            self.pos_widget.wcs_label.hide()
            self.pos_widget.ra_text.hide()
            self.pos_widget.dec_text.hide()
        else:
            self.pos_widget.wcs_label.show()
            self.pos_widget.ra_text.show()
            self.pos_widget.dec_text.show()

        # Create image view
        self.image_view = QGraphicsView(self.image_scene)
        self.fitview()   
        
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
        #self.submit_button.setShortcut('Return')
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
        self.category_boxes = [QCheckBox(text=imgmarker.io.CATEGORY_NAMES[i], parent=self) for i in range(1,6)]
        for i, box in enumerate(self.category_boxes):
            box.setFixedHeight(20)
            box.setStyleSheet("margin-left:30%; margin-right:30%;")
            box.clicked.connect(partial(self.categorize,i+1))
            box.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.categories_layout.addWidget(box)

        # Favorite box
        self.favorite_list = imgmarker.io.loadfav(username)
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
        open_menu = QAction('&Open save directory', self)
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

        ### Open external marks file
        open_ext_marks_menu = QAction('&Open external marks file', self)
        open_ext_marks_menu.setShortcuts(['Ctrl+Shift+m'])
        open_ext_marks_menu.setStatusTip('Open external marks file')
        open_ext_marks_menu.triggered.connect(self.open_ext_marks)
        file_menu.addAction(open_ext_marks_menu)
        self.ext_mark_coord_sys = None
        self.ext_mark_labels = []
        self.ext_mark_alphas = []
        self.ext_mark_betas = []

        ## Edit menu
        edit_menu = menu_bar.addMenu("&Edit")

        ### Delete marks menu
        del_menu = QAction('&Delete all marks', self)
        del_menu.setStatusTip('Delete all marks')
        del_menu.triggered.connect(partial(self.del_marks,True))
        edit_menu.addAction(del_menu)

        ## View menu
        view_menu = menu_bar.addMenu("&View")

        ### Frame menu
        frame_menu = QAction('&Frames...', self)
        frame_menu.setShortcuts(['Ctrl+f'])
        frame_menu.setStatusTip('Frames...')
        frame_menu.triggered.connect(self.frame_window.show)
        view_menu.addAction(frame_menu)

        ### Toggle marks menu
        self.marks_menu = QAction('&Marks visible', self)
        self.marks_menu.setShortcuts(['Ctrl+m'])
        self.marks_menu.setStatusTip('Marks visible')
        self.marks_menu.setCheckable(True)
        self.marks_menu.setChecked(True)
        self.marks_menu.triggered.connect(self.toggle_marks)
        view_menu.addAction(self.marks_menu)

        ### Toggle mark labels menu
        self.mark_labels_menu = QAction('&Mark labels visible', self)
        self.mark_labels_menu.setShortcuts(['Ctrl+l'])
        self.mark_labels_menu.setStatusTip('Mark labels visible')
        self.mark_labels_menu.setCheckable(True)
        self.mark_labels_menu.setChecked(True)
        self.mark_labels_menu.triggered.connect(self.toggle_mark_labels)
        view_menu.addAction(self.mark_labels_menu)

        if len(self.image.marks) == 0:
            self.marks_menu.setEnabled(False)
            self.mark_labels_menu.setEnabled(False)
        else:
            self.marks_menu.setEnabled(True)
            self.mark_labels_menu.setEnabled(True)

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
        adjust_menu.triggered.connect(self.adjust_window.show)
        filter_menu.addAction(adjust_menu)

        ## Help menu
        help_menu = menu_bar.addMenu('&Help')

        ### Instructions and Keymapping window
        self.instructions_window = InstructionsWindow(imgmarker.io.GROUP_NAMES)
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
        """Initializes images."""
        # Initialize output dictionary
        self.images = imgmarker.io.load(self.username)
        
        self.favorite_list = imgmarker.io.loadfav(self.username)

        # Find all images in image directory

        try: self.image.clear()
        except: pass
        
        try:
            self.images, self.idx = imgmarker.io.glob(edited_images=self.images)
            self.image = self.images[self.idx]
            self.image.seek(self.frame)
            self.image.seen = True
            self.N = len(self.images)
        except:
            # sys.exit(f"No images of type '{self.imtype}' found in directory: '{self.image_dir}'.\n"
            #          f"Please specify a different image directory in imgmarker.cfg and try again.")
            image_dir = os.path.join(QFileDialog.getExistingDirectory(self, "Open correct image directory", imgmarker.io.IMAGE_DIR),'')
            imgmarker.io.update_config(image_dir=image_dir)
            self.images, self.idx = imgmarker.io.glob(edited_images=self.images)
            self.image = self.images[self.idx]
            self.image.seek(self.frame)
            self.image.seen = True
            self.N = len(self.images)

    def inview(self,x,y):
        """Checks if x and y are within the image."""
        return (x>=0) and (x<=self.image.width-1) and (y>=0) and  (y<=self.image.height-1)

    # === Events ===

    def eventFilter(self, source, event):
        # Event filter for zooming without scrolling
        if (source == self.image_view.viewport()) and (event.type() == 31):
            x = event.angleDelta().y()
            if x > 0: self.zoom(1/1.2)
            elif x < 0: self.zoom(1.2)
            return True

        return super().eventFilter(source, event)

    def keyPressEvent(self,event):
        # Check if key is bound with marking the image
        markButtons = imgmarker.io.check_marks(event)
        for i in range(0,9):
            if markButtons[i]: self.mark(group=i+1)

        if (event.key() == Qt.Key.Key_Backspace) or (event.key() == Qt.Key.Key_Delete):
            self.del_marks()

        if (event.key() == Qt.Key.Key_Space):
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.KeyboardModifier.ShiftModifier:
                self.image.seek(self.frame-1)
            else:
                self.image.seek(self.frame+1)

            self.frame = self.image.tell()
            self.frame_window.slider.setValue(self.frame)

    def mousePressEvent(self,event):
        # Check if key is bound with marking the image
        markButtons = imgmarker.io.check_marks(event)
        for i in range(0,9):
            if markButtons[i]: self.mark(group=i+1)
        
        if (event.button() == Qt.MouseButton.MiddleButton):
            self.center_cursor()

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
    def open(self) -> None:
        """Method for the open save directory dialog."""
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        saveDir = dialog.getExistingDirectory(self, 'Open save directory', os.getcwd())
        if (saveDir == ''): return
        
        self.username = str(os.path.split(saveDir)[-1])
        if not self.username.isalnum(): raise imgmarker.io.SAVE_ALPHANUM_ERR
        
        self.__init_data__()
        self.update_images()
        self.update_marks()
        self.get_comment()
        self.update_categories()
        self.update_comments()
        self.update_favorites()

    def open_ims(self) -> None:
        """Method for the open image directory dialog."""
        image_dir = os.path.join(QFileDialog.getExistingDirectory(self, "Open image directory", imgmarker.io.IMAGE_DIR),'')
        if (image_dir == ''): return
        imgmarker.io.update_config(image_dir=image_dir)
        self.images, self.idx = imgmarker.io.glob(edited_images=[])
        self.N = len(self.images)
        
        self.update_images()
        self.update_marks()
        self.get_comment()
        self.update_categories()
        self.update_comments()

    def open_ext_marks(self):
        ext_mark_file = QFileDialog.getOpenFileName(self, 'Select external marks file', os.getcwd(), '*.txt')[0]
        if (ext_mark_file == ''): return
        
        labels, alphas, betas, coord_sys = imgmarker.io.load_ext_marks(ext_mark_file)
        self.ext_mark_labels = labels
        self.ext_mark_alphas = alphas
        self.ext_mark_betas = betas
        self.ext_mark_coord_sys = coord_sys

        if labels == None:
            return
        
        else:
            self.update_ext_marks()

        return

    def favorite(self,state) -> None:
        """Favorite the current image."""
        state = Qt.CheckState(state)
        if state == Qt.CheckState.PartiallyChecked:
            self.favorite_box.setIcon(QIcon(HEART_SOLID))
            self.favorite_list.append(self.image.name)
            imgmarker.io.savefav(self.username,self.date,self.images,self.favorite_list)
        else:
            self.favorite_box.setIcon(QIcon(HEART_CLEAR))
            if self.image.name in self.favorite_list: 
                self.favorite_list.remove(self.image.name)
            imgmarker.io.savefav(self.username,self.date,self.images,self.favorite_list)

    def categorize(self,i:int) -> None:
        """Categorize the current image"""
        if (self.category_boxes[i-1].checkState() == Qt.CheckState.Checked) and (i not in self.image.categories):
            self.image.categories.append(i)
        elif (i in self.image.categories):
            self.image.categories.remove(i)
        imgmarker.io.save(self.username,self.date,self.images)
        imgmarker.io.savefav(self.username,self.date,self.images,self.favorite_list)

    def mark(self, group:int=0) -> None:
        """Add a mark to the current image."""

        # get event position and position on image
        pix_pos = self.mouse_pix_pos()
        x, y = pix_pos.x(), pix_pos.y()
        
        # Mark if hovering over image
        if imgmarker.io.GROUP_MAX[group - 1] == 'None': limit = inf
        else: limit = int(imgmarker.io.GROUP_MAX[group - 1])

        marks_in_group = [m for m in self.image.marks if m.g == group]

        if len(self.image.marks) >= 1: self.image.marks[-1].label.enter()

        if self.inview(x,y):
            mark = self.image_scene.mark(x,y,group=group)
            
            if (limit == 1) and (len(marks_in_group) == 1):
                prev_mark = marks_in_group[0]
                self.image_scene.rmmark(prev_mark)
                self.image.marks.remove(prev_mark)
                self.image.marks.append(mark)

            elif len(marks_in_group) < limit:
                self.image.marks.append(mark)

            imgmarker.io.save(self.username,self.date,self.images)
            imgmarker.io.savefav(self.username,self.date,self.images,self.favorite_list)
        
        if len(self.image.marks) == 0:
            self.marks_menu.setEnabled(False)
            self.mark_labels_menu.setEnabled(False)
        else:
            self.marks_menu.setEnabled(True)
            self.mark_labels_menu.setEnabled(True)

    def shift(self,delta:int):
        """Move back or forward *delta* number of images."""
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
        """Enter the text in the comment box into the image."""
        self.update_comments()
        self.comment_box.clearFocus()
        imgmarker.io.save(self.username,self.date,self.images)
        imgmarker.io.savefav(self.username,self.date,self.images,self.favorite_list)

    def center_cursor(self):
        """Center on the cursor."""
        center = self.image_view.viewport().rect().center()
        scene_center = self.image_view.mapToScene(center)
        pix_pos = self.mouse_pix_pos(correction=False)

        delta = scene_center.toPoint() - pix_pos
        self.image_view.translate(delta.x(),delta.y())

        if self.cursor_focus:
            global_center = self.image_view.mapToGlobal(center)
            self.cursor().setPos(global_center)

    def zoom(self,scale:float,mode:str='mouse'):
        """
        Zoom in on the image.

        Parameters
        ----------
        scale: str
            Scale of the zoom. Greater than 1 means zooming in, less than 1 means zooming out
        mode: str, optional
            Zoom mode. To zoom from the center of the viewport, use mode='viewport'. To zoom from the mouse
            cursor location, use mode='mouse'. Defaults to 'mouse'.
        
        Returns
        ----------
        None
        """
        if self.zoom_level*scale > 1/3:
            self.zoom_level *= scale
            if mode == 'viewport': center = self.image_view.viewport().rect().center()
            if mode == 'mouse': center = self.mouse_view_pos()

            transform = self.image_view.transform()
            center = self.image_view.mapToScene(center)
            transform.translate(center.x(), center.y())
            transform.scale(scale, scale)
            transform.translate(-center.x(), -center.y())
            self.image_view.setTransform(transform)

    def fitview(self):
        """Fit the image view in the viewport."""
        self.image_view.fitInView(self.image, Qt.AspectRatioMode.KeepAspectRatio)
        self.zoom(scale=9,mode='viewport')
        self.zoom_level = 1

    # === Update methods ===

    def update_ext_marks(self):
        """Loads in each external mark to the appropriate image if RA, Dec, otherwise loads all."""
        labels = self.ext_mark_labels
        alphas = self.ext_mark_alphas
        betas = self.ext_mark_betas

        for i in range(len(labels)):
            for img in self.images:
                if self.ext_mark_coord_sys == 'galactic':
                    ra, dec = alphas[i], betas[i]
                    
                    mark_coord_cart = img.wcs.all_world2pix([[ra,dec]], 0)[0]
                    x, y = mark_coord_cart[0], img.height - mark_coord_cart[1]

                else: x, y = alphas[i], betas[i]

                if self.inview(x,y):
                    mark = Mark(x, y, shape='rect', image=img, text=labels[i])
                    img.ext_marks.append(mark)

        for mark in self.image.ext_marks: self.image_scene.mark(mark)

    def update_favorites(self):
        """Update favorite boxes based on the contents of favorite_list."""
        if self.image.name in self.favorite_list:
            self.favorite_box.setChecked(True)
            self.favorite_box.setIcon(QIcon(HEART_SOLID))
        else:
            self.favorite_box.setIcon(QIcon(HEART_CLEAR))
            self.favorite_box.setChecked(False)

    def update_images(self):
        """Updates previous image with a new image."""
        # Disconnect sliders from previous image
        try:
            self.blur_window.slider.valueChanged.disconnect(self.image.blur)
            self.adjust_window.contrast_slider.valueChanged.disconnect(self.image.contrast)
            self.adjust_window.brightness_slider.valueChanged.disconnect(self.image.brighten)
            self.frame_window.slider.valueChanged.disconnect(self.image.seek)
        except: pass

        # Update scene
        _w, _h = self.image.width, self.image.height
        try: self.image.clear()
        except: pass

        self.image = self.images[self.idx]
        self.image.seek(self.frame)
        self.image.seen = True
        self.image_scene.update(self.image)

        # Fit back to view if the image dimensions have changed
        if (self.image.width != _w) or (self.image.height != _h): self.fitview()

        # Update position widget
        if self.image.wcs == None: 
            self.pos_widget.wcs_label.hide()
            self.pos_widget.ra_text.hide()
            self.pos_widget.dec_text.hide()
        else:
            self.pos_widget.wcs_label.show()
            self.pos_widget.ra_text.show()
            self.pos_widget.dec_text.show()
             
        # Update sliders
        self.blur_window.slider.setValue(0)
        self.adjust_window.contrast_slider.setValue(0)
        self.adjust_window.brightness_slider.setValue(0)
        self.frame_window.slider.setValue(self.frame)

        self.blur_window.slider.valueChanged.connect(self.image.blur)
        self.adjust_window.contrast_slider.valueChanged.connect(self.image.contrast)
        self.adjust_window.brightness_slider.valueChanged.connect(self.image.brighten)
        self.frame_window.slider.valueChanged.connect(self.image.seek)

        self.frame_window.slider.setMaximum(self.image.n_frames-1)
        self.blur_max = int((self.image.height+self.image.width)/20)
        self.blur_window.slider.setMaximum(self.blur_max)

        # Update image label
        self.image_label.setText(f'{self.image.name} ({self.idx+1} of {self.N})')

        # Update menus
        if len(self.image.marks) == 0:
            self.marks_menu.setEnabled(False)
            self.mark_labels_menu.setEnabled(False)
        else:
            self.marks_menu.setEnabled(True)
            self.mark_labels_menu.setEnabled(True)

        self.toggle_marks()
        self.toggle_mark_labels()
    
    def update_comments(self):
        """Updates image comment with the contents of the comment box."""
        comment = self.comment_box.text()
        if not comment: comment = 'None'

        self.image.comment = comment
        imgmarker.io.save(self.username,self.date,self.images)
        imgmarker.io.savefav(self.username,self.date,self.images,self.favorite_list)

    def get_comment(self):
        """If the image has a comment, sets the text of the comment box to the image's comment"""
        if (self.image.comment == 'None'):
            self.comment_box.setText('')
        else:
            comment = self.image.comment
            self.comment_box.setText(comment)

    def update_categories(self):
        """Resets all category boxes to unchecked, then checks the boxes based on the current image's categories"""
        for box in self.category_boxes: box.setChecked(False)
        for i in self.image.categories:
            self.category_boxes[i-1].setChecked(True)

    def update_marks(self):
        """Redraws all marks in image"""
        for mark in self.image.marks: self.image_scene.mark(mark)
        for mark in self.image.ext_marks: self.image_scene.mark(mark)

    def del_marks(self,del_all=False):
        if not del_all:
            pix_pos = self.mouse_pix_pos(correction=False).toPointF()
            selected_items = [item for item in self.image.marks 
                              if item is self.image_scene.itemAt(pix_pos, item.transform())]
        else: selected_items = self.image.marks.copy()

        for item in selected_items:
            self.image_scene.rmmark(item)
            self.image.marks.remove(item)
        
        if len(self.image.marks) == 0:
            self.marks_menu.setEnabled(False)
            self.mark_labels_menu.setEnabled(False)
            
        imgmarker.io.save(self.username,self.date,self.images)
        imgmarker.io.savefav(self.username,self.date,self.images,self.favorite_list)

    def toggle_marks(self):
        state = self.marks_menu.isChecked()
        for item in self.image.marks:
            if state: 
                item.show()
                if self.mark_labels_menu.isChecked(): item.label.show()
            else: 
                item.hide()
                item.label.hide()

    def toggle_mark_labels(self):
        state = self.mark_labels_menu.isChecked()
        for item in self.image.marks:
            if state: item.label.show()
            else: item.label.hide()

    # === Utils ===

    def mouse_view_pos(self):
        """
        Gets mouse position.

        Returns
        ----------
        view_pos: `QPoint`
            position of mouse in the image view.
        """
        return self.image_view.mapFromGlobal(self.cursor().pos())
    
    def mouse_pix_pos(self,correction:bool=True):
        """
        Gets mouse position.

        Returns
        ----------
        pix_pos: `QPoint`
            position of mouse in the image.
        """
        view_pos = self.image_view.mapFromGlobal(self.cursor().pos())
        scene_pos = self.image_view.mapToScene(view_pos)

        # Get the pixel coordinates (including padding; half-pixel offset required)
        pix_pos = self.image.mapFromScene(scene_pos)

        # Get the true pixel coordinates (ignoring padding)
        if correction: pix_pos -= 4*QPointF(self.image.width,self.image.height) + QPointF(0.5,0.5)
        
        return pix_pos.toPoint()

    