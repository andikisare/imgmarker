"""This module contains the `Catalog` class for imported catalogs."""

import warnings
from typing import List
from math import ceil

class Catalog:
    """
    A class for storing object catalog data.

    Attributes
    ----------
    labels: list[str]
        A list of the labels for each object in the catalog.

    alphas: list[float]
        A list containing either the RA or x coordinate of each object in the catalog.
    
    betas: list[float]
        A list containing either the Dec or y coordinate of each object in the catalog.
    
    coord_sys: str
        A string containing either 'wcs' or 'cartesian' for designating the input coordinate
        system.

    color: QColor
        A QColor object picked using the color picker window.
    
    size_unit: str
        A string containing the unit of size for catalog marks to use.

    size: float
        The size for catalog marks to use.
    """

    def __init__(self,path:str):
        """
        Parameters
        ----------
        path: str
            A string containing the full path of the catalog file.
        """     
        self.path:str = path
        self.labels:List[str] = []
        self.alphas:List[float] = []
        self.betas:List[float] = []
        line0 = True
        self.size_unit = None
        self.size = None
        self.color = None # default color is just None, can be changed if we want to import QColor

        for l in open(self.path):
            var = l.split(',')
            if line0:
                if (var[1].strip().lower() == 'ra'):
                    self.coord_sys:str = 'wcs'
                elif (var[1].strip().lower() == 'x'):
                    self.coord_sys:str = 'cartesian'
                else:
                    warnings.warn('WARNING: Invalid catalog coordinate system. Valid coordinate systems: "world", "cartesian"')
                    break
                try:
                    size_input = var[3].split(":")
                    self.size_unit = size_input[0].strip().lower()
                    self.size = float(size_input[1].strip())
                except:
                    warnings.warn('WARNING: Invalid size input format or no size indicated, using default size. Valid format: "[arcseconds, pixels]: [size]"')
                    self.size_unit = None
                    self.size = None
                line0 = False
            else:
                self.labels.append(var[0])
                self.alphas.append(float(var[1].strip().replace('\n', '')))
                self.betas.append(float(var[2].strip().replace('\n', '')))

    def __len__(self): return len(self.labels)
    def __bool__(self): return bool(self.labels)
