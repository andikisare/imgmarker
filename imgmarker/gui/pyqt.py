"""This module simply imports PyQt5 or PyQt6 depending on which one the user has installed."""

try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QPushButton, QLabel, 
        QScrollArea, QGraphicsView, QVBoxLayout, QWidget, 
        QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, 
        QSlider, QLineEdit, QFileDialog, QFrame, QDialog,
        QSizePolicy, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsProxyWidget,
        QLineEdit, QGraphicsScene, QGraphicsPixmapItem, QSpinBox, QAbstractGraphicsShapeItem, QMessageBox,
        QTableWidget, QTableWidgetItem, QHeaderView
    )
    from PyQt6.QtGui import QIcon, QFont, QAction, QPen, QColor, QPixmap, QPainter, QImage, QShortcut, QDesktopServices
    from PyQt6.QtCore import Qt, QPoint, QPointF, QEvent, QUrl, PYQT_VERSION_STR

except: 
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QPushButton, QLabel, 
        QScrollArea, QGraphicsView, QVBoxLayout, QWidget, 
        QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, 
        QSlider, QLineEdit, QFileDialog, QFrame, QDialog,
        QSizePolicy, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsProxyWidget,
        QLineEdit, QGraphicsScene, QGraphicsPixmapItem, QAction, QSpinBox, QAbstractGraphicsShapeItem, QMessageBox,
        QTableWidget, QTableWidgetItem, QHeaderView
    )
    from PyQt5.QtGui import QIcon, QFont, QPen, QColor, QPixmap, QPainter, QImage, QShortcut, QDesktopServices
    from PyQt5.QtCore import Qt, QPoint, QPointF, QEvent, PYQT_VERSION_STR