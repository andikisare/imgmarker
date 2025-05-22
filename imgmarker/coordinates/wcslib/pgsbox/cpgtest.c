/*============================================================================
  PGSBOX 8.4 - draw curvilinear coordinate axes for PGPLOT.
  Copyright (C) 1997-2024, Mark Calabretta

  This file is part of PGSBOX.

  PGSBOX is free software: you can redistribute it and/or modify it under the
  terms of the GNU Lesser General Public License as published by the Free
  Software Foundation, either version 3 of the License, or (at your option)
  any later version.

  PGSBOX is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
  FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for
  more details.

  You should have received a copy of the GNU Lesser General Public License
  along with PGSBOX.  If not, see http://www.gnu.org/licenses.

  Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
  http://www.atnf.csiro.au/people/Mark.Calabretta
  $Id: cpgtest.c,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
*=============================================================================
*
*   cpgtest
*
*---------------------------------------------------------------------------*/

// Needed to get nanosleep() from time.h.
#define _POSIX_C_SOURCE 199309L

#include <math.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#include <cpgplot.h>

#include <cpgsbox.h>
#include <wcs.h>
#include <wcsfix.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define lngvel_ F77_FUNC(lngvel, LNGVEL)
#define fscan_  F77_FUNC(fscan,  FSCAN)
#define pgcrfn_ F77_FUNC(pgcrfn, PGCRFN)
#define pgwcsl_ F77_FUNC(pgwcsl, PGWCSL)

int main()

