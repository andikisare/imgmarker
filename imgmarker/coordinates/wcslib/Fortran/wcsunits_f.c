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
  $Id: wcsunits_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*===========================================================================*/

#include <stdio.h>
#include <string.h>

#include <wcsutil.h>
#include <wcsunits.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define wcsunitse_ F77_FUNC(wcsunitse, WCSUNITSE)
#define wcsutrne_  F77_FUNC(wcsutrne,  WCSUTRNE)
#define wcsulexe_  F77_FUNC(wcsulexe,  WCSULEXE)

// Deprecated.
#define wcsunits_ F77_FUNC(wcsunits, WCSUNITS)
#define wcsutrn_  F77_FUNC(wcsutrn,  WCSUTRN)
#define wcsulex_  F77_FUNC(wcsulex,  WCSULEX)

#ifdef BINDC
  #undef  wcsunitse_
  #define wcsunitse_ wcsunitse_c

  #undef  wcsutrne_
  #define wcsutrne_ wcsutrne_c

  #undef  wcsulexe_
  #define wcsulexe_ wcsulexe_c

  #undef  wcsunits_
  #define wcsunits_ wcsunits_c

  #undef  wcsutrn_
  #define wcsutrn_ wcsutrn_c

  #undef  wcsulex_
  #define wcsulex_ wcsulex_c
#endif

//----------------------------------------------------------------------------

int wcsunitse_(
  const char have[72],
  const char want[72],
  double *scale,
  double *offset,
  double *power,
  iptr err)

{
  char have_[73], want_[73];
  wcsutil_strcvt(72, '\0', 1, have, have_);
  wcsutil_strcvt(72, '\0', 1, want, want_);

  return wcsunitse(have_, want_, scale, offset, power, (struct wcserr **)err);
}

// : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : :

int wcsunits_(
  const char have[72],
  const char want[72],
  double *scale,
  double *offset,
  double *power)

{
  return wcsunitse_(have, want, scale, offset, power, 0x0);
}

//----------------------------------------------------------------------------

int wcsutrne_(
  const int *ctrl,
  char unitstr[72],
  iptr err)

{
  char unitstr_[73];
  wcsutil_strcvt(72, '\0', 1, unitstr, unitstr_);

  // This may or may not force the Fortran I/O buffers to be flushed.  If
  // not, try CALL FLUSH(6) before calling WCSUTRNE in the Fortran code.
  fflush(NULL);

  int status = wcsutrne(*ctrl, unitstr_, (struct wcserr **)err);

  wcsutil_strcvt(72, ' ', 0, unitstr_, unitstr);

  return status;
}

// : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : :

int wcsutrn_(
  const int *ctrl,
  char unitstr[72])

{
  return wcsutrne_(ctrl, unitstr, 0x0);
}

//----------------------------------------------------------------------------

int wcsulexe_(
  const char unitstr[72],
  int *func,
  double *scale,
  double units[WCSUNITS_NTYPE],
  iptr err)

{
  char unitstr_[73];
  wcsutil_strcvt(72, '\0', 1, unitstr, unitstr_);

  // This may or may not force the Fortran I/O buffers to be flushed.  If
  // not, try CALL FLUSH(6) before calling WCSULEXE in the Fortran code.
  fflush(NULL);

  return wcsulexe(unitstr_, func, scale, units, (struct wcserr **)err);
}

// : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : :

int wcsulex_(
  const char unitstr[72],
  int *func,
  double *scale,
  double units[WCSUNITS_NTYPE])

{
  return wcsulexe_(unitstr, func, scale, units, 0x0);
}
