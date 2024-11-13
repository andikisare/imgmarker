try:
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                                 QScrollArea, QGraphicsView, QVBoxLayout, QWidget, 
                                 QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, 
                                 QSlider, QLineEdit, QFileDialog, QFrame, 
                                 QSizePolicy, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsProxyWidget,
                                 QLineEdit, QGraphicsScene, QGraphicsPixmapItem, QSpinBox)
    from PyQt6.QtGui import QIcon, QFont, QAction, QPen, QColor, QPixmap, QPainter
    from PyQt6.QtCore import Qt, QPoint, QPointF, QEvent
    QT_VERSION = '6'

except: 
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                                 QScrollArea, QGraphicsView, QVBoxLayout, QWidget, 
                                 QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, 
                                 QSlider, QLineEdit, QFileDialog, QFrame, 
                                 QSizePolicy, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsProxyWidget,
                                 QLineEdit, QGraphicsScene, QGraphicsPixmapItem, QAction, QSpinBox)
    from PyQt5.QtGui import QIcon, QFont, QPen, QColor, QPixmap, QPainter
    from PyQt5.QtCore import Qt, QPoint, QPointF, QEvent
    QT_VERSION = '5'