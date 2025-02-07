from astropy.io.fits import open as _open
from astropy.io.fits import ImageHDU, PrimaryHDU, Header, HDUList

def open(path):
    _hdus = _open(path)

    if any(isinstance(hdu,ImageHDU) for hdu in _hdus):
        hdus = HDUList([_hdu for _hdu in _hdus if isinstance(_hdu,ImageHDU)])
    else:
        hdus = HDUList([_hdu for _hdu in _hdus if isinstance(_hdu,PrimaryHDU)])

    return hdus