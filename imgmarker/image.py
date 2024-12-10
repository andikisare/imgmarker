from .pyqt import QGraphicsScene, QGraphicsPixmapItem, QPixmap, QPainter, Qt, QImage
from . import mark as _mark
from io import StringIO
import os
from math import floor
import PIL.Image as pillow
from PIL.TiffTags import TAGS
from math import nan
import numpy as np
from typing import overload, Union, List
from astropy.visualization import ZScaleInterval, MinMaxInterval, ManualInterval, LinearStretch, LogStretch
from astropy.convolution import Gaussian2DKernel
from scipy.signal import convolve
from astropy.io import fits
from astropy.wcs import WCS
from enum import Enum

class Interval(Enum):
    ZSCALE = ZScaleInterval()
    MINMAX = MinMaxInterval()
    
class Stretch(Enum):
    LINEAR = LinearStretch()
    LOG = LogStretch()

class Mode(Enum):
    RGB = 0
    I16 = 1
    def __init__(self,value):
        self.format = {0: QImage.Format.Format_RGB888, 
                       1: QImage.Format.Format_Grayscale16}[value]
        self.iinfo:np.iinfo = {0: np.iinfo(np.uint8), 
                               1: np.iinfo(np.uint16)}[value]

FORMATS = ['TIFF','FITS','PNG','JPEG']

pillow.MAX_IMAGE_PIXELS = None # change this if we want to limit the image size

def pathtoformat(path:str):
    ext = path.split('.')[-1].casefold()
    if ext == 'png': return 'PNG'
    if ext in {'jpeg', 'jpg'}: return 'JPEG'
    if ext in {'tiff', 'tif'}: return 'TIFF'
    if ext in {'fit', 'fits'}: return 'FITS'

