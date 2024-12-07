import os
import numpy as np
from . import mark as _mark
from . import image
from .pyqt import Qt, QFileDialog
from PIL.TiffTags import TAGS
from astropy.wcs import WCS
from astropy.io import fits
import io
import sys
import glob as _glob
from math import nan, isnan
from typing import Tuple, List
from functools import lru_cache
from getpass import getuser

HOME = os.path.expanduser('~')

class DefaultDialog(QFileDialog):
    def __init__(self):
        #make this work with file dialog names on MacOS
        #default to user's home directory if a path isn't given. 
        # Create a QFileDialog instance
        super().__init__()
        self.setOption(QFileDialog.Option.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.FileMode.Directory)
        self.setDirectory(HOME)
        self.closed = False

    def closeEvent(self, a0):
        self.closed = True
        return super().closeEvent(a0)
    
    def keyPressEvent(self, a0):
        if a0.key() == Qt.Key.Key_Escape: self.close()
        else: return super().keyPressEvent(a0)

    def selectedFiles(self):
        if self.closed: return None
        else: return super().selectedFiles()

def get_image_dir() -> str:
    dialog = DefaultDialog()
    dialog.setWindowTitle("Open Image directory")
    dialog.exec()

    image_dir = dialog.selectedFiles()[0]
    return image_dir 

@lru_cache(maxsize=1)
def getsave() -> str:
    dialog = DefaultDialog()
    dialog.setWindowTitle("Open save directory")
    dialog.exec()
    if dialog.closed: sys.exit()

    save_dir = dialog.selectedFiles()[0]
    return save_dir

USER = getuser()
SAVE_DIR = getsave()
CONFIG = os.path.join(SAVE_DIR,f'{USER}_config.txt')

def pathtoformat(path:str):
    ext = path.split('.')[-1].casefold()
    if ext == 'png': return 'PNG'
    if ext in {'jpeg', 'jpg'}: return 'JPEG'
    if ext in {'tiff', 'tif'}: return 'TIFF'
    if ext in {'fit', 'fits'}: return 'FITS'
    
def read_config() -> Tuple[str,str,List[str],List[str],List[int]]:
    """
    Reads in each line from imgmarker.cfg. If there is no configuration file,
    a default configuration file will be created using the required text
    format.

    Returns
    ----------
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
        with open(CONFIG,'w') as config:
            image_dir = None
            group_names = ['None','1','2','3','4','5','6','7','8','9']
            category_names = ['None','1','2','3','4','5']
            group_max = ['None','None','None','None','None','None','None','None','None']
            randomize_order = True

            config.write(f'image_dir = {image_dir}\n')
            config.write(f"groups = {','.join(group_names)}\n")
            config.write(f"categories = {','.join(category_names)}\n")
            config.write(f"group_max = {','.join(group_max)}\n")
            config.write(f'randomize_order = {randomize_order}')  

    else:
        for l in open(CONFIG):
            var, val = [i.strip() for i in l.replace('\n','').split('=')]

            if var == 'image_dir':
                if val == './': image_dir = os.getcwd()
                else: image_dir = val
                image_dir =  os.path.join(image_dir,'')

            if var == 'groups':
                group_names = []
                group_names_temp = val.split(',')
                for group_name in group_names_temp:
                    group_names.append(group_name.strip())
                group_names.insert(0, 'None')

            if var == 'categories':
                category_names = []
                category_names_temp = val.split(',')
                for category_name in category_names_temp:
                    category_names.append(category_name.strip())
                category_names.insert(0, 'None')
            
            if var == 'group_max':
                group_max = []
                group_max_temp = val.split(',')
                for group_max_val in group_max_temp:
                    group_max.append(group_max_val.strip())

            if var == 'randomize_order':
                randomize_order = val == 'True'

    return image_dir, group_names, category_names, group_max, randomize_order

IMAGE_DIR, GROUP_NAMES, CATEGORY_NAMES, GROUP_MAX, RANDOMIZE_ORDER = read_config()

def check_marks(event) -> List[bool]:
    """
    Checks and resets each group's activation key on the keyboard.

    Parameters
    ----------
    event: PyQt5 event

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
    
def parse_wcs(img:image.Image) -> WCS:
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
        if img.format == 'FITS':
            with fits.open(img.filename) as hdulist:
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

    fav_out_path = os.path.join(SAVE_DIR, f'{USER}_favorites.txt')

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
                    categories = ','.join([CATEGORY_NAMES[i] for i in category_list])
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

    mark_out_path = os.path.join(SAVE_DIR,f'{USER}_marks.txt')
    images_out_path = os.path.join(SAVE_DIR,f'{USER}_images.txt')

    # Create the file
    if os.path.exists(mark_out_path): os.remove(mark_out_path)
    if os.path.exists(images_out_path): os.remove(images_out_path)

    if images:
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
                        if mark.text == group_name: label = 'None'
                        else: label = mark.text
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

    fav_out_path = os.path.join(SAVE_DIR, f'{USER}_favorites.txt')
    
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

    mark_out_path = os.path.join(SAVE_DIR,f'{USER}_marks.txt')
    images_out_path = os.path.join(SAVE_DIR,f'{USER}_images.txt')
    images:List[image.Image] = []
    
    # Get list of images from images.txt
    if os.path.exists(images_out_path):
        line0 = True
        for l in open(images_out_path):
            if line0: line0 = False
            else:
                date,name,ra,dec,categories,comment = [i.strip() for i in l.replace('|\n','').split('|')]
                categories = categories.split(',')
                categories = [CATEGORY_NAMES.index(cat) for cat in categories if cat != 'None']
                categories.sort()

                img = image.open(os.path.join(IMAGE_DIR,name))
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
                    group = GROUP_NAMES.index(group)
                    mark_args = (float(x),float(y))
                    mark_kwargs = {'image': img, 'group': group}
                    if label != 'None': mark_kwargs['text'] = label
                    mark = _mark.Mark(*mark_args, **mark_kwargs)
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
    paths = sorted(_glob.glob(os.path.join(IMAGE_DIR, '*.*')))
    paths = [fp for fp in paths if pathtoformat(fp) in image.FORMATS]

    # Get list of paths to images if they are in the dictionary (have been edited)
    edited_paths = [os.path.join(IMAGE_DIR,img.name) for img in edited_images]
    unedited_paths = [fp for fp in paths if fp not in edited_paths]

    if RANDOMIZE_ORDER:
        # Shuffle the remaining unedited images
        rng = np.random.default_rng()
        rng.shuffle(unedited_paths)

    # Put edited images at the beginning, unedited images at front
    images = edited_images + [image.open(fp) for fp in unedited_paths]

    idx = min(len(edited_images),len(paths)-1)

    return images, idx



def update_config() -> None:
    """Updates any of the global config variables with the corresponding parameter."""
    
    with open(CONFIG,'w') as config:
        config.write(f'image_dir = {IMAGE_DIR}\n')
        config.write(f"groups = {','.join(GROUP_NAMES[1:])}\n")
        config.write(f"categories = {','.join(CATEGORY_NAMES[1:])}\n")
        config.write(f"group_max = {','.join(GROUP_MAX)}\n")
        config.write(f'randomize_order = {RANDOMIZE_ORDER}')
