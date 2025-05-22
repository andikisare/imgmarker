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
  $Id: wcserr_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*===========================================================================*/

#include <stdio.h>
#include <string.h>

#include <wcserr.h>
#include <wcsutil.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define wcserr_get_  F77_FUNC(wcserr_get, WCSERR_GET)
#define wcserr_gtc_  F77_FUNC(wcserr_gtc, WCSERR_GTC)
#define wcserr_gti_  F77_FUNC(wcserr_gti, WCSERR_GTI)

#define wcserr_enable_  F77_FUNC(wcserr_enable, WCSERR_ENABLE)
#define wcserr_size_    F77_FUNC(wcserr_size, WCSERR_SIZE)
#define wcserr_prt_     F77_FUNC(wcserr_prt, WCSERR_PRT)
#define wcserr_clear_   F77_FUNC(wcserr_clear, WCSERR_CLEAR)

#ifdef BINDC
  #undef  wcserr_gtc_
  #define wcserr_gtc_ wcserr_gtc_c

  #undef  wcserr_prt_
  #define wcserr_prt_ wcserr_prt_c
#endif

// Must match the values set in wcserr.inc.
#define WCSERR_STATUS   200
#define WCSERR_LINE_NO  201
#define WCSERR_FUNCTION 202
#define WCSERR_FILE     203
#define WCSERR_MSG      204

#define WCSERR_MSG_LENGTH 512

//----------------------------------------------------------------------------

int wcserr_get_(const int *err, const int *what, void *value)

{
  char   *cvalp;
  int    *ivalp;
  const struct wcserr *errp;

  // Cast pointers.
  errp  = (const struct wcserr *)err;
  cvalp = (char *)value;
  ivalp = (int *)value;

  switch (*what) {
  case WCSERR_STATUS:
    *ivalp = errp->status;
    break;
  case WCSERR_LINE_NO:
    *ivalp = errp->line_no;
    break;
  case WCSERR_FUNCTION:
    wcsutil_strcvt(72, ' ', 0, errp->function, cvalp);
    break;
  case WCSERR_FILE:
    wcsutil_strcvt(72, ' ', 0, errp->file, cvalp);
    break;
  case WCSERR_MSG:
    // The character variable must be of length WCSERR_MSG_LENGTH.
    if (errp) {
      wcsutil_strcvt(WCSERR_MSG_LENGTH, ' ', 0, errp->msg, cvalp);
    } else {
      wcsutil_strcvt(WCSERR_MSG_LENGTH, ' ', 0, "", cvalp);
    }
    break;
  default:
    return 1;
  }

  return 0;
}

int wcserr_gtc_(const int *err, const int *what, char *value)
{
  return wcserr_get_(err, what, value);
}

int wcserr_gti_(const int *err, const int *what, int *value)
{
  return wcserr_get_(err, what, value);
}

//----------------------------------------------------------------------------

int wcserr_enable_(const int *enable)

{
  return wcserr_enable(*enable);
}

//----------------------------------------------------------------------------

int wcserr_size_(const int *err, int sizes[2])

{
  return wcserr_size((const struct wcserr *)err, sizes);
}

//----------------------------------------------------------------------------

// If null-terminated (using the Fortran CHAR(0) intrinsic), prefix may be of
// length less than but not exceeding 72 and trailing blanks are preserved.
// Otherwise, it must be of length 72 and trailing blanks are stripped off.

int wcserr_prt_(const int *err, const char prefix[72])

{
  char prefix_[73];
  wcsutil_strcvt(72, '\0', 1, prefix, prefix_);

  // This may or may not force the Fortran I/O buffers to be flushed.  If
  // not, try CALL FLUSH(6) before calling WCSERR_PRT in the Fortran code.
  fflush(NULL);

  return wcserr_prt((const struct wcserr *)err, prefix_);
}

//----------------------------------------------------------------------------

int wcserr_clear_(int **errp)

{
  return wcserr_clear((struct wcserr **)errp);
}
