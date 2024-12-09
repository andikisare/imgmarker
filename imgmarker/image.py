from .pyqt import QGraphicsScene, QGraphicsPixmapItem, QPixmap, QPainter, Qt, QImage
from . import mark as _mark
from io import StringIO
import os
from math import floor
import PIL.Image as pillow
from PIL.ImageQt import align8to32
from PIL.ImageFilter import GaussianBlur
from PIL.TiffTags import TAGS
from math import nan
import numpy as np
from typing import overload, Union, List, Dict
from functools import lru_cache
from astropy.visualization import ZScaleInterval, MinMaxInterval, BaseInterval, BaseStretch, ManualInterval, LinearStretch, LogStretch
from astropy.convolution import Gaussian2DKernel
from scipy.signal import convolve
from astropy.io import fits
from astropy.wcs import WCS

INTERVAL:Dict[str,BaseInterval] = {'zscale': ZScaleInterval(), 'min-max': MinMaxInterval()}
STRETCH:Dict[str,BaseStretch] = {'linear': LinearStretch(), 'log': LogStretch()}
IINFO:Dict[str,np.iinfo] = {'RGB': np.iinfo(np.uint8), 'I;16': np.iinfo(np.uint16)}
FORMATS = ['TIFF','FITS','PNG','JPEG']
pillow.MAX_IMAGE_PIXELS = None # change this if we want to limit the image size

def pathtoformat(path:str):
    ext = path.split('.')[-1].casefold()
    if ext == 'png': return 'PNG'
    if ext in {'jpeg', 'jpg'}: return 'JPEG'
    if ext in {'tiff', 'tif'}: return 'TIFF'
    if ext in {'fit', 'fits'}: return 'FITS'

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
            self.imagefile = self.load()

            self.width = self.imagefile.width
            self.height = self.imagefile.width
            
            try: self.n_frames = self.imagefile.n_frames
            except: self.n_frames = 1
            self.n_channels = len(self.imagefile.getbands())
            self.mode = self.imagefile.mode
            self.iinfo = IINFO[self.mode]

            self.wcs = self.read_wcs()
            
            self.r:float = 0.0
            self.stretch = 'linear'
            self.interval = 'min-max'
            
            self.comment = 'None'
            self.categories:List[int] = []
            self.marks:List['_mark.Mark'] = []
            self.cat_marks:List['_mark.Mark'] = []
            self.seen:bool = False
            self.catalogs:List[str] = []

            self.imagefile.close()
    
    @property
    def interval(self) -> ManualInterval: 
        """ 
        Interval of the image brightness.\n
        Set with `Image.interval = 'zscale'` or `Image.interval = 'min-max'`. 
        """

        interval = INTERVAL[self._interval_str]
        vlims = interval.get_limits(self.vibrance)
        return ManualInterval(*vlims)
    @interval.setter
    def interval(self,value): self._interval_str = value

    @property
    def stretch(self) -> BaseStretch:
        """
        Stretch of the image brightness.\n
        Set with `Image.stretch = 'linear'` or `Image.stretch = 'log'`.
        """

        return STRETCH[self._stretch_str]
    
    @stretch.setter
    def stretch(self,value): self._stretch_str = value

    @property
    def scaling(self): return self.stretch + self.interval

    @property
    def vibrance(self):
        if self.n_channels == 3:
            arr = np.array(self.load().convert('HSV'))
            v = arr[:, :, 2]
        else: v = np.array(self.load())
        return v

    @property
    @lru_cache(maxsize=1)
    def wcs_center(self) -> list:
        try: return self.wcs.all_pix2world([[self.width/2, self.height/2]], 0)[0]
        except: return nan, nan

    def read_wcs(self):
        """Reads WCS information from headers if available. Returns `astropy.wcs.WCS`."""
        try:
            if self.format == 'FITS':
                with fits.open(self.path) as hdulist:
                    wcs = WCS(hdulist[0].header)
                return wcs
            else:
                meta_dict = {TAGS[key] : self.load().tag[key] for key in self.load().tag_v2}
                
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
                wcs = WCS(header)
            return wcs
        except: return None

    def load(self) -> pillow.Image:
        if self.format == 'FITS':
            with fits.open(self.path) as f:
                arr = np.flipud(f[0].data)
                arr = 65535 * (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

            file = pillow.fromarray(arr.astype(np.uint16),mode='I;16')

        else: file = pillow.open(self.path)

        file.seek(self.frame)
        return file
    
    def close(self):
        self.imagefile.close()
        self.setPixmap(QPixmap())
    
    def tell(self): return self.imagefile.tell()

    def seek(self,frame:int=0):
        """Switches to a new frame if it exists"""

        frame = floor(frame)
        
        if frame > self.n_frames - 1: frame = 0
        elif frame < 0: frame = self.n_frames - 1

        self.frame = frame
        self.imagefile = self.load()

        self.width = self.imagefile.width
        self.height = self.imagefile.width
        
        # reapply blur
        self.blur()

    def rescale(self):
        if self.n_channels == 3:
            arr = np.array(self.imagefile.copy().convert('HSV'))
            h,s,v = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

            v = (self.scaling(v))*self.iinfo.max
            arr[:, :, 0], arr[:, :, 1], arr[:, :, 2] = h,s,v

            image_scaled = pillow.fromarray(arr.astype(self.iinfo.dtype),mode='HSV').convert('RGB')

        else:
            arr = np.array(self.imagefile.copy())
            arr = self.scaling(arr)*self.iinfo.max
            image_scaled = pillow.fromarray(arr.astype(self.iinfo.dtype),mode=self.mode)
        
        self.setPixmap(self.topixmap(image_scaled))

    def toqimage(self,image:pillow.Image):
        if self.format == 'FITS':
            data = align8to32(image.tobytes(),image.width,image.mode)
            qim = QImage(data,image.width,image.height,QImage.Format.Format_Grayscale16)
        else: qim = image.toqimage()
        return qim

    def topixmap(self,image:pillow.Image) -> QPixmap:
        """Creates a QPixmap with a pillows on each side to allow for fully zooming out."""

        qimage = self.toqimage(image)
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

        newfile = self.load()

        if self.r != 0:
            if self.iinfo.bits <= 8:
                newfile = newfile.filter(GaussianBlur(self.r))
            else:
                _arr = np.array(newfile)
                kernel = Gaussian2DKernel(self.r).array

                # Compute padding (based on astropy)
                ph, pw = np.array(kernel.shape) // 2
                pad_width = ((ph,), (pw,))
      
                # Add padding
                _arr = np.pad(_arr, pad_width=pad_width, mode='edge')

                # Convolve padded image
                _arr = convolve(_arr,kernel,mode='same')
                
                # Remove padding
                arr = _arr[ph:-ph, pw:-pw]
                newfile = pillow.fromarray(arr.astype(self.iinfo.dtype),self.mode)

        self.imagefile = newfile.copy()
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


