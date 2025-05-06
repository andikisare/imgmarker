"""This module simply imports PyQt5 or PyQt6 depending on which one the user has installed."""

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QPushButton, QLabel, 
        QScrollArea, QGraphicsView, QVBoxLayout, QWidget, 
        QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, 
        QSlider, QLineEdit, QFileDialog, QFrame, QDialog,
        QSizePolicy, QGraphicsPathItem, QGraphicsProxyWidget,
        QLineEdit, QGraphicsScene, QGraphicsPixmapItem, QSpinBox, QMessageBox,
        QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QColorDialog
    )
    from PyQt6.QtGui import QIcon, QFont, QClipboard, QAction, QPen, QColor, QPixmap, QPainter, QPainterPathStroker, QPainterPath, QImage, QShortcut, QDesktopServices
    from PyQt6.QtCore import Qt, QPoint, QKeyCombination, QPointF, QEvent, QUrl, PYQT_VERSION_STR

except: 
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QPushButton, QLabel, 
        QScrollArea, QGraphicsView, QVBoxLayout, QWidget, 
        QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, 
        QSlider, QLineEdit, QFileDialog, QFrame, QDialog,
        QSizePolicy, QGraphicsPathItem, QGraphicsProxyWidget,
        QLineEdit, QGraphicsScene, QGraphicsPixmapItem, QAction, QSpinBox, QMessageBox,
        QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QColorDialog
    )
    from PyQt5.QtGui import QIcon, QFont, QPen, QColor, QPixmap, QPainter, QPainterPath, QImage, QShortcut, QDesktopServices
    from PyQt5.QtCore import Qt, QPoint, QPointF, QEvent, PYQT_VERSION_STR