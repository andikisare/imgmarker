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

A wide range of scientific imaging datasets benefit from human inspection for purposes ranging from prosaic---such as fault identification and quality inspection---to profound, enabling the discovery of new phenomena. As such, these datasets come in a wide variety of forms, with diverse inspection needs. In this paper we present a software package `Image Marker` designed to help facilitate human categorization of images. The software enables flexible marking and logging of up to 9 different classes of features and their locations in files of FITS, PNG, TIFF, and JPEG format. Additional tools are provided to add text-based comments to the marking logs and for displaying external *mark* datasets on images during the classification process. As our primary use case will be the identification of features in astronomical survey data, `Image Marker` will also utilize standard World Coordinate Systems (WCS) headers embedded in FITS headers and TIFF metadata when available.  The lightweight software, based on the Qt Framework to build the GUI application, enables efficient marking of thousands of images on personal-scale computers.  We provide `Image Marker` as a Python package, and as Mac and Windows executables. It is available [on Github](https://github.com/andikisare/imgmarker/) or via pip installation. 

# Statement of need

The rapid advancement in detector technology across all fields of science has led to larger and larger datasets without an equal increase in the number of scientists available to analyze the data. This imbalance of available work to available workers has led to a need for developing more efficient methods of parsing data. In astronomy, SAO-DS9 [@SAO_DS9] is widely used for viewing and analyzing data, but handles smaller datasets best. In response to large datasets, projects like DES Exposure Checker [@DES_Exposure_Checker], and Space Warps [@Space_Warps] and Galaxy Zoo [@Galaxy_Zoo] using the Zooniverse framework [@Zooniverse] emerged to crowdsource classification and identification tasks in large datasets. Zooniverse offers the ability to easily outsource image identification and advanced classification statistics through the power of citizen science. This level of sophistication is not required, however, for projects which may involve fewer collaborators or for low-level data or algorithmic phases that are not suitable for a broader audience. Zooniverse also requires an internet connection. FitsMap [@FitsMap] takes a different approach with a focus on large images and their associated catalogs by hosting a web client on the user's local machine and displaying a reduced-scale image with catalog objects overlaid. While FitsMap has broad functionality, it does not contain a method for scanning many images quickly, saving feature coordinates, or methods for crowdsourcing efforts. 

![Diagram of all `Image Marker` windows: (a) main window; The 9 different group marks available and visible on the image of the cat. We have changed some of the labels on the marks to demonstrate customized labels, which are mark-specific comments and do not change the group that the mark is in. Users can read off from below the image display the pixel coordinates, and WCS coordinates if available, of the cursor. Note that the image has a comment in the main comment box in the center and has been favorited, as evidenced by the checked and filled-in heart at the bottom right of the main window. (b) controls window (c) Gaussian blur window; Note that blur has not been applied to the example image in (a). (d) window for selecting frames (e) window displaying basic information about the user's installation of `Image Marker` (f) color picker window, used to select the color of an imported *catalog* of *marks*. Window themes are dependent on the user's operating system.\label{fig:figure1}](Figure1.pdf)

`Image Marker` is a tool specifically designed for quickly scanning images and tagging locations in the images or the images themselves. It is run locally, has a user-friendly interface, a fail-safe saving mechanism, and also includes a suite of features and options for customization, image manipulation, and testing user consistency (see \ref{fig:figure1}). By sharing an `Image Marker` configuration file and data with other users, `Image Marker` also allows joint analyses of datasets at the expense of requiring manual sharing of files after marking is completed. This, however, enables trained observers to quickly scan through images with loading times not limited by internet connections and thus faster identifications or classifications. 

## Our use case

The SPT-3G camera has surveyed ~10,000 square degrees of the Southern sky [@Sobrin22; @Prabhu24] at millimeter-wavelengths. Two important objectives of these observations are to identify a sample of galaxy clusters through the Sunyaev-Zel'dovich (SZ) effect [@SZ1972] and to use this sample to constrain cosmology [@Chaubal22; @Raghunathan22]. 
As part of this process, one must select the centers of the galaxy clusters in order to enable calibration of cluster observables to theoretical models (using e.g., weak gravitational lensing, see reviews in @Allen11; @Umetsu20). The most commonly adopted choice for such centers are cluster galaxies known as "brightest cluster galaxies" (BCGs). Automatic BCG selection algorithms typically fail 15-20% of the time, however, and human inspection plays an important role in both validating these algorithms and improving centering choices when they fail [@Rozo14; @Ding-miscentering; @Kelly-miscentering]. Our first use case for `Image Marker` is the identification of BCGs in the SPT-3G cluster sample (see \ref{fig:figure2}). This human-generated BCG dataset will be analyzed and compared to results from algorithms such as redMaPPer [@Rykoff14] and MCMF [@Klein19] that will also be run on the sample. The validated BCG dataset of thousands of clusters ( $>5,000$ galaxy clusters expected in the SPT-3G main survey, @Benson14]) also offers the opportunity to develop and test machine learning BCG identification tools that can be applied not only to the SPT-3G sample but also cluster samples from other surveys (e.g., @Hilton21; @Bulbul24; @LSST). We are currently testing the use of convolutional neural networks (CNN; @ImageNet_Classification_Deep_CNNs) and vision transformers (ViT; @ViTs) for this task.


