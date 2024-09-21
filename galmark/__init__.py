

import sys
import os

__dirname__ = os.path.dirname(os.path.realpath(__file__))
sys.path.append(__dirname__.removesuffix('galmark'))

from PyQt6.QtWidgets import QApplication
from galmark.window import MainWindow, StartupWindow
from galmark.io import readConfig

def config(config='galmark.cfg'):
    out_path, images_path, group_names, problem_names = readConfig(config)
    username = StartupWindow().getUser()

    return username, out_path, images_path, group_names, problem_names

def main():
    app = QApplication(sys.argv)
    
    window = MainWindow(*config())
    window.show()

    app.exec()

if __name__ == '__main__': main()

