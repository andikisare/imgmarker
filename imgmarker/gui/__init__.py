"""
Copyright © 2025, UChicago Argonne, LLC

Full license found at _YOUR_INSTALLATION_DIRECTORY_/imgmarker/LICENSE
"""

from imgmarker.gui.pyqt import QApplication
from imgmarker.gui.mark import *
from imgmarker.gui.widget import *

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