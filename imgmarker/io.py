import os
import numpy as np
import imgmarker.window
import imgmarker.mark
import imgmarker.image
from imgmarker import __dirname__, CONFIG
from PyQt6.QtCore import Qt
from PIL.TiffTags import TAGS
from astropy.wcs import WCS
from astropy.io import fits
import io
import glob as glob_
import shutil
from math import nan, isnan
import warnings

SAVE_ALPHANUM_ERR = ValueError('Name of save folder must contain only letters or numbers.')

def read_config() -> tuple[str,str,list[str],list[str],list[int]]:
    """
    Reads in each line from imgmarker.cfg. If there is no configuration file,
    a default configuration file will be created using the required text
    format.

    Returns
    ----------
    out_dir: str
        Output directory for all save files.

    image_dir: str
        Directory containing desired image files.

    group_names: list[str]
        A list of containing labels for each mark button.

    category_names: list[str]
        A list containing labels for each image category.

    group_max: list[int]
        A list containing the maximum allowed number of marks for each group.
    """

    # If the config doesn't exist, create one
    if not os.path.exists(CONFIG):
        config_file = open(CONFIG,'w')
        
        out_dir = os.path.join(os.getcwd(),'')
        image_dir = os.path.join(os.getcwd(),'')
        group_names = ['None','1','2','3','4','5','6','7','8','9']
        category_names = ['None','1','2','3','4','5']
        group_max = ['None','None','None','None','None','None','None','None','None']

        config_file.write(f'out_dir = {out_dir}\n')
        config_file.write(f'image_dir = {image_dir}\n')
        config_file.write('groups = 1,2,3,4,5,6,7,8,9\n')
        config_file.write('categories = 1,2,3,4,5\n')
        config_file.write('group_max = None,None,None,None,None,None,None,None,None\n')
        config_file.write('randomize_order = True')

    else:
        for l in open(CONFIG):
            var, val = [i.strip() for i in l.replace('\n','').split('=')]

            if var == 'out_dir':
                if val == './':
                    out_dir = os.getcwd()
                    print('WARNING: Setting output/save directory to current directory. This can be configured in \'imgmarker.cfg\'.')
                else: out_dir = val
                if not os.path.exists(out_dir):
                    print("WARNING: out_dir does not exist. Creating out_dir directory.")
                    os.mkdir(out_dir)

            if var == 'image_dir':
                if val == './': image_dir = os.getcwd()
                else: image_dir = val
                image_dir =  os.path.join(image_dir,'')

            if var == 'groups':
                group_names = val.split(',')
                group_names.insert(0, 'None')

            if var == 'categories':
                category_names = val.split(',')
                category_names.insert(0, 'None')
            
            if var == 'group_max':
                group_max = val.split(',')

            if var == 'randomize_order':
                randomize_order = val
        
    return out_dir, image_dir, group_names, category_names, group_max, randomize_order

OUT_DIR, IMAGE_DIR, GROUP_NAMES, CATEGORY_NAMES, GROUP_MAX, RANDOMIZE_ORDER = read_config()
    
def check_marks(event) -> list[bool]:
    """
    Checks and resets each group's activation key on the keyboard.

    Parameters
    ----------
    event: PyQt6 event

    Returns
    ----------
    A list of bools corresponding to if the respective button was pressed or not. 
    """
    button1 = button2 = button3 = button4 = button5 = button6 = button7 = button8 = button9 = False

    try: button1 = event.button() == Qt.MouseButton.LeftButton
    except: button1 = event.key() == Qt.Key.Key_1

    try:
        button2 = event.key() == Qt.Key.Key_2
        button3 = event.key() == Qt.Key.Key_3
        button4 = event.key() == Qt.Key.Key_4
        button5 = event.key() == Qt.Key.Key_5
        button6 = event.key() == Qt.Key.Key_6
        button7 = event.key() == Qt.Key.Key_7
        button8 = event.key() == Qt.Key.Key_8
        button9 = event.key() == Qt.Key.Key_9
    except: pass

    return [button1, button2, button3, button4, button5, button6, button7, button8, button9]
    
