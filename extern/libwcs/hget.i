%feature("autodoc", "1");

%module(package="imgmarker.libwcs") hget

%{
/* Includes the header in the wrapper code */
#include "fitshead.h"
%}

char* ksearch(		/* Return pointer to keyword in FITS header */
  const char* hstring,	/* FITS header string */
  const char* keyword);	/* FITS keyword */