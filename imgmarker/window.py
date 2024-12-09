from .pyqt import ( QApplication, QMainWindow, QPushButton,
                    QLabel, QScrollArea, QGraphicsView,
                    QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QCheckBox, 
                    QSlider, QLineEdit, QFileDialog, QIcon, QFont, QAction, Qt, QPoint, QPointF, QSpinBox, PYQT_VERSION_STR)

from . import ICON, HEART_SOLID, HEART_CLEAR, SCREEN_WIDTH, SCREEN_HEIGHT, __version__, __license__
from . import io
from . import image
from .widget import QHLine, PosWidget, RestrictedLineEdit
from .catalog import Catalog
import sys
import datetime as dt
import textwrap
from math import floor, inf, nan
from numpy import argsort
from functools import partial
from typing import Union, List

class SettingsWindow(QWidget):
    """Class for the window for settings."""

    def __init__(self,mainwindow:'MainWindow'):
        super().__init__()
        
        self.setWindowIcon(QIcon(ICON))
        layout = QVBoxLayout()
        self.setWindowTitle('Settings')
        self.setLayout(layout)
        self.mainwindow = mainwindow

        # Groups
        self.group_label = QLabel()
        self.group_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.group_label.setText('Groups')

        self.group_boxes = []
        for i in range(1,10):
            lineedit = RestrictedLineEdit([Qt.Key.Key_Comma])
            lineedit.setPlaceholderText(io.GROUP_NAMES[i])
            lineedit.setFixedHeight(30)
            lineedit.setText(io.GROUP_NAMES[i])
            self.group_boxes.append(lineedit)

        self.group_layout = QHBoxLayout()
        for box in self.group_boxes: self.group_layout.addWidget(box)

        # Max marks per group
        self.max_label = QLabel()
        self.max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.max_label.setText('Max marks per group')

        self.max_boxes = []
        for i in range(0,9):
            spinbox = QSpinBox()
            spinbox.setSpecialValueText('-')
            spinbox.setFixedHeight(30)
            spinbox.setMaximum(9)
            value:str = io.GROUP_MAX[i]
            if value.isnumeric(): spinbox.setValue(int(value))
            spinbox.valueChanged.connect(self.update_config)
            self.max_boxes.append(spinbox)

        self.max_layout = QHBoxLayout()
        for box in self.max_boxes: self.max_layout.addWidget(box)

        # Categories
        self.category_label = QLabel()
        self.category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.category_label.setText('Categories')

        self.category_boxes = []
        for i in range(1,6):
            lineedit = RestrictedLineEdit([Qt.Key.Key_Comma])
            lineedit.setPlaceholderText(io.CATEGORY_NAMES[i])
            lineedit.setFixedHeight(30)
            lineedit.setText(io.CATEGORY_NAMES[i])
            self.category_boxes.append(lineedit)

        self.category_layout = QHBoxLayout()
        for box in self.category_boxes: self.category_layout.addWidget(box)

        # Options
        self.focus_box = QCheckBox(text='Middle-click to focus centers the cursor', parent=self)
        self.randomize_box = QCheckBox(text='Randomize order of images', parent=self)
        self.randomize_box.setChecked(io.RANDOMIZE_ORDER)

        # Main layout
        layout.addWidget(self.group_label)
        layout.addLayout(self.group_layout)
        layout.addWidget(self.max_label)
        layout.addLayout(self.max_layout)
        layout.addWidget(QHLine())
        layout.addWidget(self.category_label)
        layout.addLayout(self.category_layout)
        layout.addWidget(QHLine())
        layout.addWidget(self.focus_box)
        layout.addWidget(self.randomize_box)
        layout.addWidget(QHLine())
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedWidth(int(SCREEN_WIDTH/3))
        self.setFixedHeight(layout.sizeHint().height())

        # Set position of window
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def show(self):
        super().show()
        self.activateWindow()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            for i, box in enumerate(self.group_boxes): box.clearFocus()
            for i, box in enumerate(self.category_boxes): box.clearFocus()
            for box in self.max_boxes: box.clearFocus()

            self.update_config()

        return super().keyPressEvent(event)
    
    def closeEvent(self, a0):
        for box in self.group_boxes: box.clearFocus()
        for box in self.category_boxes: box.clearFocus()
        for box in self.max_boxes: box.clearFocus()

        self.update_config()
        self.mainwindow.save()
        return super().closeEvent(a0)
    
    def update_config(self):
        group_names_old = io.GROUP_NAMES.copy()

        # Get the new settings from the boxes
        io.GROUP_NAMES = ['None'] + [box.text() for box in self.group_boxes]
        io.GROUP_MAX = [str(box.value()) if box.value() != 0 else 'None' for box in self.max_boxes]
        io.CATEGORY_NAMES = ['None'] + [box.text() for box in self.category_boxes]
        io.RANDOMIZE_ORDER = self.randomize_box.isChecked()

        for i, box in enumerate(self.mainwindow.category_boxes): box.setText(io.CATEGORY_NAMES[i+1])

        # Update mark labels that haven't been changed
        for image in self.mainwindow.images:
            for mark in image.marks:
                if mark.label.lineedit.text() in group_names_old:
                    mark.label.lineedit.setText(io.GROUP_NAMES[mark.g])

        # Update text in the instructions window 
        self.mainwindow.instructions_window.update_text()

        # Save the new settings into the config file
        io.update_config()

