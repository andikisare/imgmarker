import os
import numpy as np
import galmark.window
from galmark.mark import Mark
from galmark import __dirname__
from PyQt6.QtCore import Qt
from PIL import Image
from PIL.TiffTags import TAGS
from astropy.wcs import WCS
from astropy.io import fits
from collections import defaultdict
import io
import glob as _glob

class DataDict(defaultdict):
    def __init__(self, *args, **kwargs):
        super(DataDict, self).__init__(DataDict, *args, **kwargs)

    def __repr__(self):
        return repr(dict(self))
    
def markBindingCheck(event):
    button1 = button2 = button3 = button4 = button5 = button6 = button7 = button8 = button9 = False

    try: button1 = event.button() == Qt.MouseButton.LeftButton
    except: button1 = event.key() == Qt.Key.Key_1

    try: button2 = event.button() == Qt.MouseButton.RightButton
    except: button2 = event.key() == Qt.Key.Key_2

    try:
        button3 = event.key() == Qt.Key.Key_3
        button4 = event.key() == Qt.Key.Key_4
        button5 = event.key() == Qt.Key.Key_5
        button6 = event.key() == Qt.Key.Key_6
        button7 = event.key() == Qt.Key.Key_7
        button8 = event.key() == Qt.Key.Key_8
        button9 = event.key() == Qt.Key.Key_9
    except: pass

    return [button1, button2, button3, button4, button5, button6, button7, button8, button9]
    
def parseWCS(image_tif):
    #tif_image_data = np.array(Image.open(image_tif))
    img = Image.open(image_tif)
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

def readConfig(config='galmark.cfg'):
    '''
    Read each line from the config and parse it
    '''

    # If the config doesn't exist, create one
    if not os.path.exists(config):
        config_file = open(config,'w')
        
        out_path = os.path.join(os.getcwd(),'')
        images_path = os.path.join(os.getcwd(),'')
        group_names = ['None','1','2','3','4','5','6','7','8','9']
        category_names = ['None','1','2','3','4','5']
        group_max = ['None','None','None','None','None','None','None','None','None']

        config_file.write(f'out_path = {out_path}\n')
        config_file.write(f'images_path = {images_path}\n')
        config_file.write('groups = 1,2,3,4,5,6,7,8,9\n')
        config_file.write('categories = 1,2,3,4,5\n')
        config_file.write('group_max = None,None,None,None,None,None,None,None,None')

    else:
        for l in open(config):
            var, val = [i.strip() for i in l.replace('\n','').split('=')]

            if var == 'out_path':
                if var == './': out_path = os.getcwd()
                else: out_path = val
                os.path.join(out_path,'')

            if var == 'images_path':
                if val == './': images_path = os.getcwd()
                else: images_path = val
                images_path =  os.path.join(images_path,'')

            if var == 'groups':
                group_names = val.split(',')
                group_names.insert(0, 'None')

            if var == 'categories':
                category_names = val.split(',')
                category_names.insert(0, 'None')
            
            if var == 'group_max':
                group_max = val.split(',')
        
    return out_path, images_path, group_names, category_names, group_max
                
def checkUsername(username):
    return (username != "None") and (username != "")

def save(data,username,date):
    lines = []
    name_lengths = []
    group_lengths = []
    x_lengths = []
    y_lengths = []
    ra_lengths = []
    dec_lengths = []
    category_lengths = []
    comment_lengths = []

    out_path, images_path, group_names, category_names, group_max = readConfig()
    outfile = os.path.join(out_path, username + '.txt')
    
    # Create the file
    if os.path.exists(outfile): 
        os.remove(outfile)
    out = open(outfile,"a")

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
                    mark_list = data[name][group]['marks']

                    for mark in mark_list:
                        ra, dec = mark.centerWCS()
                        x, y = mark.center().x(), mark.center().y()
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

def load(username,config='galmark.cfg'):
    out_path, images_path, group_names, category_names, group_max = readConfig(config=config)
    outfile = os.path.join(out_path,username+'.txt')
    data = DataDict()
    skip = True
    
    if os.path.exists(outfile):
        for l in open(outfile):
            if skip: skip = False
            else:
                date,name,group,x,y,ra,dec,categories,comment = [i.strip() for i in l.replace('|\n','').split('|')]
                group_idx = group_names.index(group)
                category_list = categories.split(',')
                category_list = [category_names.index(cat) for cat in category_list]
                category_list.sort()
                
                if (x!='NaN') and (y!='NaN'):
                    mark_args = (int(x),int(y))
                    mark_kwargs = {'wcs': parseWCS(os.path.join(images_path,name)), 'group': group_idx}
                    mark = Mark(*mark_args, **mark_kwargs)

                    if not data[name][group_idx]['marks']:
                        data[name][group_idx]['marks'] = []

                    data[name][group_idx]['marks'].append(mark)

                data[name]['comment'] = comment
                data[name]['categories'] = category_list
                
    return data

def glob(dir,ext,data_filt:DataDict={}):
     # Find all images in image directory
    all_images = _glob.glob(dir + '*.' + ext)

    # Get list of paths to images if they are in the dictionary (have been edited)
    if (data_filt):
        edited_images = [dir + f for f in data_filt.keys()]
        unedited_images = [i for i in all_images if i not in edited_images]
    else:
        edited_images = []
        unedited_images = all_images

    # Shuffle the remaining unedited images
    rng = np.random.default_rng()
    rng.shuffle(unedited_images)

    # Put edited images at the beginning, unedited images at front
    images = edited_images + unedited_images
    if len(edited_images) < len(all_images): idx = len(edited_images)
    else: idx = len(edited_images) - 1

    return images, idx

def inputs(config='galmark.cfg'):
    out_path, images_path, group_names, category_names, group_max = readConfig(config)
    username = galmark.window.StartupWindow().getUser()

    return username, out_path, images_path, group_names, category_names, group_max
