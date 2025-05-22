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
  $Id: pgwcsl.c,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
*===========================================================================*/

#include <math.h>

#include <wcs.h>
#include <sph.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define pgwcsl_ F77_FUNC(pgwcsl, PGWCSL)

#ifdef BINDC
  #undef  pgwcsl_
  #define pgwcsl_ pgwcsl_c
#endif

void pgwcsl_(
  const int *opcode,
  const int *nlc,
  const int *nli,
  const int *nld,
  const char *nlcprm,
  int    *wcs,
  double *nldprm,
  double *world,
  double *pixel,
  int    *contrl,
  double contxt[20],
  int    *ierr)

{
  // Avert nuisance compiler warnings about unused parameters.
  (void)nlc;
  (void)nld;
  (void)nlcprm;
  (void)nldprm;

  int    stat;
  double imgcrd[9], phi, theta;
  static double wrld[9];

  struct wcsprm *wcsp = (struct wcsprm *)wcs;
  struct celprm *wcscel = &(wcsp->cel);

  *ierr = 0;

  if (*opcode == 2) {
    // Compute pixel coordinates from world coordinates.
    if (wcsp->lng < 0) {
      // Simple linear coordinates.
      if (wcss2p(wcsp, 1, 0, world, &phi, &theta, imgcrd, pixel, &stat)) {
        *ierr = 1;
      }
      return;
    }

    wrld[wcsp->lng] = world[0];
    int outside;
    if (world[1] > 90.0) {
      wrld[wcsp->lat] = 90.0;
      outside = -2;
    } else if (world[1] < -90.0) {
      wrld[wcsp->lat] = -90.0;
      outside = -2;
    } else {
      wrld[wcsp->lat] = world[1];
      outside = 0;
    }

    if (*contrl == 0) {
      if (wcss2p(wcsp, 1, 0, wrld, &phi, &theta, imgcrd, pixel, &stat)) {
        // Translate status return values.
        *ierr = stat ? 2 : 1;
        return;
      }

      if (fabs(phi-contxt[2]) > 180.0) {
        // Hit a discontinuity at phi = +/- 180.
        contxt[4] = pixel[0];
        contxt[5] = pixel[1];

        double ph, dp;
        if (contxt[2] > phi) {
          ph = 179.9999;
          dp = (phi - contxt[2]) + 360.0;
        } else {
          ph = -179.9999;
          dp = (phi - contxt[2]) - 360.0;
        }

        // First approximation for theta.
        double th;
        if (dp == 0.0) {
          th = contxt[3];
        } else {
          th = contxt[3] + (ph-contxt[2])*(theta-contxt[3])/dp;
        }

        // Iterate once to refine the value of theta.
        double lng, lat;
        sphx2s(wcscel->euler, 1, 1, 1, 1, &ph, &th, &lng, &lat);
        if (wrld[wcsp->lng] == contxt[0]) {
          // We are following a meridian of longitude.
          lng = wrld[wcsp->lng];
        } else {
          // We are following a parallel of latitude.
          lat = wrld[wcsp->lat];
        }

        double sdummy;
        sphs2x(wcscel->euler, 1, 1, 1, 1, &lng, &lat, &sdummy, &th);

        contxt[0] = wrld[wcsp->lng];
        contxt[1] = wrld[wcsp->lat];
        contxt[2] = phi;
        contxt[3] = theta;

        // Pixel coordinates crossing into the discontinuity.
        sphx2s(wcscel->euler, 1, 1, 1, 1, &ph, &th, wrld+wcsp->lng,
          wrld+wcsp->lat);
        if (wcss2p(wcsp, 1, 0, wrld, &phi, &theta, imgcrd, pixel, &stat)) {
          // Translate status return values.
          *ierr = stat ? 2 : 1;
          return;
        }

        // Pixel coordinates crossing out of the discontinuity.
        ph *= -1.0;
        sphx2s(wcscel->euler, 1, 1, 1, 1, &ph, &th, wrld+wcsp->lng,
          wrld+wcsp->lat);
        if (wcss2p(wcsp, 1, 0, wrld, &phi, &theta, imgcrd, contxt+6, &stat)) {
          // Translate status return values.
          *ierr = stat ? 2 : 1;
          return;
        }

        *contrl = 1;
      } else {
        // Normal mode, no discontinuity.
        contxt[0] = wrld[wcsp->lng];
        contxt[1] = wrld[wcsp->lat];
        contxt[2] = phi;
        contxt[3] = theta;
      }
    } else {
      if (*contrl == 1) {
        // Move to the other side of the discontinuity.
        pixel[0] = contxt[6];
        pixel[1] = contxt[7];
        *contrl = 2;
      } else {
        // Complete the traversal.
        pixel[0] = contxt[4];
        pixel[1] = contxt[5];
        *contrl = 0;
      }
    }

    *ierr = outside;

  } else if (*opcode == 1) {
    // Compute pixel coordinates from world coordinates.
    if (wcsp->lng < 0) {
      // Simple linear coordinates.
      if (wcss2p(wcsp, 1, 0, world, &phi, &theta, imgcrd, pixel, &stat)) {
        *ierr = 1;
      }
      return;
    }

    wrld[wcsp->lng] = world[0];
    int outside;
    if (world[1] > 90.0) {
      wrld[wcsp->lat] = 90.0;
      outside = -2;
    } else if (world[1] < -90.0) {
      wrld[wcsp->lat] = -90.0;
      outside = -2;
    } else {
      wrld[wcsp->lat] = world[1];
      outside = 0;
    }

    if (wcss2p(wcsp, 1, 0, wrld, &phi, &theta, imgcrd, pixel, &stat)) {
      // Translate status return values.
      *ierr = stat ? 2 : 1;
      return;
    }

    contxt[0] = wrld[wcsp->lng];
    contxt[1] = wrld[wcsp->lat];
    contxt[2] = phi;
    contxt[3] = theta;

    *ierr = outside;

  } else if (*opcode == 0) {
    // Initialize.
    if (*nli < (int)WCSLEN) {
      *ierr = 1;
      return;
    }

    if ((*ierr = wcsset(wcsp))) {
      *ierr = *ierr <= 2 ? 1 : 2;
    }

    for (int i = 2; i < 9; i++) {
      wrld[i] = 0.0;
    }

    *contrl = 0;

  } else if (*opcode == -1) {
    // Compute world coordinates from pixel coordinates.
    if (wcsp2s(wcsp, 1, 0, pixel, imgcrd, &phi, &theta, wrld, &stat)) {
      // Translate status return values.
      *ierr = stat ? 3 : 1;
      return;
    }

    if (wcsp->lng < 0) {
      // Simple linear coordinates.
      world[0] = wrld[0];
      world[1] = wrld[1];
    } else {
      world[0] = wrld[wcsp->lng];
      world[1] = wrld[wcsp->lat];

      if (phi < -180.0 || phi > 180.0) {
        // Pixel is outside the principle range of native longitude.
        *ierr = 3;
        return;
      }
    }

  } else {
    *ierr = 1;
  }

  return;
}
