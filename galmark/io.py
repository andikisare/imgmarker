import os
import numpy as np
from galmark.window import StartupWindow

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

def writeToTxt(data,username,date):
    lines = []
    name_lengths = []
    group_lengths = []
    ra_lengths = []
    dec_lengths = []
    problem_lengths = []
    comment_lengths = []

    out_path, images_path, group_names, problem_names = readConfig()
    outfile = os.path.join(out_path, username + '.txt')
    
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

def inputs(config='galmark.cfg'):
    out_path, images_path, group_names, problem_names = readConfig(config)
    username = StartupWindow().getUser()

    return username, out_path, images_path, group_names, problem_names
