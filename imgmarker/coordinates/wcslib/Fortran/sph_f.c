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
  $Id: sph_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*===========================================================================*/

#include <sph.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define sphx2s_ F77_FUNC(sphx2s, SPHX2S)
#define sphs2x_ F77_FUNC(sphs2x, SPHS2X)
#define sphdpa_ F77_FUNC(sphdpa, SPHDPA)
#define sphpad_ F77_FUNC(sphpad, SPHPAD)

//----------------------------------------------------------------------------

int sphx2s_(
  const double eul[5],
  const int *nphi,
  const int *ntheta,
  const int *spt,
  const int *sll,
  const double phi[],
  const double theta[],
  double lng[],
  double lat[])

{
  return sphx2s(eul, *nphi, *ntheta, *spt, *sll, phi, theta, lng, lat);
}

//----------------------------------------------------------------------------

int sphs2x_(
  const double eul[5],
  const int *nlng,
  const int *nlat,
  const int *sll,
  const int *spt,
  const double lng[],
  const double lat[],
  double phi[],
  double theta[])

{
  return sphs2x(eul, *nlng, *nlat, *sll, *spt, lng, lat, phi, theta);
}

//----------------------------------------------------------------------------

int sphdpa_(
  const int *nfield,
  const double *lng0,
  const double *lat0,
  const double lng[],
  const double lat[],
  double dist[],
  double pa[])

{
  return sphdpa(*nfield, *lng0, *lat0, lng, lat, dist, pa);
}

//----------------------------------------------------------------------------

int sphpad_(
  const int *nfield,
  const double *lng0,
  const double *lat0,
  const double dist[],
  const double pa[],
  double lng[],
  double lat[])

{
  return sphpad(*nfield, *lng0, *lat0, dist, pa, lng, lat);
}
