

import sys
import os

__dirname__ = os.path.dirname(os.path.realpath(__file__))
__icon__ = os.path.join(__dirname__,'icon.png')
__heart_solid__ = os.path.join(__dirname__,'heart_clear.png')
__heart_clear__ = os.path.join(__dirname__,'heart_solid.png')

sys.path.append(__dirname__.removesuffix('galmark'))

from PyQt6.QtWidgets import QApplication
from galmark.window import MainWindow
from galmark.io import inputs

def main():
    app = QApplication(sys.argv)
    window = MainWindow(*inputs())
    window.show()
    app.exec()

if __name__ == '__main__': main()

