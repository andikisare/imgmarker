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
  $Id: dis_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=============================================================================
*
* In these wrappers, if
*
*   deref == 0, then dis is the address of a Fortran INTEGER array of length
*               DISLEN containing a disprm struct.
*
*   deref == 1, then dis is the address of a Fortran INTEGER(2) array holding
*               the address of a disprm struct, such as is returned by
*               disalloc_(), or linget() with LIN_DISPRE or LIN_DISSEQ.
*
*---------------------------------------------------------------------------*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <wcserr.h>
#include <wcsutil.h>
#include <dis.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define disalloc_ F77_FUNC(disalloc, DISALLOC)
#define disput_   F77_FUNC(disput,   DISPUT)
#define disptc_   F77_FUNC(disptc,   DISPTC)
#define disptd_   F77_FUNC(disptd,   DISPTD)
#define dispti_   F77_FUNC(dispti,   DISPTI)
#define disget_   F77_FUNC(disget,   DISGET)
#define disgtc_   F77_FUNC(disgtc,   DISGTC)
#define disgtd_   F77_FUNC(disgtd,   DISGTD)
#define disgti_   F77_FUNC(disgti,   DISGTI)

#define disndp_   F77_FUNC(disndp,   DISNDP)
#define dpfill_   F77_FUNC(dpfill,   DPFILL)
#define dpkeyi_   F77_FUNC(dpkeyi,   DPKEYI)
#define dpkeyd_   F77_FUNC(dpkeyd,   DPKEYD)
#define disini_   F77_FUNC(disini,   DISINI)
#define disinit_  F77_FUNC(disinit,  DISINIT)
#define discpy_   F77_FUNC(discpy,   DISCPY)
#define disfree_  F77_FUNC(disfree,  DISFREE)
#define dissize_  F77_FUNC(dissize,  DISSIZE)
#define disenq_   F77_FUNC(disenq,   DISENQ)
#define disprt_   F77_FUNC(disprt,   DISPRT)
#define disperr_  F77_FUNC(disperr,  DISPERR)
#define dishdo_   F77_FUNC(dishdo,   DISHDO)
#define disset_   F77_FUNC(disset,   DISSET)
#define disp2x_   F77_FUNC(disp2x,   DISP2X)
#define disx2p_   F77_FUNC(disx2p,   DISX2P)
#define diswarp_  F77_FUNC(diswarp,  DISWARP)

#ifdef BINDC
  #undef  disptc_
  #define disptc_ disptc_c

  #undef  disgtc_
  #define disgtc_ disgtc_c

  #undef  dpfill_
  #define dpfill_ dpfill_c

  #undef  disperr_
  #define disperr_ disperr_c
#endif

// Must match the values set in dis.inc.
#define DIS_FLAG   100
#define DIS_NAXIS  101
#define DIS_DTYPE  102
#define DIS_NDP    103
#define DIS_NDPMAX 104
#define DIS_DP     105
#define DIS_TOTDIS 106
#define DIS_MAXDIS 107

#define DIS_DOCORR 200
#define DIS_NHAT   201
#define DIS_AXMAP  202
#define DIS_OFFSET 203
#define DIS_SCALE  204
#define DIS_IPARM  205
#define DIS_DPARM  206
#define DIS_INAXIS 207
#define DIS_NDIS   208
#define DIS_ERR    209

//----------------------------------------------------------------------------

// disp should be the address of an INTEGER(2) array.  On return it holds
// the address of an allocated disprm struct.

int disalloc_(int *disp)

{
  if ((*(struct disprm **)disp = calloc(1, sizeof(struct disprm))) == 0x0) {
    return DISERR_MEMORY;
  }

  return 0;
}

//----------------------------------------------------------------------------

int disput_(
  const int *deref,
  int *dis,
  const int *what,
  const void *value,
  const int *j,
  const int *dummy)

{
  // Avert nuisance compiler warnings about unused parameters.
  (void)dummy;

  // Cast pointers.
  struct disprm *disp;
  if (*deref == 0) {
    disp = (struct disprm *)dis;
  } else {
    disp = *(struct disprm **)dis;
  }

  const char   *cvalp = (const char *)value;
  const int    *ivalp = (const int *)value;
  const double *dvalp = (const double *)value;

  // Convert 1-relative FITS (and Fortran) axis numbers and parameter
  // indices to 0-relative C array indices.
  int j0 = *j - 1;

  // Preserve bypass mode.
  int flag = 0;
  if (disp->flag == 1 || disp->flag < 0) flag = 1;

  switch (*what) {
  case DIS_FLAG:
    disp->flag = *ivalp;
    break;
  case DIS_NAXIS:
    disp->naxis = *ivalp;
    disp->flag = flag;
    break;
  case DIS_DTYPE:
    wcsutil_strcvt(72, '\0', 0, cvalp, disp->dtype[j0]);
    disp->flag = 0;
    break;
  case DIS_NDP:
  case DIS_NDPMAX:
    return 1;
    break;
  case DIS_DP:
    // Use DPFILL to create the struct.
    memcpy((char *)(disp->dp + disp->ndp), cvalp, DPLEN*sizeof(int));
    (disp->ndp)++;
    disp->flag = flag;
    break;
  case DIS_TOTDIS:
    disp->totdis = *dvalp;
    break;
  case DIS_MAXDIS:
    disp->maxdis[j0] = *dvalp;
    break;
  default:
    return 1;
  }

  return 0;
}

