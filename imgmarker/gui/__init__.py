
from .pyqt import QApplication
from .mark import *
from .widget import *

class Screen:
    @staticmethod
    def width():
        return QApplication.primaryScreen().size().width()
    
    @staticmethod
    def height():
        return QApplication.primaryScreen().size().height()
    
    @staticmethod
    def center():
        return QApplication.primaryScreen().geometry().center()