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
  $Id: cel_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*===========================================================================*/

#include <stdio.h>
#include <string.h>

#include <wcserr.h>
#include <wcsutil.h>
#include <cel.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define celput_  F77_FUNC(celput,  CELPUT)
#define celptc_  F77_FUNC(celptc,  CELPTC)
#define celptd_  F77_FUNC(celptd,  CELPTD)
#define celpti_  F77_FUNC(celpti,  CELPTI)
#define celget_  F77_FUNC(celget,  CELGET)
#define celgtc_  F77_FUNC(celgtc,  CELGTC)
#define celgtd_  F77_FUNC(celgtd,  CELGTD)
#define celgti_  F77_FUNC(celgti,  CELGTI)

#define celini_  F77_FUNC(celini,  CELINI)
#define celfree_ F77_FUNC(celfree, CELFREE)
#define celsize_ F77_FUNC(celsize, CELSIZE)
#define celenq_  F77_FUNC(celenq,  CELENQ)
#define celprt_  F77_FUNC(celprt,  CELPRT)
#define celperr_ F77_FUNC(celperr, CELPERR)
#define celset_  F77_FUNC(celset,  CELSET)
#define celx2s_  F77_FUNC(celx2s,  CELX2S)
#define cels2x_  F77_FUNC(cels2x,  CELS2X)

#ifdef BINDC
  #undef  celptc_
  #define celptc_ celptc_c

  #undef  celgtc_
  #define celgtc_ celgtc_c

  #undef  celperr_
  #define celperr_ celperr_c
#endif

// Must match the values set in cel.inc.
#define CEL_FLAG   100
#define CEL_OFFSET 101
#define CEL_PHI0   102
#define CEL_THETA0 103
#define CEL_REF    104
#define CEL_PRJ    105

#define CEL_EULER  200
#define CEL_LATPRQ 201
#define CEL_ISOLAT 202
#define CEL_ERR    203

//----------------------------------------------------------------------------

int celput_(int *cel, const int *what, const void *value, const int *i)

{
  // Cast pointers.
  struct celprm *celp = (struct celprm *)cel;
  const int    *ivalp = (const int *)value;
  const double *dvalp = (const double *)value;

  if (celp->flag == 1 || celp->flag < 0) {
    // Preserve bypass mode.
    celp->flag = 1;
  } else {
    celp->flag = 0;
  }

  int *icelp;
  switch (*what) {
  case CEL_FLAG:
    celp->flag = *ivalp;
    break;
  case CEL_OFFSET:
    celp->offset = *ivalp;
    break;
  case CEL_PHI0:
    celp->phi0 = *dvalp;
    break;
  case CEL_THETA0:
    celp->theta0 = *dvalp;
    break;
  case CEL_REF:
    celp->ref[*i-1] = *dvalp;
    break;
  case CEL_PRJ:
    icelp = cel + ((int *)(&(celp->prj)) - (int *)celp);
    for (size_t l = 0; l < PRJLEN; l++) {
      *(icelp++) = *(ivalp++);
    }
    break;
  default:
    return 1;
  }

  return 0;
}

int celptc_(int *cel, const int *what, const char *value, const int *i)
{
  return celput_(cel, what, value, i);
}

int celptd_(int *cel, const int *what, const double *value, const int *i)
{
  return celput_(cel, what, value, i);
}

int celpti_(int *cel, const int *what, const int *value, const int *i)
{
  return celput_(cel, what, value, i);
}

//----------------------------------------------------------------------------

int celget_(const int *cel, const int *what, void *value)

