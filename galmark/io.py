import os
import numpy as np
import galmark.window
from galmark.mark import Mark
import galmark.image
from galmark import __dirname__
from PyQt6.QtCore import Qt
from PIL import Image, ImageFile
from PIL.TiffTags import TAGS
from astropy.wcs import WCS
from astropy.io import fits
from collections import defaultdict
import io
import glob as glob_
import shutil

class DataDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(DataDict, self).__init__(DataDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))
    
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

def readConfig(config:str='galmark.cfg') -> tuple[str]:
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

out_dir, image_dir, group_names, category_names, group_max = readConfig()

def checkUsername(username:str) -> bool:
    return (username != "None") and (username != "")

def savefav(data:DataDict,username:str,date,save_list:list) -> None:
    lines = []
    name_lengths = []
    group_lengths = []
    x_lengths = []
    y_lengths = []
    ra_lengths = []
    dec_lengths = []
    category_lengths = []
    comment_lengths = []

    save_dir = os.path.join(out_dir, username)
    fav_out_path = os.path.join(save_dir, 'fav.txt')

    # Create the file
    if os.path.exists(fav_out_path):
        os.remove(fav_out_path)
    out = open(fav_out_path,"a")



    if checkUsername(username) and data:
        all_names = list(data.keys())
        
    if len(save_list) > 0:
        fav_names = [i for i in all_names if i in save_list]
        for name in fav_names:
            comment = data[name]['comment']
            category_list = data[name]['categories']
            category_list.sort()
            if (len(category_list) != 0):
                categories = ','.join([category_names[i] for i in category_list])
            else: categories = 'None'

            # Get list of groups containing data
            level2_keys = list(data[name].keys())
            groups = [ key for key in level2_keys if isinstance(key,int) 
                        and data[name][key]['marks'] ]

            # If there is data in groups, then add this data to lines
            if (len(groups) != 0):
                for group in groups:
                    group_name = group_names[group]
                    mark_list:list[Mark] = data[name][group]['marks']

                    for mark in mark_list:
                        ra, dec = mark.wcs_center()
                        x, y = mark.img_center().x(), mark.img_center().y()
                        l = [date,name,group_name,x,y,ra,dec,categories,comment]
       
                        lines.append(l)
                        name_lengths.append(len(name))
                        group_lengths.append(len(group_name))
                        x_lengths.append(len(str(x)))
                        y_lengths.append(len(str(y)))
                        ra_lengths.append(len(f'{ra:.8f}'))
                        dec_lengths.append(len(f'{dec:.8f}'))
                        category_lengths.append(len(categories))
                        comment_lengths.append(len(comment))
            
            # Otherwise, if there is a category or a comment, replace ra/dec with NaNs
            else: # (len(categories_to_print) != 0) or (comment != 'None'):
                group_name = 'None'
                x = 'NaN'
                y = 'NaN'
                ra = 'NaN'
                dec = 'NaN'

                l = [date,name,group_name,x,y,ra,dec,categories,comment]

                lines.append(l)
                name_lengths.append(len(name))
                group_lengths.append(len(group_name))
                x_lengths.append(len(x))
                y_lengths.append(len(y))
                ra_lengths.append(len(ra))
                dec_lengths.append(len(dec))
                category_lengths.append(len(categories))
                comment_lengths.append(len(comment))
            
            # Otherwise, (no comment, no category, and no data) delete entry from dictionary
            # else: pass

    # Print out lines if there are lines to print
    if len(lines) != 0:
        # Dynamically adjust column widths
        nameln = np.max(name_lengths) + 2
        groupln = max(np.max(group_lengths), 5) + 2
        xln = max(np.max(x_lengths), 1) + 2
        yln = max(np.max(y_lengths), 1) + 2
        raln = max(np.max(ra_lengths), 2) + 2
        decln = max(np.max(dec_lengths), 2) + 2
        categoryln = max(np.max(category_lengths), 16) + 2
        commentln = max(np.max(comment_lengths), 7) + 2
        dateln = 12

        l_fmt = [ f'^{dateln}',f'^{nameln}',f'^{groupln}',
                  f'^{xln}', f'^{yln}', f'^{raln}.8f', f'^{decln}.8f',
                  f'^{categoryln}', f'^{commentln}' ]
        l_fmt_nofloat = [ f'^{dateln}',f'^{nameln}',f'^{groupln}',
                          f'^{xln}', f'^{yln}', f'^{raln}', f'^{decln}',
                          f'^{categoryln}', f'^{commentln}' ]
        
        header = ['date','image','group','x','y','RA','DEC','image categories','comment']
        header = ''.join(f'{h:{l_fmt_nofloat[i]}}|' for i, h in enumerate(header)) + '\n'
        
        out.write(header)

        for l in lines:
            try: outline = ''.join(f'{_l:{l_fmt[i]}}|' for i, _l in enumerate(l)) + '\n'           
            except: outline = ''.join(f'{_l:{l_fmt_nofloat[i]}}|' for i, _l in enumerate(l)) + '\n'
            out.write(outline)

