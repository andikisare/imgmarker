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
  $Id: ttab2.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=============================================================================
*
* ttab2 tests the -TAB routines using PGPLOT for graphical display.  It
* demonstrates the nature of linear interpolation in 2 dimensions by
* contouring the interior of a single 2 x 2 interpolation element as the
* values in each corner change.
*
*---------------------------------------------------------------------------*/

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <cpgplot.h>

#include <tab.h>

// 2 x 2 lookup table parameters.
const int M  = 2;
const int K1 = 2;
const int K2 = 2;
const int map[] = {0, 1};
const double crval[] = {0.0, 0.0};

// Number of subdivisions on each side of the interpolation element.
const int NP = 128;


int main()

{
  printf("Testing WCSLIB coordinate lookup table routines (ttab2.c)\n"
         "---------------------------------------------------------\n");

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

  // The viewport is slightly oversized.
  cpgwnad(-0.65f, 1.65f, -0.65f, 1.65f);

  float clev[31];
  for (int l = 0; l <= 30; l++) {
    clev[l] = 0.2f*(l-10);
  }

  float ltm[6];
  const float scl = 2.0f / (NP-1);
  ltm[0] = -scl*(1.0f + (NP-1)/4.0f);
  ltm[1] =  scl;
  ltm[2] =  0.0f;
  ltm[3] = -scl*(1.0f + (NP-1)/4.0f);
  ltm[4] =  0.0f;
  ltm[5] =  scl;


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

  // Subdivide the interpolation element.
  double x[NP][NP][2];
  for (int i = 0; i < NP; i++) {
    for (int j = 0; j < NP; j++) {
      x[i][j][0] = j*(K1-1.0)*scl - 0.5 - crval[0];
      x[i][j][1] = i*(K2-1.0)*scl - 0.5 - crval[1];
    }
  }

  // The first coordinate element is static.
  tab.coord[0] = 0.0;
  tab.coord[2] = 0.0;
  tab.coord[4] = 0.0;
  tab.coord[6] = 0.0;

  // (k1,k2) = (0,0).
  tab.coord[1] = 0.0;

  // The second coordinate element varies in three of the corners.
  for (int l3 = 0; l3 <= 100; l3 += 20) {
    // (k1,k2) = (1,1).
    tab.coord[7] = 0.01 * l3;

    for (int l2 = 0; l2 <= 100; l2 += 20) {
      // (k1,k2) = (0,1).
      tab.coord[5] = 0.01 * l2;

      cpgpage();
      for (int l1 = 0; l1 <= 100; l1 += 2) {
        // (k1,k2) = (1,0).
        tab.coord[3] = 0.01 * l1;

        // Compute coordinates within the interpolation element.
        tab.flag = 0;
        int stat[NP*NP];
        double world[NP][NP][2];
        if ((status = tabx2s(&tab, NP*NP, 2, (double *)x, (double *)world,
                             stat))) {
          printf("tabx2s ERROR %d: %s.\n", status, tab_errmsg[status]);
        }

        // Start a new plot.
        cpgbbuf();
        cpgeras();
        cpgsci(1);
        cpgslw(3);
        cpgbox("BCNST", 0.0f, 0, "BCNSTV", 0.0f, 0);
        cpgmtxt("T", 0.7f, 0.5f, 0.5f, "-TAB coordinates:  "
          "linear interpolation / extrapolation in 2-D");

        // Draw the boundary of the interpolation element in red.
        cpgsci(2);
        cpgmove(-0.5f,  0.0f);
        cpgdraw( 1.5f,  0.0f);

        cpgmove( 1.0f, -0.5f);
        cpgdraw( 1.0f,  1.5f);

        cpgmove( 1.5f,  1.0f);
        cpgdraw(-0.5f,  1.0f);

        cpgmove( 0.0f,  1.5f);
        cpgdraw( 0.0f, -0.5f);

        // Label the value of the coordinate element in each corner.
        sprintf(text, "%.1f", tab.coord[1]);
        cpgtext(-0.09f, -0.05f, text);
        sprintf(text, "%.2f", tab.coord[3]);
        cpgtext( 1.02f, -0.05f, text);
        sprintf(text, "%.1f", tab.coord[5]);
        cpgtext(-0.13f,  1.02f, text);
        sprintf(text, "%.1f", tab.coord[7]);
        cpgtext( 1.02f,  1.02f, text);

        cpgsci(1);
        float v0, v1;

        // Contour labelling: bottom.
        v0 = world[0][0][1];
        v1 = world[0][NP-1][1];
        if (v0 != v1) {
          int lstep = (abs((int)((v1-v0)/0.2f)) < 10) ? 20 : 40;
          for (int l = -200; l <= 300; l += lstep) {
            float w = -0.5f + 2.0f * (l*0.01f - v0) / (v1 - v0);
            if (w < -0.5 || w > 1.5) continue;

            sprintf(text, "%4.1f", l*0.01f);
            cpgptxt(w+0.04f, -0.56f, 0.0f, 1.0f, text);
          }
        }

        // Contour labelling: left.
        v0 = world[0][0][1];
        v1 = world[NP-1][0][1];
        if (v0 != v1) {
          int lstep = (abs((int)((v1-v0)/0.2f)) < 10) ? 20 : 40;
          for (int l = -200; l <= 300; l += lstep) {
            float w = -0.5f + 2.0f * (l*0.01f - v0) / (v1 - v0);
            if (w < -0.5 || w > 1.5) continue;

            sprintf(text, "%4.1f", l*0.01f);
            cpgptxt(-0.52f, w-0.02f, 0.0f, 1.0f, text);
          }
        }

        // Contour labelling: right.
        v0 = world[0][NP-1][1];
        v1 = world[NP-1][NP-1][1];
        if (v0 != v1) {
          int lstep = (abs((int)((v1-v0)/0.2f)) < 10) ? 20 : 40;
          for (int l = -200; l <= 300; l += lstep) {
            float w = -0.5f + 2.0f * (l*0.01f - v0) / (v1 - v0);
            if (w < -0.5 || w > 1.5) continue;

            sprintf(text, "%.1f", l*0.01f);
            cpgptxt(1.52f, w-0.02f, 0.0f, 0.0f, text);
          }
        }

        // Contour labelling: top.
        v0 = world[NP-1][0][1];
        v1 = world[NP-1][NP-1][1];
        if (v0 != v1) {
          int lstep = (abs((int)((v1-v0)/0.2f)) < 10) ? 20 : 40;
          for (int l = -200; l <= 300; l += lstep) {
            float w = -0.5f + 2.0f * (l*0.01f - v0) / (v1 - v0);
            if (w < -0.5 || w > 1.5) continue;

            sprintf(text, "%4.1f", l*0.01f);
            cpgptxt(w+0.04f, 1.52f, 0.0f, 1.0f, text);
          }
        }

        // Draw contours for the second coordinate element.
        float array[NP][NP];
        for (int i = 0; i < NP; i++) {
          for (int j = 0; j < NP; j++) {
            array[i][j] = world[i][j][1];
          }
        }

        cpgsci(4);
        cpgslw(2);
        cpgcont(array[0], NP, NP, 1, NP, 1, NP, clev, 10, ltm);

        cpgsci(7);
        cpgcont(array[0], NP, NP, 1, NP, 1, NP, clev+10, 1, ltm);

        cpgsci(5);
        cpgcont(array[0], NP, NP, 1, NP, 1, NP, clev+11, 20, ltm);

        cpgebuf();
      }
    }
  }

  cpgend();

  tabfree(&tab);

  return 0;
}
