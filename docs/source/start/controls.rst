Controls and Keybindings
======================

Currently, there is no functionality for modifying the keybindings.

.. Note::
   **Changing the names of** ``groups`` **and** ``categories`` **will change their name in the Controls window of** ``imgmarker`` **to help keep track of which** ``group`` **and** ``category`` **corresponds to which buttons.**

Terminology (brief)
-------------------
.. Note::
  See the `Configuration page <https://imgmarker.readthedocs.io/en/latest/start/config.html#terminology>`_ for more explicit definitions of terminology, but we provide a brief description below.
mark(s)
  A tag used for identifying objects **within** an image and saving their coordinates. Each ``mark`` belongs to a ``group``.

group(s)
  Each ``mark`` belongs to a ``group``. Each ``group`` name can be customized. If there are multiple different types of features you want to tag in one image, you want to use multiple ``groups`` of ``marks`` to identify them.

categor(y/ies)
  Image-level classification. If you want to tag an image as a whole, use a ``category``. ``Category`` names can also be customized.

catalog(s)
  An external set of coordinates that can be overlaid on each image. The function of a ``catalog`` differs based on whether the input coordinates are RA and Dec and the images loaded have WCS solutions, or if the input is in cartesian (x,y) pixel coordinates.

Keybindings
-----------

Below is a table of the keybindings.

.. list-table::
   :widths: 50 50
   :header-rows: 0

   * - Group "1"
     - :kbd:`LMB` [1]_ or :kbd:`1`
   * - Group "2" 
     - :kbd:`2`
   * - Group "3"
     - :kbd:`3`
   * - Group "4"
     - :kbd:`4`
   * - Group "5"
     - :kbd:`5`
   * - Group "6"
     - :kbd:`6`
   * - Group "7"
     - :kbd:`7`
   * - Group "8"
     - :kbd:`8`
   * - Group "9"
     - :kbd:`9`
   * - Category "1"
     - :kbd:`Ctrl` + :kbd:`1`
   * - Category "2"
     - :kbd:`Ctrl` + :kbd:`2`
   * - Category "3"
     - :kbd:`Ctrl` + :kbd:`3`
   * - Category "4"
     - :kbd:`Ctrl` + :kbd:`4`
   * - Category "5"
     - :kbd:`Ctrl` + :kbd:`5`
   * - Next
     - :kbd:`Tab`
   * - Back
     - :kbd:`Shift` + :kbd:`Tab`
   * - Change frame
     - :kbd:`Space`
   * - Delete
     - :kbd:`RMB` [2]_ or :kbd:`Delete` or :kbd:`Backspace`
   * - Undo mark
     - :kbd:`Ctrl` + :kbd:`Z`
   * - Redo mark
     - :kbd:`Ctrl` + :kbd:`Shift` + :kbd:`Z`
   * - Enter comment
     - :kbd:`Enter`
   * - Focus
     - :kbd:`MMB` [3]_
   * - Zoom in/out
     - :kbd:`Wheel`
   * - Favorite image
     - :kbd:`F`
   * - Open Save...
     - :kbd:`Ctrl` + :kbd:`O`
   * - Open Images...
     - :kbd:`Ctrl` + :kbd:`Shift` + :kbd:`O`
   * - Open Catalog...
     - :kbd:`Ctrl` + :kbd:`Shift` + :kbd:`C`
   * - Settings
     - :kbd:`Ctrl` + :kbd:`,`
   * - Zoom In
     - :kbd:`Ctrl` + :kbd:`=`
   * - Zoom Out
     - :kbd:`Ctrl` + :kbd:`-`
   * - Zoom to Fit
     - :kbd:`Ctrl` + :kbd:`0`
   * - Frames...
     - :kbd:`Ctrl` + :kbd:`F`
   * - Show Marks
     - :kbd:`Ctrl` + :kbd:`M`
   * - Show Mark Labels
     - :kbd:`Ctrl` + :kbd:`L`
   * - Show Catalog
     - :kbd:`Ctrl` + :kbd:`Shift` + :kbd:`M`
   * - Show Catalog Labels
     - :kbd:`Ctrl` + :kbd:`Shift` + :kbd:`L`
   * - Gaussian Blur...
     - :kbd:`Ctrl` + :kbd:`B`
   * - Controls
     - :kbd:`F1`
   

.. [1] LMB refers to the Left Mouse Button (left click).
.. [2] RMB refers to the Right Mouse Button (right click).
.. [3] MMB refers to the Middle Mouse Button (scroll wheel button).
