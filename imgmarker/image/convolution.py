import numpy as np
from scipy.ndimage import uniform_filter

def sigma_to_size(sigma, n:int):
    """
    Calculates the equivalent box filter sizes from a Gaussian filter radius.

    Algorithm taken from P. Kovesi (2010).

    Parameters
    ----------
    sigma: 
        Radius of the Gaussian filter.
    n: int
        Number of equivalent box filters.
    
    Returns
    ----------
    sizes: list
        Equivalent box filter sizes.

    """
    w = np.sqrt((12*sigma**2/n)+1)
    
    wl = np.floor(w)
    if wl % 2 == 0: wl -= 1
    wu = wl+2
				
    m = int((12*sigma**2 - n*wl*wl - 4*n*wl - 3*n)/(-4*wl - 4))
	
    sizes = [wl]*m + [wu]*(n-m) 

    return sizes

def gaussian_filter(array:np.ndarray, sigma, n:int=3) -> np.ndarray:
    """
    Applies an approximate gaussian filter as a series of `n` box filters.
    
    Parameters
    ----------
    array: `numpy.ndarray`
        Array to be filtered.
    sigma: 
        Radius of the Gaussian filter.
    n: int, optional
        Number of equivalent box filters. Default is 3.
    
    Returns
    ----------
    out: `numpy.ndarray`
        Filtered array.
    """

    out = array.copy()
    if sigma > 0:
        sizes = sigma_to_size(sigma, 3)
        for s in sizes:
            if out.ndim == 3:
                for i in range(out.shape[2]):
                    out[:, :, i] = uniform_filter(out[:, :, i], s)
            else:
                out = uniform_filter(out,s)
    return out
