Filters
======================

Image Marker includes some basic image manipulation. In **Filter > Stretch**, the user can set the brightness scaling, the two options being **Linear** (default) and **Log**. In **Filter > Interval**, the user can set the interval of brightness values which are displayed. The two options are **Min-Max** (default) and **ZScale**. Computation of the stretch and interval is done with ``astropy``. In **Filter > Gaussian Blur**, the user can blur the image using a slider. The blurring computations are done using ``astropy`` and ``scipy``.