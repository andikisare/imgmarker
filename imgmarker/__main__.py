"""
Copyright © 2025, UChicago Argonne, LLC

Full license found at _YOUR_INSTALLATION_DIRECTORY_/imgmarker/LICENSE
"""

from imgmarker.gui.pyqt import QApplication, QIcon
from imgmarker.gui.window import MainWindow, _open_save
from imgmarker import config, ICON, __version__
import sys

if sys.platform == "darwin":
    try:
        from Foundation import NSBundle
        bundle = NSBundle.mainBundle()
        info = bundle.localizedInfoDictionary() or bundle.infoDictionary()
        if info is not None:
            info["CFBundleName"] = "Image Marker"
    except ImportError:
        pass  # pyobjc not installed



def run():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(ICON))
    app.setApplicationName(f"Image Marker v. {__version__}")
    
    config.SAVE_DIR = _open_save()
    config.IMAGE_DIR, config.GROUP_NAMES, config.CATEGORY_NAMES, config.GROUP_MAX, config.RANDOMIZE_ORDER = config.read()

    window = MainWindow()
    window.show()
    window.image_view.zoomfit()
    sys.exit(app.exec())

if __name__ == '__main__': 
    run()