import sys
import os

__dirname__ = os.path.dirname(os.path.realpath(__file__))
def _resource_path(rel_path):
    if hasattr(sys,'_MEIPASS'): base_path = sys._MEIPASS
    else: base_path = __dirname__
    return os.path.join(base_path, rel_path)

ICON = _resource_path('icon.png')
HEART_SOLID = _resource_path('heart_solid.png')
HEART_CLEAR = _resource_path('heart_clear.png')
SUPPORTED_EXTS = ['tif','tiff','fits','fit','png','jpeg','jpg']
CONFIG = os.path.join(os.getcwd(),'imgmarker.cfg')