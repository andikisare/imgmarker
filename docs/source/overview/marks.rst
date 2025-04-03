.. _marks:

Marks
======================

Marks are used to identify features in a particular image, like a cat's four paws. They are instantiated through the :py:class:`~imgmarker.gui.mark.Mark` class. 

- Marks can be placed in any of 9 :ref:`groups <groups>`
- Placing a mark will save the x and y pixel coordinates (and right ascension and declination if available) of the center of that mark in the marks file (``<username>_marks.txt``) in your save directory.
- The maximum number of marks in a group can be customized in **Edit > Settings**.
- If you place a mark in a group with a limit of 1, then placing another mark will replace the original mark with a new mark at the cursor.
- The user can place a mark by pressing any number on the keyboard between 1 and 9.
- Pressing each number will place a mark at the location of the cursor, and in the group associated with that number.
- The names of each group can be modified in **Edit > Settings**.
- Once a mark is placed, its pixel coordinates, WCS coordinates (if applicable), group, label, the name of the image associated with the mark, and the current date are all saved into <username>_marks.txt.
- The label of the mark can be modified simply by clicking on the label of the mark, and typing. Pressing enter, or clicking outside the label, will save this information into the same text file. *This does not change the name of the* group *that the* mark *is in; the label is saved separately.*

The left panel in Figure 1 shows an image of Messier 31, a nearby galaxy, before placing marks, while the right panel shows the same image but after each galaxy in the image is marked with the group "Galaxy" (which is the first group here, placed using the left mouse button or the "1" key on the keyboard).

.. figure:: Before_after_mark.jpg
  :align: center

  Figure 1: Before and after placing marks to identify each galaxy in the image. Image credit: `Ryan Walker <https://astrorya.github.io>`_
