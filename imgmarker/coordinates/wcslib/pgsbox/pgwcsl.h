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
  $Id: pgwcsl.h,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
*=============================================================================
*
*   pgwcsl_() is an NLFUNC for PGSBOX that defines curvilinear celestial
*   coordinate systems by interfacing to WCSLIB 4.x.
*
*   Since WCSLIB 4.x is a C library, pgwcsl_() is written in C.  However, as
*   PGSBOX expects NLFUNC to be a FORTRAN subroutine, its interfaces
*   necessarily emulate those of a FORTRAN subroutine.  Hence the trailing
*   underscore in the name of the function and the pointer (reference)
*   argument list.
*
*   The wcsprm struct on which WCSLIB 4.x is based is passed as an integer
*   array of size WCSLEN at least (WCSLEN is defined in wcs.h).  While the
*   contents of this array are not interpretable in FORTRAN, it may be
*   constructed and interrogated by service routines (WCSPUT and WCSGET)
*   provided with the FORTRAN wrappers for WCSLIB 4.x.  The array is cast to
*   (struct wcsprm *) for use here and in WCSLIB.
*
*   Given:
*      opcode   int*     Transformation code:
*                            2: Compute a set of pixel coordinates that
*                               describe a path between this and the previous
*                               pair of world coordinates remembered from the
*                               last call with opcode == 1 || 2.
*                            1: Compute pixel coordinates from world
*                               coordinates.
*                            0: Initialize.
*                           -1: Compute world coordinates from pixel
*                               coordinates.
*
*      nlc      int*     Number of elements in nlcprm[] (not used).
*
*      nli      int*     Number of elements in wcs (at least WCSLEN).
*
*      nld      int*     Number of elements in nldprm (not used).
*
*      nlcprm   char[nlc]
*                        Character array (not used).
*
*   Given and/or returned:
*      wcs      int[nli] Integer array that contains the wcsprm struct (see
*                        below).
*
*      nldprm   double[nld]
*                        Double precision array (not used).
*
*      world    double[2]
*                        World coordinates.  world[0] and world[1] are the
*                        longitude and latitude, in degrees.  Given if
*                        opcode > 0, returned if opcode < 0.
*
*      pixel    double[2]
*                        Pixel coordinates.  Given if opcode < 0, returned if
*                        opcode > 0.
*
*      contrl   int*     Control flag for opcode == 2:
*                           0: Normal state
*                           1: A discontinuity has been encountered; force
*                              PGSBOX to flush its plotting buffer and call
*                              pgwcsl_() again with the same world
*                              coordinates.
*                           2: Call pgwcsl_() again with the same world
*                              coordinates.
*
*      contxt   double[20]
*                        Context elements for opcode == 2.
*
*   Returned:
*      ierr     int*     Status return value:
*                           0: Success.
*                           1: Invalid parameters.
*                           2: Invalid world coordinate.
*                           3: Invalid pixel coordinate.
*
*   Notes
*   -----
*    1) pgwcsl_() assumes a simple 2-D image.
*
*    2) The wcsprm struct (contained in the wcs[] array) is maintained by
*       pgwcsl_() and WCSLIB and must not be disturbed by the caller after
*       initialization with opcode == 0.
*
*    3) pgwcsl_() doesn't properly handle discontinuities between the faces
*       of the quadcube projections nor in the polar region of the HPX
*       projection.
*
*
*===========================================================================*/
#ifndef PGSBOX_PGWCSL
#define PGSBOX_PGWCSL

#include "cpgsbox.h"

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define pgwcsl_ F77_FUNC(pgwcsl, PGWCSL)

#ifdef __cplusplus
extern "C" {
#endif

nlfunc_t pgwcsl_;
nlfunc_t pgwcsl_c;

#ifdef __cplusplus
}
#endif

#endif // PGSBOX_PGWCSL