def parse_wcs(img:imgmarker.image.Image) -> WCS:
    """
    Reads WCS information from TIFF/TIF metadata and FITS/FIT headers if available.

    Parameters
    ----------
    img: `imgmarker.image.Image` object

    Returns
    ----------
    wcs: `astropy.wcs.WCS` or None
        Astropy WCS object. Returns None if there is no WCS present.
    """
    try:
        if (img.format == 'FITS'):
            hdulist = fits.open(img.filename)
            wcs = WCS(hdulist[0].header)
            return wcs
        else:
            meta_dict = {TAGS[key] : img.tag[key] for key in img.tag_v2}
            
            long_header_str = meta_dict['ImageDescription'][0]

            line_length = 80

            # Splitting the string into lines of 80 characters
            lines = [long_header_str[i:i+line_length] for i in range(0, len(long_header_str), line_length)]
            
            # Join the lines with newline characters to form a properly formatted header string
            corrected_header_str = "\n".join(lines)

            # Use an IO stream to mimic a file
            header_stream = io.StringIO(corrected_header_str)

            # Read the header using astropy.io.fits
            header = fits.Header.fromtextfile(header_stream)

            # Create a WCS object from the header
            wcs = WCS(header)
        return wcs
    except: return None

def check_save(savename:str) -> bool:
    """Checks if savename is empty."""
    return (savename != 'None') and (savename != '')

def savefav(savename:str,date:str,images:list[imgmarker.image.Image],fav_list:list[str]) -> None:
    """
    Creates a file, \'favorites.txt\', in the save directory containing all images that were favorited.
    This file is in the same format as \'images.txt\' so that a user can open their favorites file to show
    only favorited images with a little bit of file name manipulation. More details on how to do this can
    be found in \'README.md\'.

    Parameters
    ----------
    savename: str
        A string containing the savename/username.

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

    save_dir = os.path.join(OUT_DIR, savename)
    fav_out_path = os.path.join(save_dir, 'favorites.txt')

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Create the file
    if os.path.exists(fav_out_path):
        os.remove(fav_out_path)
    
    fav_out = open(fav_out_path,'a')

    fav_images = [img for img in images if img.name in fav_list]

    if check_save(savename) and (len(fav_list) != 0):
        for img in fav_images:
            if img.seen:
                name = img.name
                comment = img.comment

                category_list = img.categories
                category_list.sort()
                if (len(category_list) != 0):
                    categories = ','.join([CATEGORY_NAMES[i] for i in category_list])
                else: categories = 'None'

                img_ra, img_dec = img.wcs_center()

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
        
        fav_out.write(header)

        for l in image_lines:
            outline = ''.join(f'{_l:{il_fmt[i]}}|' for i, _l in enumerate(l)) + '\n'           
            fav_out.write(outline)


def save(savename:str,date,images:list[imgmarker.image.Image]) -> None:
    """
    Saves image data.

    Parameters
    ----------
    savename: str
        A string containing the savename/username.

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

    save_dir = os.path.join(OUT_DIR, savename)
    mark_out_path = os.path.join(save_dir,'marks.txt')
    images_out_path = os.path.join(save_dir,'images.txt')

    # Create the file
    if os.path.exists(save_dir): 
        shutil.rmtree(save_dir)
    os.makedirs(save_dir)

    mark_out = open(mark_out_path,"a")
    images_out = open(images_out_path,"a")

    if check_save(savename) and images:
        for img in images:
            if img.seen:
                name = img.name
                comment = img.comment

                category_list = img.categories
                category_list.sort()
                if (len(category_list) != 0):
                    categories = ','.join([CATEGORY_NAMES[i] for i in category_list])
                else: categories = 'None'

                if not img.marks: mark_list = [None]
                else: mark_list = img.marks.copy()
                
                for mark in mark_list:
                    if mark != None:
                        group_name = GROUP_NAMES[mark.g]
                        ra, dec = mark.wcs_center
                        img_ra, img_dec = img.wcs_center()
                        x, y = mark.center.x(), mark.center.y()
                    else:
                        group_name = 'None'
                        ra, dec = nan, nan
                        img_ra, img_dec = img.wcs_center()
                        x, y = nan, nan
                        
                    ml = [date,name,group_name,x,y,ra,dec]
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

    # Print out lines if there are lines to print
    if len(mark_lines) != 0:
        # Dynamically adjust column widths
        nameln = np.max(name_lengths) + 2
        groupln = max(np.max(group_lengths), 5) + 2
        xln = max(np.max(x_lengths), 1) + 2
        yln = max(np.max(y_lengths), 1) + 2
        raln = max(np.max(ra_lengths), 2) + 2
        decln = max(np.max(dec_lengths), 3) + 2
        dateln = 12

        ml_fmt = [ f'^{dateln}',f'^{nameln}',f'^{groupln}',
                  f'^{xln}', f'^{yln}', f'^{raln}.8f', f'^{decln}.8f' ]
        
        ml_fmt_nofloat = [ f'^{dateln}',f'^{nameln}',f'^{groupln}',
                          f'^{xln}', f'^{yln}', f'^{raln}', f'^{decln}' ]
        
        header = ['date','image','group','x','y','RA','DEC']
        header = ''.join(f'{h:{ml_fmt_nofloat[i]}}|' for i, h in enumerate(header)) + '\n'
        
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
        
        images_out.write(header)

        for l in image_lines:
            outline = ''.join(f'{_l:{il_fmt[i]}}|' for i, _l in enumerate(l)) + '\n'           
            images_out.write(outline)

