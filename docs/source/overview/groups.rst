.. _groups:

Mark groups
======================
A mark group is a collection of :ref:`marks:marks` that have been grouped together by the user. The group of a mark is accessed through the mark's :py:attr:`~imgmarker.gui.mark.Mark.g` attribute. 

For example, in an image of a cat, there are four paws, one nose, and one tail: with three groups named "paws," "nose," and "tail," we can use the group of marks named "paws" to identify each paw and their location in the image, the group of marks named "nose" to identify the nose of the cat, and the group of marks named "tail" to identify the tail of the cat. 

A few things worth reiterating:

1. A mark group is a collection of marks that each contain a similarity, like each being a paw.
2. The name of a mark group can be customized
3. As mentioned for marks, a custom upper-limit of marks per group can be set in **Edit > Settings**.
4. There are up to 9 mark groups that can be customized.