{
  // Cast pointers.
  const struct celprm *celp = (const struct celprm *)cel;
  int    *ivalp = (int *)value;
  double *dvalp = (double *)value;

  const int *icelp;
  switch (*what) {
  case CEL_FLAG:
    *ivalp = celp->flag;
    break;
  case CEL_OFFSET:
    *ivalp = celp->offset;
    break;
  case CEL_PHI0:
    *dvalp = celp->phi0;
    break;
  case CEL_THETA0:
    *dvalp = celp->theta0;
    break;
  case CEL_REF:
    for (int k = 0; k < 4; k++) {
      *(dvalp++) = celp->ref[k];
    }
    break;
  case CEL_PRJ:
    icelp = (int *)(&(celp->prj));
    for (size_t l = 0; l < PRJLEN; l++) {
      *(ivalp++) = *(icelp++);
    }
    break;
  case CEL_EULER:
    for (int k = 0; k < 5; k++) {
       *(dvalp++) = celp->euler[k];
    }
    break;
  case CEL_LATPRQ:
    *ivalp = celp->latpreq;
    break;
  case CEL_ISOLAT:
    *ivalp = celp->isolat;
    break;
  case CEL_ERR:
    // Copy the contents of the wcserr struct.
    if (celp->err) {
      icelp = (int *)(celp->err);
      for (size_t l = 0; l < ERRLEN; l++) {
        *(ivalp++) = *(icelp++);
      }
    } else {
      for (size_t l = 0; l < ERRLEN; l++) {
        *(ivalp++) = 0;
      }
    }
    break;
  default:
    return 1;
  }

  return 0;
}

int celgtc_(const int *cel, const int *what, char *value)
{
  return celget_(cel, what, value);
}

int celgtd_(const int *cel, const int *what, double *value)
{
  return celget_(cel, what, value);
}

int celgti_(const int *cel, const int *what, int *value)
{
  return celget_(cel, what, value);
}

//----------------------------------------------------------------------------

int celini_(int *cel)

{
  return celini((struct celprm *)cel);
}

//----------------------------------------------------------------------------

int celfree_(int *cel)

{
  return celfree((struct celprm *)cel);
}

//----------------------------------------------------------------------------

int celsize_(const int *cel, int sizes[2])

{
  return celsize((const struct celprm *)cel, sizes);
}

//----------------------------------------------------------------------------

int celenq_(const int *cel, int *enquiry)

{
  return celenq((const struct celprm *)cel, *enquiry);
}

//----------------------------------------------------------------------------

int celprt_(const int *cel)

{
  // This may or may not force the Fortran I/O buffers to be flushed.  If
  // not, try CALL FLUSH(6) before calling CELPRT in the Fortran code.
  fflush(NULL);

  return celprt((const struct celprm *)cel);
}

//----------------------------------------------------------------------------

// If null-terminated (using the Fortran CHAR(0) intrinsic), prefix may be of
// length less than but not exceeding 72 and trailing blanks are preserved.
// Otherwise, it must be of length 72 and trailing blanks are stripped off.

int celperr_(int *cel, const char prefix[72])

{
  // This may or may not force the Fortran I/O buffers to be flushed.
  // If not, try CALL FLUSH(6) before calling CELPERR in the Fortran code.
  fflush(NULL);

  char prefix_[73];
  wcsutil_strcvt(72, '\0', 1, prefix, prefix_);
  return celperr((struct celprm *)cel, prefix_);
}

//----------------------------------------------------------------------------

int celset_(int *cel)

{
  return celset((struct celprm *)cel);
}

//----------------------------------------------------------------------------

int celx2s_(
  int *cel,
  const int *nx,
  const int *ny,
  const int *sxy,
  const int *sll,
  const double x[],
  const double y[],
  double phi[],
  double theta[],
  double lng[],
  double lat[],
  int stat[])

{
  return celx2s((struct celprm *)cel, *nx, *ny, *sxy, *sll, x, y, phi, theta,
                lng, lat, stat);
}

//----------------------------------------------------------------------------

int cels2x_(
  int *cel,
  const int *nlng,
  const int *nlat,
  const int *sll,
  const int *sxy,
  const double lng[],
  const double lat[],
  double phi[],
  double theta[],
  double x[],
  double y[],
  int stat[])

{
  return cels2x((struct celprm *)cel, *nlng, *nlat, *sll, *sxy, lng, lat,
                phi, theta, x, y, stat);
}
