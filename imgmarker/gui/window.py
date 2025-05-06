"""This contains the classes for the various windows displayed by Image Marker."""

from .pyqt import (
    QApplication, QMainWindow, QPushButton,
    QLabel, QScrollArea, QGraphicsView, QDialog,
    QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, 
    QCheckBox, QGraphicsScene, QColor, QSlider,
    QLineEdit, QFileDialog, QIcon, QFont, QAction, 
    Qt, QPoint, QSpinBox, QMessageBox, QTableWidget, 
    QTableWidgetItem, QHeaderView, QShortcut,
    QDesktopServices, QUrl, QMenu, QColorDialog, PYQT_VERSION_STR
)
from . import Screen
from .. import HEART_SOLID, HEART_CLEAR, __version__, __license__, __docsurl__
from .. import io
from .. import image
from .. import config
from . import QHLine, QVLine, PosWidget, RestrictedLineEdit, DefaultDialog
import sys
import datetime as dt
from math import floor, inf, nan, dist
import numpy as np
from numpy import argsort
from functools import partial
from typing import Union, List
import os
from astropy.coordinates import Angle
from copy import deepcopy
import gc
import shutil

def _open_save() -> str:
    dialog = DefaultDialog()
    dialog.setWindowTitle("Open save directory")
    dialog.exec()
    if dialog.closed: sys.exit()

    save_dir = dialog.selectedFiles()[0]
    return save_dir

def _open_ims() -> str:
    dialog = DefaultDialog(config.SAVE_DIR)
    dialog.setWindowTitle("Open image directory")
    dialog.exec()
    if dialog.closed: sys.exit()

    image_dir = dialog.selectedFiles()[0]
    return image_dir

class SettingsWindow(QWidget):
    """Class for the window for settings."""

    def __init__(self,mainwindow:'MainWindow'):
        super().__init__()
        
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
            lineedit.setPlaceholderText(config.GROUP_NAMES[i])
            lineedit.setFixedHeight(30)
            lineedit.setText(config.GROUP_NAMES[i])
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
            value:str = config.GROUP_MAX[i]
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
            lineedit.setPlaceholderText(config.CATEGORY_NAMES[i])
            lineedit.setFixedHeight(30)
            lineedit.setText(config.CATEGORY_NAMES[i])
            self.category_boxes.append(lineedit)

        self.category_layout = QHBoxLayout()
        for box in self.category_boxes: self.category_layout.addWidget(box)

        # Options
        self.show_sexagesimal_box = QCheckBox(text='Show sexagesimal coordinates of cursor', parent=self)
        if self.mainwindow.image.wcs == None:
            self.show_sexagesimal_box.setEnabled(False)
        else:
            self.show_sexagesimal_box.setEnabled(True)

        self.focus_box = QCheckBox(text='Middle-click to focus centers the cursor', parent=self)
        
        self.randomize_box = QCheckBox(text='Randomize order of images', parent=self)
        self.randomize_box.setChecked(config.RANDOMIZE_ORDER)

        self.duplicate_box = QCheckBox(text='Insert duplicate images for testing user consistency', parent=self)
        self.duplicate_box.setChecked(False)
        try:
            self.duplicate_box.checkStateChanged.connect(self.duplicate_percentage_state)
        except:
            self.duplicate_box.stateChanged.connect(self.duplicate_percentage_state)

        horizontal_duplicate_layout = QHBoxLayout()

        self.duplicate_percentage_label = QLabel()
        self.duplicate_percentage_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.duplicate_percentage_label.setText("Percentage of dataset to duplicate:")
        
        self.duplicate_percentage_spinbox = QSpinBox()
        self.duplicate_percentage_spinbox.setFixedHeight(25)
        self.duplicate_percentage_spinbox.setFixedWidth(50)
        self.duplicate_percentage_spinbox.setRange(1,100)
        
        self.duplicate_percentage_spinbox.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.duplicate_percentage_spinbox.valueChanged.connect(self.update_duplicate_percentage)

        if not self.duplicate_box.isChecked():
            self.duplicate_percentage_spinbox.setEnabled(False)
        else:
            self.duplicate_percentage_spinbox.setEnabled(True)
        horizontal_duplicate_layout.setContentsMargins(0,0,345,0)
        horizontal_duplicate_layout.addWidget(self.duplicate_percentage_label)
        horizontal_duplicate_layout.addWidget(self.duplicate_percentage_spinbox)

        # Main layout
        layout.addWidget(self.group_label)
        layout.addLayout(self.group_layout)
        layout.addWidget(self.max_label)
        layout.addLayout(self.max_layout)
        layout.addWidget(QHLine())
        layout.addWidget(self.category_label)
        layout.addLayout(self.category_layout)
        layout.addWidget(QHLine())
        layout.addWidget(self.show_sexagesimal_box)
        layout.addWidget(self.focus_box)
        layout.addWidget(self.randomize_box)
        layout.addWidget(self.duplicate_box)
        layout.addLayout(horizontal_duplicate_layout)
        layout.addWidget(QHLine())
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedWidth(int(Screen.width()/3))
        self.setFixedHeight(layout.sizeHint().height())

        # Set position of window
        qt_rectangle = self.frameGeometry()
        qt_rectangle.moveCenter(Screen.center())
        self.move(qt_rectangle.topLeft())

    def show(self):
        super().show()
        self.activateWindow()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            for box in self.group_boxes: box.clearFocus()
            for box in self.category_boxes: box.clearFocus()
            for box in self.max_boxes: box.clearFocus()

            self.update_config()

        return super().keyPressEvent(event)
    
    def closeEvent(self, a0):
        for box in self.group_boxes: box.clearFocus()
        for box in self.category_boxes: box.clearFocus()
        for box in self.max_boxes: box.clearFocus()

        self.update_config()
        self.mainwindow.save()
        self.mainwindow.centralWidget().setFocus()
        return super().closeEvent(a0)
    
    def duplicate_percentage_state(self):
        if not self.duplicate_box.isChecked():
            self.duplicate_percentage_spinbox.setEnabled(False)
        else:
            self.duplicate_percentage_spinbox.setEnabled(True)

    def update_duplicate_percentage(self):
        percentage = self.duplicate_percentage_spinbox.value()
        self.mainwindow.update_duplicates(percentage)

    def update_config(self):
        group_names_old = config.GROUP_NAMES.copy()

        # Get the new settings from the boxes
        config.GROUP_NAMES = ['None'] + [box.text() for box in self.group_boxes]
        config.GROUP_MAX = [str(box.value()) if box.value() != 0 else 'None' for box in self.max_boxes]
        config.CATEGORY_NAMES = ['None'] + [box.text() for box in self.category_boxes]
        config.RANDOMIZE_ORDER = self.randomize_box.isChecked()

        for i, box in enumerate(self.mainwindow.category_boxes): 
            box.setText(config.CATEGORY_NAMES[i+1])
            box.setShortcut(self.mainwindow.category_shortcuts[i])
            
        # Update mark labels that haven't been changed
        for image in self.mainwindow.images:
            if image.duplicate == True: marks = image.dupe_marks
            else: marks = image.marks
            for mark in marks:
                try:
                    if mark.label.lineedit.text() in group_names_old:
                        mark.label.lineedit.setText(config.GROUP_NAMES[mark.g])
                except: pass

        # Update text in the controls window 
        self.mainwindow.controls_window.update_text()

        # Save the new settings into the config file
        config.update()

