<div align="center">
<img src="https://raw.githubusercontent.com/andikisare/imgmarker/main/imgmarker/icon.png" alt="logo" width="250"> </img>
</div>

[can add link to paper like so: Add link to paper here like so: "{!{arXiv}(://img.shields.io/badge/arXiv-{our link}.svg)}(link to arXiv paper)"]: # 

[where the squiggly brackets are square brackets and the link is completed]: #

# Image Marker (imgmarker)

## Description

Image Marker (imgmarker) is a tool for marking, categorizing, and annotating TIFF, FITS, PNG, and JPEG files.
Imgmarker does not modify the image itself, it only displays it and creates text files (.txt) containing the information
that you mark.

It is designed to be configurable for multiple purposes using the configuration file generated upon first running imgmarker
(imgmarker.cfg). Imgmarker looks for the configuration file in the current working directory (the directory you run it from).

## Installation instructions

### **Linux:**
#### *It is recommended that you create a python environment for imgmarker. Installing imgmarker automatically installs Python dependencies in the environment.*

In your python environment of your choice, run:

```sh
git clone git@github.com:andikisare/imgmarker.git
cd imgmarker
pip install ./imgmarker
```

You can now run imgmarker from anywhere. The configuration file generated upon first running imgmarker is made in the directory
that you run imgmarker.

### **Mac:**
(WIP) We provide an executable file for Mac users to run.

### **Windows 11:**
(WIP) We provide an executable file for Windows 11 users to run.

*Note: We have not tested the Windows 11 executable in Windows 10.*

## Configuration instructions

Some settings can be configured within the GUI, but some must be specified within the configuration file (imgmarker.cfg).

### *Settings that can only be modified in the configuration file:*
**groups** (the name of each group)\*\
**categories** (the name of each category)\*\
*group_max** (the maximum number of marks that can be placed for a particular group)\**

\* Names must not contain commas.\
\** The position of the value that is replaced in this variable corresponds to which group it limits (see example below).

### *Settings that can be modified in the GUI or in the configuration file:*
**out_dir** (the output directory, where imgmarker will create directories named after the username inputted on startup)\
**img_dir** (the image directory, where imgmarker looks for images of all supported formats)\
**randomize_order** (True or False, whether or not the displayed images are shuffled randomly or displayed in alphabetical order)\

### Configuration example
This configuration:
```txt
groups = BCG, Candidate BCG,3,4,5,6,7,8, weird
region_limits = 1,3,None,None,None,None,None,None,2
```
keybinds the '*Left click OR 1*' buttons to group 'BCG' and limits the number of group 'BCG' marks placed to 1, the '*2*' button to group 'Candidate BCG' and limits the number of group 'Candidate BCG' marks placed to 3, and the '*9*' button to group 'weird' and limits the number of group 'weird' marks placed to 2.

Currently, there is no functionality for changing the keybindings. This means that each custom group still keeps the original keybinding. Keybindings can be found in the instructions window while imgmarker is running or in the keybinds section below.

## Loading a previous save and favorites

To load a previous save, use the same username you used to create the save file. To open favorite files, navigate to your save directory (out_dir in imgmarker.cfg) and copy-paste the directory containing the 'favorites.txt' file you wish to open with a new name (do not include special characters, it needs to be in the format of an imgmarker 'username'). Enter the new directory and rename 'favorites.txt' as 'images.txt'. Now navigate back to the directory containing your custom imgmarker.cfg file and reopen imgmarker using the name of your new directory as your 'username'. This will open your favorites file as if it were an 'images.txt' file, which puts all of your favorited images first.

Note: imgmarker makes the first visible image one that you have not yet looked at, so to view your favorited images, use Shift+Tab (which cycles backwards through the images).

## Keybinds (with default configuration file)
Group "1"..........................Left click OR 1\
Group "2".....................................2\
Group "3".....................................3\
Group "4".....................................4\
Group "5".....................................5\
Group "6".....................................6\
Group "7".....................................7\
Group "8".....................................8\
Group "9".....................................9\
Next.............................................Tab\
Back.......................................Shift+Tab\
Change frame........................Spacebar\
Delete.......................Right click OR Backspace\
Enter comment........................Enter\
Focus....................................Middle click\
Zoom in/out.........................Scroll wheel\
Exit...........................................Esc OR Q\
Help..............................................F1

## Citation
(coming soon)