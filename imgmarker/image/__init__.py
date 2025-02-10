"""This module contains code for the `Image` class and image manipulation."""

from ..gui.pyqt import *
from ..gui import Mark
from io import StringIO
import os
from math import floor
import PIL.Image as pillow
from PIL.TiffTags import TAGS
from math import nan
import numpy as np
from typing import overload, Union, List
from astropy.visualization import ZScaleInterval, MinMaxInterval, ManualInterval, LinearStretch, LogStretch
import astropy.convolution
import scipy.signal
from . import fits
from astropy.wcs import WCS
from enum import Enum

class Interval:
    ZSCALE = ZScaleInterval()
    MINMAX = MinMaxInterval()
    
class Stretch:
    LINEAR = LinearStretch()
    LOG = LogStretch()  

class Mode(Enum):
    RGB = 0
    RGBA = 1
    I8 = 2
    I16 = 3
    
    def __init__(self,value):
        self.format = {0: QImage.Format.Format_RGB888, 
                       1: QImage.Format.Format_RGBA8888,
                       2: QImage.Format.Format_Grayscale8,
                       3: QImage.Format.Format_Grayscale16}[value]
        self.iinfo:np.iinfo = {0: np.iinfo(np.uint8), 
                               1: np.iinfo(np.uint8),
                               2: np.iinfo(np.uint8),
                               3: np.iinfo(np.uint16)}[value]

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
    converts each scanline of data from 8 bit to 32 bit aligned. slightly modified from Pillow
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

def vibrance(c,mode:Mode):
    if mode == Mode.RGB:
        v = np.max(c, axis=2)
    elif mode == Mode.RGBA:
        v = np.max(c[:, :, :3], axis=2)
    else: 
        v = c
    return v

def convolve(c,kernel,mode):
    nans =  np.isnan(c)
    ## Use astropy if there are nans
    if True in nans: 
        method = scipy.signal.choose_conv_method(c,kernel,mode=mode)
        if method == 'direct': 
            c = astropy.convolution.convolve(c,kernel,boundary='fill',preserve_nan=True)
        else:
            c = astropy.convolution.convolve_fft(c,kernel,boundary='fill',preserve_nan=True)
    
    ## Use scipy otherwise
    else: 
        c = scipy.signal.convolve(c,kernel,mode=mode)
        c[nans] = np.nan

    return c

