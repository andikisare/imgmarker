import os
import numpy as np
import galmark.window
from galmark.region import Region
from galmark import __dirname__
from PyQt6.QtCore import Qt
from PIL import Image
from PIL.TiffTags import TAGS
from astropy.wcs import WCS
from astropy.io import fits
from collections import defaultdict
import io
import pickle

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
        group_names = ['1','2','3','4','5','6','7','8','9']
        problem_names = ['None','not_centered','bad_scaling','no_cluster','high_redshift','other']

        config_file.write(f'out_path = {out_path}\n')
        config_file.write(f'images_path = {images_path}\n')
        config_file.write('groups = 1,2,3,4,5,6,7,8,9\n')
        config_file.write(f'problems = {problem_names[1]},{problem_names[2]},{problem_names[3]},{problem_names[4]},{problem_names[5]}')


    else:
        for l in open(config):
            var, val = l.replace(' ','').replace('\n','').split('=')

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

            if var == 'problems':
                problem_names = val.split(',')
                problem_names.insert(0, 'None')
        
    return out_path, images_path, group_names, problem_names
                
def checkUsername(username):
    return (username != "None") and (username != "")

def save(data,username,date):
    data_pkl = []
    lines = []
    name_lengths = []
    group_lengths = []
    ra_lengths = []
    dec_lengths = []
    problem_lengths = []
    comment_lengths = []

    out_path, images_path, group_names, problem_names = readConfig()
    outfile = os.path.join(out_path, username + '.txt')
    outpkl = os.path.join(__dirname__, username + '.pkl')
    
    # Create the file
    if os.path.exists(outfile): 
        os.remove(outfile)
    out = open(outfile,"a")

    
    if checkUsername(username) and data:
        names = list(data.keys())

        for name in names:
            comment = data[name]['comment']
            problem = problem_names[data[name]['problem']]

            # Get list of groups containing data
            level2_keys = list(data[name].keys())
            groups = [ key for key in level2_keys if isinstance(key,int) 
                        and data[name][key]['Regions'] ]

            # If there are no image problems, and there is data in groups, then add this data to lines
            if (problem == 'None') and (len(groups) != 0):
                for group in groups:
                    group_name = group_names[group]
                    region_list = data[name][group]['Regions']

                    for region in region_list:
                        ra, dec = region.centerWCS()
                        l = [date,name,group_name,ra,dec,problem,comment]

                        lines.append(l)
                        name_lengths.append(len(name))
                        group_lengths.append(len(group_name))
                        ra_lengths.append(len(f'{ra:.8f}'))
                        dec_lengths.append(len(f'{dec:.8f}'))
                        problem_lengths.append(len(problem))
                        comment_lengths.append(len(comment))

                        region_args = (region.center().x(), region.center().y())
                        region_kwargs = {'r': region.r, 'wcs': region.wcs, 'group': region.g}
                        region_data = [name,problem,comment,region_args,region_kwargs]
                        
                        data_pkl.append(region_data)
            
            # Otherwise, if there is a problem or a comment, replace ra/dec with NaNs
            elif (problem != 'None') or (comment != 'None'):
                group_name = 'None'
                ra = 'NaN'
                dec = 'NaN'
                l = [date,name,group_name,ra,dec,problem,comment]

                lines.append(l)
                name_lengths.append(len(name))
                group_lengths.append(len(group_name))
                ra_lengths.append(len(ra))
                dec_lengths.append(len(dec))
                problem_lengths.append(len(problem))
                comment_lengths.append(len(comment))
            
            # Otherwise, (no comment, no problem, and no data) delete entry from dictionary
            else: pass

    # Print out lines if there are lines to print
    if len(lines) != 0:
        # Dynamically adjust column widths
        nameln = np.max(name_lengths) + 2
        groupln = max(np.max(group_lengths), 5) + 2
        raln = max(np.max(ra_lengths), 2) + 2
        decln = max(np.max(dec_lengths), 2) + 2
        problemln = max(np.max(problem_lengths), 9) + 2
        commentln = max(np.max(comment_lengths), 7) + 2
        dateln = 12

        out.write(f'{'date':^{dateln}}|{'name':^{nameln}}|{'group':^{groupln}}|{'RA':^{raln}}|{'DEC':^{decln}}|{'problem':^{problemln}}|{'comment':^{commentln}}\n')

        for l in lines:
            try: outline = f'{l[0]:^{dateln}}|{l[1]:^{nameln}}|{l[2]:^{groupln}}|{l[3]:^{raln}.8f}|{l[4]:^{decln}.8f}|{l[5]:^{problemln}}|{l[6]:^{commentln}}\n'
            except: outline = f'{l[0]:^{dateln}}|{l[1]:^{nameln}}|{l[2]:^{groupln}}|{l[3]:^{raln}}|{l[4]:^{decln}}|{l[5]:^{problemln}}|{l[6]:^{commentln}}\n'
            out.write(outline)

        pickle.dump(data_pkl, open(outpkl, 'wb'))

def load(username,config='galmark.cfg'):
    out_path, images_path, group_names, problem_names = readConfig(config=config)
    outfile = os.path.join(out_path,username+'.txt')
    savefile = os.path.join(__dirname__,username+'.pkl')
    
    raw_data = np.loadtxt(outfile,delimiter='|',dtype=str)[1:]
    date_list = [ d.replace(' ', '') for d in raw_data[:,0] ]
    name_list = [ n.replace(' ', '') for n in  raw_data[:,1] ]
    group_list = [ g.replace(' ', '') for g in raw_data[:,2] ]
    RA_list = [ float(ra.replace(' ', '')) for ra in raw_data[:,3] ]
    DEC_list = [ float(dec.replace(' ', '')) for dec in raw_data[:,4] ]
    problem_list = [ p.replace(' ', '') for p in raw_data[:,5] ]
    comment_list = [ c.replace(' ', '') for c in raw_data[:,6] ]

    data_pkl = pickle.load(open(savefile,'rb'))
    data = DataDict()

    for region_data in data_pkl:
        name = region_data[0]
        problem = region_data[1]
        comment = region_data[2]
        region_args = region_data[3]
        region_kwargs = region_data[4]

        group_idx = region_kwargs['group']
        problem_idx = problem_names.index(problem)

        data[name]['comment'] = comment
        data[name]['problem'] = problem_idx

        region = Region(*region_args, **region_kwargs)

        if not data[name][group_idx]['Regions']:
            data[name][group_idx]['Regions'] = []

        data[name][group_idx]['Regions'].append(region)

    return data

def inputs(config='galmark.cfg'):
    out_path, images_path, group_names, problem_names = readConfig(config)
    username = galmark.window.StartupWindow().getUser()

    return username, out_path, images_path, group_names, problem_names
