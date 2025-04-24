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
date: 02 April 2025
bibliography: paper.bib

# Optional fields if submitting to a AAS journal too, see this blog post:
# https://blog.joss.theoj.org/2018/12/a-new-collaboration-with-aas-publishing
# aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
# aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

A wide range of scientific imaging datasets benefit from human inspection for purposes ranging from prosaic---such as fault identification and quality inspection---to profound, enabling the discovery of new phenomena. As such, these datasets come in a wide variety of forms, with diverse inspection needs. In this paper we present a software package, `Image Marker`, designed to help facilitate human categorization of images. The software allows for quick seeking through images and enables flexible marking and logging of up to 9 different classes of features and their locations in files of FITS, PNG, TIFF, and JPEG format. Additional tools are provided to add text-based comments to the marking logs and for displaying external *mark* datasets on images during the classification process. As our primary use case will be the identification of features in astronomical survey data, `Image Marker` will also utilize standard World Coordinate Systems (WCS) headers embedded in FITS headers and TIFF metadata when available.  The lightweight software, based on the Qt Framework to build the GUI application, enables efficient marking of thousands of images on personal-scale computers.  We provide `Image Marker` as a Python package, and as Mac and Windows 11 executables. It is available [on GitHub](https://github.com/andikisare/imgmarker/) or via pip installation. 

# Statement of need

The rapid advancement in detector technology across all fields of science has led to larger and larger datasets without an equal increase in the number of scientists available to analyze the data. This imbalance of available work to available workers has led to a need for developing more efficient methods of parsing data. In response to large datasets in astronomy, projects like DES Exposure Checker [@DES_Exposure_Checker], and Space Warps [@Space_Warps] and Galaxy Zoo [@Galaxy_Zoo] using the Zooniverse framework [@Zooniverse] emerged to crowdsource classification and identification tasks in large datasets. Zooniverse offers the ability to easily outsource image identification and advanced classification statistics through the power of citizen science. This level of sophistication is not required, however, for projects which may involve fewer collaborators or for low-level data or algorithmic phases that are not suitable for a broader audience. Zooniverse also requires an internet connection. FitsMap [@FitsMap] takes a different approach with a focus on large images and their associated catalogs by hosting a web client on the user's local machine and displaying a reduced-scale image with catalog objects overlaid. While FitsMap has broad functionality, it does not contain a method for scanning many images quickly, saving feature coordinates, or methods for crowdsourcing efforts.  Other software for viewing and analyzing data, like the widely-used SAO-DS9 [@SAO_DS9], handle smaller datasets best.

![Diagram of `Image Marker` windows highlighting main features of the application: (a) main window; nine different group marks are available for tagging features. Below the image users can read the pixel coordinates (and, if available, WCS coordinates) of the cursor. Note that a comment has been written in the main comment box in the center. (b) controls window; updates group and category names when they are customized, helping keep track of what buttons are for which group or category. Other shortcuts are shown as well. (c) Gaussian blur window; note that blur has not been applied to the example image in (a). (d) frames window; for selecting frames in multi-extension images/FITS files. (e) about window; displays basic information about the user's installation of `Image Marker`. (f) color picker window; used to select the color of an imported *catalog* of *marks*. Window themes are dependent on the user's operating system.\label{fig:figure1}](Figure1.pdf)

`Image Marker` is a tool specifically designed for quickly scanning images and tagging locations in the images or the images themselves. It is run locally, has a user-friendly interface, a fail-safe saving mechanism, and also includes a suite of features and options for customization, image manipulation, and testing user consistency (see Figure \ref{fig:figure1} for application interface). By sharing an `Image Marker` configuration file and data with other users, `Image Marker` also allows joint analyses of datasets at the expense of requiring manual sharing of files after marking is completed. This, however, enables trained observers to quickly scan through images with loading times not limited by internet connections and thus faster identifications or classifications.

## Our use case

The SPT-3G camera has surveyed ~10,000 square degrees of the Southern sky [@Sobrin22; @Prabhu24] at millimeter-wavelengths. Two objectives of these observations are to identify a sample of galaxy clusters through the Sunyaev-Zel'dovich (SZ) effect [@SZ1972] and to use this sample to constrain cosmology [@Chaubal22; @Raghunathan22]. 
As part of this process, one must select the centers of the galaxy clusters in order to enable connection of cluster observables to theoretical models (using e.g., weak gravitational lensing, see reviews in @Allen11; @Umetsu20). The most commonly adopted choice for such centers are cluster galaxies known as "brightest cluster galaxies" (BCGs). Automatic BCG selection algorithms typically fail 10-20% of the time, however, and human inspection plays an important role in both validating these algorithms and improving centering choices when they fail [@Rozo14; @Ding-miscentering; @Kelly-miscentering]. Our first use case for `Image Marker` is the identification of BCGs in the SPT-3G cluster sample (see Figure \ref{fig:figure2}) using optical image data from DeCALS [@Dey19]. This human-generated BCG dataset will be analyzed and compared to results from algorithms such as redMaPPer [@Rykoff14] and MCMF [@Klein19] that will also be run on the sample. The validated BCG dataset from thousands of clusters ( $>5,000$ galaxy clusters expected in the SPT-3G main survey alone, @Benson14) also offers the opportunity to develop and test machine learning BCG identification tools that can be applied not only to the SPT-3G sample but also cluster samples from other surveys (e.g., @Hilton21; @Bulbul24; @LSST). We are currently testing the use of convolutional neural networks (CNN; @ImageNet_Classification_Deep_CNNs) and vision transformers (ViT; @ViTs) for this task.


![Optical *grz* band image of a galaxy cluster from the SPT-3G survey (Optical images from DeCALS [@Dey19]). (a, Left) We display the first frame of the image file with just optical image data. (b, Right) The second frame of the image file, which contains the optical image data with contours overlaid indicating the SZ detection signal-to-noise from SPT-3G. The human-selected candidate BCG is denoted by the red mark in both images. \label{fig:figure2}](Figure2.pdf)

### *Broader use cases*

While `Image Marker` was initially designed with the above use cases in mind, we have found it valuable as a general tool for inspecting data products and validating algorithmic development. As a second example usage, the ability to rapidly scan hundreds of small thumbnail cutouts in a matter of minutes, mark problematic locations, and easily read in lists of these locations, helped us to improve data cleaning for an upcoming analysis of SPT-3G data in the Euclid Deep Field South region.  This broad applicability motivated us to publicly release the software.


# Functionality

## Loading Images

Currently supported image formats are FITS, TIFF, PNG, and JPEG. PyQt has limitations on bit depth. For RGB(A) images, up to 8 bits per channel is supported. For grayscale images, up to 16 bits is supported. Images that exceed these limitations will have their bit depth lowered.

`Image Marker` can handle multi-frame FITS and TIFF files (Figure \ref{fig:figure2}). World Coordinate System (WCS) information stored in FITS and TIFF files is also accessed by `Image Marker`. If an image contains a WCS solution in its header, `Image Marker` will display the WCS coordinates of the cursor in addition to the pixel coordinates below the image. WCS solutions can be embedded in TIFFs using e.g., STIFF [@STIFF].

## Marking Images

Marks can be placed in any of 9 *groups*. The user can place a *mark* by pressing any number between 1 and 9. Pressing each number will place a *mark* at the location of the cursor and in the corresponding *group*. The names of each *group* can be modified in **Edit &rarr; Settings.** The label of a *mark* can be edited by clicking on the text next to the *mark* and entering the desired text. This does not change the *group* the *mark* is in. Once a *mark* is placed, its pixel coordinates, WCS coordinates (if applicable), *group*, label, the name of the image where the *mark* was placed, and the current date are all saved into `<username>_marks.txt`, where `<username>` is the username of the user’s profile on their computer. Figure \ref{fig:figure1}a shows an example of an image with several marks placed.

*Marks* can also be loaded into `Image Marker` in the format of a CSV file, called *catalogs*. Example files can be found on the [GitHub](https://github.com/andikisare/imgmarker/tree/main/examples/catalogs).

## Categorizing and Commenting on Images

Images can be placed in any of 5 *categories*. These *categories* are listed as check boxes on the bottom panel of `Image Marker`. In the bottom panel, comments can be entered for the current image. This information is saved in the save directory in a file named `<username>_images.txt`. The user can also click the heart button on the far right of the bottom panel or press 'F', which will add the image to the user's Favorites. A list of Favorite images is saved in `<username>_favorites.txt`.

## Filters

`Image Marker` includes some basic image manipulation. In **Filter &rarr; Stretch**, the user can set the brightness scaling, the two options being **Linear** (default) and **Log**. In **Filter &rarr; Interval**, the user can set the interval of brightness values that are displayed. The two options are **Min-Max** (default) and **ZScale**. **In Filter &rarr; Gaussian Blur**, the user can blur the image using a slider.

## Settings

Settings can be edited through **Edit &rarr; Settings**. In the settings window, there are several customizations the user can make. Most importantly, the user can define the names of the *groups*, the names of the image *categories*, and the maximum *marks* per *group*. The user can also set whether to randomize the order of images, and whether the mouse cursor will move to the center of the image display window when the user pans to a point using the middle mouse button.

# Acknowledgements

We thank Keren Sharon, Mike Gladders, and Giulia Campitiello for helpful suggestions on features to include in `Image Marker`, Will Hicks for help compiling `Image Marker` on an Intel based Mac, and Florian Keruzore for providing helpful comments.
This work was supported in part by the U.S. Department of Energy, Office of Science, Office of Workforce Development for Teachers and Scientists (WDTS) under the Science Undergraduate Laboratory Internships (SULI) program. Work at Argonne National Lab is supported by UChicago Argonne LLC, Operator of Argonne National Laboratory (Argonne). Argonne, a U.S. Department of Energy Office of Science Laboratory, is operated under contract no. DE-AC02-06CH11357.
We thank the SPT-3G collaboration for the use of the Sunyaev Zel'dovich detection contours displayed on the image in Figure \ref{fig:figure2}.
This work made use of Astropy[^1]: a community-developed core Python package and an ecosystem of tools and resources for astronomy [@astropy13; @astropy18; @astropy22]; Pillow [@clark15]; SciPy [@Virtanen20]; NumPy [@Harris20]; and PyQt [@PyQt].

[^1]: [http://www.astropy.org](http://www.astropy.org)

# References




<!-- The South Pole Telescope (SPT) is a 10 meter telescope designed for observing the sky at  millimeter- and submillimeter-wavelengths with arcminute resolution. It has a specific focus on fluctuations in the cosmic microwave background [@SPT]. -->


<!-- Clusters identified through the SZ effect often demonstrate miscentering: an offset between the Brightest Cluster Galaxy (BCG) and the center of the gravitational well of the cluster. This miscentering can be due to astrophysical effects, most notably mergers, which keep the cluster out of equilibrium, or systematic effects in cluster identification algorithms [@Ding-miscentering; @Kelly-miscentering]. Hydrodynamical simulations can be used to study and predict astrophysical miscentering [@Seppi_etal; @Yan_etal; @Cozio_etal]. Visual identification of BCGs is therefore a method of evaluating cluster identification algorithms [@Kelly-miscentering] as well as hydrodynamical simulations of galaxy clusters. By using `Image Marker` to identify BCGs in an ensemble of galaxy clusters from SPT, a human truth table of offsets will be analyzed and compared to results from algorithms. -->

<!-- stuff on cluster cosmology multi-wavelength efforts, not exactly sure what the notes lindsey left are saying to do, if anything -->

<!--The production of a well curated BCG dataset of thousands of clusters also offers the opportunity to develop and test machine learning BCG identification tools that can be applied not only to the full SPT survey dataset but also cluster samples from other surveys such as from the Atacama Cosmology Telescope [@Hilton21], eROSITA [@Bulbul24], or, in the future, the Rubin Observatory's Legacy Survey of Space and Time (LSST; @LSST). Machine learning has been deployed virtually everywhere in modern science for classification and identification tasks [@ImageNet_Classification_Deep_CNNs; @OverFeat_CNNs; @Deep_CNN_Analysis; @Lensing_CNNs] and has proven to be of great value for large datasets. Perhaps the greatest challenge in training a machine learning model, like a convolutional neural network (CNN; @ImageNet_Classification_Deep_CNNs) or vision transformer (ViT; @ViTs), is curating the training, validation, and test datasets. Machine learning models require large datasets to train on, especially ViTs, and the larger the training dataset, the more accurate a model can be. However, curating a large image dataset, with specific features for a machine learning model to learn, takes a lot of time and effort. We are currently exploring the use of machine learning to identify BCGs in SPT-3G clusters. -->

<!-- We will use `Image Marker` to help curate these training sets by creating a human truth table for BCGs in galaxy clusters, which we will train a machine learning model to identify. -->
