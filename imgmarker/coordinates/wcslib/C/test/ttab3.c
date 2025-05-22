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
  $Id: ttab3.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=============================================================================
*
* ttab3 tests the -TAB routines using PGPLOT for graphical display.  It
* constructs a table that approximates Bonne's projection and uses it to
* draw a graticule.
*
*---------------------------------------------------------------------------*/

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <cpgplot.h>

#include <prj.h>
#include <tab.h>

// Lookup table parameters.
const int M  = 2;
const int K1 = 271;
const int K2 = 235;
const int map[] = {0, 1};
const double crval[] = {135.0, 95.0};


int main()

{
  printf(
    "Testing WCSLIB inverse coordinate lookup table routines (ttab3.c)\n"
    "-----------------------------------------------------------------\n");

  // List status return messages.
  int status;
  printf("\nList of tab status return values:\n");
  for (status = 1; status <= 5; status++) {
    printf("%4d: %s.\n", status, tab_errmsg[status]);
  }

  printf("\n");


  // PGPLOT initialization.
  char text[80];
  strcpy(text, "/xwindow");
  cpgbeg(0, text, 1, 1);
  cpgvstd();
  cpgsch(0.7f);
  cpgwnad(-135.0f, 135.0f, -95.0f, 140.0f);
  cpgbox("BC", 0.0f, 0, "BC", 0.0f, 0);

  cpgscr(0, 0.00f, 0.00f, 0.00f);
  cpgscr(1, 1.00f, 1.00f, 0.00f);
  cpgscr(2, 1.00f, 1.00f, 1.00f);
  cpgscr(3, 0.50f, 0.50f, 0.80f);
  cpgscr(4, 0.80f, 0.50f, 0.50f);
  cpgscr(5, 0.80f, 0.80f, 0.80f);
  cpgscr(6, 0.50f, 0.50f, 0.80f);
  cpgscr(7, 0.80f, 0.50f, 0.50f);
  cpgscr(8, 0.30f, 0.50f, 0.30f);


  // Set up the lookup table.
  int K[] = {K1, K2};
  struct tabprm tab;
  tab.flag = -1;
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

  // Set up the lookup table to approximate Bonne's projection.
  double x[K1], y[K2];
  for (int i = 0; i < K1; i++) {
    x[i] = (double)(135 - i);
  }
  for (int j = 0; j < K2; j++) {
    y[j] = (double)(j - 95);
  }

  struct prjprm prj;
  prjini(&prj);
  prj.pv[1] = 35.0;

  // Disable bounds checking (or alternatively, simply ignore out-of-bounds
  // errors).  This is necessary to provide continuity beyond the -180 and
  // +180 meridians, noting that bonx2s() computes out-of-bounds values so
  // as to provide continuity.
  prj.bounds = 0;

  int stat[K2*K1];
  status = bonx2s(&prj, K1, K2, 1, 2, x, y, tab.coord, tab.coord+1, stat);


  float xr[361], yr[361];
  double world[361][2], xy[361][2];

  // Draw meridians.
  for (int ilng = -180, ci = 1; ilng <= 180; ilng += 15) {
    if (++ci > 7) ci = 2;
    cpgsci(ilng?ci:1);

    for (int ilat = -90, j = 0; ilat <= 90; ilat++, j++) {
      world[j][0] = (double)ilng;
      world[j][1] = (double)ilat;
    }

    // A fudge to account for the singularity at the poles.
    world[0][0] = 0.0;
    world[180][0] = 0.0;

    status = tabs2x(&tab, 181, 2, world[0], xy[0], stat);

    int k = 0;
    for (int j = 0; j < 181; j++) {
      if (stat[j]) {
        if (k > 1) cpgline(k, xr, yr);
        k = 0;
        continue;
      }

      xr[k] = xy[j][0];
      yr[k] = xy[j][1];
      k++;
    }

    cpgline(k, xr, yr);
  }


  // Draw parallels.
  for (int ilat = -75, ci = 1; ilat <= 75; ilat += 15) {
    if (++ci > 7) ci = 2;
    cpgsci(ilat?ci:1);

    for (int ilng = -180, j = 0; ilng <= 180; ilng++, j++) {
      world[j][0] = (double)ilng;
      world[j][1] = (double)ilat;
    }

    status = tabs2x(&tab, 361, 2, world[0], xy[0], stat);

    int k = 0;
    for (int j = 0; j < 361; j++) {
      if (stat[j]) {
        if (k > 1) cpgline(k, xr, yr);
        k = 0;
        continue;
      }

      xr[k] = xy[j][0];
      yr[k] = xy[j][1];
      k++;
    }

    cpgline(k, xr, yr);
  }

  cpgend();

  // Defeat spurious reporting of memory leaks.
  tabfree(&tab);

  return 0;
}