def loadfav(savename:str) -> list[str]:
    """
    Loads 'favorites.txt' from the save directory.

    Parameters
    ----------
    savename: str
        A string containing the savename/username.

    Returns
    ----------
    list: str
        A list of strings containing the names of the files (images) that were saved.
    """

    save_dir = os.path.join(OUT_DIR, savename)
    fav_out_path = os.path.join(save_dir, 'favorites.txt')
    
    if os.path.exists(fav_out_path):
        fav_list = [ l.split('|')[1].strip() for l in open(fav_out_path) ][1:]
    else: fav_list = []

    return list(set(fav_list))

def load(savename:str) -> list[imgmarker.image.Image]:
    """
    Takes data from marks.txt and images.txt and from them returns a list of `imgmarker.image.Image`
    objects.

    Parameters
    ----------
    savename: str
        A string containing the savename/username.

    Returns
    ----------
    images: list[`imgmarker.image.Image`]
    """

    save_dir = os.path.join(OUT_DIR, savename)
    mark_out_path = os.path.join(save_dir,'marks.txt')
    images_out_path = os.path.join(save_dir,'images.txt')
    images:list[imgmarker.image.Image] = []
    
    # Get list of images from images.txt
    if os.path.exists(images_out_path):
        skip = True
        for l in open(images_out_path):
            if skip: skip = False
            else:
                date,name,ra,dec,categories,comment = [i.strip() for i in l.replace('|\n','').split('|')]
                categories = categories.split(',')
                categories = [CATEGORY_NAMES.index(cat) for cat in categories if cat != 'None']
                categories.sort()

                img = imgmarker.image.open(os.path.join(IMAGE_DIR,name))
                img.comment = comment
                img.categories = categories
                img.seen = True
                images.append(img)
    
    # Get list of marks for each image
    for img in images:
        skip = True
        for l in open(mark_out_path):
            if skip: skip = False
            else:
                date,name,group,x,y,ra,dec = [i.strip() for i in l.replace('|\n','').split('|')]

                if (name == img.name) and (not isnan(float(x))) and (not isnan(float(y))):
                    group = GROUP_NAMES.index(group)
                    mark_args = (float(x),float(y))
                    mark_kwargs = {'image': img, 'group': group}
                    mark = imgmarker.mark.Mark(*mark_args, **mark_kwargs)
                    img.marks.append(mark)
    return images

