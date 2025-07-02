__version__ = '1.1.4'
__license__ = 'MIT License'
__docsurl__ = 'https://imgmarker.readthedocs.io/en/latest/'

import sys
import os
from importlib import resources

def resource_path(resource):
    if hasattr(sys,'_MEIPASS'):
        return os.path.join(sys._MEIPASS, resource)
    else: 
        return str(resources.files(__package__).joinpath(resource))

ICON = resource_path('icon.ico')
HEART_SOLID = resource_path('heart_solid.ico')
HEART_CLEAR = resource_path('heart_clear.ico')
