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
  $Id: getwcstab_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*===========================================================================*/

#include <getwcstab.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define ftwcst_ F77_FUNC(ftwcst, FTWCST)

// CFITSIO global variable defined by/for the FITSIO wrappers that maps
// Fortran unit numbers to fitsfile *; see f77_wrap.h and f77_wrap1.c.
extern fitsfile *gFitsFiles[];

//----------------------------------------------------------------------------

int ftwcst_(
  int *unit,
  int *nwtb,
  int *wtb,
  int *status)

{
  // *wtb is meant to hold a pointer to a wtbarr struct.  On 64-bit machines
  // sizeof(void *) = 2 * sizeof(int) = sizeof(long).
  long wtbp = *((long *)wtb);
  return fits_read_wcstab(gFitsFiles[*unit], *nwtb, (void *)wtbp, status);
}