def save(data:DataDict,username:str,date) -> None:
    mark_lines = []
    image_lines = []

    name_lengths = []
    group_lengths = []
    x_lengths = []
    y_lengths = []
    ra_lengths = []
    dec_lengths = []
    category_lengths = []
    comment_lengths = []

    save_dir = os.path.join(out_dir, username)
    mark_out_path = os.path.join(save_dir,'marks.txt')
    images_out_path = os.path.join(save_dir,'images.txt')

    # Create the file
    if os.path.exists(save_dir): 
        shutil.rmtree(save_dir)
    os.makedirs(save_dir)

    mark_out = open(mark_out_path,"a")
    images_out = open(images_out_path,"a")

    if checkUsername(username) and data:
        names = list(data.keys())

        for name in names:
            comment = data[name]['comment']
            category_list = data[name]['categories']
            category_list.sort()
            if (len(category_list) != 0):
                categories = ','.join([category_names[i] for i in category_list])
            else: categories = 'None'

            # Get list of groups containing data
            level2_keys = list(data[name].keys())
            groups = [ key for key in level2_keys if isinstance(key,int) 
                        and data[name][key]['marks'] ]

            # If there is data in groups, then add this data to lines
            if (len(groups) != 0):
                for group in groups:
                    group_name = group_names[group]
                    mark_list:list[Mark] = data[name][group]['marks']

                    for mark in mark_list:
                        ra, dec = mark.wcs_center()
                        x, y = mark.img_center().x(), mark.img_center().y()
                        ml = [date,name,group_name,x,y,ra,dec]
                        il = [date,name,categories,comment]
       
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
                        category_lengths.append(len(categories))
                        comment_lengths.append(len(comment))
            
            # Otherwise, if there is a category or a comment, replace ra/dec with NaNs
            else: # (len(categories_to_print) != 0) or (comment != 'None'):
                group_name = 'None'
                x = 'NaN'
                y = 'NaN'
                ra = 'NaN'
                dec = 'NaN'

                ml = [date,name,group_name,x,y,ra,dec]
                il = [date,name,categories,comment]

                mark_lines.append(ml)
                
                for l in image_lines:
                    if l[1] == name: image_lines.remove(l)
                image_lines.append(il)

                name_lengths.append(len(name))
                group_lengths.append(len(group_name))
                x_lengths.append(len(x))
                y_lengths.append(len(y))
                ra_lengths.append(len(ra))
                dec_lengths.append(len(dec))
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
        decln = max(np.max(dec_lengths), 2) + 2
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
        categoryln = max(np.max(category_lengths), 16) + 2
        commentln = max(np.max(comment_lengths), 7) + 2 

        il_fmt = [ f'^{dateln}',f'^{nameln}',f'^{categoryln}', f'^{commentln}' ]
        
        header = ['date','image','image categories','comment']
        header = ''.join(f'{h:{il_fmt[i]}}|' for i, h in enumerate(header)) + '\n'
        
        images_out.write(header)

        for l in image_lines:
            outline = ''.join(f'{_l:{il_fmt[i]}}|' for i, _l in enumerate(l)) + '\n'           
            images_out.write(outline)

