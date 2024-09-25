Galaxy Marker (galmark) is a tool for marking Brightest Cluster Galaxies, interesting phenomena, and more in galaxy clusters.
It is designed to be configurable for multiple purposes using the configuration file generated upon first running galmark
(galmark.cfg).

To install galmark, clone the galmark repository from github, then in the python environment of your choice, run:

pip install ./galmark

outside of the 'galmark' directory.

You can now run galmark from anywhere. The configuration file generated upon first running galmark is made in the directory
that you run galmark.

Within the configuration file, the output path ('out_path', where your data files will be saved) can be configured. Make sure to include
the final forward or backward slash ('/' or '\' depending on your operating system) at the end of the directory. The directory
containing image files can also be specified under 'images_path' and follows the same directory rule as above.
Group names can be specified but must not contain spaces or special characters (use underscores instead, e.g. 'maybe_BCG').
Problem names can also be specified and also must not contain spaces or special characters (e.g. 'no_BCG').
Using the 'region_limits' variable, it is possible to limit the number of regions of a particular group that can be placed (e.g. there is only ONE Brightest Cluster
Galaxy in a galaxy cluster, but there can be multiple images of lensing evidence to label). The position of the value that is
replaced in this variable corresponds to which group it limits (see example below).

Example
This configuration:

groups = BCG,maybe_BCG,3,4,5,6,7,8,weird
region_limits = 1,3,None,None,None,None,None,None,2

sets 'Left click OR 1' to group 'BCG' and limits the number of group 'BCG' regions placed to 1, '2' to group 'maybe_BCG'
and limits the number of group 'maybe_BCG' regions placed to 3, and '9' to group 'weird' and limits the number of group
'weird' regions placed to 2.

Currently, there is no functionality for changing the keybindings. This means that each custom group still keeps the original
keybinding.

To load a previous save, use the same username you used to create the save file. Future functionality will be added to
load save files and save as a separate username.