class BlurWindow(QWidget):
    """Class for the blur adjustment window."""

    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(QIcon(ICON))
        layout = QVBoxLayout()
        self.setWindowTitle('Gaussian Blur')
        self.setLayout(layout)

        self.slider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.valueChanged.connect(self.slider_moved) 
        self.slider.setPageStep(0)

        self.value_label = QLabel()
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setText(f'Radius: {self.slider.value()}')

        layout.addWidget(self.value_label)
        layout.addWidget(self.slider)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedWidth(int(SCREEN_WIDTH/6))
        self.setFixedHeight(layout.sizeHint().height())

        # Set position of window
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

    def slider_moved(self, pos):
        self.value_label.setText(f'Radius: {floor(pos)/10}')

    def show(self):
        super().show()
        self.activateWindow()

class FrameWindow(QWidget):
    """Class for the window for switching between frames in an image."""

    def __init__(self):
        super().__init__()
        
        self.setWindowIcon(QIcon(ICON))
        layout = QVBoxLayout()
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
        self.setFixedWidth(int(SCREEN_WIDTH/6))
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

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(ICON))
        layout = QVBoxLayout()
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

        self.update_text()

        # Add scroll area to layout, get size of layout
        layout.addWidget(self.scroll_area)
        layout_width, layout_height = layout.sizeHint().width(), layout.sizeHint().height()

        # Resize window according to size of layout
        self.resize(int(layout_width*1.1),int(layout_height*1.1))

    def update_text(self):
        # Lists for keybindings
        actions_list = ['Next','Back','Change frame','Delete','Enter comment', 'Focus', 'Zoom in/out', 'Favorite', 'Exit', 'Help']
        group_list = [f'Group \"{group}\"' for group in io.GROUP_NAMES[1:]]
        category_list = [f'Category \"{category}\"' for category in io.CATEGORY_NAMES[1:]]
        actions_list = group_list + category_list + actions_list
        buttons_list = ['Left click OR 1', '2', '3', '4', '5', '6', '7', '8', '9', 'Ctrl+1', 'Ctrl+2', 'Ctrl+3', 'Ctrl+4', 'Ctrl+5', 'Tab', 'Shift+Tab', 'Spacebar', 'Right click OR Backspace', 'Enter', 'Middle click', 'Scroll wheel', 'F', 'Ctrl+Q', 'F1', ]

        # Determing widths for keybindings list
        actions_width = max([len(a) for a in actions_list])
        buttons_width = max([len(b) for b in buttons_list]) + 10
        fullw_text = actions_width + buttons_width

        # Create text
        text = 'All changes are autosaved.'
        text = textwrap.wrap(text, width=fullw_text)
        text = '\n'.join([f'{l:<{fullw_text}}' for l in text]) + '\n'
        text += '-'*(fullw_text) + '\n'
        text += f"{'Keybindings':^{fullw_text}}\n"
        text += '-'*(fullw_text) + '\n'
        for i in range(0,len(actions_list)):
            text += f'{actions_list[i]:.<{actions_width}}{buttons_list[i]:.>{buttons_width}}\n'
        self.label.setText(text)

    def show(self):
        """Shows the window and moves it to the front."""

        super().show()
        self.activateWindow()

