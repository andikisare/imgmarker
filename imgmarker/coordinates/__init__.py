import numpy as np
from astropy.wcs import WCS


class Angle:
    def __init__(self,value):
        self.value = value

    def __add__(self, value):
        return Angle(self.value.__add__(value))
    
    def __sub__(self, value):
        return Angle(self.value.__sub__(value))
    
    def __mul__(self, value):
        return Angle(self.value.__mul__(value))
    
    def __truediv__(self, value):
        return Angle(self.value.__truediv__(value))
    
    def __repr__(self):
        return self.__str__+'°'
    
    def __str__(self):
        try:
            return f'{float(self.value).__repr__()}'
        except:
            return f'{self.value.__repr__()}'
    
    def __float__(self):
        try:
            return float(self.value)
        except:
            return self.value.astype(np.float64)
    
    @property
    def hms(self):
        sign = np.sign(self.value)
        m, s = np.divmod(np.abs(self.value)*240, 60)
        h, m = np.divmod(m, 60)
        return sign*h, sign*m, sign*s

    @property
    def dms(self):
        sign = np.sign(self.value)
        m, s = np.divmod(np.abs(self.value)*3600, 60)
        d, m = np.divmod(m, 60)
        return sign*d, sign*m, sign*s
    
    
class WorldCoord:
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
        _radec = np.dstack((self.ra.value,self.dec.value))[0]
        x, _y = wcs.all_world2pix(_radec, 0).T
        y = wcs.pixel_shape[1] - _y
        
        if len(x) == 1:
            return PixCoord(x[0],y[0])
        else:
            return PixCoord(x,y)


class PixCoord:
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
        _x, _y = self.x, wcs.pixel_shape[1] - self.y
        _xy = np.dstack((_x,_y))[0]
        ra, dec = wcs.all_pix2world(_xy, 0).T

        if len(ra) == 1:
            return WorldCoord(ra[0],dec[0])
        else:
            return WorldCoord(ra,dec)