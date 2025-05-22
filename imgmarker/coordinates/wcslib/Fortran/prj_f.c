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
  $Id: prj_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*===========================================================================*/

#include <stdio.h>
#include <string.h>

#include <wcserr.h>
#include <wcsutil.h>
#include <prj.h>

// Fortran name mangling (see below for the remainder).
#include <wcsconfig_f77.h>
#define prjput_  F77_FUNC(prjput,  PRJPUT)
#define prjptc_  F77_FUNC(prjptc,  PRJPTC)
#define prjptd_  F77_FUNC(prjptd,  PRJPTD)
#define prjpti_  F77_FUNC(prjpti,  PRJPTI)
#define prjget_  F77_FUNC(prjget,  PRJGET)
#define prjgtc_  F77_FUNC(prjgtc,  PRJGTC)
#define prjgtd_  F77_FUNC(prjgtd,  PRJGTD)
#define prjgti_  F77_FUNC(prjgti,  PRJGTI)

#define prjini_  F77_FUNC(prjini,  PRJINI)
#define prjfree_ F77_FUNC(prjfree, PRJFREE)
#define prjsize_ F77_FUNC(prjsize, PRJSIZE)
#define prjenq_  F77_FUNC(prjenq,  PRJENQ)
#define prjprt_  F77_FUNC(prjprt,  PRJPRT)
#define prjperr_ F77_FUNC(prjperr, PRJPERR)
#define prjbchk_ F77_FUNC(prjbchk, PRJBCHK)

#ifdef BINDC
  #undef  prjptc_
  #define prjptc_ prjptc_c

  #undef  prjgtc_
  #define prjgtc_ prjgtc_c

  #undef  prjperr_
  #define prjperr_ prjperr_c
#endif

// Must match the values set in prj.inc.
#define PRJ_FLAG      100
#define PRJ_CODE      101
#define PRJ_R0        102
#define PRJ_PV        103
#define PRJ_PHI0      104
#define PRJ_THETA0    105
#define PRJ_BOUNDS    106

#define PRJ_NAME      200
#define PRJ_CATEGORY  201
#define PRJ_PVRANGE   202
#define PRJ_SIMPLEZEN 203
#define PRJ_EQUIAREAL 204
#define PRJ_CONFORMAL 205
#define PRJ_GLOBAL    206
#define PRJ_DIVERGENT 207
#define PRJ_X0        208
#define PRJ_Y0        209
#define PRJ_ERR       210
#define PRJ_W         211
#define PRJ_N         212

//----------------------------------------------------------------------------

int prjput_(int *prj, const int *what, const void *value, const int *m)

{
  // Cast pointers.
  struct prjprm *prjp = (struct prjprm *)prj;
  const char   *cvalp = (const char *)value;
  const int    *ivalp = (const int *)value;
  const double *dvalp = (const double *)value;

  // Preserve bypass mode.
  int flag = 0;
  if (prjp->flag == 1 || prjp->flag < 0) flag = 1;

  switch (*what) {
  case PRJ_FLAG:
    prjp->flag = *ivalp;
    break;
  case PRJ_CODE:
    // Only three characters need be given.
    wcsutil_strcvt(3, ' ', 1, cvalp, prjp->code);
    wcsutil_null_fill(4, prjp->code);
    prjp->flag = flag;
    break;
  case PRJ_R0:
    prjp->r0 = *dvalp;
    prjp->flag = flag;
    break;
  case PRJ_PV:
    prjp->pv[*m] = *dvalp;
    prjp->flag = flag;
    break;
  case PRJ_PHI0:
    prjp->phi0 = *dvalp;
    prjp->flag = flag;
    break;
  case PRJ_THETA0:
    prjp->theta0 = *dvalp;
    prjp->flag = flag;
    break;
  case PRJ_BOUNDS:
    prjp->bounds = *ivalp;
    break;
  default:
    return 1;
  }

  return 0;
}

int prjptc_(int *prj, const int *what, const char *value, const int *m)
{
  return prjput_(prj, what, value, m);
}