int disptc_(const int *deref, int *dis, const int *what, const char *value,
  const int *j, const int *k)
{
  return disput_(deref, dis, what, value, j, k);
}

int disptd_(const int *deref, int *dis, const int *what, const double *value,
  const int *j, const int *k)
{
  return disput_(deref, dis, what, value, j, k);
}

int dispti_(const int *deref, int *dis, const int *what, const int *value,
  const int *j, const int *k)
{
  return disput_(deref, dis, what, value, j, k);
}

//----------------------------------------------------------------------------

int disget_(const int *deref, const int *dis, const int *what, void *value)

{
  // Cast pointers.
  const struct disprm *disp;
  if (*deref == 0) {
    disp = (const struct disprm *)dis;
  } else {
    disp = *(const struct disprm **)dis;
  }

  char   *cvalp = (char *)value;
  int    *ivalp = (int *)value;
  double *dvalp = (double *)value;

  int naxis = disp->naxis;

  switch (*what) {
  case DIS_FLAG:
    *ivalp = disp->flag;
    break;
  case DIS_NAXIS:
    *ivalp = naxis;
    break;
  case DIS_DTYPE:
    for (int j = 0; j < naxis; j++) {
      wcsutil_strcvt(72, ' ', 0, disp->dtype[j], cvalp);
      cvalp += 72;
    }
    break;
  case DIS_NDP:
    *ivalp = disp->ndp;
    break;
  case DIS_NDPMAX:
    *ivalp = disp->ndpmax;
    break;
  case DIS_DP:
    memcpy(cvalp, (char *)disp->dp, disp->ndp*DPLEN*sizeof(int));
    break;
  case DIS_TOTDIS:
    *dvalp = disp->totdis;
    break;
  case DIS_MAXDIS:
    for (int j = 0; j < naxis; j++) {
      *(dvalp++) = disp->maxdis[j];
    }
    break;
  case DIS_DOCORR:
    for (int j = 0; j < naxis; j++) {
      *(ivalp++) = disp->docorr[j];
    }
    break;
  case DIS_NHAT:
    for (int j = 0; j < naxis; j++) {
      *(ivalp++) = disp->Nhat[j];
    }
    break;
  case DIS_AXMAP:
    for (int j = 0; j < naxis; j++) {
      for (int k = 0; k < naxis; k++) {
        *(ivalp++) = disp->axmap[j][k];
      }
    }
    break;
  case DIS_OFFSET:
    for (int j = 0; j < naxis; j++) {
      for (int k = 0; k < naxis; k++) {
        *(dvalp++) = disp->offset[j][k];
      }
    }
    break;
  case DIS_SCALE:
    for (int j = 0; j < naxis; j++) {
      for (int k = 0; k < naxis; k++) {
        *(dvalp++) = disp->scale[j][k];
      }
    }
    break;
  case DIS_IPARM:
    for (int j = 0; j < naxis; j++) {
      for (int k = 0; k < disp->iparm[j][0]; k++) {
        *(ivalp++) = disp->iparm[j][k];
      }
    }
    break;
  case DIS_DPARM:
    for (int j = 0; j < naxis; j++) {
      for (int k = 0; k < disp->iparm[j][1]; k++) {
        *(dvalp++) = disp->dparm[j][k];
      }
    }
    break;
  case DIS_INAXIS:
    *ivalp = disp->i_naxis;
    break;
  case DIS_NDIS:
    *ivalp = disp->ndis;
    break;
  case DIS_ERR:
    // Copy the contents of the wcserr struct.
    if (disp->err) {
      const int *idisp = (int *)(disp->err);
      for (size_t l = 0; l < ERRLEN; l++) {
        *(ivalp++) = *(idisp++);
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

int disgtc_(const int *deref, const int *dis, const int *what, char *value)
{
  return disget_(deref, dis, what, value);
}

int disgtd_(const int *deref, const int *dis, const int *what, double *value)
{
  return disget_(deref, dis, what, value);
}

int disgti_(const int *deref, const int *dis, const int *what, int *value)
{
  return disget_(deref, dis, what, value);
}

//----------------------------------------------------------------------------

int disndp_(int *ndpmax) { return disndp(*ndpmax); }

//----------------------------------------------------------------------------

// keyword and field should be null-terminated, or else of length 72 in which
// case trailing blanks are not significant.

int dpfill_(
  const int *dp,
  const char *keyword,
  const char *field,
  int *j,
  int *type,
  int *ival,
  double *fval)

{
  char keyword_[73], field_[73];
  wcsutil_strcvt(72, '\0', 1, keyword, keyword_);
  wcsutil_strcvt(72, '\0', 1, field, field_);

  return dpfill((struct dpkey *)dp, keyword_, field_, *j, *type, *ival,
                 *fval);
}

//----------------------------------------------------------------------------

int dpkeyi_(
  const int *dp)

{
  return dpkeyi((struct dpkey *)dp);
}

//----------------------------------------------------------------------------

double dpkeyd_(
  const int *dp)

{
  return dpkeyd((struct dpkey *)dp);
}

//----------------------------------------------------------------------------

int disini_(const int *deref, const int *naxis, int *dis)

{
  struct disprm *disp;
  if (*deref == 0) {
    disp = (struct disprm *)dis;
  } else {
    disp = *(struct disprm **)dis;
  }

  return disini(1, *naxis, disp);
}

//----------------------------------------------------------------------------

int disinit_(const int *deref, const int *naxis, int *dis, int *ndpmax)

{
  struct disprm *disp;
  if (*deref == 0) {
    disp = (struct disprm *)dis;
  } else {
    disp = *(struct disprm **)dis;
  }

  return disinit(1, *naxis, disp, *ndpmax);
}

//----------------------------------------------------------------------------

int discpy_(const int *deref, const int *dissrc, int *disdst)

{
  const struct disprm *dissrcp;
  if ((*deref&1) == 0) {
    dissrcp = (const struct disprm *)dissrc;
  } else {
    dissrcp = *(const struct disprm **)dissrc;
  }

  struct disprm *disdstp;
  if ((*deref&2) == 0) {
    disdstp = (struct disprm *)disdst;
  } else {
    disdstp = *(struct disprm **)disdst;
  }

  return discpy(1, dissrcp, disdstp);
}

//----------------------------------------------------------------------------

int disfree_(const int *deref, int *dis)

{
  struct disprm *disp;
  if (*deref == 0) {
    disp = (struct disprm *)dis;
  } else {
    disp = *(struct disprm **)dis;
  }

  return disfree(disp);
}

//----------------------------------------------------------------------------

int dissize_(const int *dis, int sizes[2])

{
  return dissize((const struct disprm *)dis, sizes);
}

//----------------------------------------------------------------------------

int disenq_(const int *dis, int *enquiry)

{
  return disenq((const struct disprm *)dis, *enquiry);
}

//----------------------------------------------------------------------------

int disprt_(const int *deref, const int *dis)

{
  const struct disprm *disp;
  if (*deref == 0) {
    disp = (const struct disprm *)dis;
  } else {
    disp = *(const struct disprm **)dis;
  }

  // This may or may not force the Fortran I/O buffers to be flushed.  If
  // not, try CALL FLUSH(6) before calling DISPRT in the Fortran code.
  fflush(NULL);

  return disprt(disp);
}

//----------------------------------------------------------------------------

// If null-terminated (using the Fortran CHAR(0) intrinsic), prefix may be of
// length less than but not exceeding 72 and trailing blanks are preserved.
// Otherwise, it must be of length 72 and trailing blanks are stripped off.

int disperr_(const int *deref, int *dis, const char prefix[72])

{
  const struct disprm *disp;
  if (*deref == 0) {
    disp = (const struct disprm *)dis;
  } else {
    disp = *(const struct disprm **)dis;
  }

  char prefix_[73];
  wcsutil_strcvt(72, '\0', 1, prefix, prefix_);

  // This may or may not force the Fortran I/O buffers to be flushed.
  // If not, try CALL FLUSH(6) before calling DISPERR in the Fortran code.
  fflush(NULL);

  return wcserr_prt(disp->err, prefix_);
}

//----------------------------------------------------------------------------

int dishdo_(const int *deref, int *dis)

{
  struct disprm *disp;
  if (*deref == 0) {
    disp = (struct disprm *)dis;
  } else {
    disp = *(struct disprm **)dis;
  }

  return dishdo(disp);
}

//----------------------------------------------------------------------------

int disset_(const int *deref, int *dis)

{
  struct disprm *disp;
  if (*deref == 0) {
    disp = (struct disprm *)dis;
  } else {
    disp = *(struct disprm **)dis;
  }

  return disset(disp);
}

//----------------------------------------------------------------------------

int disp2x_(
  const int *deref,
  int *dis,
  const double rawcrd[],
  double discrd[])

{
  struct disprm *disp;
  if (*deref == 0) {
    disp = (struct disprm *)dis;
  } else {
    disp = *(struct disprm **)dis;
  }

  return disp2x(disp, rawcrd, discrd);
}

//----------------------------------------------------------------------------

int disx2p_(
  const int *deref,
  int *dis,
  const double discrd[],
  double rawcrd[])

{
  struct disprm *disp;
  if (*deref == 0) {
    disp = (struct disprm *)dis;
  } else {
    disp = *(struct disprm **)dis;
  }

  return disx2p(disp, discrd, rawcrd);
}

//----------------------------------------------------------------------------

int diswarp_(
  int *dis,
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
  return diswarp((struct disprm *)dis, pixblc, pixtrc, pixsamp, nsamp,
                 maxdis, maxtot, avgdis, avgtot, rmsdis, rmstot);
}
