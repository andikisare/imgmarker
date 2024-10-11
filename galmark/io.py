import os
import numpy as np
import galmark.window
from galmark.mark import Mark
import galmark.image
from galmark import __dirname__
from PyQt6.QtCore import Qt
from PIL import Image
from PIL.TiffTags import TAGS
from astropy.wcs import WCS
from astropy.io import fits
import io
import glob as glob_
import shutil
from math import nan, isnan

SAVE_ALPHANUM_ERR = ValueError('Name of save folder must contain only letters or numbers.')

def readConfig(config:str='galmark.cfg') -> tuple[str,str,list[str],list[str],list[int]]:
    '''
    Read each line from the config and parse it
    '''

    # If the config doesn't exist, create one
    if not os.path.exists(config):
        config_file = open(config,'w')
        
        out_dir = os.path.join(os.getcwd(),'')
        image_dir = os.path.join(os.getcwd(),'')
        group_names = ['None','1','2','3','4','5','6','7','8','9']
        category_names = ['None','1','2','3','4','5']
        group_max = ['None','None','None','None','None','None','None','None','None']

        config_file.write(f'out_dir = {out_dir}\n')
        config_file.write(f'image_dir = {image_dir}\n')
        config_file.write('groups = 1,2,3,4,5,6,7,8,9\n')
        config_file.write('categories = 1,2,3,4,5\n')
        config_file.write('group_max = None,None,None,None,None,None,None,None,None')

    else:
        for l in open(config):
            var, val = [i.strip() for i in l.replace('\n','').split('=')]

            if var == 'out_dir':
                if val == './':
                    out_dir = os.getcwd()
                    print('WARNING: Setting output/save directory to current directory. This can be configured in \'galmark.cfg\'.')
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
        
    return out_dir, image_dir, group_names, category_names, group_max

OUT_DIR, IMAGE_DIR, GROUP_NAMES, CATEGORY_NAMES, GROUP_MAX = readConfig()
    
def markCheck(event):
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
    
def parseWCS(img:str|Image.Image) -> WCS:
    try:
        #tif_image_data = np.array(Image.open(image_tif))
        if type(img) == str: img = Image.open(img)
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

def checkUsername(username:str) -> bool:
    return (username != 'None') and (username != '')

def savefav(username:str,save_list:list) -> None:

    save_dir = os.path.join(OUT_DIR, username)
    fav_out_path = os.path.join(save_dir, 'favorites.txt')

    # Create the file
    if os.path.exists(fav_out_path):
        os.remove(fav_out_path)
    out = open(fav_out_path,'a')

    for name in save_list:
        out.write(f'{name}\n')

def save(username:str,date,images:list[galmark.image.GImage]) -> None:
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

    save_dir = os.path.join(OUT_DIR, username)
    mark_out_path = os.path.join(save_dir,'marks.txt')
    images_out_path = os.path.join(save_dir,'images.txt')

    # Create the file
    if os.path.exists(save_dir): 
        shutil.rmtree(save_dir)
    os.makedirs(save_dir)

    mark_out = open(mark_out_path,"a")
    images_out = open(images_out_path,"a")

    if checkUsername(username) and images:

        for img in images:
            name = img.name
            comment = img.comment

            category_list = img.categories
            category_list.sort()
            if (len(category_list) != 0):
                categories = ','.join([CATEGORY_NAMES[i] for i in category_list])
            else: categories = 'None'

            if img.marks:
                for mark in img.marks:
                    group_name = GROUP_NAMES[mark.g]
                    ra, dec = mark.wcs_center()
                    img_ra, img_dec = img.wcs_center()
                    x, y = mark.img_center().x(), mark.img_center().y()
                    ml = [date,name,group_name,x,y,ra,dec]
                    il = [date,name,img_ra,img_dec,categories,comment]

                    mark_lines.append(ml)

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
            
            # Otherwise, if there is a category or a comment, replace ra/dec with NaNs
            elif img.seen: # (len(categories_to_print) != 0) or (comment != 'None'):
                group_name = 'None'
                x, y = nan, nan
                ra, dec = nan, nan
                img_ra, img_dec = img.wcs_center()

                ml = [date,name,group_name,x,y,ra,dec]
                il = [date,name,img_ra,img_dec,categories,comment]

                mark_lines.append(ml)
                
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

def loadfav(username:str) -> list[str]:
    out_path = os.path.join(OUT_DIR, username)
    favfile = os.path.join(out_path, 'favorites.txt')
    
    if os.path.exists(favfile):
        fav_list = [ l.replace('\n','') for l in open(favfile) ]
    else: fav_list = []
    
    return list(set(fav_list))

def load(username:str) -> list[galmark.image.GImage]:
    save_dir = os.path.join(OUT_DIR, username)
    mark_out_path = os.path.join(save_dir,'marks.txt')
    images_out_path = os.path.join(save_dir,'images.txt')
    images:list[galmark.image.GImage] = []
    
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

                img = galmark.image.open(os.path.join(IMAGE_DIR,name))
                img.comment = comment
                img.categories = categories
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
                    mark_args = (int(x),int(y))
                    mark_kwargs = {'image': img, 'group': group}
                    mark = Mark(*mark_args, **mark_kwargs)
                    img.marks.append(mark)

    return images

def glob(edited_images:list[galmark.image.GImage]=[]) -> tuple[list[galmark.image.GImage],int]:
     # Find all images in image directory
    all_images = glob_.glob(IMAGE_DIR + '*.*')
    all_images = [img for img in all_images if img.split('.')[-1] in galmark.image.SUPPORTED_EXTS]

    # Get list of paths to images if they are in the dictionary (have been edited)
    edited_image_paths = [os.path.join(IMAGE_DIR,img.name) for img in edited_images]
    unedited_image_paths = [fp for fp in all_images if fp not in edited_image_paths]

    # Shuffle the remaining unedited images
    rng = np.random.default_rng()
    rng.shuffle(unedited_image_paths)

    # Put edited images at the beginning, unedited images at front
    images = edited_images + [galmark.image.open(fp) for fp in unedited_image_paths]
    idx = min(len(edited_images),len(all_images)-1)

    return images, idx

def inputs() -> str:
    username = galmark.window.StartupWindow().getUser()
    return username

def configUpdate(out_dir=OUT_DIR, image_dir=IMAGE_DIR, group_names=GROUP_NAMES, category_names=CATEGORY_NAMES, group_max=GROUP_MAX, config:str='galmark.cfg'):
    global OUT_DIR; OUT_DIR = out_dir
    global IMAGE_DIR; IMAGE_DIR = image_dir
    global GROUP_NAMES; GROUP_NAMES = group_names
    global CATEGORY_NAMES; CATEGORY_NAMES = category_names
    global GROUP_MAX; GROUP_MAX = group_max
    
    config_file = open(config,'w')
    config_file.write(f'out_dir = {out_dir}\n')
    config_file.write(f'image_dir = {image_dir}\n')
    config_file.write(f'groups = {','.join(group_names[1:])}\n')
    config_file.write(f'categories = {','.join(category_names[1:])}\n')
    config_file.write(f'group_max = {','.join(group_max)}\n')