class BlurWindow(QWidget):
    """Class for the blur adjustment window."""

    def __init__(self):
        super().__init__()
        
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
        self.setFixedWidth(int(Screen.width()/6))
        self.setFixedHeight(layout.sizeHint().height())

        # Set position of window
        qt_rectangle = self.frameGeometry()
        qt_rectangle.moveCenter(Screen.center())
        self.move(qt_rectangle.topLeft())

    def slider_moved(self, pos):
        self.value_label.setText(f'Radius: {floor(pos)/2}')

    def show(self):
        super().show()
        self.activateWindow()

class FrameWindow(QWidget):
    """Class for the window for switching between frames in an image."""

    def __init__(self):
        super().__init__()
        
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
        self.setFixedWidth(int(Screen.width()/6))
        self.setFixedHeight(layout.sizeHint().height())

        # Set position of window
        qt_rectangle = self.frameGeometry()
        qt_rectangle.moveCenter(Screen.center())
        self.move(qt_rectangle.topLeft())

    def slider_moved(self, pos):
        self.slider.setValue(floor(pos))

    def value_changed(self,value):
        self.value_label.setText(f'Frame: {self.slider.value()}')

    def show(self):
        super().show()
        self.activateWindow()

class ControlsWindow(QWidget):
    """Class for the window that displays the controls."""

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle('Controls')

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setSizeAdjustPolicy(QScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)  

        self.update_text()

        layout.addWidget(self.table)

        # Resize window according to size of layout
        self.resize(int(Screen.width()*0.2), self.sizeHint().height())
        self.setMaximumHeight(self.height())
        
    def update_text(self):
        # Lists for keybindings
        actions_list = ['Next','Back','Change frame','Delete','Enter comment', 'Focus', 'Zoom in/out', 'Copy mark coordinates' ,'Favorite']
        group_list = [f'Group \"{group}\"' for group in config.GROUP_NAMES[1:]]
        category_list = [f'Category \"{category}\"' for category in config.CATEGORY_NAMES[1:]]
        actions_list = group_list + category_list + actions_list
        buttons_list = ['1 OR Left click', '2', '3', '4', '5', '6', '7', '8', '9', 'Ctrl+1', 'Ctrl+2', 'Ctrl+3', 'Ctrl+4', 'Ctrl+5', 'Tab', 'Shift+Tab', 'Spacebar', 'Delete OR Shift+Right Click', 'Enter', 'Middle Click', 'Scroll Wheel', 'Ctrl + C', 'F']
        
        items = [ (action, button) for action, button in zip(actions_list, buttons_list) ]

        self.table.setRowCount(len(actions_list))

        for i, (action, button) in enumerate(items):
            action_item = QTableWidgetItem(action)
            button_item = QTableWidgetItem(button)

            action_item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            button_item.setFlags(Qt.ItemFlag.ItemIsEnabled)

            self.table.setItem(i, 0, action_item)
            self.table.setItem(i, 1, button_item)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    
    def show(self):
        """Shows the window and moves it to the front."""

        super().show()
        self.activateWindow()

class AboutWindow(QWidget):
    """Class for the window that displays information about Image Marker."""

    def __init__(self):
        super().__init__()

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
                  QLabel(f'<div>Andi Kisare, Ryan Walker, and Lindsey Bleem</div>')]

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
        qt_rectangle.moveCenter(Screen.center())
        self.move(qt_rectangle.topLeft()) 

    def show(self):
        """Shows the window and moves it to the front."""

        super().show()
        self.activateWindow()

