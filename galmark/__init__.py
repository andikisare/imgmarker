

import sys
import os

__dirname__ = os.path.dirname(os.path.realpath(__file__))
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

