Loading
======================

Supported image formats
----------

Currently, Image Marker supports the following image formats (file types):

- FITS/FIT
- TIFF/TIF
- JPEG/JPG
- PNG

These formats are supported with the following limitations:

- FITS/FIT
  - Files **MUST** have only an image(s) in them, as any FITS/FIT file with a table or other data that isn't image data (header data is of course okay) will not be handled by Image Marker
  - Image Marker will only show FITS/FIT in grayscale, since there is no functionality for creating RGB images from grayscale images in Image Marker
  - Supports logging WCS coordinates (RA and Dec in degrees)
  - Supports multiple frames (if two images are embedded in one file, seeking to the other image within the same file is available)
  - 8 and 16 bit
- TIFF/TIF
  - Supports RGB and grayscale images
  - Supports logging WCS coordinates (RA and Dec in degrees) 
    - **Only when WCS solution is embedded in the TIFF/TIF header using** `STIFF <https://www.astromatic.net/software/stiff/>`_ **for embedding WCS solutions.**
  - Supports multiple frames (if two images are embedded in one file, seeking to the other image within the same file is available)
  - Supports 8 bit images
- JPEG/JPG
  - Supports RGB with Alpha channel
  - **Does not** support logging WCS coordinates
  - Supports 8 bit images
- PNG
  - Supports RGB with Alpha channel
  - **Does not** support logging WCS coordinates
  - Supports 8 bit images

Image loading
------------
When Image Marker is first opened, the user is prompted to select the directory in which all of their output data will be automatically saved. The user is then prompted to select the directory from which to load images. The currently supported image formats are under `Supported image formats`_. FITS files support up to a 16 bit depth, which is a limitation of PyQt. For TIFFs, PNGs and JPEGs, Image Marker currently only officially supports RGB color channels with 8 bits per channel, but this may be expanded in the future. 
Pillow is used to open TIFF, PNG and JPEG files. Though Pillow can currently handle FITS files, this is a relatively recent feature. As such we use astropy to open FITS files, so as to maintain compatibility with older versions of Python. 

Image Marker can handle multi-frame FITS and TIFF files. If a file has multiple frames, these frames can be cycled through using spacebar, or by using the **View > Frames** dialog. WCS information stored in FITS and TIFF files is also accessed by Image Marker. If an image contains a WCS solution in its header, Image Marker will display the WCS coordinates of the cursor in addition to the pixel coordinates.