def read_wcs(f):
    """Reads WCS information from headers if available. Returns `astropy.wcs.WCS`."""
    try:
        if isinstance(f,fits.PrimaryHDU) or isinstance(f,fits.ImageHDU):
            
            if not 'CRPIX1' in f.header.keys(): return None
            else: 
                _header = f.header.copy()
                _header['NAXIS'] = 2
                return WCS(_header)
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
        self.incompatible = False
        if self.format in FORMATS:
            
            self.frame:int = 0
            metadata = self.read_metadata()
            if metadata != None:
                self.incompatible = False
                self.duplicate = False
                self.width = metadata['width']
                self.height = metadata['height']
                self.mode:Mode = metadata['mode']
                self.n_channels = metadata['n_channels'] 
                self.n_frames = metadata['n_frames']
                self.wcs:WCS = metadata['wcs']

                self.r:float = 0.0
                self.stretch = Stretch.LINEAR
                self.interval = Interval.MINMAX
                
                self.comment = 'None'
                self.categories:List[int] = []
                self.marks:List['Mark'] = []
                self.cat_marks:List['Mark'] = []
                self.seen:bool = False
                self.catalogs:List[str] = []
            else:
                self.incompatible = True

    @property
    def scaling(self):
        return self.stretch + ManualInterval(*self.vlims)

    @property
    def v(self):
        return vibrance(self.array,self.mode)
    
    @property
    def vlims(self):
        v = vibrance(self._array,self.mode) 
        vlims = self.interval.get_limits(v)
        return vlims
    
    @property
    def wcs_center(self) -> list:
        try: return self.wcs.all_pix2world([[self.width/2, self.height/2]], 0)[0]
        except: return nan, nan

    def read(self) -> np.ndarray:
        if self.format == 'FITS':
            with fits.open(self.path) as f:
                data = f[self.frame].data
                if self.n_channels > 1:
                    data = np.dstack((data[0], data[1], data[2]))
                data = np.flipud(data)
                data = (2**self.mode.iinfo.bits - 1) * ((data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data)))
        
        else:
            with pillow.open(self.path) as f:
                f.seek(self.frame)
                data = np.array(f)

        return data
    
    def read_metadata(self) -> dict:
        metadata = {}
        if self.format == 'FITS':
            with fits.open(self.path) as f:
                try:
                    metadata['width'] = f[self.frame].header['NAXIS2']
                    metadata['height'] = f[self.frame].header['NAXIS1']

                    # If more than 1 channel, set number of channels and force 8 bits per channel
                    
                    if 'NAXIS3' in f[self.frame].header.keys():
                        metadata['n_channels'] = abs(f[self.frame].header['NAXIS3'])
                        metadata['mode'] = Mode.RGB

                    # Otherwise set number of channels to 1, get the bit depth from header
                    else: 
                        metadata['n_channels'] = 1
                        if abs(f[self.frame].header['BITPIX']) == 8: metadata['mode'] = Mode.I8
                        else: metadata['mode'] = Mode.I16

                    metadata['n_frames'] = len(f)
                    metadata['wcs'] = read_wcs(f[self.frame])
                    
                except:
                    print(f"File \"{self.name}\" is not compatible and will not be loaded. Skipping \"{self.name}\".")
                    self.incompatible = True
                    return None

        else:
            with pillow.open(self.path) as f: 
                f.seek(self.frame)
                metadata['width'] = f.width
                metadata['height'] = f.height
                metadata['mode'] = Mode[f.mode.replace(';','')]
                metadata['n_channels'] = len(f.getbands())
                try: metadata['n_frames'] = f.n_frames
                except: metadata['n_frames'] = 1
                metadata['wcs'] = read_wcs(f)
        
        return metadata
    
    def close(self):
        self._array = None
        self.array = None
        self.setPixmap(QPixmap())
    
    def seek(self,frame:int=0):
        """Switches to a new frame if it exists"""

        # Set frame
        frame = floor(frame)
        
        if frame > self.n_frames - 1: frame = 0
        elif frame < 0: frame = self.n_frames - 1

        self.frame = frame

        # Read data from the frame
        self._array = self.read()
        self.array = self._array
        self.width = self._array.shape[1]
        self.height = self._array.shape[0]
        
        # Apply blur (and scaling)
        self.blur()

    def rescale(self):
        out = self.array.astype(np.float64)

        if (self.mode == Mode.RGB) or (self.mode == Mode.RGBA):
            # Calculate scale factor
            scale = self.mode.iinfo.max*self.scaling(self.v)/self.v

            # Apply scale factor
            out[:, :, 0] *= scale
            out[:, :, 1] *= scale
            out[:, :, 2] *= scale

            # Truncate values greater than the max pixel value for this mode
            out = np.minimum(self.mode.iinfo.max,out)

        else:
            out = self.mode.iinfo.max*self.scaling(out)

        self.setPixmap(self.topixmap(out.astype(self.mode.iinfo.dtype)))

    def toqimage(self,array:np.ndarray) -> QImage:
        width, height  = array.shape[1], array.shape[0]
        data = array.tobytes()

        if self.mode.iinfo.bits > 8: data = align8to32(data,width,self.mode.iinfo.bits)

        if array.ndim == 3:
            n = array.shape[2]
            qim = QImage(data,width,height,n*width,self.mode.format)
        else:
            qim = QImage(data,width,height,self.mode.format)

        return qim

    def topixmap(self,array:np.ndarray) -> QPixmap:
        """Creates a QPixmap from an array."""
        
        qimage = self.toqimage(array)
        pixmap = QPixmap.fromImage(qimage)

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

        if self.r != 0:
            # Create kernel and compute padding
            kernel = astropy.convolution.Gaussian2DKernel(self.r).array
            ph, pw = np.array(kernel.shape) // 2
            pad_width = ((ph,), (pw,))

            def _blur(c):
                # Add padding, convolve, then remove padding
                c = np.pad(c, pad_width=pad_width, mode='edge')
                c = convolve(c,kernel,mode='same')
                c = c[ph:c.shape[0]-ph, pw:c.shape[1]-pw]          
                return c
            
            if self.n_channels > 1:
                out = [_blur(self._array[:, :, i]) for i in range(self.n_channels)]
                out = np.stack(out,-1)
            else: out = _blur(self._array)

        else: out = self._array

        self.array = out.copy().astype(self.mode.iinfo.dtype)
        self.rescale()