def align8to32(bytes: bytes, width: int, bits_per_pixel: str) -> bytes:
    """
    converts each scanline of data from 8 bit to 32 bit aligned. slightly modified from astropy
    """

    # calculate bytes per line and the extra padding if needed
    bits_per_line = bits_per_pixel * width
    full_bytes_per_line, remaining_bits_per_line = divmod(bits_per_line, 8)
    bytes_per_line = full_bytes_per_line + (1 if remaining_bits_per_line else 0)

    extra_padding = -bytes_per_line % 4

    # already 32 bit aligned by luck
    if not extra_padding:
        return bytes

    new_data = [
        bytes[i * bytes_per_line : (i + 1) * bytes_per_line] + b"\x00" * extra_padding
        for i in range(len(bytes) // bytes_per_line)
    ]

    return b"".join(new_data)

def rgb_to_hsv(r, g, b):
    r = np.array(r)
    g = np.array(g)
    b = np.array(b)

    maxc = np.max((r, g, b),axis=0)
    minc = np.min((r, g, b),axis=0)
    v = maxc
    
    np.seterr(divide='ignore', invalid='ignore')
    s = (maxc-minc) / maxc

    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    np.seterr()

    h = 4.0+gc-rc
    h = np.where(r==maxc,bc-gc,h)
    h = np.where(g==maxc,2.0+rc-bc,h)
    h = np.where(minc == maxc,0,h)

    h = (h/6.0) % 1.0
    
    return h, s, v

def hsv_to_rgb(h, s, v):
    h = np.array(h)
    s = np.array(s)
    v = np.array(v)

    r = np.where(s==0,v,np.nan)
    g = np.where(s==0,v,np.nan)
    b = np.where(s==0,v,np.nan)

    i = (h*6.0).astype(int) # XXX assume int() truncates!
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6

    conv = [[v,t,p], [q,v,p], [p,v,t], [p,q,v], [t,p,v], [v,p,q]]
    
    for j in range(0,6):
        r = np.where(i==j,conv[j][0],r)
        g = np.where(i==j,conv[j][1],g)
        b = np.where(i==j,conv[j][2],b)
    
    return r, g, b

def read_wcs(f):
    """Reads WCS information from headers if available. Returns `astropy.wcs.WCS`."""
    try:
        if isinstance(f,fits.HDUList):
            return WCS(f[0].header)
        else:
            meta_dict = {TAGS[key] : f.tag[key] for key in f.tag_v2}
            
            long_header_str = meta_dict['ImageDescription'][0]

            line_length = 80

            # Splitting the string into lines of 80 characters
            lines = [long_header_str[i:i+line_length] for i in range(0, len(long_header_str), line_length)]
            
            # Join the lines with newline characters to form a properly formatted header string
            corrected_header_str = "\n".join(lines)

            # Use an IO stream to mimic a file
            header_stream = StringIO(corrected_header_str)

            # Read the header using astropy.io.fits
            header = fits.Header.fromtextfile(header_stream)

            # Create a WCS object from the header
            return WCS(header)
    except: return None

class Image(QGraphicsPixmapItem):
    """
    Image class based on the PyQt QGraphicsPixmapItem.

    Attributes
    ----------
    path: str
        Path to the image.

    name: str
        File name.

    format: str
        Image format. Can be TIFF, FITS, PNG, or JPEG.

    frame: int
        Current frame of the image.

    n_frame: int
        Number of frames in the image.

    imagefile: `PIL.Image.ImageFile`
        Pillow imagefile object that allows loading of image data and image manipulation.

    width: int
        Image width.

    height: int
        Image height.

    wcs: `astropy.wcs.WCS` or None
        WCS solution.

    wcs_center: list[float]
        Center of the image in WCS coordinates.

    r: float
        Blur radius applied to the image.

    stretch: `BaseStretch`, default=`LinearStretch()`
        Stretch of the image brightness. Can be set with `Image.stretch = 'linear'` or `Image.stretch = 'log'`

    interval: `BaseInterval`, default=`ZScaleInterval()`
        Interval of the image brightness. Can be set with `Image.interval = 'zscale'` or `Image.stretch = 'min-max'`

    comment: str
        Image comment.

    categories: list[int]
        List containing the categories for this image.

    marks: list[imgmarker.mark.Mark]
        List of the marks in this image.

    cat_marks: list[imgmarker.mark.Mark]
        List of catalog marks in this image.

    seen: bool
        Whether this image has been seen by the user or not.

    catalogs: list[str]
        List of paths to the catalogs that have been imported for this image
    """
    
    def __init__(self,path:str):
        """
        Parameters
        ----------
        path: str 
            Path to the image.
        """
        
        super().__init__(QPixmap())

        self.path = path
        self.name = path.split(os.sep)[-1]
        self.format = pathtoformat(path)

        if self.format in FORMATS:
            
            self.frame:int = 0
            metadata = self.read_metadata()
            self.mode:str = metadata['mode']
            self.n_channels = metadata['n_channels'] 
            self.n_frames = metadata['n_frames']
            self.wcs = metadata['wcs']

            self.r:float = 0.0
            self.stretch = Stretch.LINEAR
            self.interval = Interval.MINMAX
            
            self.comment = 'None'
            self.categories:List[int] = []
            self.marks:List['_mark.Mark'] = []
            self.cat_marks:List['_mark.Mark'] = []
            self.seen:bool = False
            self.catalogs:List[str] = []

    @property
    def interval(self): 
        """ Interval of the image brightness."""

        interval = self._interval
        vlims = interval.get_limits(self.vibrance)
        return ManualInterval(*vlims)
    @interval.setter
    def interval(self,enum:Interval): self._interval = enum.value

    @property
    def stretch(self):
        """Stretch of the image brightness."""
        return self._stretch
    @stretch.setter
    def stretch(self,enum:Stretch): self._stretch = enum.value

    @property
    def scaling(self): return self.stretch + self.interval

    @property
    def vibrance(self):
        if self.n_channels == 3:
            array = self.read()
            r,g,b = array[:, :, 0], array[:, :, 1], array[:, :, 2]
            v = np.max((r, g, b),axis=0)
        else: v = self.read()
        return v
    
    @property
    def width(self):
        return self.array.shape[1]
    
    @property
    def height(self):
        return self.array.shape[0]

    @property
    def wcs_center(self) -> list:
        try: return self.wcs.all_pix2world([[self.width/2, self.height/2]], 0)[0]
        except: return nan, nan

    def read(self) -> np.ndarray:
        if self.format == 'FITS':
            with fits.open(self.path) as f:
                data = np.flipud(f[self.frame].data)
                data = 65535 * (data - np.min(data)) / (np.max(data) - np.min(data))
        else:
            with pillow.open(self.path) as f:
                f.seek(self.frame)
                data = np.array(f)
        return data
    
    def read_metadata(self) -> dict:
        metadata = {}
        if self.format == 'FITS':
            metadata['mode'] = Mode.I16
            metadata['n_channels'] = 1
            with fits.open(self.path) as f:
                metadata['n_frames'] = len(f)
                metadata['wcs'] = read_wcs(f)
        else:
            with pillow.open(self.path) as f: 
                metadata['mode'] = Mode[f.mode.replace(';','')]
                metadata['n_channels'] = len(f.getbands())
                try: metadata['n_frames'] = f.n_frames
                except: metadata['n_frames'] = 1
                metadata['wcs'] = read_wcs(f)
        
        return metadata
    
    def close(self):
        self.array = None
        self.setPixmap(QPixmap())
    
    def seek(self,frame:int=0):
        """Switches to a new frame if it exists"""

        frame = floor(frame)
        
        if frame > self.n_frames - 1: frame = 0
        elif frame < 0: frame = self.n_frames - 1

        self.frame = frame
        self.array = self.read()
        
        # reapply blur
        self.blur()

    def rescale(self):
        if self.n_channels == 3:
            array = self.array.copy()
            _r,_g,_b = array[:, :, 0], array[:, :, 1], array[:, :, 2]
            h,s,v = rgb_to_hsv(_r,_g,_b)

            v = (self.scaling(v))*self.mode.iinfo.max
            r,g,b = hsv_to_rgb(h,s,v)

            array_scaled = np.stack([r,g,b],-1)
        
        else:
            array_scaled = self.scaling(self.array.copy())*self.mode.iinfo.max
        
        self.setPixmap(self.topixmap(array_scaled.astype(self.mode.iinfo.dtype)))

    def toqimage(self,array:np.ndarray) -> QImage:
        width, height  = array.shape[1], array.shape[0]
        data = align8to32(array.tobytes(),width,self.mode.iinfo.bits)

        if len(array.shape) == 3:
            n = array.shape[2]
            qim = QImage(data,width,height,n*width,self.mode.format)
        else:
            qim = QImage(data,width,height,self.mode.format)

        return qim

    def topixmap(self,array:np.ndarray) -> QPixmap:
        """Creates a QPixmap with a pillows on each side to allow for fully zooming out."""

        qimage = self.toqimage(array)
        pixmap_base = QPixmap.fromImage(qimage)

        w, h = self.width, self.height
        _x, _y = int(w*4), int(h*4)

        pixmap = QPixmap(w*9,h*9)

        painter = QPainter(pixmap)
        painter.drawPixmap(_x, _y, pixmap_base)
        painter.end()

        return pixmap
    
    @overload
    def blur(self) -> None: 
        """Applies the blur to the image"""
    @overload
    def blur(self,value) -> None:
        """Applies the blur to the image"""
    def blur(self,*args):
        if len(args) > 0: 
            value = args[0]
            if callable(value): r = value()
            else: r = value
            self.r = floor(r)/10

        _out = self.read()

        if self.r != 0:
            # Create kernel and compute padding
            kernel = Gaussian2DKernel(self.r).array
            ph, pw = np.array(kernel.shape) // 2
            pad_width = ((ph,), (pw,))

            def _blur(c):
                # Add padding, convolve, then remove padding
                c = np.pad(c, pad_width=pad_width, mode='edge')
                c = convolve(c,kernel,mode='same')
                c = c[ph:c.shape[0]-ph, pw:c.shape[1]-pw]                
                return c
            
            if self.n_channels > 1:
                out = [_blur(_out[:, :, i]) for i in range(self.n_channels)]
                out = np.stack(out,-1)
            else: out = _blur(_out)

        else: out = _out

        self.array = out.copy().astype(self.mode.iinfo.dtype)
        self.rescale()

class ImageScene(QGraphicsScene):
    """A class for storing and manipulating the information/image that is currently displayed."""
    def __init__(self,image:Image):
        super().__init__()
        self.image = image

        self.setBackgroundBrush(Qt.GlobalColor.black)
        self.addItem(self.image)

    def update(self,image:Image):
        """Updates the current image with a new image."""
        # Remove items
        for item in self.items(): self.removeItem(item)

        # Update the pixmap
        self.image = image
        self.addItem(self.image)
        self.setSceneRect(0,0,9*self.image.width,9*self.image.height)

    @overload
    def mark(self,x:float,y:float,shape='ellipse',text:Union[int,str]=0) -> '_mark.Mark': ...
    @overload
    def mark(self,ra:float=None,dec:float=None,shape='ellipse',text:Union[int,str]=0) -> '_mark.Mark': ...
    @overload
    def mark(self,mark:'_mark.Mark') -> '_mark.Mark': ... 

    def mark(self,*args,**kwargs) -> '_mark.Mark':
        """Creates a mark object and adds it to the image scene and returns the mark."""

        if len(args) == 1: mark = args[0]
        else: mark = _mark.Mark(*args,image=self.image,**kwargs)
        self.addItem(mark.label)
        self.addItem(mark)
        return mark
    
    def rmmark(self,mark:'_mark.Mark') -> None:
        """Removes the specified mark from the image scene."""

        self.removeItem(mark)
        self.removeItem(mark.label)