![Optical *grz* band image of a galaxy cluster from the SPT-3G survey. (a, Left) We display the first frame of the image file with just optical image data. (b, Right) The second frame of the image file, which contains the optical image data with contours overlaid indicating the SZ detection signal-to-noise from SPT-3G. Optical images from DeCALS [@Dey19]. \label{fig:figure2}](Figure2.pdf)

### *Broader use cases*

While `Image Marker` was initially designed with the above use cases in mind, we have found it valuable as a general tool for inspecting data products and validating algorithmic development. This broad applicability motivated us to publicly release the software. As a second example usage, the ability to rapidly scan hundreds of small thumbnail cutouts in a matter of minutes, mark problematic locations, and easily read in lists of these locations, helped us to improve data cleaning for an upcoming analysis of SPT-3G data in the Euclid Deep Field South region. 

<!-- -
##Add example output marks file picture to show what saved data looks like

add citations to Pillow, astropy, scipy, numpy, etc
- -->

# Functionality


## Loading Images

Currently supported image formats are FITS, TIFF, PNG, and JPEG. PyQt has limitations on bit depth. For RGB(A) images, up to 8 bits per channel is supported. For grayscale images, up to 16 bits is supported. Images that exceed these limitations will have their bit depth lowered.

`Image Marker` can handle multi-frame FITS and TIFF files. World Coordinate System (WCS) information stored in FITS and TIFF files is also accessed by `Image Marker`. If an image contains a WCS solution in its header, `Image Marker` will display the WCS coordinates of the cursor in addition to the pixel coordinates. WCS solutions can be embedded in TIFFs using STIFF [@STIFF].

## Marking Images

Marks can be placed in any of 9 *groups*. The user can place a *mark* by pressing any number between 1 and 9. Pressing each number will place a *mark* at the location of the cursor and in the corresponding *group*. The names of each *group* can be modified in **Edit &rarr; Settings.** The label of a *mark* can be edited by clicking on the text next to the *mark* and entering the desired text. This does not change the *group* the *mark* is in. Once a *mark* is placed, its pixel coordinates, WCS coordinates (if applicable), *group*, label, the name of the image where the *mark* was placed, and the current date are all saved into `<username>_marks.txt`, where `<username>` is the username of the user’s profile on their computer. Figure \ref{fig:figure1}a shows an example of what an image may look like after placing several marks.

*Marks* can also be loaded into `Image Marker` in the format of a CSV file, called *catalogs*. Example files can be found on the [Github](https://github.com/andikisare/imgmarker/tree/main/examples/catalogs).

## Categorizing and Commenting on Images

Images can be placed in any of 5 *categories*. These *categories* are listed as check boxes on the bottom panel of `Image Marker`; clicking these check boxes or using the associated keyboard shortcuts will place the image in that *category*. In the bottom panel, comments can be entered for the current image. This information is saved in the save directory in a file named `<username>_images.txt`. The user can also click the heart button on the far right of the bottom panel or press 'F', which will add the image to the user's Favorites. A list of Favorite images is saved in `<username>_favorites.txt`.

## Filters

`Image Marker` includes some basic image manipulation. In **Filter &rarr; Stretch**, the user can set the brightness scaling, the two options being **Linear** (default) and **Log**. In **Filter &rarr; Interval**, the user can set the interval of brightness values that are displayed. The two options are **Min-Max** (default) and **ZScale**. **In Filter &rarr; Gaussian Blur**, the user can blur the image using a slider.

## Settings

Settings can be edited through **Edit &rarr; Settings**. In the settings window, there are several customizations the user can make. Most importantly, the user can define the names of the *groups*, the names of the image *categories*, and the maximum *marks* per *group*. The user can also set whether to randomize the order of images, and whether the mouse cursor will move to the center of the image display window when the user pans to a point using the middle mouse button.

# Acknowledgements

We thank Keren Sharon, Mike Gladders, and Giulia Campitiello for helpful suggestions on features to include in `Image Marker`, and Will Hicks for help compiling `Image Marker` on an Intel based Mac.
This work was supported in part by the U.S. Department of Energy, Office of Science, Office of Workforce Development for Teachers and Scientists (WDTS) under the Science Undergraduate Laboratory Internships (SULI) program. Work at Argonne National Lab is supported by UChicago Argonne LLC, Operator of Argonne National Laboratory (Argonne). Argonne, a U.S. Department of Energy Office of Science Laboratory, is operated under contract no. DE-AC02-06CH11357.
We thank the SPT-3G collaboration for the use of the Sunyaev Zel'dovich detection contours displayed on the image in Figure \ref{fig:figure2}. 

# References