class ImageScene(QGraphicsScene):
    """A class in which images and marks are stored."""
    def __init__(self,image:Image):
        super().__init__()
        self.image = image

        self.setBackgroundBrush(Qt.GlobalColor.black)
        self.addItem(self.image)
        self.setSceneRect(-4*self.image.width,-4*self.image.height,9*self.image.width,9*self.image.height)

    def update_image(self,image:Image):
        """Updates the current image with a new image."""
        # Remove items
        for item in self.items(): self.removeItem(item)

        # Update the pixmap
        self.image = image
        self.addItem(self.image)
        self.setSceneRect(-4*self.image.width,-4*self.image.height,9*self.image.width,9*self.image.height)

    @overload
    def mark(self,x:float,y:float,shape='ellipse',text:Union[int,str]=0) -> 'Mark': ...
    @overload
    def mark(self,ra:float=None,dec:float=None,shape='ellipse',text:Union[int,str]=0) -> 'Mark': ...
    @overload
    def mark(self,mark:'Mark') -> 'Mark': ... 

    def mark(self,*args,**kwargs) -> 'Mark':
        """Creates a mark object and adds it to the image scene and returns the mark."""

        if len(args) == 1: mark = args[0]
        else: mark = Mark(*args,image=self.image,**kwargs)
        self.addItem(mark.label)
        self.addItem(mark)
        return mark
    
    def rmmark(self,mark:'Mark') -> None:
        """Removes the specified mark from the image scene."""

        self.removeItem(mark)
        self.removeItem(mark.label)

class ImageView(QGraphicsView):
    """A class in which the image scene is stored."""
    def __init__(self,scene:ImageScene):
        super().__init__(scene)

        self.zoom_level = 1
        self.cursor_focus = False

        self.move(0, 0)
        self.setTransformationAnchor(self.ViewportAnchor(1))

        # Mouse tracking
        self.setMouseTracking(True)

        # Disable scrollbars
        self.verticalScrollBar().blockSignals(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.horizontalScrollBar().blockSignals(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        #Install event filter for zooming
        self.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        """
        Performs operations based on the event source and type.

        Parameters
        ----------
        source: `QObject` object
            Source of the event
        event: `QEvent` object
            Event

        Returns
        ----------
        True if the event triggered an some operation.
        """

        if (source == self.viewport()) and (event.type() == 31):
            x = event.angleDelta().y()/120
            self.zoom(1.2**x)
            return True

        return super().eventFilter(source, event)
    
    def scene(self) -> ImageScene:
        """Returns the associated image scene."""
        return super().scene()
    
    def mouse_pix_pos(self,correction:bool=True):
        """
        Gets mouse image coordinates.

        Returns
        ----------
        pix_pos: `QPoint`
            position of mouse in the image.
        """

        view_pos = self.mapFromGlobal(self.cursor().pos())
        scene_pos = self.mapToScene(view_pos)

        # Get the pixel coordinates (including padding; half-pixel offset required)
        pix_pos = self.scene().image.mapFromScene(scene_pos)

        # Correct half-pixel error
        if correction: pix_pos -= QPointF(0.5,0.5)
        
        return pix_pos.toPoint()
    
    def mouse_pos(self):
        """
        Gets mouse position.

        Returns
        ----------
        view_pos: `QPoint`
            position of mouse in the image view.
        """

        return self.mapFromGlobal(self.cursor().pos())
    
    def zoom(self,scale:float,mode:str='mouse'):
        """
        Zoom in on the image.

        Parameters
        ----------
        scale: str
            Scale of the zoom. Greater than 1 means zooming in, less than 1 means zooming out
        mode: str, optional
            Zoom mode. To zoom from the center of the viewport, use mode='viewport'. To zoom from the mouse
            cursor location, use mode='mouse'. Defaults to 'mouse'.
        
        Returns
        ----------
        None
        """

        if self.zoom_level*scale > 1/3:
            self.zoom_level *= scale
            if mode == 'viewport': center = self.viewport().rect().center()
            if mode == 'mouse': center = self.mouse_pos()

            transform = self.transform()
            center = self.mapToScene(center)
            transform.translate(center.x(), center.y())
            transform.scale(scale, scale)
            transform.translate(-center.x(), -center.y())
            self.setTransform(transform)

    def zoomfit(self):
        """Fit the image view in the viewport."""

        self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.zoom(scale=9,mode='viewport')
        self.zoom_level = 1

    def center_cursor(self):
        """Center on the cursor."""

        center = self.viewport().rect().center()
        scene_center = self.mapToScene(center)
        pix_pos = self.mouse_pix_pos(correction=False)

        delta = scene_center.toPoint() - pix_pos
        self.translate(delta.x(),delta.y())
        
        if self.cursor_focus:
            global_center = self.mapToGlobal(center)
            self.cursor().setPos(global_center)
    