int prjptd_(int *prj, const int *what, const double *value, const int *m)
{
  return prjput_(prj, what, value, m);
}

int prjpti_(int *prj, const int *what, const int *value, const int *m)
{
  return prjput_(prj, what, value, m);
}

//----------------------------------------------------------------------------

int prjget_(const int *prj, const int *what, void *value)

{

  // Cast pointers.
  const struct prjprm *prjp = (const struct prjprm *)prj;
  char   *cvalp = (char *)value;
  int    *ivalp = (int *)value;
  double *dvalp = (double *)value;

  switch (*what) {
  case PRJ_FLAG:
    *ivalp = prjp->flag;
    break;
  case PRJ_CODE:
    wcsutil_strcvt(4, ' ', 0, prjp->code, cvalp);
    break;
  case PRJ_R0:
    *dvalp = prjp->r0;
    break;
  case PRJ_PV:
    for (int m = 0; m < PVN; m++) {
      *(dvalp++) = prjp->pv[m];
    }
    break;
  case PRJ_PHI0:
    *dvalp = prjp->phi0;
    break;
  case PRJ_THETA0:
    *dvalp = prjp->theta0;
    break;
  case PRJ_BOUNDS:
    *ivalp = prjp->bounds;
    break;
  case PRJ_NAME:
    wcsutil_strcvt(40, ' ', 0, prjp->name, cvalp);
    break;
  case PRJ_CATEGORY:
    *ivalp = prjp->category;
    break;
  case PRJ_PVRANGE:
    *ivalp = prjp->pvrange;
    break;
  case PRJ_SIMPLEZEN:
    *ivalp = prjp->simplezen;
    break;
  case PRJ_EQUIAREAL:
    *ivalp = prjp->equiareal;
    break;
  case PRJ_CONFORMAL:
    *ivalp = prjp->conformal;
    break;
  case PRJ_GLOBAL:
    *ivalp = prjp->global;
    break;
  case PRJ_DIVERGENT:
    *ivalp = prjp->divergent;
    break;
  case PRJ_X0:
    *dvalp = prjp->x0;
    break;
  case PRJ_Y0:
    *dvalp = prjp->y0;
    break;
  case PRJ_ERR:
    // Copy the contents of the wcserr struct.
    if (prjp->err) {
      const int *iprjp = (int *)(prjp->err);
      for (size_t l = 0; l < ERRLEN; l++) {
        *(ivalp++) = *(iprjp++);
      }
    } else {
      for (size_t l = 0; l < ERRLEN; l++) {
        *(ivalp++) = 0;
      }
    }
    break;
  case PRJ_W:
    for (int m = 0; m < 10; m++) {
      *(dvalp++) = prjp->w[m];
    }
    break;
  case PRJ_N:
    *ivalp = prjp->n;
    break;
  default:
    return 1;
  }

  return 0;
}

int prjgtc_(const int *prj, const int *what, char *value)
{
  return prjget_(prj, what, value);
}

int prjgtd_(const int *prj, const int *what, double *value)
{
  return prjget_(prj, what, value);
}

int prjgti_(const int *prj, const int *what, int *value)
{
  return prjget_(prj, what, value);
}

//----------------------------------------------------------------------------

int prjini_(int *prj)

{
  return prjini((struct prjprm *)prj);
}

//----------------------------------------------------------------------------

int prjfree_(int *prj)

{
  return prjfree((struct prjprm *)prj);
}

//----------------------------------------------------------------------------

int prjsize_(const int *prj, int sizes[2])

{
  return prjsize((const struct prjprm *)prj, sizes);
}

//----------------------------------------------------------------------------

int prjenq_(const int *prj, int *enquiry)

{
  return prjenq((const struct prjprm *)prj, *enquiry);
}

//----------------------------------------------------------------------------

int prjprt_(const int *prj)

{
  // This may or may not force the Fortran I/O buffers to be flushed.  If
  // not, try CALL FLUSH(6) before calling PRJPRT in the Fortran code.
  fflush(NULL);

  return prjprt((const struct prjprm *)prj);
}

