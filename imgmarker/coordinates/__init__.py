
import numpy as np
from imgmarker import libwcs
from astropy.io.fits import Header
from ctypes import c_double

class Angle(float):
    def __add__(self, value):
        return Angle(super().__add__(value))
    
    def __sub__(self, value):
        return Angle(super().__sub__(value))
    
    def __mul__(self, value):
        return Angle(super().__mul__(value))
    
    def __truediv__(self, value):
        return Angle(super().__truediv__(value))
    
    def __repr__(self):
        return f'{super().__repr__()}°'
    
    def __str__(self):
        return f'{super().__repr__()}'
    
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
    
class WorldCoord(tuple):
    def __new__(cls, ra:Angle|float|int, dec:Angle|float|int):
        return super(WorldCoord, cls).__new__(cls, (Angle(ra),Angle(dec)))

    @property
    def ra(self) -> Angle:
        return self[0]
    
    @property
    def dec(self) -> Angle:
        return self[1]
    
    def __add__(self, value):
        return WorldCoord(*np.add(self,value))
    
    def __sub__(self, value):
        return WorldCoord(*np.subtract(self,value))
    
    def __mul__(self, value):
        return WorldCoord(*np.multiply(self,value))
    
    def __truediv__(self, value):
        return WorldCoord(*np.divide(self,value))
    
    def __repr__(self):
        return f'RA: {self.ra.__repr__()}\nDEC: {self.dec.__repr__()}'
    
    def topix(self,wcs:'WCS') -> 'PixCoord':
        """Convert to pixel coordinates."""
        return wcs.world2pix(self)
    
class PixCoord(tuple):
    def __new__(cls, x:int|float, y:int|float):
        return super(PixCoord, cls).__new__(cls, (round(x),round(y)))

    @property
    def x(self) -> int:
        return self[0]
    
    @property
    def y(self) -> int:
        return self[1]
    
    def __add__(self, value):
        return PixCoord(*np.add(self,value))
    
    def __sub__(self, value):
        return PixCoord(*np.subtract(self,value))
    
    def __mul__(self, value):
        return PixCoord(*np.multiply(self,value))
    
    def __truediv__(self, value):
        return PixCoord(*np.divide(self,value))
    
    def __repr__(self):
        return f'X: {self.x} px\nY: {self.y} px'
        
    def toworld(self,wcs:'WCS') -> WorldCoord:
        """Convert to world coordinates."""
        return wcs.pix2world(self)

class WCS:
    def __init__(self,header:Header|str):
        self.header = header
        self._wcs = libwcs.wcs.wcsinit(self.hstring)

    @property
    def hstring(self):
        _hstring = ''
        for card in self.header.cards:
            _hstring+=str(card)
        return _hstring

    def pix2world(self,pix:PixCoord) -> WorldCoord:
        """Convert pixel coordinates into world coordinates. The origin is set to the top left corner."""

        pix *= (1,-1) # vertical reflection
        pix += (0,self.nypix) # shift by image height
        pix += 1 # one pixel offset

        ra,dec = libwcs.wcs.pix2wcs(self._wcs,*pix)
        world = WorldCoord(ra,dec)

        return world
    
    def world2pix(self,world:WorldCoord) -> WorldCoord:
        """Convert world coordinates into pixel coordinates. The origin is set to the top left corner."""

        x,y,_ = libwcs.wcs.wcs2pix(self._wcs,*world)
        pix = PixCoord(x,y)

        pix -= 1 # one pixel offset
        pix *= (1,-1) # vertical reflection
        pix += (0,self.nypix) # shift by image height

        return pix
    
    @property
    def nypix(self) -> int:
        return int(self._wcs.nypix)
    
    @property
    def nxpix(self) -> int:
        return int(self._wcs.nxpix)
    
    @property
    def cdelt(self):
        _cdelt = (c_double*2).from_address(int(self._wcs.cdelt))
        _cdelt = tuple(_cdelt)
        return _cdelt
    
    @property
    def cd(self):
        _cd = (c_double*4).from_address(int(self._wcs.cd))
        _cd = np.array(_cd).reshape(2,2)
        return _cd
    
    @property
    def pc(self):
        _pc = (c_double*4).from_address(int(self._wcs.pc))
        _pc = np.array(_pc).reshape(2,2)
        return _pc