class MarkMenu(QMenu):
    def __init__(self,mainwindow:'MainWindow'):
        super().__init__()
        self.menus:dict[str,QMenu] = {}
        self.mainwindow = mainwindow
        self.setTitle('&Mark')

    def menu_setup(self,path:str):
        file = path.split(os.sep)[-1]

        if path == self.mainwindow.markpath:
            self.menus[path] = QMenu(f'&{file} (default)')
        else:
            self.menus[path] = QMenu(f'&{file}')

        # Toggle marks
        marks_action = QAction('&Show Marks', self)
        marks_action.setShortcuts(['Ctrl+m'])
        marks_action.setCheckable(True)
        marks_action.setChecked(True)
        marks_action.triggered.connect(partial(self.mainwindow.toggle_marks,path))
        self.menus[path].addAction(marks_action)
        
        ### Toggle mark labels menu
        labels_action = QAction('&Show Mark Labels', self)
        labels_action.setCheckable(True)
        labels_action.setChecked(True)
        labels_action.triggered.connect(partial(self.mainwindow.toggle_mark_labels,path))
        self.menus[path].addAction(labels_action)

        if self.mainwindow.n_marks(path) == 0:
            marks_action.setEnabled(False)
            labels_action.setEnabled(False)
        else:
            marks_action.setEnabled(True)
            labels_action.setEnabled(True)

        self.menus[path].addSeparator()

        if path == self.mainwindow.markpath:
            labels_action.setShortcuts(['Ctrl+l'])

            del_marks_action = QAction(f'Delete Marks in Current Image', self)
            del_marks_action.triggered.connect(partial(self.mainwindow.del_usermarks,'all'))
            self.menus[path].addAction(del_marks_action)
        else:
            labels_action.setShortcuts(['Ctrl+Shift+l'])

            del_file_action = QAction(f'Delete', self)
            del_file_action.triggered.connect(partial(self.mainwindow.del_markfile,path))
            self.menus[path].addAction(del_file_action)

        self.addMenu(self.menus[path])

    def update_menu(self,path:str):
        if self.mainwindow.n_marks(path) == 0:
            self.marks_action(path).setEnabled(False)
            self.labels_action(path).setEnabled(False)
        else:
            self.marks_action(path).setEnabled(True)
            self.labels_action(path).setEnabled(True)
    
    def marks_action(self,path):
        return [action for action in self.menus[path].actions() if action.text() == "&Show Marks"][0]
    
    def labels_action(self,path):
        return [action for action in self.menus[path].actions() if action.text() == "&Show Mark Labels"][0]
        