def loadfav(username:str,config:str='galmark.cfg') -> list[str]:
    out_path = os.path.join(out_dir, username)
    outfile = os.path.join(out_path, 'fav.txt')

    skip = True
    fav_list = []
    if os.path.exists(outfile):
        print('saved loaded')
        for l in open(outfile):
            if skip: skip = False
            else:
                date,name,group,x,y,ra,dec,categories,comment = [i.strip() for i in l.replace('|\n','').split('|')]
                fav_list.append(name)
    fav_list = list(set(fav_list))
    return fav_list

def load(username:str,config:str='galmark.cfg') -> DataDict:

    save_dir = os.path.join(out_dir, username)
    mark_out_path = os.path.join(save_dir,'marks.txt')
    images_out_path = os.path.join(save_dir,'images.txt')

    data = DataDict()
    skip = True
    
    if os.path.exists(mark_out_path):
        for l in open(mark_out_path):
            if skip: skip = False
            else:
                date,name,group,x,y,ra,dec = [i.strip() for i in l.replace('|\n','').split('|')]
                image_path = os.path.join(image_dir,name)
                image = Image.open(image_path)

                
                group_idx = group_names.index(group)
                
                if (x!='NaN') and (y!='NaN'):
                    mark_args = (int(x)+4*image.width,int(y)+4*image.height)
                    mark_kwargs = {'wcs': parseWCS(image), 'group': group_idx}
                    mark = Mark(*mark_args, **mark_kwargs)

                    if not data[name][group_idx]['marks']:
                        data[name][group_idx]['marks'] = []

                    data[name][group_idx]['marks'].append(mark)
    
    skip = True
    
    if os.path.exists(images_out_path):
        for l in open(images_out_path):
            if skip: skip = False
            else:
                date,name,categories,comment = [i.strip() for i in l.replace('|\n','').split('|')]
                category_list = categories.split(',')
                category_list = [category_names.index(cat) for cat in category_list if cat != 'None']
                category_list.sort()

                data[name]['comment'] = comment
                data[name]['categories'] = category_list
                
    return data

def glob(image_dir:str,ext:str,data_filt:DataDict={}) -> tuple[list[galmark.image.GImage],int]:
     # Find all images in image directory
    all_images = glob_.glob(image_dir + '*.' + ext)

    # Get list of paths to images if they are in the dictionary (have been edited)
    if (data_filt):
        edited_images = [os.path.join(image_dir,f) for f in data_filt.keys()]
        unedited_images = [i for i in all_images if i not in edited_images]
    else:
        edited_images = []
        unedited_images = all_images

    # Shuffle the remaining unedited images
    rng = np.random.default_rng()
    rng.shuffle(unedited_images)

    # Put edited images at the beginning, unedited images at front
    images = edited_images + unedited_images
    images = [galmark.image.open(im) for im in images]
    idx = min(len(edited_images),len(all_images)-1)

    return images, idx

def inputs(config:str='galmark.cfg') -> tuple[str,str,str,list[str],list[str],int]:
    username = galmark.window.StartupWindow().getUser()

    return username, out_dir, image_dir, group_names, category_names, group_max

def configUpdate(outDir=out_dir, imageDir=image_dir, groupNames=group_names, categoryNames=category_names, groupMax=group_max, config:str='galmark.cfg'):
    config_file = open(config,'w')

    config_file.write(f'out_dir = {outDir}\n')
    config_file.write(f'image_dir = {imageDir}\n')
    config_file.write(f'groups = {groupNames[1]},{groupNames[2]},{groupNames[3]},{groupNames[4]},'
                        f'{groupNames[5]},{groupNames[6]},{groupNames[7]},{groupNames[8]},'
                        f'{groupNames[9]}\n')
    config_file.write(f'categories = {categoryNames[1]},{categoryNames[2]},{categoryNames[3]},'
                        f'{categoryNames[4]},{categoryNames[5]}\n')
    config_file.write(f'group_max = {groupMax[0]},{groupMax[1]},{groupMax[2]},{groupMax[3]},'
                        f'{groupMax[4]},{groupMax[5]},{groupMax[6]},{groupMax[7]},'
                        f'{groupMax[8]}\n')