class AboutWindow(QWidget):
    """Class for the window that displays information about Image Marker."""

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(ICON))
        layout = QVBoxLayout()
        self.setWindowTitle('About')
        self.setLayout(layout)

        # Create text
        font = QFont('Courier')
        self.layouts = [QHBoxLayout(),QHBoxLayout(),QHBoxLayout(),QHBoxLayout()]
        params = ['Version','PyQt Version','License','Authors']
        labels = [QLabel(f'<div>{__version__}</div>'),
                  QLabel(f'<div>{PYQT_VERSION_STR}</div>'),
                  QLabel(f'<div><a href="https://opensource.org/license/mit">{__license__}</a></div>'),
                  QLabel(f'<div>Andi Kisare and Ryan Walker</div>')]

        for label, param in zip(labels, params):
            param_layout = QHBoxLayout()

            param_label = QLabel(f'{param}:')
            param_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            param_label.setFont(font)

            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label.setFont(font)
            if param != 'License': label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            else: label.setOpenExternalLinks(True)

            param_layout.addWidget(param_label)
            param_layout.addWidget(label)
            param_layout.addStretch(1)
            layout.addLayout(param_layout)

        # Add scroll area to layout, get size of layout
        layout_width, layout_height = layout.sizeHint().width(), layout.sizeHint().height()

        # Resize window according to size of layout
        self.setFixedSize(int(layout_width*1.1),int(layout_height*1.1))       

        # Set position of window
        qt_rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().geometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft()) 

    def show(self):
        """Shows the window and moves it to the front."""

        super().show()
        self.activateWindow()

