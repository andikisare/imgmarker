Configuration
======================

Settings can be configured within the GUI or directly edited in the configuration file (``$USERNAME_config.txt``).

Settings
---------------------
.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Setting
     - Description
   * - ``image_dir``
     - The image directory, where Image Marker looks for images of all supported formats.
   * - ``groups`` 
     - The name of each group. Names must not contain commas.
   * - ``categories``
     - The name of each category. Names must not contain commas.
   * - ``group_max``
     - The maximum number of marks that can be placed for a particular group. The position of the value that is replaced in this variable corresponds to which group it limits.
   * - ``randomize_order``
     - True or False, whether or not the displayed images are shuffled randomly or displayed in alphabetical order.

Example
---------------------

This configuration::

   image_dir = /home/akisare/science/megacluster
   groups = BCG, Candidate BCG,3,4,5,6,7,8, weird
   categories = 1,2,3,4,5
   group_max = 1,3,None,None,None,None,None,None,2
   randomize_order = True

renames 'Group 1' to 'BCG' and limits the number of marks in 'BCG' to 1, renames 'Group 2' to 'Candidate BCG' and limits the number of marks in 'Candidate BCG' to 3, and renames 'Group 9' button to 'weird' and limits the number of marks in 'weird' to 2.


