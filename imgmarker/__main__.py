from PyQt6.QtWidgets import QApplication
from .window import MainWindow
from .io import inputs
import sys

def main():
    app = QApplication(sys.argv)
    window = MainWindow(inputs())
    window.show()
    app.exec()

if __name__ == '__main__': main()