"""
Copyright © 2025, UChicago Argonne, LLC

Full license found at _YOUR_INSTALLATION_DIRECTORY_/imgmarker/LICENSE
"""

from imgmarker.gui.pyqt import QApplication, QIcon
from imgmarker.gui.window import MainWindow, _open_save
from imgmarker import config, ICON
import sys

def run():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ICON))
    
    config.SAVE_DIR = _open_save()
    config.IMAGE_DIR, config.GROUP_NAMES, config.CATEGORY_NAMES, config.GROUP_MAX, config.RANDOMIZE_ORDER = config.read()

    window = MainWindow()
    window.show()
    window.image_view.zoomfit()
    sys.exit(app.exec())

if __name__ == '__main__': 
    run()