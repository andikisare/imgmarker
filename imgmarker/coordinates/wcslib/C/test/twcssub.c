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
  $Id: twcssub.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=============================================================================
*
* twcssub tests wcssub() which extracts the coordinate description for a
* subimage from a wcsprm struct.
*
*---------------------------------------------------------------------------*/

#include <stdio.h>
#include <string.h>

#include <tab.h>
#include <wcs.h>
#include <wcserr.h>


// In real life these would be encoded as FITS header keyrecords.
const int NAXIS = 4;
const double CRPIX[4] =  { 1025.0,  64.0,   1.0,   1.0};
const double PC[4][4] = {{    1.1,   0.0,   0.0,   0.0},
                         {    0.0,   1.0,   0.0,   0.0},
                         {    0.0,   0.0,   1.0,   0.1},
                         {    0.0,   0.0,   0.2,   1.0}};
const double CDELT[4] =  {-9.2e-6,  10.0,   1.0,  -1.0};
char CUNIT[4][16] = {"m", "s", "deg", "deg"};
char CTYPE[4][16] = {"WAVE-F2W",  "TIME", "XLAT-TAB",  "XLON-TAB"};

const double CRVAL[4] =  {0.214982042, -2e3, 135.0, 95.0};

char CNAME[4][16] = {"Wavelength", "Time", "Latitude", "Longitude"};

const int NPS = 6;
const int NPV = 6;

// Lookup table parameters.
const int M  = 2;
const int K1 = 7;
const int K2 = 3;
const int map[] = {3, 2};
const double crval[] = {CRVAL[2], CRVAL[3]};


int main()

