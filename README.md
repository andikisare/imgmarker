<div align="center">
<img src="https://raw.githubusercontent.com/andikisare/imgmarker/main/imgmarker/icon.ico" alt="logo" width="250"> </img>
</div>

[can add link to paper like so: Add link to paper here like so: "{!{arXiv}(://img.shields.io/badge/arXiv-{our link}.svg)}(link to arXiv paper)"]: # 

[where the squiggly brackets are square brackets and the link is completed]: #

# Image Marker (`imgmarker`)

[![astropy](http://img.shields.io/badge/powered%20by-AstroPy-orange.svg?style=flat)](http://www.astropy.org/)

## Description

Image Marker (`imgmarker`) is a tool for marking, categorizing, and annotating TIFF, FITS, PNG, and JPEG files.
`Imgmarker` does not modify the image itself, it only displays it and creates text files (.txt) containing the information that you mark. `Imgmarker` uses [PyQt6](https://pypi.org/project/PyQt6/) to build the GUI application, [Pillow](https://pypi.org/project/pillow/) to handle images, and [Astropy](https://www.astropy.org/) to load FITS data and convert coordinates.

It is designed to be configurable for multiple purposes using the configuration file generated upon first running `imgmarker` ($USERNAME_config.txt). `Imgmarker` looks for the configuration file in the save directory (the directory you first choose on startup).

## Installation instructions

### Using pip:
#### *It is recommended that you create a python environment for `imgmarker`. Installing `imgmarker` automatically installs Python dependencies in the environment.*

In the Python environment of your choice, run:

```sh
git clone git@github.com:andikisare/imgmarker.git
cd imgmarker
pip install ./imgmarker
```
You can now run `imgmarker` from anywhere. The configuration file generated upon first running `imgmarker` is made in the save directory selected on startup.

### **Executables**:
(WIP) We provide compiled executable files for Windows 11, M1+ Mac, and Ubuntu 18.04+.

## Configuration file

Settings can be configured within the GUI or directly edited in the configuration file ($USERNAME_config.txt)

### Settings
**image_dir** (the image directory, where `imgmarker` looks for images of all supported formats)\
**groups** (the name of each group)\*\
**categories** (the name of each category)\*\
**group_max** (the maximum number of marks that can be placed for a particular group)\**\
**randomize_order** (True or False, whether or not the displayed images are shuffled randomly or displayed in alphabetical order)

\* Names must not contain commas.\
\** The position of the value that is replaced in this variable corresponds to which group it limits (see example below).

### Example
This configuration:
```txt
image_dir = /home/akisare/science/megacluster
groups = BCG, Candidate BCG,3,4,5,6,7,8, weird
categories = 1,2,3,4,5
group_max = 1,3,None,None,None,None,None,None,2
randomize_order = True
```
keybinds the '*Left click OR 1*' buttons to group 'BCG' and limits the number of group 'BCG' marks placed to 1, the '*2*' button to group 'Candidate BCG' and limits the number of group 'Candidate BCG' marks placed to 3, and the '*9*' button to group 'weird' and limits the number of group 'weird' marks placed to 2.

Currently, there is no functionality for changing the keybindings. This means that each custom group still keeps the original keybinding. Keybindings can be found in the instructions window while `imgmarker` is running or in the keybinds section below.

## Loading a previous save and favorites

To load a previous save, open the same directory you used previously (to create the save files). To open favorite files, navigate outside of your chosen save directory and copy-paste the directory containing the '$USERNAME_favorites.txt' file you wish to open with a new name (do not include special characters). Enter the new directory, delete '$USERNAME_images.txt' and copy-paste '$USERNAME_favorites.txt' as '$USERNAME_images.txt'. Now reopen `imgmarker` and select your new directory as your save directory. This will open your favorites file as if it were an 'images.txt' file, which puts all of your favorited images first, while also keeping your favorited images as favorites.

Note: `imgmarker` makes the first visible image one that you have not yet looked at, so to view your favorited images, use Shift+Tab (which cycles backwards through the images).

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
