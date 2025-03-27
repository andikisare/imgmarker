__version__ = '0.8.7'
__license__ = 'MIT License'
__docsurl__ = 'https://imgmarker.readthedocs.io/en/latest/'
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

from .gui.pyqt import QApplication, QIcon
from .gui.window import MainWindow, _open_save
from . import config

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ICON))
    
    config.SAVE_DIR = _open_save()
    config.IMAGE_DIR, config.GROUP_NAMES, config.CATEGORY_NAMES, config.GROUP_MAX, config.RANDOMIZE_ORDER = config.read()

    window = MainWindow()
    window.show()
    window.image_view.zoomfit()
    sys.exit(app.exec())

if __name__ == '__main__': 
    main()