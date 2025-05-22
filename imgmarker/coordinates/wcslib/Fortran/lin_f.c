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
  $Id: lin_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*===========================================================================*/

#include <stdio.h>
#include <string.h>

#include <wcserr.h>
#include <wcsutil.h>
#include <dis.h>
#include <lin.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define linput_  F77_FUNC(linput,  LINPUT)
#define linptd_  F77_FUNC(linptd,  LINPTD)
#define linpti_  F77_FUNC(linpti,  LINPTI)
#define linget_  F77_FUNC(linget,  LINGET)
#define lingtd_  F77_FUNC(lingtd,  LINGTD)
#define lingti_  F77_FUNC(lingti,  LINGTI)

#define linini_  F77_FUNC(linini,  LININI)
#define lininit_ F77_FUNC(lininit, LININIT)
#define lindis_  F77_FUNC(lindis,  LINDIS)
#define lindist_ F77_FUNC(lindist, LINDIST)
#define lincpy_  F77_FUNC(lincpy,  LINCPY)
#define linfree_ F77_FUNC(linfree, LINFREE)
#define linsize_ F77_FUNC(linsize, LINSIZE)
#define linenq_  F77_FUNC(linenq,  LINENQ)
#define linprt_  F77_FUNC(linprt,  LINPRT)
#define linperr_ F77_FUNC(linperr, LINPERR)
#define linset_  F77_FUNC(linset,  LINSET)
#define linp2x_  F77_FUNC(linp2x,  LINP2X)
#define linx2p_  F77_FUNC(linx2p,  LINX2P)
#define linwarp_ F77_FUNC(linwarp, LINWARP)

#ifdef BINDC
  #undef  linperr_
  #define linperr_ linperr_c
#endif

// Must match the values set in lin.inc.
#define LIN_FLAG   100
#define LIN_NAXIS  101
#define LIN_CRPIX  102
#define LIN_PC     103
#define LIN_CDELT  104
#define LIN_DISPRE 105
#define LIN_DISSEQ 106

#define LIN_PIXIMG 200
#define LIN_IMGPIX 201
#define LIN_INAXIS 202
#define LIN_UNITY  203
#define LIN_AFFINE 204
#define LIN_SIMPLE 205
#define LIN_ERR    206

//----------------------------------------------------------------------------

int linput_(
  int *lin,
  const int *what,
  const void *value,
  const int *i,
  const int *j)

{
  // Cast pointers.
  struct linprm *linp = (struct linprm *)lin;
  const int    *ivalp = (const int *)value;
  const double *dvalp = (const double *)value;

  // Convert 1-relative FITS axis numbers to 0-relative C array indices.
  int i0 = *i - 1;
  int j0 = *j - 1;

  // Preserve bypass mode.
  int flag = 0;
  if (linp->flag == 1 || linp->flag < 0) flag = 1;

  int k, status = 0;
  switch (*what) {
  case LIN_FLAG:
    linp->flag = *ivalp;
    break;
  case LIN_NAXIS:
    linp->naxis = *ivalp;
    linp->flag = flag;
    break;
  case LIN_CRPIX:
    linp->crpix[i0] = *dvalp;
    break;
  case LIN_PC:
    k = (i0)*(linp->naxis) + (j0);
    *(linp->pc+k) = *dvalp;
    linp->flag = flag;
    break;
  case LIN_CDELT:
    linp->cdelt[i0] = *dvalp;
    linp->flag = flag;
    break;
  case LIN_DISPRE:
    // N.B. value is the address of an allocated disprm struct.
    status = lindis(1, linp, (struct disprm *)value);
    linp->flag = flag;
    break;
  case LIN_DISSEQ:
    // N.B. value is the address of an allocated disprm struct.
    status = lindis(2, linp, (struct disprm *)value);
    linp->flag = flag;
    break;
  default:
    return 1;
  }

  return status;
}

int linptd_(int *lin, const int *what, const double *value,
  const int *i, const int *j)
{
  return linput_(lin, what, value, i, j);
}

int linpti_(int *lin, const int *what, const int *value,
  const int *i, const int *j)
{
  return linput_(lin, what, value, i, j);
}

//----------------------------------------------------------------------------

int linget_(const int *lin, const int *what, void *value)

