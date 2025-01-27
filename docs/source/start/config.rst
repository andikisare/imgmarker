Configuration
#####################

Settings can be configured within the GUI or directly edited in the configuration file (``$USERNAME_config.txt``).

Settings
*********************

* ``image_dir``: The image directory, where ``imgmarker`` looks for images of all supported formats.
* ``groups``: The name of each group. Names must not contain commas.
* ``categories``: The name of each category. Names must not contain commas.
* ``group_max``: The maximum number of marks that can be placed for a particular group. The position of the value that is replaced in this variable corresponds to which group it limits.
* ``randomize_order``: True or False, whether or not the displayed images are shuffled randomly or displayed in alphabetical order.

Example
*********************

This configuration::

   image_dir = /home/akisare/science/megacluster
   groups = BCG, Candidate BCG,3,4,5,6,7,8, weird
   categories = 1,2,3,4,5
   group_max = 1,3,None,None,None,None,None,None,2
   randomize_order = True

keybinds the '*Left click OR 1*' buttons to group 'BCG' and limits the number of group 'BCG' marks placed to 1, the '*2*' button to group 'Candidate BCG' and limits the number of group 'Candidate BCG' marks placed to 3, and the '*9*' button to group 'weird' and limits the number of group 'weird' marks placed to 2.

Currently, there is no functionality for changing the keybindings. This means that each custom group still keeps the original keybinding. Keybindings can be found in the instructions window while ``imgmarker`` is running or in the keybinds section below.

Keybinds
*********************

.. csv-table::
   :file: keybind_table.csv
   :widths: 50, 50
   :header-rows: 1