class MainWindow(QMainWindow):
    """Class for the main window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Marker")
        self.setWindowIcon(QIcon(ICON))

        self.zoom_level = 1
        self.cursor_focus = False
        self.frame = 0
    
        # Initialize data
        self.date = dt.datetime.now(dt.timezone.utc).date().isoformat()
        self.order = []
        self.catalogs:List['Catalog'] = []
        self.__init_data__()
        self.image_scene = image.ImageScene(self.image)

        # Setup child windows
        self.blur_window = BlurWindow()
        self.blur_window.slider.sliderReleased.connect(partial(self.image.blur,self.blur_window.slider.sliderPosition))
        
        self.frame_window = FrameWindow()
        self.frame_window.slider.valueChanged.connect(self.image.seek)
        self.frame_window.slider.setMaximum(self.image.n_frames-1)

        self.settings_window = SettingsWindow(self)
        self.settings_window.focus_box.stateChanged.connect(partial(setattr,self,'cursor_focus'))
        self.settings_window.randomize_box.stateChanged.connect(self.toggle_randomize)

        self.instructions_window = InstructionsWindow()
        self.about_window = AboutWindow()

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
        self.category_shortcuts = ['Ctrl+1', 'Ctrl+2', 'Ctrl+3', 'Ctrl+4', 'Ctrl+5']
        self.category_boxes = [QCheckBox(text=io.CATEGORY_NAMES[i], parent=self) for i in range(1,6)]
        for i, box in enumerate(self.category_boxes):
            box.setFixedHeight(20)
            box.setStyleSheet("margin-left:30%; margin-right:30%;")
            box.clicked.connect(partial(self.categorize,i+1))
            box.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            box.setShortcut(self.category_shortcuts[i])
            self.categories_layout.addWidget(box)

        # Favorite box
        self.favorite_list = io.loadfav()
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
        menubar = self.menuBar()

        ## File menu
        file_menu = menubar.addMenu("&File")

        ### Open menus
        open_menu = file_menu.addMenu('&Open')

        ### Open file menu
        open_action = QAction('&Open save...', self)
        open_action.setShortcuts(['Ctrl+o'])
        open_action.triggered.connect(self.open)
        open_menu.addAction(open_action)

        ### Open image folder menu
        open_ims_action = QAction('&Open images...', self)
        open_ims_action.setShortcuts(['Ctrl+Shift+o'])
        open_ims_action.triggered.connect(self.open_ims)
        open_menu.addAction(open_ims_action)

        ### Open catalog file
        open_marks_action = QAction('&Open catalog...', self)
        open_marks_action.setShortcuts(['Ctrl+Shift+m'])
        open_marks_action.triggered.connect(self.open_catalog)
        open_menu.addAction(open_marks_action)
        
        ### Exit menu
        file_menu.addSeparator()
        exit_action = QAction('&Exit', self)
        exit_action.setShortcuts(['Ctrl+q'])
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        ## Edit menu
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.setToolTipsVisible(True)

        ### Delete marks menu
        del_menu = QAction('&Delete all marks', self)
        del_menu.triggered.connect(partial(self.del_marks,True))
        edit_menu.addAction(del_menu)

        ### Randomize image order menu
        edit_menu.addSeparator()
        settings_action = QAction('&Settings...', self)
        settings_action.setShortcuts(['Ctrl+,'])
        settings_action.setToolTip('Randomize the order in which images appear')
        settings_action.triggered.connect(self.settings_window.show)
        edit_menu.addAction(settings_action)

        ## View menu
        view_menu = menubar.addMenu("&View")

        ### Frame menu
        frame_action = QAction('&Frames...', self)
        frame_action.setShortcuts(['Ctrl+f'])
        frame_action.triggered.connect(self.frame_window.show)
        view_menu.addAction(frame_action)

        ### Toggle marks menu
        view_menu.addSeparator()
        self.marks_action = QAction('&Show marks', self)
        self.marks_action.setShortcuts(['Ctrl+m'])
        self.marks_action.setCheckable(True)
        self.marks_action.setChecked(True)
        self.marks_action.triggered.connect(self.toggle_marks)
        view_menu.addAction(self.marks_action)

        ### Toggle mark labels menu
        self.labels_action = QAction('&Show mark labels', self)
        self.labels_action.setShortcuts(['Ctrl+l'])
        self.labels_action.setCheckable(True)
        self.labels_action.setChecked(True)
        self.labels_action.triggered.connect(self.toggle_mark_labels)
        view_menu.addAction(self.labels_action)

        ### Toggle catalogs menu
        self.catalogs_action = QAction('&Show catalog', self)
        self.catalogs_action.setShortcuts(['Ctrl+Shift+m'])
        self.catalogs_action.setCheckable(True)
        self.catalogs_action.setChecked(True)
        self.catalogs_action.triggered.connect(self.toggle_catalogs)
        view_menu.addAction(self.catalogs_action)
        self.catalogs_action.setEnabled(False)

        ### Toggle catalog labels menu
        self.catalog_labels_action = QAction('&Show catalog labels', self)
        self.catalog_labels_action.setShortcuts(['Ctrl+Shift+l'])
        self.catalog_labels_action.setCheckable(True)
        self.catalog_labels_action.setChecked(True)
        self.catalog_labels_action.triggered.connect(self.toggle_catalog_labels)
        view_menu.addAction(self.catalog_labels_action)
        self.catalog_labels_action.setEnabled(False)

        if len(self.image.marks) == 0:
            self.marks_action.setEnabled(False)
            self.labels_action.setEnabled(False)
        else:
            self.marks_action.setEnabled(True)
            self.labels_action.setEnabled(True)

        ## Filter menu
        filter_menu = menubar.addMenu("&Filter")

        ### Blur
        blur_action = QAction('&Gaussian Blur...',self)
        blur_action.setShortcuts(['Ctrl+b'])
        blur_action.triggered.connect(self.blur_window.show)
        filter_menu.addAction(blur_action)

        ### Scale menus
        filter_menu.addSeparator()
        stretch_menu = filter_menu.addMenu('&Stretch')

        linear_action = QAction('&Linear', self)
        linear_action.setCheckable(True)
        linear_action.setChecked(True)
        stretch_menu.addAction(linear_action)

        log_action = QAction('&Log', self)
        log_action.setCheckable(True)
        stretch_menu.addAction(log_action)

        linear_action.triggered.connect(partial(setattr,self,'stretch','linear'))
        linear_action.triggered.connect(partial(linear_action.setChecked,True))
        linear_action.triggered.connect(partial(log_action.setChecked,False))

        log_action.triggered.connect(partial(setattr,self,'stretch','log'))
        log_action.triggered.connect(partial(linear_action.setChecked,False))
        log_action.triggered.connect(partial(log_action.setChecked,True))

        ### Interval menus
        interval_menu = filter_menu.addMenu('&Interval')

        minmax_action = QAction('&Min-Max', self)
        minmax_action.setCheckable(True)
        minmax_action.setChecked(True)
        interval_menu.addAction(minmax_action)

        zscale_action = QAction('&ZScale', self)
        zscale_action.setCheckable(True)
        interval_menu.addAction(zscale_action)

        minmax_action.triggered.connect(partial(setattr,self,'interval','min-max'))
        minmax_action.triggered.connect(partial(minmax_action.setChecked,True))
        minmax_action.triggered.connect(partial(zscale_action.setChecked,False))

        zscale_action.triggered.connect(partial(setattr,self,'interval','zscale'))
        zscale_action.triggered.connect(partial(minmax_action.setChecked,False))
        zscale_action.triggered.connect(partial(zscale_action.setChecked,True))

        ## Help menu
        help_menu = menubar.addMenu('&Help')

        ### Instructions window
        instructions_menu = QAction('&Instructions', self)
        instructions_menu.setShortcuts(['F1'])
        instructions_menu.triggered.connect(self.instructions_window.show)
        help_menu.addAction(instructions_menu)

        ### About window
        about_menu = QAction('&About', self)
        about_menu.triggered.connect(self.about_window.show)
        help_menu.addAction(about_menu)
        
        # Resize and center MainWindow; move instructions off to the right
        self.resize(int(SCREEN_HEIGHT*0.8),int(SCREEN_HEIGHT*0.8))
        
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
        self.images = io.load()
        
        self.favorite_list = io.loadfav()

        # Find all images in image directory

        try: self.image.close()
        except: pass
        
        try:
            self.images, self.idx = io.glob(edited_images=self.images)
            self.image = self.images[self.idx]
            self.image.seek(self.frame)
            self.image.seen = True
            self.N = len(self.images)
            if self.image.name not in self.order:
                self.order.append(self.image.name)
        except:
            io.IMAGE_DIR = io.get_image_dir()
            if io.IMAGE_DIR == None: sys.exit()
            io.update_config()
            
            self.images, self.idx = io.glob(edited_images=self.images)
            self.image = self.images[self.idx]
            self.image.seek(self.frame)
            self.image.seen = True
            self.N = len(self.images)

    @property
    def interval(self): return self._interval_str
    @interval.setter
    def interval(self,value):
        self._interval_str = value
        for img in self.images: img.interval = value
        self.image.rescale()
        
    @property
    def stretch(self): return self._stretch_str
    @stretch.setter
    def stretch(self,value):
        self._stretch_str = value
        for img in self.images: img.stretch = value
        self.image.rescale()

    def inview(self,x:Union[int,float],y:Union[int,float]):
        """
        Checks if x and y are contained within the image.

        Parameters
        ----------
        x: int OR float
            x coordinate
        y: int OR float
            y coordinate

        Returns
        ----------
        True if the (x,y) is contained within the image, False otherwise.
        """

        return (x>=0) and (x<=self.image.width-1) and (y>=0) and  (y<=self.image.height-1)

    # === Events ===

    def eventFilter(self, source, event):
        """
        Perform operations based on the event source and type.

        Parameters
        ----------
        source: `QObject` object
            Source of the event
        event: `QEvent` object
            Event

        Returns
        ----------
        True if the event triggered an some operation.
        """

        if (source == self.image_view.viewport()) and (event.type() == 31):
            x = event.angleDelta().y()
            if x > 0: self.zoom(1/1.2)
            elif x < 0: self.zoom(1.2)
            return True

        return super().eventFilter(source, event)

    def keyPressEvent(self,event):
        """Checks which keyboard button was pressed and calls the appropriate function."""
        
        # Check if key is bound with marking the image
        for group, binds in io.MARK_KEYBINDS.items():
            if event.key() in binds: self.mark(group=group)

        if (event.key() == Qt.Key.Key_Backspace) or (event.key() == Qt.Key.Key_Delete):
            self.del_marks()

        if (event.key() == Qt.Key.Key_Space):
            modifiers = QApplication.keyboardModifiers()
            if modifiers == Qt.KeyboardModifier.ShiftModifier:
                self.image.seek(self.frame-1)
            else:
                self.image.seek(self.frame+1)

            self.frame = self.image.frame
            self.frame_window.slider.setValue(self.frame)

    def mousePressEvent(self,event):
        """Checks which mouse button was pressed and calls the appropriate function."""

        modifiers = QApplication.keyboardModifiers()
        leftbutton = event.button() == Qt.MouseButton.LeftButton
        rightbutton = event.button() == Qt.MouseButton.RightButton
        middlebutton = event.button() == Qt.MouseButton.MiddleButton
        ctrl = modifiers == Qt.KeyboardModifier.ControlModifier
        nomod = modifiers == Qt.KeyboardModifier.NoModifier

        # Check if key is bound with marking the image
        for group, binds in io.MARK_KEYBINDS.items():
            if (event.button() in binds) and nomod: self.mark(group=group)

        if middlebutton or (ctrl and leftbutton): self.center_cursor()

        if rightbutton: self.del_marks()

    def mouseMoveEvent(self, event):
        """Parses the mouse coordinates and gets galactic coordinates if available to show in scene."""

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

    def closeEvent(self, a0):
        self.update_comments()
        self.about_window.close()
        self.blur_window.close()
        self.frame_window.close()
        self.instructions_window.close()
        self.settings_window.close()
        return super().closeEvent(a0)

    # === Actions ===
    def save(self) -> None:
        """Method for saving image data"""
        io.save(self.date,self.images)
        io.savefav(self.date,self.images,self.favorite_list)

    def open(self) -> None:
        """Method for the open save directory dialog."""

        save_dir = QFileDialog.getExistingDirectory(self, 'Open save directory', io.SAVE_DIR)
        if save_dir == '': return
        
        io.SAVE_DIR = save_dir
        io.read_config()
        
        self.__init_data__()
        self.update_images()
        self.update_marks()
        self.get_comment()
        self.update_categories()
        self.update_comments()
        self.update_favorites()

    def open_ims(self) -> None:
        """Method for the open image directory dialog."""

        image_dir = QFileDialog.getExistingDirectory(self, 'Open image directory', io.SAVE_DIR)
        if image_dir == '': return

        io.IMAGE_DIR = image_dir
        io.update_config()

        self.images, self.idx = io.glob(edited_images=[])
        self.N = len(self.images)
        
        self.update_images()
        self.update_marks()
        self.get_comment()
        self.update_categories()
        self.update_comments()

    def open_catalog(self):
        """Method for opening a catalog file."""

        path = QFileDialog.getOpenFileName(self, 'Open catalog', io.SAVE_DIR, 'Text files (*.txt *.csv)')[0]
        if path == '': return
        
        catalog = Catalog(path)
        if catalog: self.catalogs.append(catalog)
        self.update_catalogs()

    def favorite(self,state) -> None:
        """Favorite the current image."""

        state = Qt.CheckState(state)
        if state == Qt.CheckState.PartiallyChecked:
            self.favorite_box.setIcon(QIcon(HEART_SOLID))
            self.favorite_list.append(self.image.name)
            io.savefav(self.date,self.images,self.favorite_list)
        else:
            self.favorite_box.setIcon(QIcon(HEART_CLEAR))
            if self.image.name in self.favorite_list: 
                self.favorite_list.remove(self.image.name)
            io.savefav(self.date,self.images,self.favorite_list)

    def categorize(self,i:int) -> None:
        """Categorize the current image."""

        if (self.category_boxes[i-1].checkState() == Qt.CheckState.Checked) and (i not in self.image.categories):
            self.image.categories.append(i)
        elif (i in self.image.categories):
            self.image.categories.remove(i)
        self.save()

    def mark(self, group:int=0) -> None:
        """Add a mark to the current image."""

        # get event position and position on image
        pix_pos = self.mouse_pix_pos()
        x, y = pix_pos.x(), pix_pos.y()
        
        # Mark if hovering over image
        if io.GROUP_MAX[group - 1] == 'None': limit = inf
        else: limit = int(io.GROUP_MAX[group - 1])

        marks_in_group = [m for m in self.image.marks if m.g == group]

        if len(self.image.marks) >= 1: self.image.marks[-1].label.enter()

        if self.inview(x,y) and ((len(marks_in_group) < limit) or limit == 1):            
            mark = self.image_scene.mark(x,y,group=group)
            
            if (limit == 1) and (len(marks_in_group) == 1):
                prev_mark = marks_in_group[0]
                self.image_scene.rmmark(prev_mark)
                self.image.marks.remove(prev_mark)
                self.image.marks.append(mark)

            else: self.image.marks.append(mark)

            marks_enabled = self.marks_action.isChecked()
            labels_enabled = self.labels_action.isChecked()

            if labels_enabled: mark.label.show()
            else: mark.label.hide()

            if marks_enabled: 
                mark.show()
                if labels_enabled: mark.label.show()
            else: 
                mark.hide()
                mark.label.hide()

            self.save()
        
        if len(self.image.marks) == 0:
            self.marks_action.setEnabled(False)
            self.labels_action.setEnabled(False)
        else:
            self.marks_action.setEnabled(True)
            self.labels_action.setEnabled(True)

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
        self.update_catalogs()
        self.get_comment()
        self.update_categories()
        self.update_favorites()
            
    def enter(self):
        """Enter the text in the comment box into the image."""

        self.update_comments()
        self.comment_box.clearFocus()
        self.save()

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
            self.blur_window.slider.sliderReleased.disconnect()
            self.frame_window.slider.valueChanged.disconnect(self.image.seek)
        except: pass

        # Update scene
        _w, _h = self.image.width, self.image.height
        try: self.image.close()
        except: pass

        self.image = self.images[self.idx]
        self.image.seek(self.frame)
        self.image.seen = True
        self.image_scene.update(self.image)
        if self.image.name not in self.order:
                self.order.append(self.image.name)

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
        self.blur_window.slider.setValue(int(self.image.r*10))
        self.frame_window.slider.setValue(self.frame)

        self.blur_window.slider.sliderReleased.connect(partial(self.image.blur,self.blur_window.slider.sliderPosition))
        self.frame_window.slider.valueChanged.connect(self.image.seek)

        self.frame_window.slider.setMaximum(self.image.n_frames-1)
        self.blur_max = int((self.image.height+self.image.width)/20)
        self.blur_window.slider.setMaximum(self.blur_max)

        # Update image label
        self.image_label.setText(f'{self.image.name} ({self.idx+1} of {self.N})')

        # Update menus
        if len(self.image.marks) == 0:
            self.marks_action.setEnabled(False)
            self.labels_action.setEnabled(False)
        else:
            self.marks_action.setEnabled(True)
            self.labels_action.setEnabled(True)

        self.toggle_marks()
        self.toggle_mark_labels()
        self.toggle_catalogs()
        self.toggle_catalog_labels()
    
    def update_comments(self):
        """Updates image comment with the contents of the comment box."""

        comment = self.comment_box.text()
        if not comment: comment = 'None'

        self.image.comment = comment
        self.save()

    def get_comment(self):
        """If the image has a comment, sets the text of the comment box to the image's comment."""

        if (self.image.comment == 'None'):
            self.comment_box.setText('')
        else:
            comment = self.image.comment
            self.comment_box.setText(comment)

    def update_categories(self):
        """Resets all category boxes to unchecked, then checks the boxes based on the current image's categories."""

        for box in self.category_boxes: box.setChecked(False)
        for i in self.image.categories:
            self.category_boxes[i-1].setChecked(True)

    def update_catalogs(self):
        for mark in self.image.cat_marks: 
            if mark not in self.image_scene.items(): self.image_scene.mark(mark)
        
        for catalog in self.catalogs:
            if catalog.path not in self.image.catalogs:
                for label, a, b in zip(catalog.labels,catalog.alphas,catalog.betas):
                    if catalog.coord_sys == 'galactic':
                        ra, dec = a, b   
                        mark_coord_cart = self.image.wcs.all_world2pix([[ra,dec]], 0)[0]
                        x, y = mark_coord_cart[0], self.image.height - mark_coord_cart[1]
                    else: x, y = a, b

                    if self.inview(x,y):
                        mark = self.image_scene.mark(x, y, shape='rect', text=label)
                        self.image.cat_marks.append(mark)

                self.image.catalogs.append(catalog.path)

        if len(self.image.cat_marks) > 0:
            self.catalogs_action.setEnabled(True)
            self.catalog_labels_action.setEnabled(True)
        else:
            self.catalogs_action.setEnabled(False)
            self.catalog_labels_action.setEnabled(False)

    def update_marks(self):
        """Redraws all marks in image."""
        
        for mark in self.image.marks: self.image_scene.mark(mark)

    def del_marks(self,del_all=False):
        """Deletes marks, either the selected one or all."""
        
        if not del_all:
            pix_pos = self.mouse_pix_pos(correction=False).toPointF()
            selected_items = [item for item in self.image.marks 
                              if item is self.image_scene.itemAt(pix_pos, item.transform())]
        else: selected_items = self.image.marks.copy()

        for item in selected_items:
            self.image_scene.rmmark(item)
            self.image.marks.remove(item)
        
        if len(self.image.marks) == 0:
            self.marks_action.setEnabled(False)
            self.labels_action.setEnabled(False)
            
        self.save()

    def toggle_randomize(self,state):
        """Updates the config file for randomization and reloads unseen images."""
        
        io.RANDOMIZE_ORDER = bool(state)
        io.update_config()

        names = [img.name for img in self.images]

        if not state: self.images = [self.images[i] for i in argsort(names)]

        else:
            unedited_names = [n for n in names if n not in self.order]

            rng = io.np.random.default_rng()
            rng.shuffle(unedited_names)

            randomized_names = self.order + unedited_names
            indices = [names.index(n) for n in randomized_names]
            self.images = [self.images[i] for i in indices]
     
        self.idx = self.images.index(self.image)

        self.update_images()
        self.update_marks()
        self.get_comment()
        self.update_categories()
        self.update_comments()

    def toggle_marks(self):
        """Toggles whether or not marks are shown."""

        marks_enabled = self.marks_action.isChecked()
        labels_enabled = self.labels_action.isChecked()

        for mark in self.image.marks:
            if marks_enabled: 
                mark.show()
                if labels_enabled: mark.label.show()
            else: 
                mark.hide()
                mark.label.hide()     

    def toggle_mark_labels(self):
        """Toggles whether or not mark labels are shown."""

        marks_enabled = self.marks_action.isChecked()
        labels_enabled = self.labels_action.isChecked()

        for mark in self.image.marks:
            if marks_enabled and labels_enabled: mark.label.show()
            else: mark.label.hide()

    def toggle_catalogs(self):
        """Toggles whether or not catalogs are shown."""

        catalogs_enabled = self.catalogs_action.isChecked()
        catalog_labels_enabled = self.catalog_labels_action.isChecked()

        for mark in self.image.cat_marks:
            if catalogs_enabled:
                mark.show()
                if catalog_labels_enabled:
                    mark.label.show()
            else:
                mark.hide()
                mark.label.hide()

    def toggle_catalog_labels(self):
        """Toggles whether or not catalog labels are shown."""

        catalogs_enabled = self.catalogs_action.isChecked()
        catalog_labels_enabled = self.catalog_labels_action.isChecked()

        for mark in self.image.cat_marks:
            if catalogs_enabled and catalog_labels_enabled:
                mark.label.show()
            else:
                mark.label.hide()

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