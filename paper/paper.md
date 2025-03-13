---
title: 'Image Marker'
tags:
  - Python
  - PyQt
  - Qt
  - astropy
authors:
  - name: Ryan Walker
    orcid: 0000-0001-5424-3698
    equal-contrib: true
    affiliation: 1 # (Multiple affiliations must be quoted)
  - name: Andi Kisare
    orcid: 0009-0006-7664-877X
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 1
  - name: Lindsey Bleem
    orcid: 0000-0001-7665-5079
    equal-contrib: true
    affiliation: 1
affiliations:
 - name: Argonne National Laboratory, United States
   index: 1
date: 06 February 2025
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
# aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
# aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

A rich diversity of scientific imaging datasets benefit from human inspection for purposes ranging from prosaic---such as fault identification and quality inspection---to profound, enabling the discovery of new phenomena. As such, imaging datasets come in a wide variety of forms, with diverse inspection needs. In this paper we present a software package `Image Marker` designed to help facilitate human categorization of images. The software enables flexible marking and logging of up to 9 different classes of features in files of FITS, PNG, TIFF, and JPEG format. Additional tools are provided to add text-based comments to the marking logs and for displaying external *mark* datasets on images during the classification process. As our primary use case will be the identification of features in astronomical survey data, `Image Marker` will also utilize standard World Coordinate Systems (WCS) headers embedded in FITS headers and TIFF metadata when available.  The lightweight software, based on the Qt Framework to build the GUI application, enables efficient marking of thousands of images on personal-scale computers.  We provide `Image Marker` as a Python package, and as Mac, Windows, and Linux executables. It is available [on Github](https://github.com/andikisare/imgmarker/) or via pip installation. 

# Statement of need

<!-- set the stage of the current field in one paragraph and be less critical of tools in the field, and make second paragraph for what image marker is good for and say image marker is local and is meant for rapid vetting of various things, image marker is useful whenver you want to tag images for classification, get coordinates easily, save your progress and come back later, prevent using too much memory by opening all images at once, and mention that most (almost all) GUI buttons on the main window are also keyboard shortcuts to make it easier to use fast -->

The rapid advancement in detector technology across all fields of science has led to larger and larger datasets without an equal increase in scientists with time to parse all of the data. This imbalance of available work to available workers has led to a need for developing more efficient methods of parsing data. In astronomy, SAO-DS9 [@SAO_DS9] is widely used for viewing and analyzing data, but handles smaller datasets best. In response to large datasets, projects like DES Exposure Checker [@DES_Exposure_Checker], and Space Warps [@Space_Warps] and Galaxy Zoo [@Galaxy_Zoo] using the Zooniverse framework [@Zooniverse] emerged to crowdsource classification and identification tasks in large datasets. However, Zooniverse requires creating a project and uploading data, which then becomes public, requires an internet connection, and cannot be run on a local machine. FitsMap [@FitsMap] takes a different approach with a focus on large images containing large catalogs by hosting a web client on the user's local machine and displaying a reduced-scale image with catalog objects overlaid. While FitsMap has broad functionality, it does not contain a method for scanning many images quickly, saving feature coordinates, or methods for crowdsourcing efforts. 

We designed `Image Marker` specifically for quickly scanning an image, logging identifications, and seeking to the next available image with a user-friendly interface and a fail-safe saving mechanism while including a suite of features and options for customization, image manipulation, and testing user consistency. By sharing an `Image Marker` configuration file and data with other users, `Image Marker` achieves a similar result as the previously mentioned projects, but with data stored locally, therefore requiring the user to share their output files. This, however, enables quicker loading times and faster identifications or classifications. `Image Marker` is entirely local and is specially designed for tagging images for classification, tagging features in images for classification and saving their coordinates, ease of use, easily picking up where you left off, and resource optimization.

## Our use case

The South Pole Telescope (SPT) is a 10 meter telescope designed for observing microwaves, millimeter-waves, and submillimeter-waves with a specific focus on minute fluctuations in the Cosmic Microwave Background (CMB) [@SPT]. Using the SPT-3G camera aboard SPT, the 1500 degree survey has detected over 1000 galaxy clusters via the Sunyaev Zel'dovich (SZ) effect. Clusters identified through the SZ effect often demonstrate miscentering: an offset between the Brightest Cluster Galaxy (BCG) and the center of the gravitational well of the cluster. This miscentering can be due to astrophysical effects, most notably mergers, which keep the cluster out of equilibrium, or systematic effects in cluster identification algorithms [@Ding-miscentering; @Kelly-miscentering]. Hydrodynamical simulations can be used to study and predict astrophysical miscentering [@Seppi_etal; @Yan_etal; @Cozio_etal]. Visual identification of BCGs is therefore a method of evaluating cluster identification algorithms [@Kelly-miscentering] as well as hydrodynamical simulations of galaxy clusters. By using `Image Marker` to identify BCGs in an ensemble of galaxy clusters from SPT, a human truth table of offsets will be analyzed and compared to results from hydrodynamical simulations.

Machine learning has been deployed virtually everywhere in modern science for classification and identification tasks [@ImageNet_Classification_Deep_CNNs; @OverFeat_CNNs; @Deep_CNN_Analysis; @Lensing_CNNs] and has proven to be of great value for large datasets. Perhaps the greatest challenge in training a machine learning model, like a Convolutional Neural Network (CNN) or Vision Transformer (ViT), is curating the training, validation, and test datasets. Machine learning models require large datasets to train on, especially ViTs, and the larger the training dataset, the more accurate a model can be. However, curating a large image dataset, each with specific features for a machine learning model to learn, takes a lot of time and effort. We will use `Image Marker` to help curate these training sets by filtering out bad images, images without galaxy clusters, as well as simultaneously creating a human truth table for BCGs in galaxy clusters, which we will train a machine learning model to identify.


<!-- -
##Add example output marks file picture to show what saved data looks like



important for citizen science, ds9, galaxy zoo, des-image-checker, coollamps, xmm bcg, similar tools have been used for human identification (use these references)
start with these to get references from nasa ADS

one contrast is that some are browser based tools, ds9 is much more similar because it runs locally but is not set up for this sort of work

we've built something shareable because you can share config files for crowd sourcing human-identification with control over the experiment, which bypasses internet lag (run locally)

specific experiment: statements about SPT, gonna use this for galaxy cluster and bcg identification (cite spt papers),

can also add strong lensing-ML references?

can cite recent paper using ResNet18, cite ML papers like attention is all you need? or maybe just ResNet18 paper

4 paragraphs?

add a note to reference STIFF (astrometric software) because it's particularly useful for embedding the WCS metadata into the tif files
also point out that the SPT cluster image was partially made with STIFF and Pillow

add citations to Pillow, astropy, scipy, numpy, etc

DES exposure checker: https://ui.adsabs.harvard.edu/abs/2016A%26C....16...99M/abstract
pros: offers sign-in option, hosted on server so nothing has to be downloaded, masking option is kind of like having multiple frames, data immediately stored on stable server
cons: Very specific use case, can't go back, no zooming or panning (intentionally), only black and white, scaling options not labeled, hosted on server so speed is reliant on internet speed, large marks that are all one color

SpaceWarps: https://ui.adsabs.harvard.edu/abs/2016MNRAS.455.1171M/abstract
pros: offers sign-in option, Shows four images, three in color, at different scalings, hosted online so all data is stored immediately and nothing needs to be downloaded, can *mark* lenses, gives a short tutorial, shows lenses initially, can zoom, pan, and rotate each frame individually, can move *marks* around, project included randomization of simulated images and images known not to contain lenses
cons: specific use case, cant go back, cant change scaling, not a user-friendly UI for quickly moving between images

Galaxy Zoo: https://ui.adsabs.harvard.edu/abs/2012amld.book..213F/abstract
pros: offers sign-in option, includes tutorial, web-based so saves data immediately, multiple frames, provides tutorial
cons: specific use case, sometimes slow in loading buttons, cant zoom or pan, black and white only,

Zooniverse: https://dl.acm.org/doi/10.1145/2567948.2579215
pros: provides framework for making web-based citizen science projects like galaxy zoo and spacewarps, web-based so saves immediately, already used by tons of other projects and people, don't have to download data for a project
cons: you have to build a whole project if you just want to open and scan some images quickly, a project is still relying on internet speed,

- -->

# Functionality

![Diagram of all `Image Marker` windows: (a) main window (b) controls window (c) Gaussian blur window (d) window for selecting frames (e) window displaying basic information about the user's installation of `Image Marker` (f) color picker window, used to select the color of an imported catalog of *marks*.\label{fig:figure1}](Figure1.pdf)

![Diagram showing how the user can switch between frames in a multiframe image.\label{fig:figure2}](Figure2.pdf)

## Loading Images

When `Image Marker` is first opened, the user is prompted to select the directory in which all of their output data will be automatically saved and then prompted to select the directory from which to load images. The currently supported image formats are FITS, TIFF, PNG, and JPEG. A bit depth of up to 16 bits is supported, which is a limitation of PyQt. For TIFFs, PNGs and JPEGs, `Image Marker` currently only officially supports RGB color channels with 8 bits per channel, but this may be expanded in the future.

`Image Marker` can handle multiframeFITS and TIFF files. If a file has multiple Frames, these Frames can be cycled through using spacebar, or by using the **View &rarr; Frames** dialog. World Coordinate System (WCS) information stored in FITS and TIFF files is also accessed by `Image Marker`. If an image contains a WCS solution in its header, `Image Marker` will display the WCS coordinates of the cursor in addition to the pixel coordinates.

## Marking Images

Marks can be placed in any of 9 *groups*. The user can place a *mark* by pressing any number between 1 and 9. Pressing each number will place a *mark* at the location of the cursor and in the *groups* associated with that number. The names of each *groups* can be modified in **Edit &rarr; Settings.** Once a *mark* is placed, its pixel coordinates, WCS coordinates (if applicable), *groups*, label, the name of the image associated with the *mark* and the current date are all saved into `<username>_marks.txt`, where `<username>` is the username of the user’s profile on their computer. The *mark* label can be modified simply by clicking on the label of the *mark* and typing the new label. Pressing enter or clicking outside the label will save this information in the same text file.

Mark can also be loaded into `Image Marker` in the format of a CSV file or a CSV-formatted text file, called *catalogs*. Example files can be found in the readthedocs: https://imgmarker.readthedocs.io/en/latest/. Upon selecting a file to load as a catalog, the user is prompted to pick a color to use for the catalog. Different *catalogs* can be different colors, allowing the user to differentiate between loaded *catalogs*.

## Categorizing and Commenting on Images

The user can also categorize images and enter comments on the image. Images can be placed in any of 5 *categories*. These *categories* are listed as check boxes on the bottom panel of `Image Marker`; clicking these check boxes will place the image in that *category*. In the bottom panel, comments can be entered for the current image. This information is saved in the save directory in a file named `<username>_images.txt`. The user can also click the heart button on the far right of the bottom panel, which will add the image to the user's Favorites. A list of Favorite images is saved in `<username>_favorites.txt`.

## Filters

`Image Marker` includes some basic image manipulation. In **Filter &rarr; Stretch**, the user can set the brightness scaling, the two options being **Linear** (default) and **Log**. In **Filter &rarr; Interval**, the user can set the interval of brightness values that are displayed. The two options are **Min-Max** (default) and **ZScale**. **In Filter &rarr; Gaussian Blur**, the user can blur the image using a slider.

## Settings

Settings can be edited through **Edit &rarr; Settings**. In the settings window, there are several customizations the user can make. Most importantly, the user can define the names of the *groups*, the names of the image *categories*, and the maximum *marks* per *groups*. The user can also set whether to randomize the order of images, and whether the mouse cursor will move to the center of the image when the user focuses on a point using the middle mouse button.

# Acknowledgements

Thank you Keren Sharon, Mike Gladders, Giulia Campitiello and Will Hicks for their feature suggestions and assistance with debugging.
This work was supported in part by the U.S. Department of Energy, Office of Science, Office of Workforce Development for Teachers and Scientists (WDTS) under the Science Undergraduate Laboratory Internships (SULI) program. Work at Argonne National Lab is supported by UChicago Argonne LLC, Operator of Argonne National Laboratory (Argonne). Argonne, a U.S. Department of Energy Office of Science Laboratory, is operated under contract no. DE-AC02-06CH11357.
We thank the SPT-3G collaboration for the use of the Sunyaev Zel'dovich detection contours displayed on the image in Figure \ref{fig:figure2}. 

# References
