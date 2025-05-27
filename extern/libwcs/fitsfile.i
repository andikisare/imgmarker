%feature("autodoc", "1");

%module(package="imgmarker.libwcs") fitsfile

%{
#include "fitsfile.h"
%}

%apply int *OUTPUT {int *lhead, int *nbhead};
char *fitsrhead(	/* Read a FITS header */
	char *filename,	/* Name of FITS image file */
	int *lhead,	/* Allocated length of FITS header in bytes (returned) */
	int *nbhead);	/* Number of bytes before start of data (returned) */