{
  // Simulate FITS PSi_ma and PVi_ma keywords describing the table.
  struct pscard PS[NPS];
  PS[0].i = 3;				// Table latitude on axis 3.
  PS[0].m = 0;				// Parameter number 0.
  strcpy(PS[0].value, "WCSTAB");	// PS3_0 (EXTNAME).

  PS[1].i = 3;				// Table latitude on axis 3.
  PS[1].m = 1;				// Parameter number 1.
  strcpy(PS[1].value, "COORDS");	// PS3_1 (TTYPEn for coord array).

  PS[2].i = 3;				// Table latitude on axis 3.
  PS[2].m = 2;				// Parameter number 2.
  strcpy(PS[2].value, "LATIDX");	// PS3_2 (TTYPEn for index array).

  PS[3].i = 4;				// Table latitude on axis 4.
  PS[3].m = 0;				// Parameter number 0.
  strcpy(PS[3].value, "WCSTAB");	// PS4_0 (EXTNAME).

  PS[4].i = 4;				// Table latitude on axis 4.
  PS[4].m = 1;				// Parameter number 1.
  strcpy(PS[4].value, "COORDS");	// PS4_1 (TTYPEn for coord array).

  PS[5].i = 4;				// Table latitude on axis 4.
  PS[5].m = 2;				// Parameter number 2.
  strcpy(PS[5].value, "LNGIDX");	// PS4_2 (TTYPEn for index array).

  struct pvcard PV[NPV];
  PV[0].i = 3;				// Table latitude on axis 3.
  PV[0].m = 1;				// Parameter number 1.
  PV[0].value = 1;			// PV3_1 (EXTVER).

  PV[1].i = 3;				// Table latitude on axis 3.
  PV[1].m = 2;				// Parameter number 2.
  PV[1].value = 1;			// PV3_2 (EXTLEVEL).

  PV[2].i = 3;				// Table latitude on axis 3.
  PV[2].m = 3;				// Parameter number 3.
  PV[2].value = 2;			// PV3_3 (axis number in array).

  PV[3].i = 4;				// Table longitude on axis 4.
  PV[3].m = 1;				// Parameter number 1.
  PV[3].value = 1;			// PV4_1 (EXTVER).

  PV[4].i = 4;				// Table longitude on axis 4.
  PV[4].m = 2;				// Parameter number 2.
  PV[4].value = 1;			// PV4_2 (EXTLEVEL).

  PV[5].i = 4;				// Table longitude on axis 4.
  PV[5].m = 3;				// Parameter number 3.
  PV[5].value = 1;			// PV4_3 (axis number in array).


  // Set up the lookup table.
  int K[] = {K1, K2};
  struct tabprm tab;
  tab.flag = -1;

  int status;
  if ((status = tabini(1, M, K, &tab))) {
    printf("tabini ERROR %d: %s.\n", status, tab_errmsg[status]);
    return 1;
  }

  tab.M = M;
  for (int m = 0; m < tab.M; m++) {
    tab.K[m] = K[m];
    tab.map[m] = map[m];
    tab.crval[m] = crval[m];

    for (int k = 0; k < tab.K[m]; k++) {
      tab.index[m][k] = (double)k;
    }
  }

  // Set lookup table coordinate array to approximate Bonne's projection.
  double x[K1], y[K2];
  for (int i = 0; i < K1; i++) {
    x[i] = (double)(1 - i);
  }
  for (int j = 0; j < K2; j++) {
    y[j] = (double)(j - 1);
  }

  struct prjprm prj;
  prjini(&prj);
  prj.pv[1] = 35.0;

  int stat[K2*K1];
  status = bonx2s(&prj, K1, K2, 1, 2, x, y, tab.coord, tab.coord+1, stat);


  // Set up the wcsprm struct.
  struct wcsprm wcs;
  wcs.flag = -1;
  wcsini(1, NAXIS, &wcs);

  for (int j = 0; j < NAXIS; j++) {
    wcs.crpix[j] = CRPIX[j];
  }

  double *pcij = wcs.pc;
  for (int i = 0; i < NAXIS; i++) {
    for (int j = 0; j < NAXIS; j++) {
      *(pcij++) = PC[i][j];
    }
  }

  for (int i = 0; i < NAXIS; i++) {
    wcs.cdelt[i] = CDELT[i];
  }

  for (int i = 0; i < NAXIS; i++) {
    strcpy(wcs.cunit[i], &CUNIT[i][0]);
    strcpy(wcs.ctype[i], &CTYPE[i][0]);
    strcpy(wcs.cname[i], &CNAME[i][0]);
  }

  for (int i = 0; i < NAXIS; i++) {
    wcs.crval[i] = CRVAL[i];
  }

  wcs.npv = NPV;
  for (int i = 0; i < NPV; i++) {
    wcs.pv[i] = PV[i];
  }

  wcs.nps = NPS;
  for (int i = 0; i < NPS; i++) {
    wcs.ps[i] = PS[i];
  }

  wcs.ntab = 1;
  wcs.tab = &tab;


  // Initialize the wcsprm struct.
  wcserr_enable(1);
  (void) wcsset(&wcs);

  printf("Testing WCSLIB subimage extraction routine (twcssub.c)\n"
         "------------------------------------------------------\n");
  printf("\nInitial contents of wcsprm struct:\n");
  wcsprt(&wcs);


  // Extract the coordinate description for a subimage and add a new axis.
  // Note that the time axis is extracted only once, whereas the prescription
  // would have it extracted twice.  Consequently, the extracted coordinate
  // system should have four axes, not five.
  int axes[5], nsub = 5;
  struct wcsprm wcsext;
  wcsext.flag = -1;
  axes[0] = WCSSUB_LONGITUDE;
  axes[1] = WCSSUB_LATITUDE;
  axes[2] = WCSSUB_TIME;
  axes[3] = -(WCSSUB_SPECTRAL | WCSSUB_STOKES);
  axes[4] = 0;
  printf("\n------------------------------------"
         "------------------------------------\n"
         "Extracted contents of wcsprm struct:\n");
  if (wcssub(1, &wcs, &nsub, axes, &wcsext)) {
    wcsperr(&wcsext, "");
  } else if (nsub == 0) {
    printf("None of the requested subimage axes were found.\n");
  } else if (wcsset(&wcsext)) {
    wcsperr(&wcsext, "");
  } else {
    wcsprt(&wcsext);
  }

  wcsfree(&wcsext);


  // Now test invalid subimaging requests.
  printf("\n\nTesting invalid subimaging requests; ignore status 13 messages "
    "below.\n");

  // Reset the PCi_j matrix to unity.
  pcij = wcs.pc;
  for (int i = 0; i < NAXIS; i++) {
    for (int j = 0; j < NAXIS; j++) {
      *(pcij++) = (i == j) ? 1.0 : 0.0;
    }
  }

  // Set it up for failure by extracting only one axis from a 2-D table.
  nsub = 2;
  axes[0] = WCSSUB_LONGITUDE;
  axes[1] = WCSSUB_SPECTRAL;
  status = wcssub(1, &wcs, &nsub, axes, &wcsext);
  if (status == WCSERR_NON_SEPARABLE) {
    printf("\nReceived wcssub status %d as expected for a non-separable "
           "subimage\ncoordinate system.  The error message was\n",
	   WCSERR_NON_SEPARABLE);
    wcsperr(&wcsext, "  ");
  } else {
    printf("\n\nERROR: expected wcssub status %d for a non-separable "
           "subimage coordinate\nsystem, but received status %d instead.\n",
           WCSERR_NON_SEPARABLE, status);
  }

  wcsfree(&wcsext);

  // As above, but with PC1_3 non-zero.
  *(wcs.pc+2) = 1.0;
  status = wcssub(1, &wcs, &nsub, axes, &wcsext);
  if (status == WCSERR_NON_SEPARABLE) {
    printf("\nReceived wcssub status %d as expected for a non-separable "
           "subimage\ncoordinate system.  The error message was\n",
	   WCSERR_NON_SEPARABLE);
    wcsperr(&wcsext, "  ");
  } else {
    printf("\n\nERROR: expected wcssub status %d for a non-separable "
           "subimage coordinate\nsystem, but received status %d instead.\n",
           WCSERR_NON_SEPARABLE, status);
  }

  wcsfree(&wcsext);

  tabfree(&tab);
  wcsfree(&wcs);

  return 0;
}
