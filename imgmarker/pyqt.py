try:
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                                 QScrollArea, QGraphicsView, QVBoxLayout, QWidget, 
                                 QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, 
                                 QSlider, QLineEdit, QFileDialog, QFrame, 
                                 QSizePolicy, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsProxyWidget,
                                 QLineEdit, QGraphicsScene, QGraphicsPixmapItem, QSpinBox, QAbstractGraphicsShapeItem)
    from PyQt6.QtGui import QIcon, QFont, QAction, QPen, QColor, QPixmap, QPainter
    from PyQt6.QtCore import Qt, QPoint, QPointF, QEvent, PYQT_VERSION_STR

except: 
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                                 QScrollArea, QGraphicsView, QVBoxLayout, QWidget, 
                                 QHBoxLayout, QLineEdit, QInputDialog, QCheckBox, 
                                 QSlider, QLineEdit, QFileDialog, QFrame, 
                                 QSizePolicy, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsProxyWidget,
                                 QLineEdit, QGraphicsScene, QGraphicsPixmapItem, QAction, QSpinBox, QAbstractGraphicsShapeItem)
    from PyQt5.QtGui import QIcon, QFont, QPen, QColor, QPixmap, QPainter
    from PyQt5.QtCore import Qt, QPoint, QPointF, QEvent, PYQT_VERSION_STR