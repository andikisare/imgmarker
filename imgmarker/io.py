"""Image Marker's I/O module containing functions for loading and saving data."""

import os
import numpy as np
from .gui import Mark
from . import image
from . import config
import glob as _glob
from math import nan, isnan
from typing import Tuple, List
import csv
import datetime as dt

def markpaths() -> List[str]:
    paths = [os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')]
    import_dir = os.path.join(config.SAVE_DIR,'imports')

    if not os.path.exists(import_dir):
        os.makedirs(import_dir)
    
    paths += _glob.glob(os.path.join(import_dir,'*'))
    return paths

def savefav(date:str,images:List['image.Image'],fav_list:List[str]) -> None:
    """
    Creates a file, \'favorites.csv\', in the save directory containing all images that were favorited.
    This file is in the same format as \'images.csv\' so that a user can open their favorites file to show
    only favorited images with a little bit of file name manipulation. More details on how to do this can
    be found in \'README.md\'.

    Parameters
    ----------
    date: str
        A string containing the current date in ISO 8601 extended format.

    images: list[`imgmarker.image.Image`]
        A list of Image objects for each image from the specified image directory.

    fav_list: list[str]
        A list of strings containing the file names of each favorited image.

    Returns
    ----------
    None
    """

    image_lines = []
    name_lengths = []
    img_ra_lengths = []
    img_dec_lengths = []
    category_lengths = []
    comment_lengths = []

    fav_out_path = os.path.join(config.SAVE_DIR, f'{config.USER}_favorites.csv')

    # Remove the file if it exists
    if os.path.exists(fav_out_path): os.remove(fav_out_path)
    
    fav_images = [img for img in images if img.name in fav_list]

    if len(fav_list) != 0:
        for img in fav_images:
            if img.seen:
                name = img.name
                comment = img.comment

                category_list = img.categories
                category_list.sort()
                if (len(category_list) != 0):
                    categories = ','.join([config.CATEGORY_NAMES[i] for i in category_list])
                else: categories = 'None'

                img_ra, img_dec = img.wcs_center

                il = [date,name,img_ra,img_dec,categories,comment]
                for l in image_lines:
                    if l[1] == name: image_lines.remove(l)
                image_lines.append(il)
                
                name_lengths.append(len(name))
                img_ra_lengths.append(len(f'{img_ra:.8f}'))
                img_dec_lengths.append(len(f'{img_dec:.8f}'))
                category_lengths.append(len(categories))
                comment_lengths.append(len(comment))

    if len(image_lines) != 0:
        # Dynamically adjust column widths
        dateln = 12
        nameln = np.max(name_lengths) + 2
        img_raln = max(np.max(img_ra_lengths), 2) + 2 
        img_decln = max(np.max(img_ra_lengths), 3) + 2
        categoryln = max(np.max(category_lengths), 10) + 2
        commentln = max(np.max(comment_lengths), 7) + 2 
        
        il_fmt = [ f'^{dateln}',f'^{nameln}', f'^{img_raln}.8f', f'^{img_decln}.8f', f'^{categoryln}', f'^{commentln}' ]
        il_fmt_nofloat = [ f'^{dateln}',f'^{nameln}', f'^{img_raln}', f'^{img_decln}', f'^{categoryln}', f'^{commentln}' ]
        
        header = ['date','image','RA', 'DEC','categories','comment']
        header = ''.join(f'{h:{il_fmt_nofloat[i]}}|' for i, h in enumerate(header)) + '\n'
        
        with open(fav_out_path,'a') as fav_out:
            fav_out.write(header)
            for l in image_lines:
                outline = ''.join(f'{_l:{il_fmt[i]}}|' for i, _l in enumerate(l)) + '\n'           
                fav_out.write(outline)

def save_imagesfile(date,images:List['image.Image']) -> None:
    """
    Saves image data.

    Parameters
    ----------
    date: str
        A string containing the current date in ISO 8601 extended format.

    images: list[`imgmarker.image.Image`]
        A list of Image objects for each image from the specified image directory.

    Returns
    ----------
    None
    """

    image_rows:list[dict] = []
   
    images_dst = os.path.join(config.SAVE_DIR,f'{config.USER}_images.csv')

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
        
    if len(image_rows) != 0:

        with open(images_dst, 'w') as f:

            writer = csv.DictWriter(f, fieldnames=image_rows[0].keys())
            writer.writeheader()
            for row in image_rows:
                writer.writerow(row)

def save_markfile(date,images:List[image.Image],imageless_marks:List[Mark]) -> None:
    """
    Saves image data.

    Parameters
    ----------
    date: str
        A string containing the current date in ISO 8601 extended format.

    images: list[`imgmarker.image.Image`]
        A list of Image objects for each image from the specified image directory.

    Returns
    ----------
    None
    """

    # Will organize output rows into dictionary of the path to save to
    out = {}
    for path in markpaths():
        out[path] = []

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

                if mark != None:
                    path = mark.dst
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

                    try: x, y = mark.center.x(), mark.center.y()
                    except: x, y = nan, nan
                    
                    try: ra, dec = mark.wcs_center
                    except: ra, dec = nan, nan

                # Row entries if the seen image has no marks (user looked at image without placing)
                else:
                    path = os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')
                    group_name = 'None'
                    label = 'None'
                    ra, dec = nan, nan
                    x, y = nan, nan

                row = {'date': str(date),
                        'image': str(name),
                        'group': str(group_name),
                        'label': str(label),
                        'x': str(x),
                        'y': str(y),
                        'RA': str(ra),
                        'DEC': str(dec)}
                
                out[path].append(row)

    for mark in imageless_marks:
        row = {}
        if mark != None:
            path = mark.dst
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

        else:
            path = os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')
            group_name = 'None'
            label = 'None'
            ra, dec = nan, nan
            x, y = nan, nan

        row = {'date': str(date),
                    'image': str(name),
                    'group': str(group_name),
                    'label': str(label),
                    'x': str(x),
                    'y': str(y),
                    'RA': str(ra),
                    'DEC': str(dec)}
            
        out[path].append(row)
    
    # Print out lines if there are lines to print
    if len(out) != 0:
        for path in out:
            rows = out[path]
            if len(rows) != 0:
                with open(path, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                    writer.writeheader()
                    for row in rows:
                        writer.writerow(row)

def loadfav() -> List[str]:
    """
    Loads f'{USER}_favorites.csv' from the save directory.

    Returns
    ----------
    list: str
        A list of strings containing the names of the files (images) that were saved.
    """

    fav_out_path = os.path.join(config.SAVE_DIR, f'{config.USER}_favorites.csv')
    
    if os.path.exists(fav_out_path):
        fav_list = [ l.split('|')[1].strip() for l in open(fav_out_path) ][1:]
    else: fav_list = []

    return list(set(fav_list))

def load_markfile(images:List[image.Image],**kwargs) -> Tuple[List[image.Image],List[Mark]]:
    """
    Takes data from marks.csv and images.csv and from them returns a list of `imgmarker.image.Image`
    objects.

    Returns
    ----------
    images: list[`imgmarker.image.Image`]
    """
    if 'mark_dst' in kwargs:
        mark_dst = kwargs['mark_dst']
    else:
        mark_dst = os.path.join(config.SAVE_DIR,f'{config.USER}_marks.csv')

    imageless = []
    
    # Get list of marks for each image
    if os.path.exists(mark_dst):
        with open(mark_dst,'r') as f:
            delimiter = '|' if '|' in f.readline() else ','
            f.seek(0)
            reader = csv.DictReader(f,delimiter=delimiter)

            for row in reader:
                keys = row.copy().keys()
                for key in keys: row[key.strip().lower()] = row.pop(key).strip()

                # Default values
                date = dt.datetime.now(dt.timezone.utc).date().isoformat()
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
                            mark.dst = mark_dst
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
                    mark.dst = mark_dst
                    imageless.append(mark)

    return images, imageless

def load_imagesfile() -> Tuple[List[image.Image],List[Mark]]:
    """
    Takes data from marks.csv and images.csv and from them returns a list of `imgmarker.image.Image`
    objects.

    Returns
    ----------
    images: list[`imgmarker.image.Image`]
    """

    images_dst = os.path.join(config.SAVE_DIR,f'{config.USER}_images.csv')
    images:List[image.Image] = []
    
    # Get list of images from images.csv
    if os.path.exists(images_dst):
        with open(images_dst,'r') as f:
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