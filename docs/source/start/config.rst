Configuration
======================

Settings can be configured within the GUI (**Edit > Settings**) or directly edited in the configuration file (``<username>_config.txt``). Right now, only some settings are available in the configuration file, while everything is available in the GUI.

Terminology
---------------------

We use some terminology specific to Image Marker that may not be immediately obvious, so we try to explain it here.

* "mark(s)": ``Marks`` are used to identify features in a particular image, like a cat's four paws. Placing a ``mark`` will save the x and y pixel coordinates (and right ascension and declination if available) of the center of that mark in the ``marks`` file (``<username>_marks.txt``) in your save directory. There are a few features that make ``marks`` unique:
   #. Each ``mark`` is part of a ``group`` (see definition below), therefore allowing multiple ``marks`` having a similar property to be immediately associated with each other.
   #. Each ``group`` of ``marks`` is a different color for easy visual distinction between unassociated ``marks``.
   #. Each ``mark`` saves its coordinates, **unlike** ``categories`` (see below).
   #. The maximum number of ``marks`` in a ``group`` can be customized in Settings (**Edit > Settings**).
   #. Clicking on the text label of a ``mark`` in an image allows for custom label editing, while still preserving the ``group`` that the mark belongs to. 

* "group(s)": ``Groups`` allow for automatically disassociating certain features in an object from each other. For example, in an image of a cat, there are four paws, one nose, and one tail: with three ``groups`` named "paws," "nose," and "tail," we can use the ``group`` of ``marks`` named "paws" to identify each paw and their location in the image, the ``group`` of ``marks`` named "nose" to identify the nose of the cat, and the ``group`` of ``marks`` named "tail" to identify the tail of the cat. A few things worth reiterating:
   #. A ``group`` is a subset of ``marks`` that each contain a similarity, like each being a paw.
   #. A ``group`` name can be customized
   #. As mentioned for ``marks``, a custom upper-limit of ``marks`` per group can be set in the Settings (**Edit > Settings**).
   #. There are up to nine (9) ``groups`` that can be customized, allowing for up to 9 different types of features to be identified and logged within an image.

* "categor(y/ies)":

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

renames "Group 1" to "BCG" and limits the number of marks in "BCG" to 1, renames "Group 2" to "Candidate BCG" and limits the number of marks in "Candidate BCG" to 3, and renames "Group 9" button to "weird" and limits the number of marks in "weird" to 2.