def load_ext_marks(f:str) -> dict:
    """
    Loads in an external marks file containing labels and coordinates in either galactic or
    cartesian coordinates.

    Parameters
    ----------
    f: str
        A string containing the full path of the external marks file.

    Returns
    ----------
    labels: list[str]
        A list of the labels for each external mark.

    alphas: list[float]
        A list of floats containing either the RA or x coordinates of external marks.
    
    betas: list[float]
        A list of floats containing either the Dec or y coordinates of external marks.
    
    coord_sys: str
        A string containing either 'galactic' or 'cartesian' for designating the input coordinate
        system.
    """

    labels = []
    alphas = []
    betas = []
    coord_sys = None
    skip = True

    for l in open(f):
        var = l.split(',')
        if skip:
            skip = False
            if (var[1].strip().lower() == 'ra'):
                coord_sys = 'galactic'
            elif (var[1].strip().lower() == 'x'):
                coord_type = 'cartesian'
            else:
                warnings.warn('WARNING: Invalid external marks coordinate system. Valid coordinate systems: Galactic (RA, Dec), '
                                 'Cartesian (x, y)')
                return None, None, None, None
        else:
            labels.append(var[0])
            alphas.append(float(var[1].strip().replace('\n', '')))
            betas.append(float(var[2].strip().replace('\n', '')))
            
    return labels, alphas, betas, coord_sys

def glob(edited_images:list[imgmarker.image.Image]=[]) -> tuple[list[imgmarker.image.Image],int]:
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

    if RANDOMIZE_ORDER:
        # Find all images in image directory
        all_images = glob_.glob(os.path.join(IMAGE_DIR, '*.*'))
        all_images = [img for img in all_images if img.split('.')[-1] in imgmarker.image.SUPPORTED_EXTS]

        # Get list of paths to images if they are in the dictionary (have been edited)
        edited_image_paths = [os.path.join(IMAGE_DIR,img.name) for img in edited_images]
        unedited_image_paths = [fp for fp in all_images if fp not in edited_image_paths]

        # Shuffle the remaining unedited images
        rng = np.random.default_rng()
        rng.shuffle(unedited_image_paths)
    else:
        # Find all images in image directory
        all_images = sorted(glob_.glob(os.path.join(IMAGE_DIR, '*.*')))
        all_images = [img for img in all_images if img.split('.')[-1] in imgmarker.image.SUPPORTED_EXTS]

        # Get list of paths to images if they are in the dictionary (have been edited)
        edited_image_paths = [os.path.join(IMAGE_DIR,img.name) for img in edited_images]
        unedited_image_paths = [fp for fp in all_images if fp not in edited_image_paths]

    # Put edited images at the beginning, unedited images at front
    images = edited_images + [imgmarker.image.open(fp) for fp in unedited_image_paths]
    idx = min(len(edited_images),len(all_images)-1)

    return images, idx

def inputs() -> str:
    """Returns the savename from `StartupWindow`."""
    savename = imgmarker.window.StartupWindow().getUser()
    return savename

def update_config(out_dir:str = OUT_DIR,
                  image_dir:str = IMAGE_DIR, 
                  group_names:list[str] = GROUP_NAMES, 
                  category_names:list[str] = CATEGORY_NAMES, 
                  group_max:list[int] = GROUP_MAX,
                  randomize_order:str = RANDOMIZE_ORDER
    ) -> None:
    """Updates any of the global config variables with the corresponding parameter."""
    
    global OUT_DIR; OUT_DIR = out_dir
    global IMAGE_DIR; IMAGE_DIR = image_dir
    global GROUP_NAMES; GROUP_NAMES = group_names
    global CATEGORY_NAMES; CATEGORY_NAMES = category_names
    global GROUP_MAX; GROUP_MAX = group_max
    global RANDOMIZE_ORDER; RANDOMIZE_ORDER = randomize_order
    
    config_file = open(CONFIG,'w')
    config_file.write(f'out_dir = {out_dir}\n')
    config_file.write(f'image_dir = {image_dir}\n')
    config_file.write(f'groups = {','.join(group_names[1:])}\n')
    config_file.write(f'categories = {','.join(category_names[1:])}\n')
    config_file.write(f'group_max = {','.join(group_max)}\n')
    config_file.write(f'randomize_order = {randomize_order}')