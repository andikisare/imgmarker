"""Image Marker's I/O module containing functions for loading and saving data."""

import os
import numpy as np
from .gui import Mark
from . import image
from . import config
import glob as _glob
from math import nan, isnan
from typing import Tuple, List

def savefav(date:str,images:List['image.Image'],fav_list:List[str]) -> None:
    """
    Creates a file, \'favorites.txt\', in the save directory containing all images that were favorited.
    This file is in the same format as \'images.txt\' so that a user can open their favorites file to show
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

    fav_out_path = os.path.join(config.SAVE_DIR, f'{config.USER}_favorites.txt')

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

def save(date,images:List['image.Image']) -> None:
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

    mark_lines = []
    image_lines = []

    name_lengths = []
    group_lengths = []
    x_lengths = []
    y_lengths = []
    ra_lengths = []
    dec_lengths = []
    img_ra_lengths = []
    img_dec_lengths = []
    category_lengths = []
    comment_lengths = []
    label_lengths = []

    mark_out_path = os.path.join(config.SAVE_DIR,f'{config.USER}_marks.txt')
    images_out_path = os.path.join(config.SAVE_DIR,f'{config.USER}_images.txt')

    # Create the file
    if os.path.exists(mark_out_path): os.remove(mark_out_path)
    if os.path.exists(images_out_path): os.remove(images_out_path)

    if images:
        for img in images:
            if img.seen:
                if img.duplicate == True:
                    marks = img.dupe_marks
                else:
                    marks = img.marks

                name = img.name
                comment = img.comment

                category_list = img.categories
                category_list.sort()
                if (len(category_list) != 0):
                    categories = ','.join([config.CATEGORY_NAMES[i] for i in category_list])
                else: categories = 'None'

                if not marks: mark_list = [None]
                else: mark_list = marks.copy()
                
                for mark in mark_list:
                    if mark != None:
                        group_name = config.GROUP_NAMES[mark.g]
                        if mark.text == group_name: label = 'None'
                        else: label = mark.text
                        if (img.duplicate == True) and (mark in img.dupe_marks):
                            if (mark.text == group_name):
                                label = "DUPLICATE"
                            else:
                                label = f"{mark.text}, DUPLICATE"
                        ra, dec = mark.wcs_center
                        img_ra, img_dec = img.wcs_center
                        x, y = mark.center.x(), mark.center.y()
                    else:
                        group_name = 'None'
                        label = 'None'
                        ra, dec = nan, nan
                        img_ra, img_dec = img.wcs_center
                        x, y = nan, nan
                        
                    ml = [date,name,group_name,label,x,y,ra,dec]
                    mark_lines.append(ml)

                    il = [date,name,img_ra,img_dec,categories,comment]
                    for l in image_lines:
                        if l[1] == name: image_lines.remove(l)
                    image_lines.append(il)
                    
                    name_lengths.append(len(name))
                    group_lengths.append(len(group_name))
                    x_lengths.append(len(str(x)))
                    y_lengths.append(len(str(y)))
                    ra_lengths.append(len(f'{ra:.8f}'))
                    dec_lengths.append(len(f'{dec:.8f}'))
                    img_ra_lengths.append(len(f'{img_ra:.8f}'))
                    img_dec_lengths.append(len(f'{img_dec:.8f}'))
                    category_lengths.append(len(categories))
                    comment_lengths.append(len(comment))
                    label_lengths.append(len(label))

    # Print out lines if there are lines to print
    if len(mark_lines) != 0:
        # Dynamically adjust column widths
        nameln = np.max(name_lengths) + 2
        groupln = max(np.max(group_lengths), 5) + 2
        labelln = max(np.max(label_lengths), 5) + 2
        xln = max(np.max(x_lengths), 1) + 2
        yln = max(np.max(y_lengths), 1) + 2
        raln = max(np.max(ra_lengths), 2) + 2
        decln = max(np.max(dec_lengths), 3) + 2
        dateln = 12

        ml_fmt = [ f'^{dateln}',f'^{nameln}',f'^{groupln}',f'^{labelln}',
                  f'^{xln}', f'^{yln}', f'^{raln}.8f', f'^{decln}.8f' ]
        
        ml_fmt_nofloat = [ f'^{dateln}',f'^{nameln}',f'^{groupln}',f'^{labelln}',
                          f'^{xln}', f'^{yln}', f'^{raln}', f'^{decln}' ]
        
        header = ['date','image','group','label','x','y','RA','DEC']
        header = ''.join(f'{h:{ml_fmt_nofloat[i]}}|' for i, h in enumerate(header)) + '\n'
        
        with open(mark_out_path,"a") as mark_out:
            mark_out.write(header)
            for l in mark_lines:
                try: outline = ''.join(f'{_l:{ml_fmt[i]}}|' for i, _l in enumerate(l)) + '\n'           
                except: outline = ''.join(f'{_l:{ml_fmt_nofloat[i]}}|' for i, _l in enumerate(l)) + '\n'
                mark_out.write(outline)

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
        
        with open(images_out_path,"a") as images_out:
            images_out.write(header)
            for l in image_lines:
                outline = ''.join(f'{_l:{il_fmt[i]}}|' for i, _l in enumerate(l)) + '\n'           
                images_out.write(outline)

def loadfav() -> List[str]:
    """
    Loads f'{USER}_favorites.txt' from the save directory.

    Returns
    ----------
    list: str
        A list of strings containing the names of the files (images) that were saved.
    """

    fav_out_path = os.path.join(config.SAVE_DIR, f'{config.USER}_favorites.txt')
    
    if os.path.exists(fav_out_path):
        fav_list = [ l.split('|')[1].strip() for l in open(fav_out_path) ][1:]
    else: fav_list = []

    return list(set(fav_list))

def load() -> List[image.Image]:
    """
    Takes data from marks.txt and images.txt and from them returns a list of `imgmarker.image.Image`
    objects.

    Returns
    ----------
    images: list[`imgmarker.image.Image`]
    """

    mark_out_path = os.path.join(config.SAVE_DIR,f'{config.USER}_marks.txt')
    images_out_path = os.path.join(config.SAVE_DIR,f'{config.USER}_images.txt')
    images:List[image.Image] = []
    
    # Get list of images from images.txt
    if os.path.exists(images_out_path):
        line0 = True
        for l in open(images_out_path):
            if line0: line0 = False
            else:
                date,name,ra,dec,categories,comment = [i.strip() for i in l.replace('|\n','').split('|')]
                categories = categories.split(',')
                categories = [config.CATEGORY_NAMES.index(cat) for cat in categories if cat != 'None']
                categories.sort()

                img = image.Image(os.path.join(config.IMAGE_DIR,name))
                img.comment = comment
                img.categories = categories
                img.seen = True
                images.append(img)
    
    # Get list of marks for each image
    for img in images:
        line0 = True
        for l in open(mark_out_path):
            if line0: line0 = False
            else:
                date,name,group,label,x,y,ra,dec = [i.strip() for i in l.replace('|\n','').split('|')]

                if (name == img.name) and (not isnan(float(x))) and (not isnan(float(y))):
                    group = config.GROUP_NAMES.index(group)
                    mark_args = (float(x),float(y))
                    mark_kwargs = {'image': img, 'group': group}
                    if label != 'None': mark_kwargs['text'] = label
                    mark = Mark(*mark_args, **mark_kwargs)
                    img.marks.append(mark)
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