{
  // Cast pointers.
  const struct linprm *linp  = (const struct linprm *)lin;
  int    *ivalp = (int *)value;
  double *dvalp = (double *)value;
  struct disprm **disvalp = (struct disprm **)value;

  int naxis = linp->naxis;

  switch (*what) {
  case LIN_FLAG:
    *ivalp = linp->flag;
    break;
  case LIN_NAXIS:
    *ivalp = naxis;
    break;
  case LIN_CRPIX:
    for (int i = 0; i < naxis; i++) {
      *(dvalp++) = linp->crpix[i];
    }
    break;
  case LIN_PC:
    // C row-major to FORTRAN column-major.
    for (int j = 0; j < naxis; j++) {
      const double *dlinp = linp->pc + j;
      for (int i = 0; i < naxis; i++) {
        *(dvalp++) = *dlinp;
        dlinp += naxis;
      }
    }
    break;
  case LIN_CDELT:
    for (int i = 0; i < naxis; i++) {
      *(dvalp++) = linp->cdelt[i];
    }
    break;
  case LIN_DISPRE:
    // N.B. the value returned is the address of a disprm struct.
    *disvalp = linp->dispre;
    break;
  case LIN_DISSEQ:
    // N.B. the value returned is the address of a disprm struct.
    *disvalp = linp->disseq;
    break;
  case LIN_PIXIMG:
    // C row-major to FORTRAN column-major.
    for (int j = 0; j < naxis; j++) {
      const double *dlinp = linp->piximg + j;
      for (int i = 0; i < naxis; i++) {
        *(dvalp++) = *dlinp;
        dlinp += naxis;
      }
    }
    break;
  case LIN_IMGPIX:
    // C row-major to FORTRAN column-major.
    for (int j = 0; j < naxis; j++) {
      const double *dlinp = linp->imgpix + j;
      for (int i = 0; i < naxis; i++) {
        *(dvalp++) = *dlinp;
        dlinp += naxis;
      }
    }
    break;
  case LIN_INAXIS:
    *ivalp = linp->i_naxis;
    break;
  case LIN_UNITY:
    *ivalp = linp->unity;
    break;
  case LIN_AFFINE:
    *ivalp = linp->affine;
    break;
  case LIN_SIMPLE:
    *ivalp = linp->simple;
    break;
  case LIN_ERR:
    // Copy the contents of the wcserr struct.
    if (linp->err) {
      const int *ilinp = (int *)(linp->err);
      for (size_t l = 0; l < ERRLEN; l++) {
        *(ivalp++) = *(ilinp++);
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

int lingtd_(const int *lin, const int *what, double *value)
{
  return linget_(lin, what, value);
}

int lingti_(const int *lin, const int *what, int *value)
{
  return linget_(lin, what, value);
}

//----------------------------------------------------------------------------

int linini_(const int *naxis, int *lin)

{
  return linini(1, *naxis, (struct linprm *)lin);
}

//----------------------------------------------------------------------------

int lininit_(const int *naxis, int *lin, int *ndpmax)

{
  return lininit(1, *naxis, (struct linprm *)lin, *ndpmax);
}

//----------------------------------------------------------------------------

int lindis_(const int *sequence, int *lin, int *dis)

{
  return lindis(*sequence, (struct linprm *)lin, (struct disprm *)dis);
}

//----------------------------------------------------------------------------

int lindist_(const int *sequence, int *lin, int *dis, int *ndpmax)

{
  return lindist(*sequence, (struct linprm *)lin, (struct disprm *)dis,
                 *ndpmax);
}

//----------------------------------------------------------------------------

int lincpy_(const int *linsrc, int *lindst)

{
  return lincpy(1, (const struct linprm *)linsrc, (struct linprm *)lindst);
}

//----------------------------------------------------------------------------

int linfree_(int *lin)

{
  return linfree((struct linprm *)lin);
}

//----------------------------------------------------------------------------

int linsize_(const int *lin, int sizes[2])

{
  return linsize((const struct linprm *)lin, sizes);
}

//----------------------------------------------------------------------------

int linenq_(const int *lin, int *enquiry)

{
  return linenq((const struct linprm *)lin, *enquiry);
}

//----------------------------------------------------------------------------

int linprt_(const int *lin)

{
  // This may or may not force the Fortran I/O buffers to be flushed.  If
  // not, try CALL FLUSH(6) before calling LINPRT in the Fortran code.
  fflush(NULL);

  return linprt((const struct linprm *)lin);
}

//----------------------------------------------------------------------------

// If null-terminated (using the Fortran CHAR(0) intrinsic), prefix may be of
// length less than but not exceeding 72 and trailing blanks are preserved.
// Otherwise, it must be of length 72 and trailing blanks are stripped off.

int linperr_(int *lin, const char prefix[72])

{
  // This may or may not force the Fortran I/O buffers to be flushed.
  // If not, try CALL FLUSH(6) before calling LINPERR in the Fortran code.
  fflush(NULL);

  char prefix_[73];
  wcsutil_strcvt(72, '\0', 1, prefix, prefix_);
  return linperr((struct linprm *)lin, prefix_);
}

//----------------------------------------------------------------------------

int linset_(int *lin)

{
  return linset((struct linprm *)lin);
}

//----------------------------------------------------------------------------

int linp2x_(
  int *lin,
  const int *ncoord,
  const int *nelem,
  const double pixcrd[],
  double imgcrd[])

{
  return linp2x((struct linprm *)lin, *ncoord, *nelem, pixcrd, imgcrd);
}

//----------------------------------------------------------------------------

int linx2p_(
  int *lin,
  const int *ncoord,
  const int *nelem,
  const double imgcrd[],
  double pixcrd[])

{
  return linx2p((struct linprm *)lin, *ncoord, *nelem, imgcrd, pixcrd);
}

//----------------------------------------------------------------------------

int linwarp_(
  int *lin,
  const double pixblc[],
  const double pixtrc[],
  const double pixsamp[],
  int    *nsamp,
  double maxdis[],
  double *maxtot,
  double avgdis[],
  double *avgtot,
  double rmsdis[],
  double *rmstot)

{
  return linwarp((struct linprm *)lin, pixblc, pixtrc, pixsamp, nsamp,
                 maxdis, maxtot, avgdis, avgtot, rmsdis, rmstot);
}