class MainWindow(QMainWindow):
    """Class for the main window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Marker")
        self.frame = 0
        
        # Shortcuts
        del_shortcuts = [QShortcut('Backspace', self), QShortcut('Delete', self)]
        for shortcut in del_shortcuts: shortcut.activated.connect(self.del_usermarks)

        shiftplus_shorcut = QShortcut('Space', self)
        shiftplus_shorcut.activated.connect(partial(self.shiftframe,1))

        shiftminus_shorcut = QShortcut('Shift+Space', self)
        shiftminus_shorcut.activated.connect(partial(self.shiftframe,-1))

        ctrlc_shortcut = QShortcut('Ctrl+C', self)
        ctrlc_shortcut.activated.connect(self.copy_to_clipboard)
    
        # Initialize data
        self.date = dt.datetime.now(dt.timezone.utc).date().isoformat()
        self.order = []
        self.__init_data__()
        self.image_scene = image.ImageScene(self.image)
        self.image_view = image.ImageView(self.image_scene)
        self.image_view.mouseMoveEvent = self.mouseMoveEvent
        self.clipboard = QApplication.clipboard()

        #Initialize inserting duplicates at random
        self.images_seen_since_duplicate_count = 0 #keeps track of how many images have been seen since last duplicate
        self.duplicate_image_interval = 1 #this will vary every time a duplicate image is seen
        self.duplicates_seen = []
        self.rng = np.random.default_rng()

        # Setup child windows
        self.blur_window = BlurWindow()
        self.blur_window.slider.sliderReleased.connect(partial(self.image.blur,self.blur_window.slider.sliderPosition))
        
        self.frame_window = FrameWindow()
        self.frame_window.slider.valueChanged.connect(self.image.seek)
        self.frame_window.slider.setMaximum(self.image.n_frames-1)

        self.settings_window = SettingsWindow(self)
        # self.settings_window.show_sexagesimal_box.stateChanged.connect(self.show_sexagesimal)
        self.settings_window.focus_box.stateChanged.connect(partial(setattr,self.image_view,'cursor_focus'))
        self.settings_window.randomize_box.stateChanged.connect(self.toggle_randomize)

        self.controls_window = ControlsWindow()
        self.about_window = AboutWindow()

        # Update max blur
        self.blur_window.slider.setMaximum(self.blur_max)

        # Current image widget
        self.image_label = QLabel(f'{self.image.name} ({self.idx+1} of {self.N})')
        self.image_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Mouse position widget
        self.pos_widget = PosWidget()
        if self.image.wcs == None: 
            self.pos_widget.hidewcs()
        else:
            self.pos_widget.showwcs()

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
        self.category_boxes = [QCheckBox(text=config.CATEGORY_NAMES[i], parent=self) for i in range(1,6)]
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

        ### Open file menu
        open_action = QAction('&Open Save...', self)
        open_action.setShortcuts(['Ctrl+o'])
        open_action.triggered.connect(self.open)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        ### Import image folder menu
        import_ims_action = QAction('&Import Images...', self)
        import_ims_action.setShortcuts(['Ctrl+Shift+i'])
        import_ims_action.triggered.connect(self.import_ims)
        file_menu.addAction(import_ims_action)

        ### Import mark file
        import_marks_action = QAction('&Import Mark File...', self)
        import_marks_action.setShortcuts(['Ctrl+Shift+m'])
        import_marks_action.triggered.connect(self.import_markfile)
        file_menu.addAction(import_marks_action)
        
        ### Exit menu
        file_menu.addSeparator()
        exit_action = QAction('&Exit', self)
        exit_action.setShortcuts(['Ctrl+q'])
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        ## Edit menu
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.setToolTipsVisible(True)

        ### Undo previous mark
        undo_mark_action = QAction('&Undo Previous Mark', self)
        undo_mark_action.setShortcuts(['Ctrl+z'])
        undo_mark_action.triggered.connect(self.undo_prev_mark)
        edit_menu.addAction(undo_mark_action)

        ### Redo previous mark
        redo_mark_action = QAction('&Redo Previous Mark', self)
        redo_mark_action.setShortcuts(['Ctrl+Shift+z'])
        redo_mark_action.triggered.connect(self.redo_prev_mark)
        edit_menu.addAction(redo_mark_action)

        edit_menu.addSeparator()

        color_action = QAction('&Default Color...', self)
        color_action.triggered.connect(self.update_colors)
        color_action.setToolTip('Edit color of marks that aren\'t part of a group')
        edit_menu.addAction(color_action)

        ### Settings menu
        edit_menu.addSeparator()
        settings_action = QAction('&Settings...', self)
        settings_action.setShortcuts(['Ctrl+,'])
        settings_action.triggered.connect(self.settings_window.show)
        edit_menu.addAction(settings_action)

        ## View menu
        view_menu = menubar.addMenu("&View")

        ### Zoom menu
        zoom_menu = view_menu.addMenu("&Zoom")

        #### Zoom in
        zoomin_action = QAction('&Zoom In', self)
        zoomin_action.setShortcuts(['Ctrl+='])
        zoomin_action.triggered.connect(partial(self.image_view.zoom,1.2,'viewport'))
        zoom_menu.addAction(zoomin_action)

        ### Zoom out
        zoomout_action = QAction('&Zoom Out', self)
        zoomout_action.setShortcuts(['Ctrl+-'])
        zoomout_action.triggered.connect(partial(self.image_view.zoom,1/1.2,'viewport'))
        zoom_menu.addAction(zoomout_action)

        ### Zoom to Fit
        zoomfit_action = QAction('&Zoom to Fit', self)
        zoomfit_action.setShortcuts(['Ctrl+0'])
        zoomfit_action.triggered.connect(self.image_view.zoomfit)
        zoom_menu.addAction(zoomfit_action)

        ### Frame menu
        view_menu.addSeparator()
        self.frame_action = QAction('&Frames...', self)
        self.frame_action.setShortcuts(['Ctrl+f'])
        self.frame_action.triggered.connect(self.frame_window.show)
        view_menu.addAction(self.frame_action)

        if self.image.n_frames > 1:
            self.frame_action.setEnabled(True)
        else:
            self.frame_action.setEnabled(False)

        view_menu.addSeparator()

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

        linear_action.triggered.connect(partial(setattr,self,'stretch',image.Stretch.LINEAR))
        linear_action.triggered.connect(partial(linear_action.setChecked,True))
        linear_action.triggered.connect(partial(log_action.setChecked,False))

        log_action.triggered.connect(partial(setattr,self,'stretch',image.Stretch.LOG))
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

        minmax_action.triggered.connect(partial(setattr,self,'interval',image.Interval.MINMAX))
        minmax_action.triggered.connect(partial(minmax_action.setChecked,True))
        minmax_action.triggered.connect(partial(zscale_action.setChecked,False))

        zscale_action.triggered.connect(partial(setattr,self,'interval',image.Interval.ZSCALE))
        zscale_action.triggered.connect(partial(minmax_action.setChecked,False))
        zscale_action.triggered.connect(partial(zscale_action.setChecked,True))

        ### Marks Menu
        self.mark_menu = MarkMenu(self)
        self.mark_menu.setToolTipsVisible(True)
        for path in io.markpaths():
            self.mark_menu.menu_setup(path)

        menubar.addMenu(self.mark_menu)

        ## Help menu
        help_menu = menubar.addMenu('&Help')

        ### Controls window
        controls_action = QAction('&Controls', self)
        controls_action.setShortcuts(['F1'])
        controls_action.triggered.connect(self.controls_window.show)
        help_menu.addAction(controls_action)

        ### Documentation
        docs_action = QAction('&Documentation', self)
        docs_action.triggered.connect(partial(QDesktopServices.openUrl,QUrl(__docsurl__)))
        help_menu.addAction(docs_action)

        ### About window
        help_menu.addSeparator()
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.about_window.show)
        help_menu.addAction(about_action)
        
        # Resize and center MainWindow; move controls off to the right
        self.resize(int(Screen.height()*0.8),int(Screen.height()*0.8))
        
        center = Screen.center()
        center -= QPoint(self.width(),self.height())/2
        self.move(center)

        self.controls_window.move(int(self.x()+self.width()*1.04),self.y())

        # Initialize some data
        self.get_comment()
        self.update_marks()
        self.update_categories()
        self.settings_window.update_duplicate_percentage()

    def __init_data__(self):
        """Initializes images."""
        
        # Initialize output dictionary
        self.images, self.imageless_marks = io.load_markfile(io.load_imagesfile())
        for path in io.markpaths():
            if path != self.markpath:
                self.images, imageless_marks = io.load_markfile(self.images,mark_dst=path)
                self.imageless_marks += imageless_marks
        
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
            config.IMAGE_DIR = _open_ims()
            if config.IMAGE_DIR == None: sys.exit()
            config.update()
            
            self.images, self.idx = io.glob(edited_images=self.images)
            self.image = self.images[self.idx]
            self.image.seek(self.frame)
            self.image.seen = True
            self.N = len(self.images)
            if self.image.name not in self.order:
                self.order.append(self.image.name)

        
   
    @property
    def markpath(self):
        return os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')
    
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

    @property
    def blur_max(self):
        _blur_max = int((self.image.height+self.image.width)/20)
        _blur_max = 10*round(_blur_max/10)
        return max(10, _blur_max)
    
    def n_marks(self,path):
        marks = [mark for mark in self.image.marks if mark.dst == path]
        marks += [mark for mark in self.imageless_marks if mark.dst == path]
        return len(marks)

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

    def keyPressEvent(self, a0):
        """Checks which keyboard button was pressed and calls the appropriate function."""
        
        # Check if key is bound with marking the image
        for group, binds in config.MARK_KEYBINDS.items():
            if a0.key() in binds: self.mark(group=group)

    def mousePressEvent(self, a0):
        """Checks which mouse button was pressed and calls the appropriate function."""

        #super().mousePressEvent(a0)

        modifiers = QApplication.keyboardModifiers()
        leftbutton = a0.button() == Qt.MouseButton.LeftButton
        middlebutton = a0.button() == Qt.MouseButton.MiddleButton
        alt = modifiers == Qt.KeyboardModifier.AltModifier
        shift = modifiers == Qt.KeyboardModifier.ShiftModifier
        nomod = modifiers == Qt.KeyboardModifier.NoModifier

        # Check if key is bound with marking the image
        for group, binds in config.MARK_KEYBINDS.items():
            if (a0.button() in binds) and nomod: self.mark(group=group)

        if middlebutton or (alt and leftbutton): self.image_view.center_cursor()
        if shift and leftbutton: self.del_usermarks(mode='cursor')
        
    def mouseMoveEvent(self, a0):
        """Operations executed when the mouse cursor is moved."""

        super().mouseMoveEvent(a0)
        self.update_pos()

    def closeEvent(self, a0):
        self.update_comments()
        self.about_window.close()
        self.blur_window.close()
        self.frame_window.close()
        self.controls_window.close()
        self.settings_window.close()
        return super().closeEvent(a0)

    # === Actions ===
    def save(self) -> None:
        """Method for saving image data"""
        
        io.save_markfile(self.date,self.images,self.imageless_marks)
        io.save_imagesfile(self.date,self.images)
        io.savefav(self.date,self.images,self.favorite_list)

    def open(self) -> None:
        """Method for the open save directory dialog."""

        open_msg = 'This will save all current data in the current save directory and begin saving new data in the newly selected save directory.\
            Customized configuration file data will be kept if there is no available configuration file in the new save directory.\n\nAre you sure you want to continue?'
        reply = QMessageBox.question(self, 'WARNING', 
                        open_msg, QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.No: return

        save_dir = QFileDialog.getExistingDirectory(self, 'Open save directory', config.SAVE_DIR)
        if save_dir == '': return

        before_image_dir = config.IMAGE_DIR
        group_names_old = config.GROUP_NAMES.copy()

        config.SAVE_DIR = save_dir
        config.IMAGE_DIR, config.GROUP_NAMES, config.CATEGORY_NAMES, config.GROUP_MAX, config.RANDOMIZE_ORDER = config.read()
        config.update()

        after_image_dir = config.IMAGE_DIR

        if before_image_dir != after_image_dir: # if the image directory is different in the new config file, then we need to purge these lists
            del self.order; del self.duplicates_seen; del self.images
            gc.collect()
            self.order = []
            self.images_seen_since_duplicate_count = 0
            self.duplicates_seen = []

        self.images, self.idx = io.glob(edited_images=[])
        self.N = len(self.images)

        for i, box in enumerate(self.category_boxes): 
            box.setText(config.CATEGORY_NAMES[i+1])
            box.setShortcut(self.category_shortcuts[i])
            
        # Update mark labels that haven't been changed
        for image in self.images:
            if image.duplicate == True: marks = image.dupe_marks
            else: marks = image.marks
            for mark in marks:
                try:
                    if mark.label.lineedit.text() in group_names_old:
                        mark.label.lineedit.setText(config.GROUP_NAMES[mark.g])
                except: pass

        self.__init_data__()
        self.settings_window.__init__(self)
        self.update_images()
        self.image_view.zoomfit()
        self.update_marks()
        self.get_comment()
        self.update_categories()
        self.update_comments()
        self.update_favorites()
        self.controls_window.update_text()

    def import_ims(self) -> None:
        """Method for the open image directory dialog."""

        open_msg = 'This will overwrite all data associated with your current images, including all marks.\n\nAre you sure you want to continue?'
        reply = QMessageBox.question(self, 'WARNING', 
                        open_msg, QMessageBox.StandardButton.Yes, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.No: return

        image_dir = QFileDialog.getExistingDirectory(self, 'Open image directory', config.SAVE_DIR)
        if image_dir == '': return

        _image_dir = config.IMAGE_DIR
        config.IMAGE_DIR = image_dir

        del self.order; del self.duplicates_seen; del self.images
        gc.collect()
        self.order = []
        self.images_seen_since_duplicate_count = 0
        self.duplicates_seen = []
        
        self.images, self.idx = io.glob(edited_images=[])
        self.N = len(self.images)

        if self.N == 0:
            config.IMAGE_DIR = _image_dir
            return

        config.update()
        self.update_images()
        self.update_marks()
        self.get_comment()
        self.update_categories()
        self.update_comments()

    def import_markfile(self, **kwargs):
        """Method for opening a catalog file."""
        if 'src' not in kwargs:
            src = QFileDialog.getOpenFileName(self, 'Import mark file', config.SAVE_DIR, 'Text files (*.txt *.csv)')[0]
            if src == '': return
        else:
            src = kwargs['src']
        
        file = src.split(os.sep)[-1]
        dst = os.path.join(config.SAVE_DIR,'imports')
        mark_dst = shutil.copy(src,dst)

        self.images, imageless_marks = io.load_markfile(self.images,
                                                        mark_dst = mark_dst)
            
        self.imageless_marks += imageless_marks

        self.update_marks()

        '''if catalog and not test:
            self.color_picker_window = ColorPickerWindow(self)
            self.color_picker_window.show()
            self.color_picker_window.exec()
            
            if (self.picked_color == None):
                return
            else:
                catalog.color = self.picked_color
                self.catalogs.append(catalog)
                self.update_catalogs()
        else:
            self.picked_color = QColor("Yellow")
            catalog.color = self.picked_color
            self.catalogs.append(catalog)
            self.update_catalogs()'''

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

    def copy_to_clipboard(self):

        has_wcs = self.image.wcs != None

        if self.image.duplicate == True:
            marks = self.image.dupe_marks
        else:
            marks = self.image.marks

        selected_marks = [mark for mark in marks if mark.isSelected()]

        if len(selected_marks) == 0:
            return 
        else:
            mark_to_copy = selected_marks[-1]

        if has_wcs:
            ra, dec = mark_to_copy.wcs_center
        
            if self.settings_window.show_sexagesimal_box.isChecked():
                ra_h,ra_m,ra_s = Angle(ra, unit='deg').hms
                dec_d,dec_m,dec_s = Angle(dec, unit='deg').dms

                ra_str = rf'{np.abs(ra_h):02.0f}h {np.abs(ra_m):02.0f}m {np.abs(ra_s):05.2f}s'
                dec_str = f'{np.abs(dec_d):02.0f}° {np.abs(dec_m):02.0f}\' {np.abs(dec_s):05.2f}\"'.replace('-', '')

            else:
                ra_str = f'{ra:03.6f}'
                dec_str = f'{np.abs(dec):02.6f}'

            if dec > 0: dec_str = '+' + dec_str
            else: dec_str = '-' + dec_str
            
            string_copy = ra_str + ", " + dec_str

        else:
            x, y = str(mark_to_copy.center.x()), str(mark_to_copy.center.y())
            string_copy = x + ", " + y

        self.clipboard.setText(string_copy)

    def mark(self, group:int=0, test=False) -> None:
        """Add a mark to the current image."""

        if self.image.duplicate == True:
            marks = self.image.dupe_marks
        else:
            marks = self.image.marks

        # get event position and position on image
        if not test:
            pix_pos = self.image_view.mouse_pix_pos()
            x, y = pix_pos.x(), pix_pos.y()
        else: 
            x = self.image.width/2
            y = self.image.height/2
            
        # Mark if hovering over image
        if config.GROUP_MAX[group - 1] == 'None': limit = inf
        else: limit = int(config.GROUP_MAX[group - 1])

        marks_in_group = [m for m in marks if m.g == group]

        try: 
            if len(marks) >= 1: marks[-1].label.enter()
        except: pass

        marks_action = [action for action in self.mark_menu.menus[self.markpath].actions() if action.text() == "&Show Marks"][0]
        labels_action = [action for action in self.mark_menu.menus[self.markpath].actions() if action.text() == "&Show Mark Labels"][0]

        if self.inview(x,y) and ((len(marks_in_group) < limit) or limit == 1):            
            mark = self.image_scene.mark(x,y,group=group)
            
            if (limit == 1) and (len(marks_in_group) == 1):
                prev_mark = marks_in_group[0]
                self.image_scene.rmmark(prev_mark)
                marks.remove(prev_mark)
                marks.append(mark)

            else: marks.append(mark)

            marks_enabled = marks_action.isChecked()
            labels_enabled = labels_action.isChecked()

            if labels_enabled: mark.label.show()
            else: mark.label.hide()

            if marks_enabled: 
                mark.show()
                if labels_enabled: mark.label.show()
            else: 
                mark.hide()
                mark.label.hide()

            self.save()
        
        
        if len(marks) == 0:
            marks_action.setEnabled(False)
            labels_action.setEnabled(False)
        else:
            marks_action.setEnabled(True)
            labels_action.setEnabled(True)

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

        self.save()

    def shiftframe(self,delta:int):
        self.image.seek(self.frame+delta)

        self.frame = self.image.frame
        self.frame_window.slider.setValue(self.frame)
            
    def enter(self):
        """Enter the text in the comment box into the image."""

        self.update_comments()
        self.comment_box.clearFocus()
        self.save()

    def undo_prev_mark(self):
        if self.image.duplicate == True:
            marks = self.image.dupe_marks
        else:
            marks = self.image.marks
        if len(marks) > 0:
            self.image.undone_marks.append(marks[-1])
            self.image_scene.rmmark(marks[-1])
            marks.remove(marks[-1])
        
        self.save()

    def redo_prev_mark(self):
        if self.image.duplicate == True:
            marks = self.image.dupe_marks
        else:
            marks = self.image.marks
        if len(self.image.undone_marks) > 0:
            self.image_scene.mark(self.image.undone_marks[-1])
            marks.append(self.image.undone_marks[-1])
            self.image.undone_marks.remove(self.image.undone_marks[-1])

        self.save()

    # === Update methods ===
    def update_pos(self):
        # Mark if hovering over image
        pix_pos = self.image_view.mouse_pix_pos()
        x, y = pix_pos.x(), pix_pos.y()

        if self.inview(x,y):
            _x, _y = x, self.image.height - y

            try: ra, dec = self.image.wcs.all_pix2world([[_x, _y]], 0)[0]
            except: ra, dec = nan, nan

            if self.settings_window.show_sexagesimal_box.isChecked():
                ra_h,ra_m,ra_s = Angle(ra, unit='deg').hms
                dec_d,dec_m,dec_s = Angle(dec, unit='deg').dms

                ra_str = rf'{np.abs(ra_h):02.0f}h {np.abs(ra_m):02.0f}m {np.abs(ra_s):05.2f}s'
                dec_str = f'{np.abs(dec_d):02.0f}° {np.abs(dec_m):02.0f}\' {np.abs(dec_s):05.2f}\"'.replace('-', '')

            else:
                ra_str = f'{ra:03.5f}°'
                dec_str = f'{np.abs(dec):02.5f}°'

            if dec > 0: dec_str = '+' + dec_str
            else: dec_str = '-' + dec_str

            self.pos_widget.x_text.setText(f'{x} px')
            self.pos_widget.y_text.setText(f'{y} px')

            self.pos_widget.ra_text.setText(ra_str)
            self.pos_widget.dec_text.setText(dec_str)

        else:
            self.pos_widget.cleartext()

    def update_duplicates(self, percentage):
        self.min_images_til_duplicate = int((len(self.images) - len(self.duplicates_seen)) / (percentage * 4))
        self.max_images_til_duplicate = int((len(self.images) - len(self.duplicates_seen)) / percentage)

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

        # Randomizing duplicate images to show for consistency of user marks
        if self.settings_window.duplicate_box.isChecked():
            seen_images = [image for image in self.images if (len(image.marks) != 0) and (image.name not in self.duplicates_seen)]
            if self.settings_window.duplicate_box.isChecked():
                if (len(seen_images) > self.min_images_til_duplicate):
                    self.images_seen_since_duplicate_count += 1
                    if (self.images_seen_since_duplicate_count == self.duplicate_image_interval):
                        self.duplicate_image_interval = self.rng.integers(self.min_images_til_duplicate,self.max_images_til_duplicate)
                        self.images_seen_since_duplicate_count = 0
                        duplicate_image_to_show = deepcopy(self.rng.choice(seen_images[0:-1]))
                        duplicate_image_to_show.duplicate = True
                        duplicate_image_to_show.marks.clear()
                        self.images.insert(self.idx,duplicate_image_to_show)
                        self.N = len(self.images)
                        self.duplicates_seen.append(duplicate_image_to_show.name)
        
        # Continue update_images
        self.frame = self.image.frame
        self.image = self.images[self.idx]
        self.image.seek(self.frame)
        self.image.seen = True
        self.image_scene.update_image(self.image)
        if self.image.name not in self.order:   # or self.image.duplicate == True: This could be added to preserve order when duplicates are being inserted, but the use case for someone randomizing
                self.order.append(self.image.name)   # who wants to keep the order if duplicates have been seen and then they turn off and back on randomization is quite low

        # Fit back to view if the image dimensions have changed
        if (self.image.width != _w) or (self.image.height != _h): self.image_view.zoomfit()

        # Update position widget
        self.update_pos()
        if self.image.wcs == None: 
            self.pos_widget.hidewcs()
        else:
            self.pos_widget.showwcs()
             
        # Update sliders
        self.blur_window.slider.setValue(int(self.image.r*10))
        self.frame_window.slider.setValue(self.frame)

        self.blur_window.slider.sliderReleased.connect(partial(self.image.blur,self.blur_window.slider.sliderPosition))
        self.frame_window.slider.valueChanged.connect(self.image.seek)

        self.frame_window.slider.setMaximum(self.image.n_frames-1)
        self.blur_window.slider.setMaximum(self.blur_max)

        # Update image label
        self.image_label.setText(f'{self.image.name} ({self.idx+1} of {self.N})')

        # Update menus
        self.update_mark_menu()

        if self.image.n_frames > 1:
            self.frame_action.setEnabled(True)
        else:
            self.frame_action.setEnabled(False)

        if self.image.wcs == None:
            self.settings_window.show_sexagesimal_box.setEnabled(False)
        else:
            self.settings_window.show_sexagesimal_box.setEnabled(True)

        
    
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

    def update_marks(self):
        """Redraws all marks in image."""
        
        # Update regular marks
        if self.image.duplicate == True:
            marks = self.image.dupe_marks
        else:
            marks = self.image.marks

        for mark in marks: 
            if mark not in self.image_scene.items():
                self.image_scene.mark(mark)

        # Update imageless marks
        for mark in self.imageless_marks:
            mark.image = self.image
            x,y = mark.center.x(), mark.center.y()
            if self.inview(x,y) and not (mark in self.image_scene.items()):
                self.image_scene.mark(mark)
                mark.show()
            mark.image = None
        
        self.update_mark_menu()

        self.save()

    def update_mark_menu(self):
        for path in io.markpaths():
            if path not in self.mark_menu.menus:
                self.mark_menu.menu_setup(path)
            else:
                self.mark_menu.update_menu(path)
                self.toggle_marks(path)
                self.toggle_mark_labels(path)

        menu_paths = self.mark_menu.menus.copy().keys()
        for path in menu_paths:
            if path not in io.markpaths():
                del self.mark_menu.menus[path]

    def update_colors(self):
        color = QColorDialog.getColor()
        if color.isValid():
            config.GROUP_COLORS[0] = color
        
        if self.image.duplicate == True:
            marks = self.image.dupe_marks
        else:
            marks = self.image.marks
        
        marks += self.imageless_marks

        for mark in marks:
            if mark.g == 0:
                mark.color = color
                if mark in self.image_scene.items():
                    mark.setPen(color)
                    mark.label.lineedit.setStyleSheet(f"""background-color: rgba(0,0,0,0);
                                                      border: none; 
                                                      color: rgba{color.getRgb()}""")

    def del_markfile(self, path):
        """Deletes a markfile."""

        if path == self.markpath:
            if self.image.duplicate == True:
                marks = [mark for mark in self.image.dupe_marks if mark.dst == path]
            else:
                marks = [mark for mark in self.image.marks if mark.dst == path]
        
        else:
            marks = []
            for image in self.images:
                if image.duplicate == True:
                    _marks = [mark for mark in self.image.dupe_marks if mark.dst == path]
                else:
                    _marks = [mark for mark in self.image.marks if mark.dst == path]

                marks += _marks
            os.remove(path)
                    
        imageless_marks = [mark for mark in self.imageless_marks if mark.dst == path]

        for mark in marks:
            self.image.undone_marks.append(mark)

            if mark in self.image_scene.items():
                self.image_scene.rmmark(mark)
            
            if mark in self.image.marks:
                self.image.marks.remove(mark)

            if mark in self.image.dupe_marks:
                self.image.dupe_marks.remove(mark)

        for mark in imageless_marks:
            if mark in self.image_scene.items():
                self.image_scene.rmmark(mark)
            self.imageless_marks.remove(mark)

        self.update_mark_menu()
        
        self.save()
    
    def del_usermarks(self,mode='selected'):
        """Deletes marks, either the selected one or all."""
        
        if self.image.duplicate == True:
            marks = self.image.dupe_marks
        else:
            marks = self.image.marks

        if mode == 'all':
            selected_marks = [mark for mark in marks if mark.dst == self.markpath]
        elif mode == 'selected': 
            selected_marks = [mark for mark in marks 
                              if (mark.dst == self.markpath) and mark.isSelected()]
        elif mode == 'cursor':
            pix_pos = self.image_view.mouse_pix_pos(correction=False).toPointF()
            selected_marks = [mark for mark in marks if (mark is self.image_scene.itemAt(pix_pos, mark.transform()))
                              and (mark.dst == self.markpath)]
            
        for mark in selected_marks:
            self.image.undone_marks.append(mark)
            self.image_scene.rmmark(mark)
            marks.remove(mark)
        
        self.update_mark_menu()
            
        self.save()

    def toggle_randomize(self,state):
        """Updates the config file for randomization and reloads unseen images."""
        
        config.RANDOMIZE_ORDER = bool(state)
        config.update()

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

    def toggle_marks(self,path):
        """Toggles whether or not marks are shown."""

        if self.image.duplicate == True:
            marks = [mark for mark in self.image.dupe_marks if mark.dst == path]
        else:
            marks = [mark for mark in self.image.marks if mark.dst == path]

        marks += [mark for mark in self.imageless_marks if (mark.dst == path)]

        marks_enabled = self.mark_menu.marks_action(path).isChecked()
        labels_enabled = self.mark_menu.labels_action(path).isChecked()

        for mark in marks:
            if marks_enabled: 
                mark.show()
                self.mark_menu.labels_action(path).setEnabled(True)
                if labels_enabled: mark.label.show()
            else: 
                mark.hide()
                mark.label.hide()
                self.mark_menu.labels_action(path).setEnabled(False)

    def toggle_mark_labels(self,path):
        """Toggles whether or not mark labels are shown."""

        if self.image.duplicate == True:
            marks = [mark for mark in self.image.dupe_marks if mark.dst == path]
        else:
            marks = [mark for mark in self.image.marks if mark.dst == path]

        marks += [mark for mark in self.imageless_marks if mark.dst == path]

        marks_enabled = self.mark_menu.marks_action(path).isChecked()
        labels_enabled = self.mark_menu.labels_action(path).isChecked()

        for mark in marks:
            if marks_enabled and labels_enabled: mark.label.show()
            else: mark.label.hide()
