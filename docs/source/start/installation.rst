Installation
======================

.. Important::
    - It is recommended that you create a Python environment for Image Marker using a tool like `Anaconda <https://anaconda.org/>`_.
    - Image Marker was developed using Python 3.12, so we recommend an environment with this Python version.
    - Installing Image Marker automatically installs Python dependencies in the environment.
    - Executables **do not** install Image Marker, instead they are run directly, and thus do not need a Python environment to run in.

Creating python environment
---------------------
Before continuing with the installation procedures 

Using pip (from PyPI)
---------------------

The steps below walk through the process of creating a new Python environment and installing Image Marker into it. Skip to Step 4 if you already know how to create Python environments and use them.

Using `Anaconda <https://anaconda.org/>`_, you can create a conda Python environment by running the following (with your ``base`` environment or some other conda Python environment activated)::

    conda create -n [name] python=3.12

where ``[name]`` is the name of the environment.

After ``conda`` finishes solving the environment, it will prompt you for basic packages to install alongside Python in your new environment. Press :kbd:`y` and then :kbd:`Enter` to proceed.

Next, activate the new environment with::

    conda activate [name]

Lastly, after activating the Python environment of your choice, run::

    pip install imgmarker

You can now run Image Marker from the terminal in any directory by running the command ``imgmarker``. The configuration file generated upon first running Image Marker is made in the save directory selected on startup.


Using pip (from GitHub repository)
---------------------
The PyPI version of Image Marker is not constantly up to date with the `GitHub repository <https://github.com/andikisare/imgmarker/tree/main>`_, so you may wish to install the most recent version directly from GitHub. The steps below outline this process.
We once again recommend that you create a dedicated Python environment for Image Marker to prevent any conflicts with other Python packages you may have installed in other environments, since installing Image Marker will automatically install Python dependencies in your activated environment. For instructions on how to do this using a tool like `Anaconda <https://anaconda.org/>`_, see Steps 1-3 above under `Using pip (from PyPI)`_. Once you've activated your desired Python environment or finished Step 3 above, follow the steps below to install Image Marker from GitHub.

First, clone the repository wherever you'd like. There is no specific place you need to clone the repository, so navigate to the directory you want to store it in and then run the following::

    git clone https://github.com/andikisare/imgmarker.git

or::

    git clone git@github.com:andikisare/imgmarker.git

Next, run the following command to install Image Marker and its dependencies into your Python environment::

    pip install ./imgmarker

You can now run Image Marker from the terminal in any directory by running the command ``imgmarker``. The configuration file generated upon first running Image Marker is made in the save directory selected on startup.


Executables
---------------------
.. Note::
    For your own security, you may make your own executable from the source code, but we provide precompiled executables for major releases that you may use at your own risk.

Portable executables are available on `GitHub <https://github.com/andikisare/imgmarker/releases/latest>`_. Versions are available for Windows 11 and M1+ Mac.


Building from Source
---------------------
To build Image Marker yourself, first ``pyinstaller`` in your desired Python environment::

    pip install pyinstaller

Then, clone the `GitHub repository <https://github.com/andikisare/imgmarker/releases/latest>`_::

    git clone https://github.com/andikisare/imgmarker.git

or::

    git clone git@github.com:andikisare/imgmarker.git

Then navigate to the pyinstaller folder in the main source code directory::

    cd imgmarker/pyinstaller

Lastly, run the ``.spec`` file corresponding to your operating system.
    * For Mac:: 

        pyinstaller mac.spec

    * For Windows:: 

        pyinstaller win.spec

This should create an executable file specific to your operating system and CPU architecture (your compiled version will not work on M1+ Mac if you compile on Intel Mac, and vice versa). See the `pyinstaller documentation <https://pyinstaller.org/en/stable/index.html>`_ for instructions on how to customize the build settings.
