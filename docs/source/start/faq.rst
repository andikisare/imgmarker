FAQ
======================

Consider the below solutions to common issues in building, installing, and using Image Marker. If none of these suggestions work, please open an `issue <https://github.com/andikisare/imgmarker/issues>`_ on GitHub with steps to recreate the issue, the full terminal output, and your system information including your operating system and CPU. We will then work with you to fix the issue.

General Issues
---------------------

.. dropdown:: Duplicate PyQt versions

    If you run into issues trying to build Image Marker manually, you may have both PyQt5 and PyQt6 installed, which may conflict with the compilation. We recommend making a dedicated Python environment for installing Image Marker. If you don't want to make a new Python environment, try adding "-exclude PyQt5" to the end of the ``pyinstaller`` command, to force it not to compile an older version of PyQt into the executable.

.. dropdown:: Recursion Error

    If you're getting a Recursion Error, try following the recommended steps in the error (if available). If there are no steps shown, try adding this line near the top of the program's .spec file::

        import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)

Mac Issues
---------------------

.. dropdown:: Apple is blocking Image Marker from running
    
    Apple may block Image Marker executable the first time it runs. If this happens, after attempting to launch Image Marker, navigate to **Settings > Privacy & Security** and click **Open Anyway**.

Windows Issues
---------------------

.. dropdown:: Windows is blocking Image Marker from running
    
    Windows may block the Image Marker executable the first time it runs. In the error window, click **More info**, then click **Run anyway**.