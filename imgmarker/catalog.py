import warnings
from typing import List

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
        A string containing either 'galactic' or 'cartesian' for designating the input coordinate
        system.
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

        self.color = None # default color is just None, can be changed if we want to import QColor

        for l in open(self.path):
            var = l.split(',')
            if line0:
                if (var[1].strip().lower() == 'ra'):
                    self.coord_sys:str = 'galactic'
                elif (var[1].strip().lower() == 'x'):
                    self.coord_sys:str = 'cartesian'
                else:
                    warnings.warn('WARNING: Invalid catalog coordinate system. Valid coordinate systems: "galactic", "cartesian"')
                    break
                line0 = False
            else:
                self.labels.append(var[0])
                self.alphas.append(float(var[1].strip().replace('\n', '')))
                self.betas.append(float(var[2].strip().replace('\n', '')))

    def __len__(self): return len(self.labels)
    def __bool__(self): return bool(self.labels)