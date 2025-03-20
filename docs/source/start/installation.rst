Installation
======================

Using pip (from PyPI)
---------------------

**It is recommended that you create a Python environment for** ``imgmarker`` **using a tool like** `Anaconda <https://anaconda.org/>`_. ``Imgmarker`` **was developed using Python 3.12, so we recommend an environment with this Python version.** **Installing** ``imgmarker`` **automatically installs Python dependencies in the environment.**


The steps below walk through the process of creating a new Python environment and installing ``imgmarker`` into it. Skip to Step 4 if you already know how to create Python environments and use them.

1. Using `Anaconda <https://anaconda.org/>`_, you can create a conda Python environment by running the following (with your ``base`` environment or some other conda Python environment activated)::

    conda create -n [name] python=3.12

with "``[name]``" being the name you choose to call the environment.

2. After ``conda`` finishes solving the environment, it will prompt you for basic packages to install alongside Python in your new environment. Type "y" and press ``Enter`` to proceed.

3. Next, activate the new environment with::

    conda activate [name]

4. Lastly, in the Python environment of your choice (if you followed Steps 1-3, you should already be in your new Python environment), run::

    pip install imgmarker

You can now run Image Marker from the terminal in any directory by running the command ``imgmarker``. The configuration file generated upon first running Image Marker is made in the save directory selected on startup.


Using pip (from cloning the repository)
---------------------
The PyPI version of ``imgmarker`` is not constantly up to date with the `Github repository <https://github.com/andikisare/imgmarker/tree/main>`_, so you may wish to install the most recent version directly from Github. The steps below outline this process.
We once again recommend that you create a dedicated Python environment for ``imgmarker`` to prevent any conflicts with other Python packages you may have installed in other environments, since installing ``imgmarker`` will automatically install Python dependencies in your activated environment. For instructions on how to do this using a tool like `Anaconda <https://anaconda.org/>`_, see Steps 1-3 above (under "Using pip (from PyPI)"). Once you've activated your desired Python environment or finished Step 3 above, follow the steps below to install ``imgmarker`` from Github.

1. First, clone the repository wherever you'd like. There is no specific place you need to clone the repository, so navigate to the directory you want to store it in and then run the following::

    git clone https://github.com/andikisare/imgmarker.git

or::

    git clone git@github.com:andikisare/imgmarker.git

2. Next, run the following command to install ``imgmarker`` and its dependencies into your Python environment::

    pip install ./imgmarker

You can now run Image Marker from the terminal in any directory by running the command ``imgmarker``. The configuration file generated upon first running Image Marker is made in the save directory selected on startup.


Executables
---------------------
**Due to security concerns, it is recommended that you make your own executable from the source code, but we provide precompiled executables for major releases that you may use at your own risk.**
**We will be providing the exact commands to use for compiling and executables soon. We compile using** ``pyinstaller`` **to make our executables.**

Portable executables are available on `Github <https://github.com/andikisare/imgmarker/releases/latest>`_. Versions are available for Windows 11, M1+ Mac, and Ubuntu 20.04+.

Mac
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To compile manually on **Intel Mac**:
Install ``pyinstaller`` in your desired Python environment (see Steps 1-3 in "Using pip (from PyPI)" for instructions on creating and activating a new Python environment) then follow the steps below::

1. Clone the `Github repository <https://github.com/andikisare/imgmarker/releases/latest>`_ wherever you want to store it::

    git clone https://github.com/andikisare/imgmarker.git

or::

    git clone git@github.com:andikisare/imgmarker.git

2. Then navigate to the main source code directory::

    cd imgmarker/imgmarker

3. Lastly, run::

    pyinstaller  \
     	--name imgmarker \
        --icon icon.ico \
    	--windowed  \
    	-D __init__.py \
    	--noconfirm \
    	--distpath ../dist \
    	--clean \
    	--collect-all imgmarker \
        --hidden-import=imgmarker \
        --hidden-import=imgmarker.pyqt \
        --add-data=".:."

This should create an executable file specific to your operating system and CPU architecture (your compiled version will not work on M1+ Mac if you compile on Intel Mac, and vice versa).


Apple may block Image Marker the first time you try to run the application. If this happens, after attempting to launch Image Marker, navigate to **Settings > Privacy & Security** and click **Open Anyway**.

Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Likewise, Windows may block Image Marker the first time the application is ran. In the error window, click **More info**, then click **Run anyway**.

FAQ
^^^^^^^^^^^^^^^^^^^^^^^^^^^

* If you run into issues trying to build ``imgmarker`` manually, you may have PyQt5 installed already, which may conflict with the compilation. We recommend making a dedicated Python environment for installing ``imgmarker``. If you don't want to make a new Python environment, try adding "-exclude PyQt5" to the end of the ``pyinstaller`` command, to force it not to compile an older version of PyQt into the executable. 

* If you're getting a Recursion Error, try following the recommended steps in the error (if available). If there are no steps shown, try adding this line near the top of the program's .spec file::

    import sys ; sys.setrecursionlimit(sys.getrecursionlimit() * 5)


If none of these suggestions work, please open an `issue <https://github.com/andikisare/imgmarker/issues>`_ on Github with the full terminal output and your system information including your operating system and CPU and we will work with you to fix the issue as soon as possible.
