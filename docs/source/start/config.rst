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

* "group(s)": ``Groups`` allow for automatically disassociating certain features in an object from each other, as well as associating similar features to each other. The ``group`` that a ``mark`` is in is saved in the ``marks`` file (``<username>_marks.txt``) in your save directory. For example, in an image of a cat, there are four paws, one nose, and one tail: with three ``groups`` named "paws," "nose," and "tail," we can use the ``group`` of ``marks`` named "paws" to identify each paw and their location in the image, the ``group`` of ``marks`` named "nose" to identify the nose of the cat, and the ``group`` of ``marks`` named "tail" to identify the tail of the cat. A few things worth reiterating:
   #. A ``group`` is a subset of ``marks`` that each contain a similarity, like each being a paw.
   #. A ``group`` name can be customized
   #. As mentioned for ``marks``, a custom upper-limit of ``marks`` per group can be set in the Settings (**Edit > Settings**).
   #. There are up to nine (9) ``groups`` that can be customized, allowing for up to 9 different types of features to be identified and logged within an image.

* "categor(y/ies)": ``Categories`` are used for classifying images as a whole. Pressing the ``category`` box for an image (or their respective keyboard shortcuts) will save that image's ``category`` in the ``images`` file (``<username>_images.txt``) in your save directory. For example, if you have 10 images total, 3 contain one cat each, 3 contain one dog each, and 4 contain one bird each, and you want to sort these images based on what pet is in them, you can customize one ``category`` name as "cat," another as "dog," and the last as "bird," and based on what is in the image, click that ``category`` box to classify each image for each pet type. While this is a similar idea as to ``marks``, it's important to note that ``categories`` are specifically meant for classifying **an entire image**, whereas ``marks`` are for classifying features **within an image**, which may have multiple.

* "catalog(s)": ``Catalogs`` are used for loading in external data. If there are features in images that have already been identified, these features can be tagged and labeled by loading a ``catalog``. ``Catalogs`` are in CSV format, either in a CSV file or a text file formatted to a CSV. We provide example files for various ways that these files must be formatted to load properly (here). Upon pressing the ``Open Catalog...`` button (**File > Open > Open Catalog...**), you will be prompted to select the ``catalog`` file. After pressing ``Open`` you are prompted to select a color for the ``catalog``. At present, there is no option to change the color after picking, unless you choose to delete all loaded ``catalogs`` and re-load them one by one (if you have multiple loaded) with your new desired color. ``Catalog`` files contain an option to set the size of the tag based on pixels or arcseconds (if WCS data is available in the images). If you choose to not specify a size, ``imgmarker`` will use the default size in pixels (the sum of the displayed image's width and height divided by 200, rounded up to the next integer, and multiplied by 2, e.g. image width is 100 and image height is 200, then the tag will have a diameter of 4 pixels: round((100+200)/200)*2 = 4). There are a few things worth noting about ``catalogs``:
   #. ``Catalog`` tags (which look like ``marks``, but are squares instead of circles) are loaded into an image on an image-by-image basis. This means that when you first load a ``catalog``, ``imgmarker`` will immediately check if there are any ``catalog`` tags that can be plotted in the currently displayed image. This is done to avoid having a long wait upon first loading a ``catalog`` at the cost of increasing loading times (by a small fraction) when changing images.
   #. If your ``catalog`` file uses WCS coordinates (RA and Dec, which requires **all** of the images in your dataset to have WCS solutions) and you specify a size in arcseconds for your ``catalog`` tags, ``imgmarker`` uses each image's WCS solution to convert your size in arcseconds to the correct size in pixels based on that image's WCS solution (which contains the pixel scale).
   #. If your ``catalog`` file uses x and y coordinates (Cartesian coordinates), then ``imgmarker`` will load each tag in the file into each image. We realize this is probably not always the most convenient method for loading x and y coordinates, and if there is enough interest in this feature we can improve it upon request. If this is something you're interested in, please open an `issue <https://github.com/andikisare/imgmarker/issues>`_ on Github with the "Enhancements" label and what changes you'd like to see to this feature.

As a result of #1 above, the larger your ``catalog`` is, the longer it will take to load when you seek to the next image.
One feature we intend to add in the future is the ability to track each loaded ``catalog`` and change their colors or delete specific ``catalogs``, as opposed to having to delete all ``catalogs`` to change the color of one, or delete all ``catalogs`` to remove one ``catalog`` from what is loaded (and load the others back in).

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


