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
  $Id: tspc.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=============================================================================
*
* tspc tests the spectral transformation driver routines for closure.
*
*---------------------------------------------------------------------------*/

// Needed to get nanosleep() from time.h.
#define _POSIX_C_SOURCE 199309L

#include <math.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#include <cpgplot.h>

#include <wcstrig.h>
#include <spc.h>


#define NSPEC 10001

const double tol = 1.0e-11;
const double C = 2.99792458e8;

int closure(const char[9], double, double, int, double, double, double);

// KPNO MARS spectrograph grism parameters.
double mars[7] = {4.5e5, 1.0, 27.0, 1.765, -1.077e6, 3.0, 5.0};


int main()

{
  printf(
    "Testing closure of WCSLIB spectral transformation routines (tspc.c)\n"
    "-------------------------------------------------------------------\n");

  // List status return messages.
  printf("\nList of spc status return values:\n");
  for (int status = 1; status <= 4; status++) {
    printf("%4d: %s.\n", status, spc_errmsg[status]);
  }


  // PGPLOT initialization.
  char text[80];
  strcpy(text, "/xwindow");
  cpgbeg(0, text, 1, 1);

  int    naxisj = NSPEC;
  double crpixj = naxisj/2 + 1;

  double restfrq = 1420.40595e6;
  double restwav = C/restfrq;
  double x1 = 1.0e9;
  double x2 = 2.0e9;
  double cdeltX = (x2 - x1)/(naxisj - 1);
  double crvalX = x1 + (crpixj - 1.0)*cdeltX;
  printf("\nLinear frequency axis, span: %.1f to %.1f (GHz), step: %.3f "
         "(kHz)\n---------------------------------------------------------"
         "-----------------\n", x1*1e-9, x2*1e-9, cdeltX*1e-3);

  int nFail = 0;
  nFail += closure("WAVE-F2W",     0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VOPT-F2W",     0.0, restwav, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("ZOPT-F2W",     0.0, restwav, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("AWAV-F2A",     0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VELO-F2V", restfrq,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("BETA-F2V", restfrq,     0.0, naxisj, crpixj, cdeltX, crvalX);

  restwav = 700.0e-9;
  restfrq = C/restwav;
  x1 = 300.0e-9;
  x2 = 900.0e-9;
  cdeltX = (x2 - x1)/(naxisj - 1);
  crvalX = x1 + (crpixj - 1.0)*cdeltX;
  printf("\nLinear vacuum wavelength axis, span: %.0f to %.0f (nm), "
         "step: %f (nm)\n---------------------------------------------"
         "-----------------------------\n", x1*1e9, x2*1e9, cdeltX*1e9);
  nFail += closure("FREQ-W2F",     0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("AFRQ-W2F",     0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("ENER-W2F",     0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("WAVN-W2F",     0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VRAD-W2F", restfrq,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("AWAV-W2A",     0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VELO-W2V",     0.0, restwav, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("BETA-W2V",     0.0, restwav, naxisj, crpixj, cdeltX, crvalX);


  printf("\nLinear air wavelength axis, span: %.0f to %.0f (nm), "
         "step: %f (nm)\n------------------------------------------"
         "--------------------------------\n", x1*1e9, x2*1e9, cdeltX*1e9);
  nFail += closure("FREQ-A2F", 0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("AFRQ-A2F", 0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("ENER-A2F", 0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("WAVN-A2F", 0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VRAD-A2F", restfrq, 0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("WAVE-A2W", 0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VOPT-A2W", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("ZOPT-A2W", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VELO-A2V", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("BETA-A2V", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);


  restfrq = 1420.40595e6;
  restwav = C/restfrq;
  x1 = -0.96*C;
  x2 =  0.96*C;
  cdeltX = (x2 - x1)/(naxisj - 1);
  crvalX = x1 + (crpixj - 1.0)*cdeltX;
  printf("\nLinear velocity axis, span: %.0f to %.0f m/s, step: %.0f "
         "(m/s)\n------------------------------------------------------"
         "--------------------\n", x1, x2, cdeltX);
  nFail += closure("FREQ-V2F", restfrq, 0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("AFRQ-V2F", restfrq, 0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("ENER-V2F", restfrq, 0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("WAVN-V2F", restfrq, 0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VRAD-V2F", restfrq, 0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("WAVE-V2W", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VOPT-V2W", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("ZOPT-V2W", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("AWAV-V2A", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);


  restwav = 650.0e-9;
  restfrq = C/restwav;
  x1 =  300e-9;
  x2 = 1000e-9;
  cdeltX = (x2 - x1)/(naxisj - 1);
  crvalX = x1 + (crpixj - 1.0)*cdeltX;
  printf("\nVacuum wavelength grism axis, span: %.0f to %.0f (nm), "
         "step: %f (nm)\n--------------------------------------------"
         "------------------------------\n", x1*1e9, x2*1e9, cdeltX*1e9);
  nFail += closure("FREQ-GRI", 0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("AFRQ-GRI", 0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("ENER-GRI", 0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("WAVN-GRI", 0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VRAD-GRI", restfrq, 0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("WAVE-GRI", 0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VOPT-GRI", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("ZOPT-GRI", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("AWAV-GRI", 0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VELO-GRI", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("BETA-GRI", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);


  // Reproduce Fig. 5 of Paper III.
  naxisj = 1700;
  crpixj = 719.8;
  crvalX = 7245.2e-10;
  cdeltX = 2.956e-10;
  restwav = 8500.0e-10;
  restfrq = C/restwav;
  x1 = crvalX + (1 - crpixj)*cdeltX;
  x2 = crvalX + (naxisj - crpixj)*cdeltX;
  mars[5] = 0.0;
  mars[6] = 0.0;
  printf("\nAir wavelength grism axis, span: %.0f to %.0f (nm), "
         "step: %f (nm)\n--------------------------------------------"
         "------------------------------\n", x1*1e9, x2*1e9, cdeltX*1e9);
  nFail += closure("AWAV-GRA", 0.0,     0.0, naxisj, crpixj, cdeltX, crvalX);
  nFail += closure("VELO-GRA", 0.0, restwav, naxisj, crpixj, cdeltX, crvalX);

  cpgask(0);
  cpgend();

  if (nFail) {
    printf("\nFAIL: %d closure residuals exceed reporting tolerance.\n",
      nFail);
  } else {
    printf("\nPASS: All closure residuals are within reporting tolerance.\n");
  }

  return nFail;
}

//----------------------------------------------------------------------------

int closure (
  const char ctypeS[9],
  double restfrq,
  double restwav,
  int    naxisj,
  double crpixj,
  double cdeltX,
  double crvalX)

{
  int status;

  // Get keyvalues for the required spectral axis type.
  char   ptype, xtype;
  int    restreq;
  double crvalS, dSdX;
  if ((status = spcxps(ctypeS, crvalX, restfrq, restwav, &ptype, &xtype,
                       &restreq, &crvalS, &dSdX))) {
    printf("ERROR %d from spcxps() for %s.\n", status, ctypeS);
    return 1;
  }
  double cdeltS = cdeltX * dSdX;

  struct spcprm spc;
  spcini(&spc);

  if (ctypeS[5] == 'G') {
    // KPNO MARS spectrograph grism parameters.
    spc.pv[0] = mars[0];
    spc.pv[1] = mars[1];
    spc.pv[2] = mars[2];
    spc.pv[3] = mars[3];
    spc.pv[4] = mars[4];
    spc.pv[5] = mars[5];
    spc.pv[6] = mars[6];
  }

  // Construct the axis.
  double spec1[NSPEC];
  for (int j = 0; j < naxisj; j++) {
    spec1[j] = (j+1 - crpixj)*cdeltS;
  }

  printf("%4s (CRVALk+w) range: %13.6e to %13.6e, step: %13.6e\n", ctypeS,
    crvalS+spec1[0], crvalS+spec1[naxisj-1], cdeltS);


  // Initialize.
  spc.flag = 0;
  spc.crval = crvalS;
  spc.restfrq = restfrq;
  spc.restwav = restwav;
  strncpy(spc.type, ctypeS, 4);
  spc.type[4] = '\0';
  strcpy(spc.code, ctypeS+5);

  // Convert the first to the second.
  int    stat1[NSPEC], stat2[NSPEC];
  double spec2[NSPEC];
  if ((status = spcx2s(&spc, naxisj, 1, 1, spec1, spec2, stat1))) {
    printf("spcx2s ERROR %d: %s.\n", status, spc_errmsg[status]);
  }

  // Convert the second back to the first.
  double clos[NSPEC];
  if ((status = spcs2x(&spc, naxisj, 1, 1, spec2, clos, stat2))) {
    printf("spcs2x ERROR %d: %s.\n", status, spc_errmsg[status]);
  }

  double residmax = 0.0;

  // Test closure.
  int nFail = 0;
  for (int j = 0; j < naxisj; j++) {
    if (stat1[j]) {
      printf("%s: w =%20.12e -> %s = ???, stat = %d\n", ctypeS, spec1[j],
             spc.type, stat1[j]);
      continue;
    }

    if (stat2[j]) {
      printf("%s: w =%20.12e -> %s =%20.12e -> w = ???, stat = %d\n",
             ctypeS, spec1[j], spc.type, spec2[j], stat2[j]);
      continue;
    }

    double resid = fabs((clos[j] - spec1[j])/cdeltS);
    if (resid > residmax) residmax = resid;

    if (resid > tol) {
      nFail++;
      printf("%s: w =%20.12e -> %s =%20.12e ->\n          w =%20.12e,  "
             "resid =%20.12e\n", ctypeS, spec1[j], spc.type, spec2[j],
             clos[j], resid);
    }
  }

  printf("%s: Maximum closure residual = %.1e pixel.\n", ctypeS, residmax);


  // Draw graph.
  cpgbbuf();
  cpgeras();

  float x[NSPEC], y[NSPEC];
  float xmin = (float)(crvalS + spec1[0]);
  float xmax = (float)(crvalS + spec1[naxisj-1]);
  float ymin = (float)(spec2[0]) - xmin;
  float ymax = ymin;
  for (int j = 0; j < naxisj; j++) {
    x[j] = (float)(j+1);
    y[j] = (float)(spec2[j] - (crvalS + spec1[j]));
    if (y[j] > ymax) ymax = y[j];
    if (y[j] < ymin) ymin = y[j];
  }

  int j = (int)crpixj + 1;
  if (y[j] < 0.0) {
    float tmp  = ymin;
    ymin = ymax;
    ymax = tmp;
  }

  cpgask(0);
  cpgenv(1.0f, (float)naxisj, ymin, ymax, 0, -1);

  char sname[32], title[80], units[8], ylab[80];
  cpgsci(1);
  cpgbox("ABNTS", 0.0f, 0, "BNTS", 0.0f, 0);
  spctyp(ctypeS, 0x0, 0x0, sname, units, 0x0, 0x0, 0x0);
  sprintf(ylab, "%s - correction [%s]", sname, units);
  sprintf(title, "%s:  CRVALk + w [%s]", ctypeS, units);
  cpglab("Pixel coordinate", ylab, title);

  cpgaxis("N", 0.0f, ymax, (float)naxisj, ymax, xmin, xmax, 0.0f, 0, -0.5f,
    0.0f, 0.5f, -0.5f, 0.0f);

  cpgaxis("N", (float)naxisj, ymin, (float)naxisj, ymax, (float)(ymin/cdeltS),
    (float)(ymax/cdeltS), 0.0f, 0, 0.5f, 0.0f, 0.5f, 0.1f, 0.0f);
  cpgmtxt("R", 2.2f, 0.5f, 0.5f, "Pixel offset");

  cpgline(naxisj, x, y);
  cpgsci(7);
  cpgpt1((float)crpixj, 0.0f, 24);
  cpgebuf();

  // Allow 200ms to view the plot on fast machines.
  struct timespec nano = {(time_t)0, 200000000L};
  nanosleep(&nano, 0x0);

  printf("Type <RETURN> for next page: ");
  (void)getchar();

  printf("\n");

  return nFail;
}
