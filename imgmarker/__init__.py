import sys
import os

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

def _resource_path(rel_path):
    if hasattr(sys,'_MEIPASS'): base_path = sys._MEIPASS
    else: base_path = MODULE_PATH
    return os.path.join(base_path, rel_path)

if __name__ == '__main__' and __package__ is None:
    parent, top = MODULE_PATH, MODULE_PATH.removesuffix('imgmarker')
    sys.path.append(str(top))
    try: sys.path.remove(str(parent))
    except ValueError: pass
        
    import imgmarker
    __package__ = 'imgmarker'

ICON = _resource_path('icon.png')
HEART_SOLID = _resource_path('heart_solid.png')
HEART_CLEAR = _resource_path('heart_clear.png')
SUPPORTED_EXTS = ['tif','tiff','fits','fit','png','jpeg','jpg']
CONFIG = os.path.join(os.getcwd(),'imgmarker.cfg')

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