{
  const double pi = 3.141592653589793238462643;
  const double d2r = pi/180.0;

  // cpgsbox() function arguments.
  char   fcode[2][4], idents[3][80], nlcprm[1], opt[2];
  int    c0[7], ci[7], gcode[2], ic, ierr, nliprm[2];
  double cache[257][4], grid1[9], grid2[9], nldprm[8];
  nlfunc_t lngvel_, fscan_, pgcrfn_, pgwcsl_;

  // Setup.
  int naxis[2] = {512, 512};

  float blc[2] = {0.5f, 0.5f};
  float trc[2];
  trc[0] = naxis[0] + 0.5f;
  trc[1] = naxis[1] + 0.5f;

  char devtyp[16];
  strcpy(devtyp, "/XWINDOW");
  cpgbeg(0, devtyp, 1, 1);

  int nchr = 16;
  cpgqinf("TYPE", devtyp, &nchr);
  if (strcmp(devtyp, "PS") == 0  ||
     strcmp(devtyp, "VPS") == 0 ||
     strcmp(devtyp, "CPS") == 0 ||
     strcmp(devtyp, "VCPS") == 0) {
    // Switch black and white.
    cpgscr(0, 1.0f, 1.0f, 1.0f);
    cpgscr(1, 0.0f, 0.0f, 0.0f);
  }

  int large = strcmp(devtyp, "XWINDOW") == 0;
  float scl;
  if (large) {
    scl = 1.0f;
    cpgvstd();
  } else {
    scl = 0.7f;
    cpgvsiz(1.0f, 3.0f, 1.0f, 3.0f);
  }

  // Yellow.
  cpgscr(2, 1.0f, 1.0f, 0.0f);
  // White.
  cpgscr(3, 1.0f, 1.0f, 1.0f);
  // Pale blue.
  cpgscr(4, 0.5f, 0.5f, 0.8f);
  // Pale red.
  cpgscr(5, 0.8f, 0.5f, 0.5f);
  // Grey.
  cpgscr(6, 0.7f, 0.7f, 0.7f);
  // Dark green.
  cpgscr(7, 0.3f, 0.5f, 0.3f);

  c0[0] = -1;
  c0[1] = -1;
  c0[2] = -1;
  c0[3] = -1;
  c0[4] = -1;
  c0[5] = -1;
  c0[6] = -1;

  cpgwnad(0.0f, 1.0f, 0.0f, 1.0f);
  cpgask(1);
  cpgpage();

  struct wcsprm wcs;
  wcs.flag = -1;

  // Allow 250ms to view the plot on fast machines.
  struct timespec nano = {(time_t)0, 250000000L};

  //--------------------------------------------------------------------------
  // Longitude-velocity map; the y-axis is regularly spaced in frequency but
  // is to be labelled as a true relativistic velocity.
  //   - PGSBOX uses subroutine LNGVEL.
  //   - Separable (i.e. orthogonal), non-linear coordinate system.
  //   - Automatic choice of coordinate increments.
  //   - Extraction of a common scaling factor.
  //   - Automatic choice of what edges to label.
  //   - Request for tickmarks (internal) for one coordinate and grid lines
  //     for the other.
  //   - Simple two-colour grid using two calls with deferred labelling on
  //     the first call.
  //   - Degree labelling.
  //   - Suppression of zero arcmin and arcsec fields in sexagesimal degree
  //     format.
  //--------------------------------------------------------------------------

  printf("\nLongitude-velocity map\n");

  // Reference pixel coordinates.
  nldprm[0] =   1.0;
  nldprm[1] = 256.0;

  // Reference pixel values.
  nldprm[2] = 0.0;
  nldprm[3] = 1.420e9;

  // Coordinate increments.
  nldprm[4] = 360.0/(naxis[0]-1);
  nldprm[5] = 4e6;

  // Rest frequency.
  nldprm[6] = 1.420e9;

  // Annotation.
  strcpy(idents[0], "galactic longitude");
  strcpy(idents[1], "velocity (m/s)");
  strcpy(idents[2], "HI line");

  opt[0] = 'F';
  opt[1] = ' ';

  // Normal size lettering.
  cpgsch(1.0f*scl);

  // Yellow tick marks for longitude and grid lines for velocity.
  cpgsci(2);
  gcode[0] = 1;
  gcode[1] = 2;
  grid1[0] = 0.0;
  grid2[0] = 0.0;

  // Defer labelling.
  ic = -1;
  cpgsbox(blc, trc, idents, opt, -1, 0, c0, gcode, 2.0, 0, grid1, 0, grid2,
    0, lngvel_, 1, 1, 7, nlcprm, nliprm, nldprm, 256, &ic, cache, &ierr);

  // Draw fiducial grid lines in white and do labelling.
  cpgsci(1);
  gcode[0] = 2;
  gcode[1] = 2;
  grid1[1] = 180.0;
  grid2[1] = 0.0;
  cpgsbox(blc, trc, idents, opt, 0, 0, c0, gcode, 0.0, 1, grid1, 1, grid2,
    0, lngvel_, 1, 1, 7, nlcprm, nliprm, nldprm, 256, &ic, cache, &ierr);

  // Draw the frame.
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();

  //--------------------------------------------------------------------------
  // Azimuth-frequency scan; this sort of output might be obtained from an
  // antenna that scans in azimuth with a receiver that scans simultaneously
  // in frequency.
  //   - PGSBOX uses subroutine FSCAN.
  //   - Non-separable (i.e. non-orthogonal) non-linear coordinate system.
  //   - Automatic choice of what edges to label; results in labelling the
  //     bottom, left and right sides of the plot.
  //   - Cyclic labelling.  FSCAN returns the azimuth in the range
  //     0 - 720 degrees but PGSBOX is set to normalize this to two cycles of
  //     0 - 360 degrees.
  //   - Logarithmic labelling.
  //   - Automatic choice of coordinate increments but with request for all
  //     grid lines for the logarithmic coordinate.
  //   - Degree labelling.
  //   - Suppression of common zero arcmin and arcsec fields in sexagesimal
  //     degree format.
  //--------------------------------------------------------------------------

  printf("\nAzimuth-frequency scan\n");

  // Reference pixel coordinates.
  nldprm[0] = 0.5;
  nldprm[1] = 0.5;

  // Reference pixel values.
  nldprm[2] = 0.0;
  nldprm[3] = 8.5;

  // Coordinate increments.
  nldprm[4] = 720.0/(naxis[0]+1);
  nldprm[5] = 0.002;

  // Rate of change of NLDPRM[3] with x-pixel.
  nldprm[6] = -0.002;

  // Annotation.
  strcpy(idents[0], "azimuth");
  strcpy(idents[1], "\\gn/Hz");
  strcpy(idents[2], "Frequency/azimuth scan");

  opt[0] = 'D';
  opt[1] = 'L';

  // Normal size lettering.
  cpgsch(1.0f*scl);

  // Draw full grid lines.
  cpgsci(1);
  gcode[0] = 2;
  gcode[1] = 2;
  grid1[0] = 0.0;
  grid2[0] = 0.0;

  // Setting labden = 9900 forces all logarithmic grid lines to be drawn.
  ic = -1;
  cpgsbox(blc, trc, idents, opt, 0, 9900, c0, gcode, 2.0, 0, grid1, 0, grid2,
    0, fscan_, 1, 1, 7, nlcprm, nliprm, nldprm, 256, &ic, cache, &ierr);

  // Draw the frame.
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();


  //--------------------------------------------------------------------------
  // Z versus time plot.
  //   - PGSBOX uses subroutine PGCRFN.
  //   - Separable (i.e. orthogonal), non-linear coordinate system.
  //   - Use of function PGCRFN for separable axis types.
  //   - Automatic choice of what edges to label; results in labelling the
  //     bottom and left sides of the plot.
  //   - Automatic choice of coordinate increments.
  //   - Logarithmic labelling over many orders of magnitude.
  //   - Single-character annotation on a vertical axis is upright.
  //--------------------------------------------------------------------------

  printf("\nZ versus time plot\n");

  // Function types.
  memcpy(fcode[0], "Lin ", 4);
  memcpy(fcode[1], "Log ", 4);

  // Reference pixel coordinates.
  nldprm[0] =   0.5;
  nldprm[1] = -50.0;

  // Coordinate increments.
  nldprm[2] = 0.04;
  nldprm[3] = 0.02;

  // Reference pixel values.
  nldprm[4] = -3.0;
  nldprm[5] =  1.0;

  // Annotation.
  strcpy(idents[0], "Age of universe (sec)");
  strcpy(idents[1], "Y");
  strcpy(idents[2], "");

  opt[0] = 'L';
  opt[1] = ' ';

  // Normal size lettering.
  cpgsch(1.0f*scl);

  // Draw ticks for the first coordinate, grid lines for the second.
  cpgsci(1);
  gcode[0] = 1;
  gcode[1] = 2;
  grid1[0] = 0.0;
  grid2[0] = 0.0;

  ic = -1;
  cpgsbox(blc, trc, idents, opt, 0, 0, c0, gcode, 2.0, 0, grid1, 0, grid2, 0,
    pgcrfn_, 8, 2, 4, fcode[0], nliprm, nldprm, 256, &ic, cache, &ierr);

  // Draw the frame.
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();

  //--------------------------------------------------------------------------
  // Simple SIN projection near the south celestial pole.
  //   - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
  //   - Non-separable (i.e. non-orthogonal) curvilinear coordinate system.
  //   - Demonstrate parameter definition for PGWCSL.
  //   - Discovery of grid lines that do not cross any axis.
  //   - Automatic choice of what edges to label; results in labelling all
  //     sides of the plot.
  //   - Automatic choice of coordinate increments but with request for
  //     increased grid density for each coordinate.
  //   - Double precision accuracy.
  //   - Cyclic coordinates.  PGWCSL returns the right ascension in the range
  //     -180 to +180 degrees, i.e. with a discontinuity at +/- 180 degrees.
  //   - Labelling of degrees as time in the range 0 - 24h.
  //   - Suppression of labels that would overlap one another.
  //   - Sexagesimal degree labelling with automatically determined
  //     precision.
  //   - Suppression of common zero minute and second fields in sexagesimal
  //     time format.
  //--------------------------------------------------------------------------

  printf("\nSimple SIN projection\n");

  wcs.flag = -1;
  wcsini(1, 2, &wcs);

  // Set projection type to SIN.
  strcpy(wcs.ctype[0], "RA---SIN");
  strcpy(wcs.ctype[1], "DEC--SIN");

  // Reference pixel coordinates.
  wcs.crpix[0] = 384.0;
  wcs.crpix[1] = 256.0;

  // Coordinate increments.
  wcs.cdelt[0] = -1.0/3600000.0;
  wcs.cdelt[1] =  1.0/3600000.0;

  // Spherical coordinate references.
  double dec0 = -89.99995;
  wcs.crval[0] = 25.0;
  wcs.crval[1] = dec0;

  // Set parameters for an NCP projection.
  dec0 *= d2r;
  wcs.pv[0].i = 2;
  wcs.pv[0].m = 1;
  wcs.pv[0].value = 0.0;
  wcs.pv[0].i = 2;
  wcs.pv[1].m = 2;
  wcs.pv[1].value = cos(dec0)/sin(dec0);

  // Annotation.
  strcpy(idents[0], "Right ascension");
  strcpy(idents[1], "Declination");
  strcpy(idents[2], "WCS SIN projection");

  opt[0] = 'G';
  opt[1] = 'E';

  // Compact lettering.
  cpgsch(0.8f*scl);

  // Draw full grid lines.
  cpgsci(1);
  gcode[0] = 2;
  gcode[1] = 2;
  grid1[0] = 0.0;
  grid2[0] = 0.0;

  // Draw the celestial grid.  The grid density is set for each world
  // coordinate by specifying LABDEN = 1224.
  ic = -1;
  cpgsbox(blc, trc, idents, opt, 0, 1224, c0, gcode, 0.0, 0, grid1, 0, grid2,
    0, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256, &ic,
    cache, &ierr);

  // Draw the frame.
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();

  //-------------------------------------------------------------------------
  // Conic equal area projection.
  //   - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
  //   - Non-separable (i.e. non-orthogonal) curvilinear coordinate system.
  //   - Coordinate system undefined in areas of the plot.
  //   - Demonstrate parameter definition for PGWCSL.
  //   - Discontinuous grid lines handled by PGWCSL.
  //   - Discovery of grid lines that do not cross any axis.
  //   - Colour control for grid and labelling.
  //   - Reduced size lettering.
  //   - Automatic choice of what edges to label; results in labelling all
  //     sides of the plot.
  //   - Automatic choice of coordinate increments.
  //   - Cyclic coordinates.  PGWCSL returns the longitude in the range -180
  //     to +180 degrees, i.e. with a discontinuity at +/- 180 degrees.
  //   - Suppression of labels that would overlap one another.
  //   - Suppression of common zero arcmin and arcsec fields in sexagesimal
  //     degree format.
  //--------------------------------------------------------------------------

  printf("\nConic equal area projection\n");

  wcsini(1, 2, &wcs);

  // Set projection type to conic equal-area.
  strcpy(wcs.ctype[0], "RA---COE");
  strcpy(wcs.ctype[1], "DEC--COE");

  // Reference pixel coordinates.
  wcs.crpix[0] = 256.0;
  wcs.crpix[1] = 256.0;

  // Coordinate increments.
  wcs.cdelt[0] = -1.0/3.0;
  wcs.cdelt[1] =  1.0/3.0;

  // Spherical coordinate references.
  wcs.crval[0] =  90.0;
  wcs.crval[1] =  30.0;
  wcs.lonpole  = 150.0;

  // Middle latitude and offset from standard parallels.
  wcs.npv = 2;
  wcs.pv[0].i = 2;
  wcs.pv[0].m = 1;
  wcs.pv[0].value = 60.0;
  wcs.pv[1].i = 2;
  wcs.pv[1].m = 2;
  wcs.pv[1].value = 15.0;

  // Annotation.
  strcpy(idents[0], "longitude");
  strcpy(idents[1], "latitude");
  strcpy(idents[2], "WCS conic equal area projection");

  opt[0] = 'E';
  opt[1] = 'E';

  // Reduced size lettering.
  cpgsch(0.8f*scl);

  // Draw full grid lines.
  gcode[0] = 2;
  gcode[1] = 2;
  grid1[0] = 0.0;
  grid2[0] = 0.0;

  // Use colour to associate grid lines and labels.
  // Meridians in red.
  cpgscr(10, 0.5f, 0.0f, 0.0f);
  // Parallels in blue.
  cpgscr(11, 0.0f, 0.2f, 0.5f);
  // Longitudes in red.
  cpgscr(12, 0.8f, 0.3f, 0.0f);
  // Latitudes in blue.
  cpgscr(13, 0.0f, 0.4f, 0.7f);
  // Longitude labels in red.
  cpgscr(14, 0.8f, 0.3f, 0.0f);
  // Latitude labels in blue.
  cpgscr(15, 0.0f, 0.4f, 0.7f);
  // Title in cyan.
  cpgscr(16, 0.3f, 1.0f, 1.0f);

  ci[0] = 10;
  ci[1] = 11;
  ci[2] = 12;
  ci[3] = 13;
  ci[4] = 14;
  ci[5] = 15;
  ci[6] = 16;

  // Draw the celestial grid letting PGSBOX choose the increments.
  ic = -1;
  cpgsbox(blc, trc, idents, opt, 0, 0, ci, gcode, 0.0, 0, grid1, 0, grid2, 1,
    pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256, &ic, cache,
    &ierr);

  // Set parameters to draw the native grid.
  wcs.crval[0] =   0.0;
  wcs.crval[1] =  60.0;
  wcs.lonpole  = 999.0;
  wcs.latpole  = 999.0;
  wcsset(&wcs);

  // We just want to delineate the boundary, in green.
  cpgsci(7);
  grid1[1] = -180.0;
  grid1[2] =  180.0;
  grid2[1] =  -90.0;
  grid2[2] =   90.0;

  ic = -1;
  cpgsbox(blc, trc, idents, opt, -1, 0, c0, gcode, 0.0, 2, grid1, 2, grid2,
    1, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256, &ic,
    cache, &ierr);

  // Draw the frame.
  cpgsci(1);
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();

  //--------------------------------------------------------------------------
  // Polyconic projection with colour-coded grid.
  //   - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
  //   - Non-separable (i.e. non-orthogonal) curvilinear coordinate system.
  //   - Coordinate system undefined in areas of the plot.
  //   - Demonstrate parameter definition for PGWCSL.
  //   - Discontinuous grid lines handled by PGWCSL.
  //   - Colour coded labelling.
  //   - Colour coded grid implemented by the caller.
  //   - Basic management of the axis-crossing table (see code).
  //   - Reduced size lettering.
  //   - Tick marks external to the frame.
  //   - User selection of what edges to label with request for both
  //     coordinates to be labelled on bottom, left and top edges.
  //   - User selection of grid lines to plot.
  //   - Concatenation of annotation at bottom and left; automatically
  //     suppressed at the top since only one coordinate is labelled there.
  //   - Suppression of labels that would overlap one another.
  //   - Degree labelling.
  //   - Labelling of degrees as time in the range -12 - +12h.
  //   - Suppression of common zero minute and second fields in sexagesimal
  //     time format.
  //--------------------------------------------------------------------------

  printf("\nPolyconic projection with colour-coded grid\n");

  wcsini(1, 2, &wcs);

  // Set projection type to polyconic.
  strcpy(wcs.ctype[0], "RA---PCO");
  strcpy(wcs.ctype[1], "DEC--PCO");

  // Reference pixel coordinates.
  wcs.crpix[0] = 192.0;
  wcs.crpix[1] = 640.0;

  // Rotate 30 degrees.
  double rotn = 30.0*d2r;
  *(wcs.pc)   =  cos(rotn);
  *(wcs.pc+1) =  sin(rotn);
  *(wcs.pc+2) = -sin(rotn);
  *(wcs.pc+3) =  cos(rotn);

  // Coordinate increments.
  wcs.cdelt[0] = -1.0/5.0;
  wcs.cdelt[1] =  1.0/5.0;

  // Spherical coordinate references.
  wcs.crval[0] = 332.0;
  wcs.crval[1] =  40.0;
  wcs.lonpole  = -30.0;

  // Annotation.
  strcpy(idents[0], "Hour angle");
  strcpy(idents[1], "Declination");
  strcpy(idents[2], "WCS polyconic projection");

  opt[0] = 'H';
  opt[1] = 'B';

  // Reduced size lettering.
  cpgsch(0.9f*scl);

  // Draw external (TIKLEN < 0) tick marks every 5 degrees.
  gcode[0] = 1;
  gcode[1] = 1;
  double tiklen = -2.0;

  cpgsci(6);
  grid1[0] = 5.0;
  grid2[0] = 5.0;

  ic = -1;
  cpgsbox(blc, trc, idents, opt, -1, 0, c0, gcode, tiklen, 0, grid1, 0,
    grid2, 1, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256,
    &ic, cache, &ierr);

  // Resetting the table index to zero causes information about the
  // tick marks to be discarded.
  ic = 0;

  // Draw full grid lines in yellow rather than tick marks.
  cpgsci(2);
  gcode[0] = 2;
  gcode[1] = 2;

  // Draw the primary meridian and equator.
  grid1[1] = 0.0;
  grid2[1] = 0.0;
  cpgsbox(blc, trc, idents, opt, -1, 0, c0, gcode, 0.0, 1, grid1, 1, grid2,
    1, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256, &ic,
    cache, &ierr);

  // At this point the axis-crossing table will have entries for the
  // primary meridian and equator.  Labelling was deferred in the
  // previous call, and the table is passed intact on the second call
  // to accumulate further axis-crossings.

  // Draw 90 degree meridians and poles in white.
  cpgsci(3);
  grid1[1] =  90.0;
  grid1[2] = 180.0;
  grid1[3] = 270.0;
  grid2[1] = -90.0;
  grid2[2] =  90.0;
  cpgsbox(blc, trc, idents, opt, -1, 0, c0, gcode, 0.0, 3, grid1, 2, grid2,
    1, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256, &ic,
    cache, &ierr);

  // Draw the first set of 15 degree meridians and parallels in blue.
  cpgsci(4);
  grid1[1] =  15.0;
  grid1[2] =  60.0;
  grid1[3] = 105.0;
  grid1[4] = 150.0;
  grid1[5] = 195.0;
  grid1[6] = 240.0;
  grid1[7] = 285.0;
  grid1[8] = 330.0;
  grid2[1] = -75.0;
  grid2[2] = -30.0;
  grid2[3] =  15.0;
  grid2[4] =  60.0;
  cpgsbox(blc, trc, idents, opt, -1, 0, c0, gcode, 0.0, 8, grid1, 4, grid2,
    1, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256, &ic,
    cache, &ierr);

  // Draw the second set of 15 degree meridians and parallels in red.
  cpgsci(5);
  grid1[1] =  30.0;
  grid1[2] =  75.0;
  grid1[3] = 120.0;
  grid1[4] = 165.0;
  grid1[5] = 210.0;
  grid1[6] = 255.0;
  grid1[7] = 300.0;
  grid1[8] = 345.0;
  grid2[1] = -60.0;
  grid2[2] = -15.0;
  grid2[3] =  30.0;
  grid2[4] =  75.0;
  cpgsbox(blc, trc, idents, opt, -1, 0, c0, gcode, 0.0, 8, grid1, 4, grid2,
    1, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256, &ic,
    cache, &ierr);

  // The axis-crossing table has now accumulated information for all of
  // the preceding meridians and parallels but no labels have been
  // produced.  It will acquire information for the the next set of
  // meridians and parallels before being processed by this call to
  // PGSBOX which finally produces the labels.

  // Draw the 45 degree meridians and parallels in grey and use colour
  // to differentiate grid labels.
  // Meridians and parallels in grey.
  cpgscr(10, 0.7f, 0.7f, 0.7f);
  cpgscr(11, 0.7f, 0.7f, 0.7f);
  // Longitudes tinged red.
  cpgscr(12, 1.0f, 0.9f, 0.6f);
  // Latitudes tinged green.
  cpgscr(13, 0.8f, 1.0f, 0.9f);
  // Longitude labels tinged red.
  cpgscr(14, 1.0f, 0.9f, 0.6f);
  // Latitude labels tinged green.
  cpgscr(15, 0.8f, 1.0f, 0.9f);
  // Title in white.
  cpgscr(16, 1.0f, 1.0f, 1.0f);

  ci[0] = 10;
  ci[1] = 11;
  ci[2] = 12;
  ci[3] = 13;
  ci[4] = 14;
  ci[5] = 15;
  ci[6] = 16;

  cpgsci(6);

  // Tell PGSBOX what edges to label.
  grid1[1] =  45.0;
  grid1[2] = 135.0;
  grid1[3] = 225.0;
  grid1[4] = 315.0;
  grid2[1] = -45.0;
  grid2[2] =  45.0;
  cpgsbox(blc, trc, idents, opt, 2333, 0, ci, gcode, 0.0, 4, grid1, 2, grid2,
    1, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256, &ic,
    cache, &ierr);

  // Native grid in green (delineates boundary).
  cpgsci(7);
  grid1[1] = -180.0;
  grid1[2] =  180.0;
  grid2[1] = -999.0;

  wcs.crval[0] =   0.0;
  wcs.crval[1] =   0.0;
  wcs.lonpole  = 999.0;
  wcsset(&wcs);

  ic = -1;
  cpgsbox(blc, trc, idents, opt, -1, 0, c0, gcode, 0.0, 2, grid1, 1, grid2,
    1, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256, &ic,
    cache, &ierr);

  // Draw the frame.
  cpgsci(1);
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();

  //--------------------------------------------------------------------------
  // Plate Carree projection.
  //   - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
  //   - Rectangular image.
  //   - Dual coordinate grids.
  //   - Non-separable (i.e. non-orthogonal) curvilinear coordinate system.
  //   - Demonstrate parameter definition for PGWCSL.
  //   - Discontinuous grid lines handled by PGWCSL.
  //   - Colour coding of grid and labelling.
  //   - Reduced size lettering.
  //   - Manual labelling control.
  //   - Manual and automatic choice of coordinate increments.
  //   - Cyclic coordinates.  PGWCSL returns the longitude in the range -180
  //     to +180 degrees, i.e. with a discontinuity at +/- 180 degrees.
  //   - Suppression of labels that would overlap one another.
  //--------------------------------------------------------------------------

  printf("\nPlate Carree projection\n");

  naxis[0] = 181;
  naxis[1] =  91;

  blc[0] = 0.5;
  blc[1] = 0.5;
  trc[0] = naxis[0] + 0.5;
  trc[1] = naxis[1] + 0.5;

  // Reset viewport for rectangular image.
  if (large) {
    cpgvstd();
  } else {
    cpgvsiz(1.0f, 3.0f, 1.0f, 3.0f);
  }
  cpgwnad(0.0f, 1.0f, 0.0f, ((float)naxis[1])/((float)naxis[0]));

  wcsini(1, 2, &wcs);

  // Set projection type to plate carree.
  strcpy(wcs.ctype[0], "GLON-CAR");
  strcpy(wcs.ctype[1], "GLAT-CAR");

  // Reference pixel coordinates.
  wcs.crpix[0] = 226.0;
  wcs.crpix[1] =  46.0;

  // Linear transformation matrix.
  rotn = 15.0*d2r;
  *(wcs.pc)   =  cos(rotn);
  *(wcs.pc+1) =  sin(rotn);
  *(wcs.pc+2) = -sin(rotn);
  *(wcs.pc+3) =  cos(rotn);

  // Coordinate increments.
  wcs.cdelt[0] = -1.0;
  wcs.cdelt[1] =  1.0;

  // Set parameters to draw the native grid.
  wcs.crval[0] = 0.0;
  wcs.crval[1] = 0.0;

  // The reference pixel was defined so that the native longitude runs
  // from 225 deg to 45 deg and this will cause the grid to be truncated
  // at the 180 deg boundary.  However, being a cylindrical projection
  // it is possible to recentre it in longitude.  cylfix() will modify
  // modify CRPIX, CRVAL, and LONPOLE to suit.

  cylfix(naxis, &wcs);

  // Annotation.
  strcpy(idents[0], "");
  strcpy(idents[1], "");
  strcpy(idents[2], "WCS plate caree projection");

  opt[0] = 'C';
  opt[1] = 'C';

  // Reduced size lettering.
  cpgsch(0.8f*scl);

  // Draw full grid lines.
  gcode[0] = 2;
  gcode[1] = 2;

  // Draw native grid in green.
  cpgscr(16, 0.0f, 0.2f, 0.0f);
  // Title in cyan.
  cpgscr(17, 0.3f, 1.0f, 1.0f);

  ci[0] = 16;
  ci[1] = 16;
  ci[2] =  7;
  ci[3] =  7;
  ci[4] = -1;
  ci[5] = -1;
  ci[6] = 17;

  grid1[0] = 15.0;
  grid2[0] = 15.0;
  ic = -1;
  cpgsbox(blc, trc, idents, opt, 2100, 0, ci, gcode, 0.0, 0, grid1, 0, grid2,
    1, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256, &ic,
    cache, &ierr);

  // Reset CRPIX previously modified by cylfix().
  wcs.crpix[0] = 226.0;
  wcs.crpix[1] =  46.0;

  // Galactic reference coordinates.
  wcs.crval[0] =  30.0;
  wcs.crval[1] =  35.0;
  wcs.lonpole  = 999.0;
  wcsset(&wcs);

  cylfix(naxis, &wcs);

  // Annotation.
  strcpy(idents[0], "longitude");
  strcpy(idents[1], "latitude");
  strcpy(idents[2], "");

  opt[0] = 'E';
  opt[1] = 'E';

  // Use colour to associate grid lines and labels.
  // Meridians in red.
  cpgscr(10, 0.5f, 0.0f, 0.0f);
  // Parallels in blue.
  cpgscr(11, 0.0f, 0.2f, 0.5f);
  // Longitudes in red.
  cpgscr(12, 0.8f, 0.3f, 0.0f);
  // Latitudes in blue.
  cpgscr(13, 0.0f, 0.4f, 0.7f);
  // Longitude labels in red.
  cpgscr(14, 0.8f, 0.3f, 0.0f);
  // Latitude labels in blue.
  cpgscr(15, 0.0f, 0.4f, 0.7f);

  ci[0] = 10;
  ci[1] = 11;
  ci[2] = 12;
  ci[3] = 13;
  ci[4] = 14;
  ci[5] = 15;
  ci[6] = -1;

  grid1[0] = 0.0;
  grid2[0] = 0.0;

  // Draw the celestial grid letting PGSBOX choose the increments.
  ic = -1;
  cpgsbox(blc, trc, idents, opt, 21, 0, ci, gcode, 0.0, 0, grid1, 0, grid2,
    1, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256, &ic,
    cache, &ierr);

  // Draw the frame.
  cpgsci(1);
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();

  //--------------------------------------------------------------------------
  // Plate Carree projection.
  //   - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
  //   - BLC, TRC unrelated to pixel coordinates.
  //   - Demonstrate parameter definition for PGWCSL.
  //   - Poles and 180 meridian projected along edges of the frame.
  //   - Reduced size lettering.
  //   - Manual and automatic choice of coordinate increments.
  //   - Suppression of common zero minute and second fields in sexagesimal
  //     time format.
  //--------------------------------------------------------------------------

  printf("\nPlate Carree projection\n");

  blc[0] = -180.0;
  blc[1] =  -90.0;
  trc[0] =  180.0;
  trc[1] =  +90.0;

  //  Reset viewport for rectangular image.
  if (large) {
    cpgvstd();
  } else {
    cpgvsiz(1.0f, 3.0f, 1.0f, 3.0f);
  }
  cpgwnad (blc[0], trc[0], blc[1], trc[1]);

  wcsini(1, 2, &wcs);

  // Set projection type to plate carree.
  strcpy(wcs.ctype[0], "RA---CAR");
  strcpy(wcs.ctype[1], "DEC--CAR");

  // Reference pixel coordinates.
  wcs.crpix[0] = 0.0;
  wcs.crpix[1] = 0.0;

  // Coordinate increments.
  wcs.cdelt[0] = -1.0;
  wcs.cdelt[1] =  1.0;

  // Set parameters to draw the native grid.
  wcs.crval[0] = 0.0;
  wcs.crval[1] = 0.0;

  // Annotation.
  strcpy(idents[0], "Right ascension");
  strcpy(idents[1], "Declination");
  strcpy(idents[2], "WCS plate caree projection");

  opt[0] = 'G';
  opt[1] = 'E';

  // Reduced size lettering.
  cpgsch(0.7f*scl);

  // Draw full grid lines.
  gcode[0] = 2;
  gcode[1] = 2;

  cpgsci(1);

  grid1[0] = 0.0;
  grid2[0] = 0.0;

  ic = -1;
  cpgsbox(blc, trc, idents, opt, 2121, 1212, c0, gcode, 0.0, 0, grid1, 0,
    grid2, 1, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256,
    &ic, cache, &ierr);

  // Draw the frame.
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();

  //--------------------------------------------------------------------------
  // Cylindrical perspective projection.
  //   - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
  //   - BLC, TRC unrelated to pixel coordinates.
  //   - Demonstrate parameter definition for PGWCSL.
  //   - Reduced size lettering.
  //   - Manual and automatic choice of coordinate increments.
  //   - Suppression of common zero minute and second fields in sexagesimal
  //     time format.
  //--------------------------------------------------------------------------

  printf("\nCylindrical perspective projection\n");

  blc[0] = -180.0;
  blc[1] =  -90.0;
  trc[0] =  180.0;
  trc[1] =  +90.0;

  //  Reset viewport for rectangular image.
  if (large) {
    cpgvstd();
  } else {
    cpgvsiz(1.0f, 3.0f, 1.0f, 3.0f);
  }
  cpgwnad (blc[0], trc[0], blc[1], trc[1]);

  wcsini(1, 2, &wcs);

  // Set projection type to cylindrical perspective.
  strcpy(wcs.ctype[0], "RA---CYP");
  strcpy(wcs.ctype[1], "DEC--CYP");

  // Reference pixel coordinates.
  wcs.crpix[0] = 0.0;
  wcs.crpix[1] = 0.0;

  // Coordinate increments.
  wcs.cdelt[0] = -1.0;
  wcs.cdelt[1] =  1.0;

  // Set parameters to draw the native grid.
  wcs.crval[0] =  45.0;
  wcs.crval[1] = -90.0;
  wcs.lonpole  = 999.0;

  // mu and lambda projection parameters.
  wcs.npv = 2;
  wcs.pv[0].i = 2;
  wcs.pv[0].m = 1;
  wcs.pv[0].value = 0.0;
  wcs.pv[1].i = 2;
  wcs.pv[1].m = 2;
  wcs.pv[1].value = 1.0;

  // Annotation.
  strcpy(idents[0], "Right ascension");
  strcpy(idents[1], "Declination");
  strcpy(idents[2], "WCS cylindrical perspective projection");

  opt[0] = 'G';
  opt[1] = 'E';

  // Reduced size lettering.
  cpgsch(0.7f*scl);

  // Draw full grid lines.
  gcode[0] = 2;
  gcode[1] = 2;

  cpgsci(1);

  grid1[0] = 0.0;
  grid2[0] = 0.0;

  ic = -1;
  cpgsbox(blc, trc, idents, opt, 2121, 1212, c0, gcode, 0.0, 0, grid1, 0,
    grid2, 1, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256,
    &ic, cache, &ierr);

  // Draw the frame.
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();

  //--------------------------------------------------------------------------
  // Gnomonic projection.
  //   - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
  //   - Demonstrate parameter definition for PGWCSL.
  //   - Reduced size lettering.
  //   - Manual and automatic choice of coordinate increments.
  //   - Suppression of common zero minute and second fields in sexagesimal
  //     time format.
  //--------------------------------------------------------------------------

  printf("\nTAN projection\n");

  naxis[0] = 100;
  naxis[1] = 100;

  blc[0] = 0.5;
  blc[1] = 0.5;
  trc[0] = naxis[0] + 0.5;
  trc[1] = naxis[1] + 0.5;

  //  Reset viewport for rectangular image.
  if (large) {
    cpgvstd();
  } else {
    cpgvsiz(1.0f, 3.0f, 1.0f, 3.0f);
  }
  cpgwnad(0.0f, 1.0f, 0.0f, ((float)naxis[1])/((float)naxis[0]));

  wcsini(1, 2, &wcs);

  // Set projection type to gnomonic.
  strcpy(wcs.ctype[0], "RA---TAN");
  strcpy(wcs.ctype[1], "DEC--TAN");

  // Reference pixel coordinates.
  wcs.crpix[0] = 50.5;
  wcs.crpix[1] =  1.0;

  // Coordinate increments.
  wcs.cdelt[0] = 1e-3;
  wcs.cdelt[1] = 1e-3;

  // Set parameters to draw the native grid.
  wcs.crval[0] =  45.0;
  wcs.crval[1] = -89.7;
  wcs.lonpole  = 999.0;

  // Annotation.
  strcpy(idents[0], "Right ascension");
  strcpy(idents[1], "Declination");
  strcpy(idents[2], "WCS TAN projection");

  opt[0] = 'E';
  opt[1] = 'E';

  // Reduced size lettering.
  cpgsch(0.7f*scl);

  // Draw full grid lines.
  gcode[0] = 2;
  gcode[1] = 2;

  cpgsci(1);

  grid1[0] = 0.0;
  grid2[0] = 0.0;

  ic = -1;
  cpgsbox(blc, trc, idents, opt, 0, 1212, c0, gcode, 0.0, 0, grid1, 0,
    grid2, 0, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256,
    &ic, cache, &ierr);

  // Draw the frame.
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();

  //--------------------------------------------------------------------------
  // Linear-linear plot with two types of alternative labelling.
  //   - PGSBOX uses subroutine PGCRFN.
  //   - Separable (i.e. orthogonal), linear coordinate system.
  //   - Use of function PGCRFN for separable axis types.
  //   - Alternative labelling and axis annotation.
  //   - Direct manipulation of the axis-crossing table.
  //   - Tick mark and grid line control.
  //   - User selection of what edges to label.
  //   - Automatic choice of coordinate increments.
  //--------------------------------------------------------------------------

  printf("\nLinear plot with alternative labelling\n");

  if (large) {
    cpgvstd();
  } else {
    cpgvsiz(1.0f, 3.0f, 1.0f, 3.0f);
  }
  cpgwnad(0.0f, 1.0f, 0.0f, 1.0f);

  naxis[0] = 512;
  naxis[1] = 512;

  blc[0] = 0.5;
  blc[1] = 0.5;
  trc[0] = naxis[0] + 0.5;
  trc[1] = naxis[1] + 0.5;

  // Function types.
  memcpy(fcode[0], "Lin ", 4);
  memcpy(fcode[1], "Lin ", 4);

  // Reference pixel coordinates.
  nldprm[0] = 0.5;
  nldprm[1] = 0.5;

  // Coordinate increments.
  nldprm[2] = 0.03;
  nldprm[3] = 0.03;

  // Reference pixel values.
  nldprm[4] = 20.0;
  nldprm[5] =  0.0;

  // Annotation.
  strcpy(idents[0], "temperature of frog (\\uo\\dC)");
  strcpy(idents[1], "distance hopped (m)");
  strcpy(idents[2], "");

  opt[0] = ' ';
  opt[1] = ' ';

  // Reduced size lettering.
  cpgsch(0.8f*scl);

  // Draw tick marks at the bottom for the first coordinate, grid lines
  // for the second.  Setting GCODE[0] = -1 inhibits information being
  // stored for labels on the top edge while GCODE[1] = 2 causes
  // information to be stored for labels on the right edge even if those
  // labels are not actually produced.
  cpgsci(1);
  gcode[0] = -1;
  gcode[1] =  2;
  grid1[0] = 0.0;
  grid2[0] = 0.0;

  // Set LABCTL = 21 to label the bottom and left edges only.
  ic = -1;
  cpgsbox(blc, trc, idents, opt, 21, 0, c0, gcode, 2.0, 0, grid1, 0, grid2,
    0, pgcrfn_, 8, 2, 4, fcode[0], nliprm, nldprm, 256, &ic, cache, &ierr);

  // Information for labels on the right edge was stored in the crossing
  // table on the first call to PGSBOX.  We now want to manipulate it to
  // convert metres to feet.  Note that while it's a simple matter to draw
  // alternative sets of tick marks on opposite edges of the frame, as
  // with the two temperature scales, we have the slightly more difficult
  // requirement of labelling grid lines with different values at each
  // end.
  for (int j = 0; j <= ic; j++) {
    // Look for entries associated with the right edge of the frame.
    if (cache[j][0] == 4.0) {
      // Convert to feet, rounding to the nearest 0.1.
      cache[j][3] *= 1e3/(25.4*12.0);
      cache[j][3] = floor(cache[j][3]*10.0 + 0.5)/10.0;
    }
  }

  // Annotation for the right edge.
  strcpy(idents[0], "");
  strcpy(idents[1], "(feet)");

  // Set LABCTL = 12000 to label the right edge with the second coordinate
  // without redrawing the grid lines.
  cpgsbox(blc, trc, idents, opt, 12000, 0, c0, gcode, 2.0, 0, grid1, 0,
    grid2, 0, pgcrfn_, 8, 2, 4, fcode[0], nliprm, nldprm, 256, &ic, cache,
    &ierr);

  // The alternative temperature scale in Fahrenheit is to be constructed
  // with a new set of tick marks.
  nldprm[2] = nldprm[2]*1.8;
  nldprm[4] = nldprm[4]*1.8 + 32.0;

  // Draw tick marks at the top for the first coordinate, don't redo grid
  // lines for the second.
  gcode[0] = -100;
  gcode[1] = 0;

  // Annotation for the top edge.
  strcpy(idents[0], "(\\uo\\dF)");
  strcpy(idents[1], "");

  // Set LABCTL = 100 to label the top edge; Set IC = -1 to redetermine
  // the coordinate extrema.
  ic = -1;
  cpgsbox(blc, trc, idents, opt, 100, 0, c0, gcode, 2.0, 0, grid1, 0, grid2,
    0, pgcrfn_, 8, 2, 4, fcode[0], nliprm, nldprm, 256, &ic, cache, &ierr);

  // Draw the frame.
  cpgbox("bc", 0.0f, 0, "bc", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();

  //--------------------------------------------------------------------------
  // Calendar axes using subroutine PGLBOX.
  //   - Separable (i.e. orthogonal), linear coordinate system.
  //   - Use of PGLBOX for simple linear axis types.
  //   - Automatic choice of what edges to label; results in labelling the
  //     bottom and left sides of the plot.
  //   - Automatic choice of coordinate increments.
  //   - Calendar date axis labelling.
  //   - Single-character annotation on a vertical axis is upright.
  //--------------------------------------------------------------------------

  printf("\nCalendar axes using subroutine PGLBOX\n");

  cpgswin(51900.0f, 52412.0f, 51900.0f, 57020.0f);

  // Annotation.
  strcpy(idents[0], "Date started");
  strcpy(idents[1], "Date finished");
  strcpy(idents[2], "Calendar axes using subroutine PGLBOX");

  opt[0] = 'Y';
  opt[1] = 'Y';

  // Reduced size lettering.
  cpgsch(0.7f*scl);

  // Draw tick marks on each axis.
  cpgsci(1);
  gcode[0] = 1;
  gcode[1] = 1;
  grid1[0] = 0.0;
  grid2[0] = 0.0;

  ic = -1;
  cpglbox(idents, opt, 0, 0, c0, gcode, 2.0, 0, grid1, 0, grid2, 0, 256, &ic,
    cache, &ierr);

  // Draw the frame.
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();

  //--------------------------------------------------------------------------
  // Simple linear axes handled by PGWCSL.
  //   - Separable (i.e. orthogonal), linear coordinate system.
  //   - Automatic choice of what edges to label; results in labelling the
  //     bottom and left sides of the plot.
  //   - Automatic choice of coordinate increments.
  //   - Tick marks and labels at the edges of the frame.
  //   - Single-character annotation on a vertical axis is upright.
  //--------------------------------------------------------------------------

  printf("\nSimple linear axes handled by pgwcsl()\n");

  naxis[0] = 3;
  naxis[1] = 3;

  blc[0] = 0.5;
  blc[1] = 0.5;
  trc[0] = naxis[0] + 0.5;
  trc[1] = naxis[1] + 0.5;

  wcsini(1, 2, &wcs);

  strcpy(wcs.ctype[0], "x");
  strcpy(wcs.ctype[1], "y");

  // Reference pixel coordinates.
  wcs.crpix[0] = 2.0;
  wcs.crpix[1] = 2.0;

  // Coordinate increments.
  wcs.cdelt[0] = 1.0;
  wcs.cdelt[1] = 1.0;

  // Spherical coordinate references.
  wcs.crval[0] = 2.0;
  wcs.crval[1] = 2.0;

  // Annotation.
  strcpy(idents[0], "X");
  strcpy(idents[1], "Y");
  strcpy(idents[2], "Simple linear axes handled by pgwcsl()");

  opt[0] = ' ';
  opt[1] = ' ';

  // Reduced size lettering.
  cpgsch(0.8f*scl);

  // Draw full grid lines.
  cpgsci(1);
  gcode[0] = 1;
  gcode[1] = 1;

  grid1[0] = 0.0;
  grid2[0] = 0.0;

  ic = -1;
  cpgsbox(blc, trc, idents, opt, 0, 0, c0, gcode, 2.0, 0, grid1, 0, grid2,
    0, pgwcsl_, 1, WCSLEN, 1, nlcprm, (int *)(&wcs), nldprm, 256, &ic,
    cache, &ierr);

  // Draw the frame.
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  nanosleep(&nano, 0x0);
  cpgpage();

  //--------------------------------------------------------------------------

  wcsfree(&wcs);

  cpgask(0);
  cpgend();

  return 0;
}
