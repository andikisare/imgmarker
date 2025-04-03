.. _catalogs:

Catalogs
======================
Catalogs are used for loading in external catalogs of objects and their coordinates. They are instantiated through the :py:class:`~imgmarker.catalog.Catalog` class. If there are features in images that have already been identified, these features can be marked and labeled by loading a catalog. 

Catalogs are in CSV format, either in a CSV file or a text file formatted to a CSV. We provide example files for various ways that these files must be formatted to load properly (here). 

Upon clicking **File > Open > Open Catalog...**, you will be prompted to select the catalog file. After pressing Open you are prompted to select a color for the catalog. At present, there is no option to change the color after picking, unless you choose to delete all loaded catalogs and re-load them one by one (if you have multiple loaded) with your new desired color. 

Catalog files contain an option to set the size of the mark based on pixels or arcseconds (if WCS data is available in the images). If you choose to not specify a size, imgmarker will by default use a size scaled proportionally to the size of the image in pixels.

There are a few things worth noting about catalogs:

1. Catalog marks (which look like :ref:`marks:marks`, but are squares instead of circles) are loaded into an image on an image-by-image basis. This means that when you first load a catalog, imgmarker will immediately check if there are any catalog marks that can be plotted in the currently displayed image. This is done to avoid having a long wait upon first loading a catalog at the cost of increasing loading times (by a small fraction) when changing images.
2. If your catalog file uses WCS coordinates (RA and Dec, which requires **all** of the images in your dataset to have WCS solutions) and you specify a size in arcseconds for your catalog marks, imgmarker uses each image's WCS solution to convert your size in arcseconds to the correct size in pixels based on that image's WCS solution (which contains the pixel scale).
3. If your catalog file uses x and y coordinates (Cartesian coordinates), then imgmarker will load each mark in the file into each image. We realize this is probably not always the most convenient method for loading x and y coordinates, and if there is enough interest in this feature we can improve it upon request. If this is something you're interested in, please open an `issue <https://github.com/andikisare/imgmarker/issues>`_ on Github with the "Enhancements" label and what changes you'd like to see to this feature.

As a result of (1) above, the larger your catalog is, the longer it will take to load when you seek to the next image.
One feature we intend to add in the future is the ability to track each loaded catalog and change their colors or delete specific catalogs, as opposed to having to delete all catalogs and reload them all to change the color of one, or delete all catalogs to remove one catalog from what is loaded (and load the others back in).