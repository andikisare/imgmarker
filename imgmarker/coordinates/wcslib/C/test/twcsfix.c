/*============================================================================
  WCSLIB 8.4 - an implementation of the FITS WCS standard.
  Copyright (C) 1995-2024, Mark Calabretta

  This file is part of WCSLIB.

  WCSLIB is free software: you can redistribute it and/or modify it under the
  terms of the GNU Lesser General Public License as published by the Free
  Software Foundation, either version 3 of the License, or (at your option)
  any later version.

  WCSLIB is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
  FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for
  more details.

  You should have received a copy of the GNU Lesser General Public License
  along with WCSLIB.  If not, see http://www.gnu.org/licenses.

  Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
  http://www.atnf.csiro.au/people/Mark.Calabretta
  $Id: twcsfix.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=============================================================================
*
* twcsfix tests the translation routines for non-standard WCS keyvalues, the
* wcsfix() suite.  It also tests the change of celestial coordinate system
* routine, wcsccs(), and the spectral coordinate translation routine,
* wcssptr().
*
*---------------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <wcs.h>
#include <wcserr.h>
#include <wcsfix.h>
#include <wcsprintf.h>
#include <wcsunits.h>
#include <wcsutil.h>


void parser(struct wcsprm *);

const int NAXIS = 3;
const double CRPIX[3] =  {90.0, 90.0, 1.0};
const double PC[3][3] = {{ 1.0,  0.0, 0.0},
                         { 0.0,  1.0, 0.0},
                         { 0.0,  0.0, 1.0}};
const double CDELT[3] =  {-1.0, 1.0, 19.68717093222};

char CUNIT[3][9] = {"ARCSEC", "ARCSEC", "KM/SEC"};

// N.B. non-standard spectral axis.
char CTYPE[3][9] = {"RA---NCP", "DEC--NCP", "FELO-HEL"};

// B1950.0 equatorial coordinates of the galactic pole.
// CUNITia is set to ARCSEC as an additional test.
const double CRVAL[3] = {192.2500*3600.0, 27.4000*3600.0, 5569.27104};
const double RESTFRQ = 1.42040575e9;
const double RESTWAV = 0.0;

// N.B. non-standard date-time format.
const char DATEOBS[] = "1957/02/15 01:10:00";
const char DATEBEG[] = "1957/02/15 01:10:00";
const char DATEAVG[] = "1957/02/15 02:10:00";
const char DATEEND[] = "1957/02/15 03:10:00";

const double BEPOCH  = 1957.124382563;
const double MJDBEG  = 35884.048611;

const double OBSGEO_L =   148.263510;
const double OBSGEO_B =   -32.998406;
const double OBSGEO_H =      411.793;

const double EQUINOX = 1950.0;

// For testing spcfix().
const int  VELREF = 2;
const char SPECSYS[] = "BARYCENT";

int main()

{
  int stat[NWCSFIX];

  wcsprintf("Testing WCSLIB translator for non-standard usage (twcsfix.c)\n"
          "------------------------------------------------------------\n\n");

  struct wcsprm wcs0;
  wcs0.flag = -1;
  parser(&wcs0);

  // Note: to print the unfixed wcsprm struct using wcsprt() the struct
  // would first have to be initialized by wcsset().  However, if the struct
  // contains non-standard keyvalues then wcsset() will either fix them
  // itself or else fail (e.g. for non-standard units).  Thus, in general,
  // wcsprt() cannot be used to print the unmodified struct.

  // Fix non-standard WCS keyvalues.
  struct wcserr info[NWCSFIX];
  wcserr_enable(1);
  int status = wcsfixi(7, 0, &wcs0, stat, info);
  wcsprintf("wcsfix status returns: (");
  for (int i = 0; i < NWCSFIX; i++) {
    wcsprintf(i ? ", %d" : "%d", stat[i]);
  }
  wcsprintf(")\n");

  for (int i = 0; i < NWCSFIX; i++) {
    if (info[i].status < -1 || 0 < info[i].status) {
      wcsprintf("\n");
      wcserr_prt(info+i, 0x0);

      // Free memory used to store the message.
      if (info[i].msg) wcsdealloc(info[i].msg);
    }
  }

  if (status) {
    wcsprintf("\nwcsfix error %d", status);
    return 1;
  }

  // Extract information from the FITS header.
  if (wcsset(&wcs0)) {
    wcsprintf("\n");
    wcsperr(&wcs0, 0x0);
    return 1;
  }

  // Tidy up the struct and print it.
  wcstrim(&wcs0);
  wcsprintf("\n");
  wcsprt(&wcs0);
  wcsprintf("\n------------------------------------"
            "------------------------------------\n");

  // Make a copy of the wcsprm struct.
  struct wcsprm wcs1;
  wcs1.flag = -1;
  if (wcssub(1, &wcs0, 0x0, 0x0, &wcs1)) {
    wcsperr(&wcs1, 0x0);
    return 1;
  }

  // Transform equatorial B1950 to galactic coordinates.  The WCS has been
  // constructed with the galactic pole coincident with the native pole of
  // the projection in order to test the resolution of an indeterminacy.
  if (wcsccs(&wcs1, 123.0, 27.4, 192.25, "GLON", "GLAT", 0x0, 0.0, "G")) {
    wcsperr(&wcs1, 0x0);
    return 1;
  }

  // Should now have a 'VOPT-F2W' axis, translate it to frequency.
  char ctypeS[9];
  strcpy(ctypeS, "FREQ-???");
  int i = -1;
  if (wcssptr(&wcs1, &i, ctypeS)) {
    wcsperr(&wcs1, 0x0);
    return 1;
  }

  if (wcsset(&wcs1)) {
    wcsperr(&wcs1, 0x0);
    return 1;
  }

  // Tidy up the struct and print it.
  wcstrim(&wcs1);
  wcsprt(&wcs1);

  // Print before-and-afters.
  printf("\nOriginal and new coordinates of reference point "
         "(%4.1f, %4.1f, %3.1f), lonpole, and latpole:\n",
	 CRPIX[0], CRPIX[1], CRPIX[2]);
  printf("%14.6f, %14.6f, %14.2f, %14.6f, %14.6f\n",
    wcs0.crval[0], wcs0.crval[1], wcs0.crval[2], wcs0.lonpole, wcs0.latpole);
  printf("%14.6f, %14.6f, %14.2f, %14.6f, %14.6f\n",
    wcs1.crval[0], wcs1.crval[1], wcs1.crval[2], wcs1.lonpole, wcs1.latpole);

  // Compute B1950 coordinates of a field point.
  double pixcrd[3] = {1000.0, 1000.0, 1.0};
  printf("\nOriginal and new coordinates of field point "
         "(%5.1f, %5.1f, %3.1f):\n", pixcrd[0], pixcrd[1], pixcrd[2]);

  double imgcrd[3], phi, theta, world[3];
  if (wcsp2s(&wcs0, 1, 3, pixcrd, imgcrd, &phi, &theta, world, stat)) {
    wcsperr(&wcs0, 0x0);
    return 1;
  }

  printf("%14.6f, %14.6f, %14.2f\n", world[0], world[1], world[2]);

  // Compute galactic coordinates of the same field point.
  if (wcsp2s(&wcs1, 1, 3, pixcrd, imgcrd, &phi, &theta, world, stat)) {
    wcsperr(&wcs1, 0x0);
    return 1;
  }

  printf("%14.6f, %14.6f, %14.2f\n", world[0], world[1], world[2]);

  wcsfree(&wcs0);
  wcsfree(&wcs1);

  return 0;
}

//----------------------------------------------------------------------------

void parser(wcs)

struct wcsprm *wcs;

{
  int i, j;
  double *pcij;

  // In practice a parser would read the FITS header until it encountered
  // the NAXIS keyword which must occur near the start, before any of the
  // WCS keywords.  It would then use wcsini() to allocate memory for
  // arrays in the wcsprm struct and set default values.  In this
  // simulation the header keyvalues are set as global variables.
  wcsnpv(2);
  wcsini(1, NAXIS, wcs);


  // Now the parser scans the FITS header, identifying WCS keywords and
  // loading their values into the appropriate elements of the wcsprm
  // struct.

  for (j = 0; j < NAXIS; j++) {
    wcs->crpix[j] = CRPIX[j];
  }

  pcij = wcs->pc;
  for (i = 0; i < NAXIS; i++) {
    for (j = 0; j < NAXIS; j++) {
      *(pcij++) = PC[i][j];
    }
  }

  for (i = 0; i < NAXIS; i++) {
    wcs->cdelt[i] = CDELT[i];
  }

  for (i = 0; i < NAXIS; i++) {
    strcpy(wcs->cunit[i], &CUNIT[i][0]);
  }

  for (i = 0; i < NAXIS; i++) {
    strcpy(wcs->ctype[i], &CTYPE[i][0]);
  }

  for (i = 0; i < NAXIS; i++) {
    wcs->crval[i] = CRVAL[i];
  }

  wcs->restfrq = RESTFRQ;
  wcs->restwav = RESTWAV;

  wcs->pv[0].i = -1;
  wcs->pv[0].m = -1;
  wcs->pv[0].value = -1.0;
  wcs->npv = 1;

  wcs->velref = VELREF;

  // dateobs and datebeg will be set by datfix().
  strcpy(wcs->dateavg, DATEAVG);
  strcpy(wcs->dateend, DATEEND);
  wcs->bepoch = BEPOCH;
  wcs->mjdbeg = MJDBEG;

  wcs->obsgeo[3] = OBSGEO_L;
  wcs->obsgeo[4] = OBSGEO_B;
  wcs->obsgeo[5] = OBSGEO_H;

  wcs->equinox = EQUINOX;

  strcpy(wcs->specsys, SPECSYS);

  return;
}
