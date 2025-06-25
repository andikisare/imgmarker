"""
Copyright © 2025, UChicago Argonne, LLC

Full license found at _YOUR_INSTALLATION_DIRECTORY_/imgmarker/LICENSE
"""

"""Image Marker's I/O module containing functions for reading and saving data."""

import os
import numpy as np
from imgmarker.gui import Mark
from imgmarker import image, config
import glob as _glob
from math import nan, isnan
from typing import Tuple, List
import csv
import datetime as dt

class MarkFile:
    VALID_FIELDNAMES = [
        'date','image','group',
        'label','x','y',
        'ra','dec','size'
        'size(px)','size(arcsec)'
    ]
    
    def __init__(self,path:str):
        self.path = path

        if path not in config.DEFAULT_COLORS:
            config.DEFAULT_COLORS[path] = config.GROUP_COLORS[0]

        valid, err = self.isvalid(return_err=True)
        if not valid:
            raise err
    
    def __eq__(self, value):
        if hasattr(value,'path'):
            return self.path == value.path
        else:
            return self.path == value
        
    def isvalid(self,return_err=False):
        valid = True
        err = None

        if os.path.exists(self.path):
            with open(self.path,'r') as f:
                delimiter = '|' if '|' in f.readline() else ','
                f.seek(0)
                reader = csv.DictReader(f,delimiter=delimiter)
                for fieldname in reader.fieldnames:
                    if fieldname.strip().lower() not in MarkFile.VALID_FIELDNAMES:
                        valid = False
                        err = KeyError(f'Field name "{fieldname}" in file "{self.path.split(os.sep)[-1]}" is not a valid field name.')

        if return_err:
            return valid, err
        else:
            return valid
     
    def read(self,images:List[image.Image]) -> Tuple[List[image.Image],List[Mark]]:
        """
        Takes data from marks.csv and images.csv and from them returns a list of `imgmarker.image.Image`
        objects.

        Returns
        ----------
        images: list[`imgmarker.image.Image`]
        """

        imageless = []
        
        # Get list of marks for each image
        if os.path.exists(self.path):
            with open(self.path,'r') as f:
                delimiter = '|' if '|' in f.readline() else ','
                f.seek(0)
                reader = csv.DictReader(f,delimiter=delimiter)

                for row in reader:
                    for fieldname in reader.fieldnames:
                        row[fieldname.strip().lower()] = row.pop(fieldname).strip()

                    # Default values
                    name = 'None'
                    group = config.GROUP_NAMES.index('None')
                    shape = 'rect'
                    label = 'None'
                    x,y = nan,nan
                    ra,dec = nan,nan
                    size = None
                    size_unit = None

                    # Values from row
                    if 'date' in row: date = row['date']

                    if 'image' in row: name = row['image']

                    if 'group' in row: 
                        group = config.GROUP_NAMES.index(row['group'])
                        shape = config.GROUP_SHAPES[group]
                        
                    if 'label' in row: label = row['label']

                    if 'x' in row: x = float(row['x'])
                    if 'y' in row: y = float(row['y'])

                    if 'ra' in row: ra = float(row['ra'])
                    if 'dec' in row: dec = float(row['dec'])

                    if 'size(arcsec)' in row: 
                        size = float(row['size(arcsec)'])
                        size_unit = 'arcsec'
                    
                    if 'size(px)' in row:
                        size = float(row['size(px)'])
                        size_unit = 'px'

                    if 'size' in row:
                        size = float(row['size'])
                        size_unit = 'px'

                    if name != 'None':
                        for img in images:
                            if (name == img.name) and (not isnan(float(x))) and (not isnan(float(y))):
                                args = (float(x),float(y))
                                kwargs = {'image': img, 'group': group, 'shape': shape}

                                if label != 'None': 
                                    kwargs['text'] = label

                                if size != None: 
                                    kwargs['size'] = size
                                    kwargs['size_unit'] = size_unit

                                mark = Mark(*args, **kwargs)
                                mark.dst = self.path
                                img.marks.append(mark)

                    else:
                        if isnan(float(ra)) and isnan(float(dec)):
                            args = (float(x),float(y))
                            kwargs = {'image': None, 'group': group, 'shape': shape}
                        else:
                            args = ()
                            kwargs = {'image': None,'group': group, 'shape': shape, 'ra': ra, 'dec': dec}

                        if label != 'None': 
                            kwargs['text'] = label

                        if size != None: 
                            kwargs['size'] = size
                            kwargs['size_unit'] = size_unit
                        
                        mark = Mark(*args, **kwargs)
                        mark.dst = self.path
                        imageless.append(mark)

        return images, imageless
    
    def save(self,images:List[image.Image],imageless_marks:List[Mark]) -> None:
        """
        Saves mark data.

        Parameters
        ----------

        images: list[`imgmarker.image.Image`]
            A list of Image objects for each image from the specified image directory.

        Returns
        ----------
        None
        """

        # Will organize output rows into dictionary of the path to save to

        date = dt.datetime.now(dt.timezone.utc).date().isoformat()
        rows = []

        for img in images:
            if img.seen:
                if img.duplicate == True:
                    marks = img.dupe_marks
                else:
                    marks = img.marks

                name = img.name

                if not marks: mark_list = [None]
                else: mark_list = marks.copy()
                
                for mark in mark_list:
                    
                    row = {}

                    if (mark != None) and (mark.dst == self.path):
                        group_name = config.GROUP_NAMES[mark.g]

                        if mark.text == group_name: 
                            label = 'None'
                        else: 
                            label = mark.text

                        if (img.duplicate == True) and (mark in img.dupe_marks):
                            if (mark.text == group_name):
                                label = "DUPLICATE"
                            else:
                                label = f"{mark.text}, DUPLICATE"

                        try: x, y = mark.center
                        except: x, y = nan, nan
                        
                        try: ra, dec = mark.wcs_center
                        except: ra, dec = nan, nan

                        row = {
                            'date': str(date),
                            'image': str(name),
                            'group': str(group_name),
                            'label': str(label),
                            'x': str(x),
                            'y': str(y),
                            'RA': str(ra),
                            'DEC': str(dec)
                        }
                        
                        rows.append(row)

                    # Row entries if the seen image has no marks (user looked at image without placing)
                    else:
                        row = {
                            'date': str(date),
                            'image': str(name),
                            'group': 'None',
                            'label': 'None',
                            'x': nan,
                            'y': nan,
                            'RA': nan,
                            'DEC': nan
                        }
                    
                        rows.append(row)

        for mark in imageless_marks:
            row = {}
            if mark.dst == self.path:
                group_name = config.GROUP_NAMES[mark.g]

                if mark.text == group_name: 
                    label = 'None'
                else: 
                    label = mark.text

                name = 'None'

                try: x, y = mark.center.x(), mark.center.y()
                except: x, y = nan, nan
                
                try: ra, dec = mark.wcs_center
                except: ra, dec = nan, nan

                row = {
                    'date': str(date),
                    'image': str(name),
                    'group': str(group_name),
                    'label': str(label),
                    'x': str(x),
                    'y': str(y),
                    'RA': str(ra),
                    'DEC': str(dec)
                }
                    
                rows.append(row)
        
        # Write lines if there are lines to print
        with open(self.path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

class ImagesFile:
    def __init__(self):
        self.path = os.path.join(config.SAVE_DIR,f'{config.USER}_images.csv')
    
    def __eq__(self, value):
        if hasattr(value,'path'):
            return self.path == value.path
        else:
            return self.path == value
        
    def read(self) -> Tuple[List[image.Image],List[Mark]]:
        """
        Takes data from marks.csv and images.csv and from them returns a list of `imgmarker.image.Image`
        objects.

        Returns
        ----------
        images: list[`imgmarker.image.Image`]
        """

        images:List[image.Image] = []
        
        # Get list of images from images.csv
        if os.path.exists(self.path):
            with open(self.path,'r') as f:
                delimiter = '|' if '|' in f.readline() else ','
                f.seek(0)
                reader = csv.DictReader(f,delimiter=delimiter)
                
                for row in reader:
                    keys = row.copy().keys()
                    for key in keys: row[key.strip().lower()] = row.pop(key).strip()

                    ra,dec = float(row['ra']), float(row['dec'])
                    date,name,categories,comment = row['date'], row['image'], row['categories'], row['comment']
                    categories = categories.split('+')
                    categories = [config.CATEGORY_NAMES.index(cat) for cat in categories if cat != 'None']
                    categories.sort()

                    img = image.Image(os.path.join(config.IMAGE_DIR,name))
                    img.comment = comment
                    img.categories = categories
                    img.seen = True
                    images.append(img)

        return images

    def save(self, images:List['image.Image']):
        """
        Saves image data.

        Parameters
        ----------
        images: list[`imgmarker.image.Image`]
            A list of Image objects for each image from the specified image directory.

        Returns
        ----------
        None
        """

        date = dt.datetime.now(dt.timezone.utc).date().isoformat()
        image_rows:list[dict] = []
    
        for img in images:
            if img.seen:
                name = img.name
                comment = img.comment

                category_list = img.categories
                category_list.sort()
                if (len(category_list) != 0):
                    categories = '+'.join([config.CATEGORY_NAMES[i] for i in category_list])
                else: categories = 'None'

                image_rows.append({'date': str(date),
                                    'image': str(name),
                                    'RA': str(img.wcs_center[0]),
                                    'DEC': str(img.wcs_center[1]),
                                    'categories': str(categories),
                                    'comment': str(comment)})

        with open(self.path, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=image_rows[0].keys())
            writer.writeheader()
            for row in image_rows:
                writer.writerow(row)

class FavoritesFile:
    def __init__(self):
        self.path = os.path.join(config.SAVE_DIR,f'{config.USER}_favorites.csv')
    
    def __eq__(self, value):
        if hasattr(value,'path'):
            return self.path == value.path
        else:
            return self.path == value
        
    def read(self) -> List[str]:
        """
        Takes data from favorites.csv and from them returns a list of image file names
        with full directory.

        Returns
        ----------
        favorites: list[`str`]
        """

        favorites:List[str] = []
        
        # Get list of images from favorites.csv
        if os.path.exists(self.path):
            with open(self.path,'r') as f:
                delimiter = '|' if '|' in f.readline() else ','
                f.seek(0)
                reader = csv.DictReader(f,delimiter=delimiter)
                
                for row in reader:
                    keys = row.copy().keys()
                    for key in keys: row[key.strip().lower()] = row.pop(key).strip()
                    date,name,categories,comment = row['date'], row['image'], row['categories'], row['comment']

                    favorites.append(name)
        return favorites

    def save(self, favorites:List[str], images:List['image.Image']):
        """
        Saves favorites data.

        Parameters
        ----------
        favorites: list[str]
            A list of strings of each image file name from the specified image directory.

        images: list['image.Image']
            A list of image objects.
            
        Returns
        ----------
        None
        """
        # fav_out_path = os.path.join(config.SAVE_DIR, f'{config.USER}_favorites.csv')
        date = dt.datetime.now(dt.timezone.utc).date().isoformat()
        image_rows:list[dict] = []
    
        favorited = [favorite for favorite in images if favorite.name in favorites]

        for img in favorited:
            if img.seen:
                name = img.name
                comment = img.comment

                category_list = img.categories
                category_list.sort()
                if (len(category_list) != 0):
                    categories = '+'.join([config.CATEGORY_NAMES[i] for i in category_list])
                else: categories = 'None'

                image_rows.append({'date': str(date),
                                    'image': str(name),
                                    'RA': str(img.wcs_center[0]),
                                    'DEC': str(img.wcs_center[1]),
                                    'categories': str(categories),
                                    'comment': str(comment)})
        if len(favorited) > 0:
            with open(self.path, 'w') as f:
                writer = csv.DictWriter(f, fieldnames=image_rows[0].keys())
                writer.writeheader()
                for row in image_rows:
                    writer.writerow(row)
        else:
            with open(self.path, 'w') as f:
                f.write('')
        
def markpaths() -> List[str]:
    _paths = [os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')]
    import_dir = os.path.join(config.SAVE_DIR,'imports')

    if not os.path.exists(import_dir):
        os.makedirs(import_dir)
    
    _paths += _glob.glob(os.path.join(import_dir,'*'))
    paths = []

    for path in _paths:
        try: paths.append(MarkFile(path).path)
        except: pass

    return paths

def glob(edited_images:List[image.Image]=[]) -> Tuple[List[image.Image],int]:
    """
    Globs in IMAGE_DIR, using edited_images to sort, with edited_images in order at the beginning of the list
    and the remaining unedited images in randomized order at the end of the list.

    Parameters
    ----------
    edited_images: list['imgmarker.image.Image']
        A list of Image objects containing the loaded-in information for each edited image.

    Returns
    ----------
    images: list['imgmarker.image.Image']
        A list of Image objects with the ordered edited images first and randomized unedited
        images added afterwards.
    
    idx: int
        The index to start at to not show already-edited images from a previous save.
    """

    # Find all images in image directory
    paths = sorted(_glob.glob(os.path.join(config.IMAGE_DIR, '*.*')))
    paths = [fp for fp in paths if image.pathtoformat(fp) in image.FORMATS]

    # Get list of paths to images if they are in the dictionary (have been edited)
    edited_paths = [os.path.join(config.IMAGE_DIR,img.name) for img in edited_images]
    unedited_paths = [fp for fp in paths if fp not in edited_paths]

    if config.RANDOMIZE_ORDER:
        # Shuffle the remaining unedited images
        rng = np.random.default_rng()
        rng.shuffle(unedited_paths)

    # Put edited images at the beginning, unedited images at front
    images = edited_images + [image.Image(fp) for fp in unedited_paths]
    for img in images:
        if img.incompatible == True:
            images.remove(img)

    idx = min(len(edited_images),len(paths)-1)

    return images, idx