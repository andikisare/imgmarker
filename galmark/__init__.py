

import sys
import os

__dirname__ = os.path.dirname(os.path.realpath(__file__))
ICON = os.path.join(__dirname__,'icon.png')
HEART_SOLID = os.path.join(__dirname__,'heart_solid.png')
HEART_CLEAR = os.path.join(__dirname__,'heart_clear.png')
SUPPORTED_EXTS = ['tif','tiff','fits','fit','png','jpeg','jpg']
CONFIG = os.path.join(os.getcwd(),'galmark.cfg')

sys.path.append(__dirname__.removesuffix('galmark'))

from PyQt6.QtWidgets import QApplication
from galmark.window import MainWindow
from galmark.io import inputs

def main():
    app = QApplication(sys.argv)
    window = MainWindow(inputs())
    window.show()
    app.exec()

if __name__ == '__main__': main()

