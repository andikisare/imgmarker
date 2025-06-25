"""
Copyright © 2025, UChicago Argonne, LLC

Full license found at _YOUR_INSTALLATION_DIRECTORY_/imgmarker/LICENSE
"""

import numpy as np
from astropy.wcs import WCS
import numpy as np

class Angle(np.ndarray):
    """Represents a single angle or an array of angles."""

    def __new__(cls,a):
        obj = np.asarray(a,dtype=float).view(cls)
        return obj

    def __add__(self, value):
        return Angle(super().__add__(value))
    
    def __sub__(self, value):
        return Angle(super().__sub__(value))
    
    def __mul__(self, value):
        return Angle(super().__mul__(value))
    
    def __abs__(self):
        return Angle(super().__abs__())
    
    def __truediv__(self, value):
        return Angle(super().__truediv__(value))
    
    @property
    def hms(self):
        sign = np.sign(self)
        m, s = np.divmod(np.abs(self)*240, 60)
        h, m = np.divmod(m, 60)
        return sign*h, sign*m, sign*s

    @property
    def dms(self):
        sign = np.sign(self)
        m, s = np.divmod(np.abs(self)*3600, 60)
        d, m = np.divmod(m, 60)
        return sign*d, sign*m, sign*s
    
class WorldCoord:
    """Object containing a right ascension and declination or arrays thereof."""

    def __init__(self, ra:Angle|float|int, dec:Angle|float|int):
        self.ra = Angle(ra)
        self.dec = Angle(dec)

    def __iter__(self):
        return iter((self.ra,self.dec))
    
    def __getitem__(self,index):
        return (self.ra,self.dec)[index]
    
    def __len__(self):
        return 2
    
    def topix(self, wcs:WCS) -> 'PixCoord':
        """Converts world coordinate into pixel coordinates. The origin is the upper-left corner."""

        _radec = np.dstack((self.ra,self.dec))[0]
        x, _y = wcs.all_world2pix(_radec, 0).T
        y = wcs.pixel_shape[1] - _y
        
        if len(x) == 1:
            return PixCoord(x[0],y[0])
        else:
            return PixCoord(x,y)


class PixCoord:
    """Object containing an x and y coordinate or arrays thereof."""
    
    def __init__(self, x:int|float, y:int|float):
        self.x = np.round(x)
        self.y = np.round(y)

    def __iter__(self):
        return iter((self.x,self.y))
    
    def __getitem__(self,index):
        return (self.x,self.y)[index]
    
    def __len__(self):
        return 2
    
    def toworld(self,wcs:WCS) -> WorldCoord:
        """Converts pixel coordinate into world coordinates. The origin is the upper-left corner."""

        _x, _y = self.x, wcs.pixel_shape[1] - self.y
        _xy = np.dstack((_x,_y))[0]
        ra, dec = wcs.all_pix2world(_xy, 0).T

        if len(ra) == 1:
            return WorldCoord(ra[0],dec[0])
        else:
            return WorldCoord(ra,dec)