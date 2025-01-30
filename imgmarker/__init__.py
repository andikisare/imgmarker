__version__ = '0.3.2'
__license__ = 'MIT License'
import sys
import os

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

def _resource_path(rel_path):
    if hasattr(sys,'_MEIPASS'): 
        base_path = sys._MEIPASS
    else: base_path = MODULE_PATH
    return os.path.join(base_path, rel_path)

if __name__ == '__main__' and __package__ is None:
    top = os.path.abspath(os.path.join(MODULE_PATH, '..'))
    sys.path.append(str(top))
        
    import imgmarker
    __package__ = 'imgmarker'

ICON = _resource_path('icon.ico')
HEART_SOLID = _resource_path('heart_solid.ico')
HEART_CLEAR = _resource_path('heart_clear.ico')

from .pyqt import QApplication
from .window import MainWindow
from . import config

def main():
    app = QApplication(sys.argv)
    
    config.SAVE_DIR = config.open_save()
    config.IMAGE_DIR, config.GROUP_NAMES, config.CATEGORY_NAMES, config.GROUP_MAX, config.RANDOMIZE_ORDER = config.read()

    window = MainWindow()
    window.show()
    window.fitview()
    sys.exit(app.exec())

if __name__ == '__main__': 
    main()