//----------------------------------------------------------------------------

// If null-terminated (using the Fortran CHAR(0) intrinsic), prefix may be of
// length less than but not exceeding 72 and trailing blanks are preserved.
// Otherwise, it must be of length 72 and trailing blanks are stripped off.

int prjperr_(int *prj, const char prefix[72])

{
  // This may or may not force the Fortran I/O buffers to be flushed.
  // If not, try CALL FLUSH(6) before calling PRJPERR in the Fortran code.
  fflush(NULL);

  char prefix_[73];
  wcsutil_strcvt(72, '\0', 1, prefix, prefix_);
  return wcserr_prt(((struct prjprm *)prj)->err, prefix_);
}

//----------------------------------------------------------------------------

int prjbchk_(
  const double *tol,
  const int *nphi,
  const int *ntheta,
  const int *spt,
  double phi[],
  double theta[],
  int stat[])

{
  return prjbchk(*tol, *nphi, *ntheta, *spt, phi, theta, stat);
}

//----------------------------------------------------------------------------

#define PRJSET_FWRAP(pcode, PCODE) \
  int F77_FUNC(pcode##set, PCODE##SET)(int *prj) \
  {return prjset((struct prjprm *)prj);}


#define PRJS2X_FWRAP(pcode, PCODE) \
  int F77_FUNC(pcode##s2x, PCODE##S2X)( \
    int *prj, \
    const int *nphi, \
    const int *ntheta, \
    const int *spt, \
    const int *sxy, \
    const double phi[], \
    const double theta[], \
    double x[], \
    double y[], \
    int stat[]) \
  {return prj##s2x((struct prjprm *)prj, *nphi, *ntheta, *spt, *sxy, \
                   phi, theta, x, y, stat);}

#define PRJX2S_FWRAP(pcode, PCODE) \
  int F77_FUNC(pcode##x2s, PRJ##X2S)( \
    int *prj, \
    const int *nx, \
    const int *ny, \
    const int *sxy, \
    const int *spt, \
    const double x[], \
    const double y[], \
    double phi[], \
    double theta[], \
    int stat[]) \
  {return pcode##x2s((struct prjprm *)prj, *nx, *ny, *sxy, *spt, x, y, \
                     phi, theta, stat);}

#define PRJ_FWRAP(pcode, PCODE) \
  PRJSET_FWRAP(pcode, PCODE)   \
  PRJS2X_FWRAP(pcode, PCODE)   \
  PRJX2S_FWRAP(pcode, PCODE)

PRJ_FWRAP(prj, PRJ)
PRJ_FWRAP(azp, AZP)
PRJ_FWRAP(szp, SZP)
PRJ_FWRAP(tan, TAN)
PRJ_FWRAP(stg, STG)
PRJ_FWRAP(sin, SIN)
PRJ_FWRAP(arc, ARC)
PRJ_FWRAP(zpn, ZPN)
PRJ_FWRAP(zea, ZEA)
PRJ_FWRAP(air, AIR)
PRJ_FWRAP(cyp, CYP)
PRJ_FWRAP(cea, CEA)
PRJ_FWRAP(car, CAR)
PRJ_FWRAP(mer, MER)
PRJ_FWRAP(sfl, SFL)
PRJ_FWRAP(par, PAR)
PRJ_FWRAP(mol, MOL)
PRJ_FWRAP(ait, AIT)
PRJ_FWRAP(cop, COP)
PRJ_FWRAP(coe, COE)
PRJ_FWRAP(cod, COD)
PRJ_FWRAP(coo, COO)
PRJ_FWRAP(bon, BON)
PRJ_FWRAP(pco, PCO)
PRJ_FWRAP(tsc, TSC)
PRJ_FWRAP(csc, CSC)
PRJ_FWRAP(qsc, QSC)
PRJ_FWRAP(hpx, HPX)
PRJ_FWRAP(xph, XPH)
