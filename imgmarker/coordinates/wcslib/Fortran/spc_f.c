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
  $Id: spc_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*===========================================================================*/

#include <stdio.h>
#include <string.h>

#include <wcserr.h>
#include <wcsutil.h>
#include <spc.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define spcput_  F77_FUNC(spcput,  SPCPUT)
#define spcptc_  F77_FUNC(spcptc,  SPCPTC)
#define spcptd_  F77_FUNC(spcptd,  SPCPTD)
#define spcpti_  F77_FUNC(spcpti,  SPCPTI)
#define spcget_  F77_FUNC(spcget,  SPCGET)
#define spcgtc_  F77_FUNC(spcgtc,  SPCGTC)
#define spcgtd_  F77_FUNC(spcgtd,  SPCGTD)
#define spcgti_  F77_FUNC(spcgti,  SPCGTI)

#define spcini_  F77_FUNC(spcini,  SPCINI)
#define spcfree_ F77_FUNC(spcfree, SPCFREE)
#define spcsize_ F77_FUNC(spcsize, SPCSIZE)
#define spcenq_  F77_FUNC(spcenq,  SPCENQ)
#define spcprt_  F77_FUNC(spcprt,  SPCPRT)
#define spcperr_ F77_FUNC(spcperr, SPCPERR)
#define spcset_  F77_FUNC(spcset,  SPCSET)
#define spcx2s_  F77_FUNC(spcx2s,  SPCX2S)
#define spcs2x_  F77_FUNC(spcs2x,  SPCS2X)
#define spctype_ F77_FUNC(spctype, SPCTYPE)
#define spcspxe_ F77_FUNC(spcspxe, SPCSPXE)
#define spcxpse_ F77_FUNC(spcxpse, SPCXPSE)
#define spctrne_ F77_FUNC(spctrne, SPCTRNE)
#define spcaips_ F77_FUNC(spcaips, SPCAIPS)

// Deprecated.
#define spctyp_  F77_FUNC(spctyp,  SPCTYP)
#define spcspx_  F77_FUNC(spcspx,  SPCSPX)
#define spcxps_  F77_FUNC(spcxps,  SPCXPS)
#define spctrn_  F77_FUNC(spctrn,  SPCTRN)

#ifdef BINDC
  #undef  spcptc_
  #define spcptc_ spcptc_c

  #undef  spcgtc_
  #define spcgtc_ spcgtc_c

  #undef  spcperr_
  #define spcperr_ spcperr_c

  #undef  spctype_ 
  #define spctype_ spctype_c
  #undef  spctyp_ 
  #define spctyp_  spctyp_c

  #undef  spcspxe_ 
  #define spcspxe_ spcspxe_c
  #undef  spcspx_ 
  #define spcspx_  spcspx_c

  #undef  spcxpse_ 
  #define spcxpse_ spcxpse_c
  #undef  spcxps_ 
  #define spcxps_  spcxps_c

  #undef  spctrne_ 
  #define spctrne_ spctrne_c
  #undef  spctrn_ 
  #define spctrn_  spctrn_c

  #undef  spcaips_ 
  #define spcaips_ spcaips_c
#endif

// Must match the values set in spc.inc.
#define SPC_FLAG    100
#define SPC_TYPE    101
#define SPC_CODE    102
#define SPC_CRVAL   103
#define SPC_RESTFRQ 104
#define SPC_RESTWAV 105
#define SPC_PV      106

#define SPC_W       200
#define SPC_ISGRISM 201
#define SPC_ERR     202

//----------------------------------------------------------------------------

int spcput_(int *spc, const int *what, const void *value, const int *m)

{
  // Cast pointers.
  struct spcprm *spcp = (struct spcprm *)spc;
  const char   *cvalp = (const char *)value;
  const int    *ivalp = (const int *)value;
  const double *dvalp = (const double *)value;

  if (spcp->flag == 1 || spcp->flag < 0) {
    // Preserve bypass mode.
    spcp->flag = 1;
  } else {
    spcp->flag = 0;
  }

  switch (*what) {
  case SPC_FLAG:
    spcp->flag = *ivalp;
    break;
  case SPC_TYPE:
    // Only four characters need be given.
    wcsutil_strcvt(4, ' ', 1, cvalp, spcp->type);
    wcsutil_null_fill(8, spcp->type);
    break;
  case SPC_CODE:
    // Only three characters need be given.
    wcsutil_strcvt(3, ' ', 1, cvalp, spcp->code);
    wcsutil_null_fill(4, spcp->code);
    break;
  case SPC_CRVAL:
    spcp->crval = *dvalp;
    break;
  case SPC_RESTFRQ:
    spcp->restfrq = *dvalp;
    break;
  case SPC_RESTWAV:
    spcp->restwav = *dvalp;
    break;
  case SPC_PV:
    spcp->pv[*m] = *dvalp;
    break;
  default:
    return 1;
  }

  return 0;
}

int spcptc_(int *spc, const int *what, const char *value, const int *m)
{
  return spcput_(spc, what, value, m);
}

int spcptd_(int *spc, const int *what, const double *value, const int *m)
{
  return spcput_(spc, what, value, m);
}

int spcpti_(int *spc, const int *what, const int *value, const int *m)
{
  return spcput_(spc, what, value, m);
}

//----------------------------------------------------------------------------

int spcget_(const int *spc, const int *what, void *value)

{
  // Cast pointers.
  const struct spcprm *spcp = (const struct spcprm *)spc;
  char   *cvalp = (char *)value;
  int    *ivalp = (int *)value;
  double *dvalp = (double *)value;

  switch (*what) {
  case SPC_FLAG:
    *ivalp = spcp->flag;
    break;
  case SPC_TYPE:
    wcsutil_strcvt(8, ' ', 0, spcp->type, cvalp);
    break;
  case SPC_CODE:
    wcsutil_strcvt(4, ' ', 0, spcp->code, cvalp);
    break;
  case SPC_CRVAL:
    *dvalp = spcp->crval;
    break;
  case SPC_RESTFRQ:
    *dvalp = spcp->restfrq;
    break;
  case SPC_RESTWAV:
    *dvalp = spcp->restwav;
    break;
  case SPC_PV:
    for (int m = 0; m < 7; m++) {
      *(dvalp++) = spcp->pv[m];
    }
    break;
  case SPC_W:
    for (int m = 0; m < 6; m++) {
      *(dvalp++) = spcp->w[m];
    }
    break;
  case SPC_ISGRISM:
    *ivalp = spcp->isGrism;
    break;
  case SPC_ERR:
    // Copy the contents of the wcserr struct.
    if (spcp->err) {
      const int *ispcp = (int *)(spcp->err);
      for (size_t l = 0; l < ERRLEN; l++) {
        *(ivalp++) = *(ispcp++);
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

int spcgtc_(const int *spc, const int *what, char *value)
{
  return spcget_(spc, what, value);
}

int spcgtd_(const int *spc, const int *what, double *value)
{
  return spcget_(spc, what, value);
}

int spcgti_(const int *spc, const int *what, int *value)
{
  return spcget_(spc, what, value);
}

//----------------------------------------------------------------------------

int spcini_(int *spc)

{
  return spcini((struct spcprm *)spc);
}

//----------------------------------------------------------------------------

int spcfree_(int *spc)

{
  return spcfree((struct spcprm *)spc);
}

//----------------------------------------------------------------------------

int spcsize_(const int *spc, int sizes[2])

{
  return spcsize((const struct spcprm *)spc, sizes);
}

//----------------------------------------------------------------------------

int spcenq_(const int *spc, int *enquiry)

{
  return spcenq((const struct spcprm *)spc, *enquiry);
}

//----------------------------------------------------------------------------

int spcprt_(const int *spc)

{
  // This may or may not force the Fortran I/O buffers to be flushed.  If
  // not, try CALL FLUSH(6) before calling SPCPRT in the Fortran code.
  fflush(NULL);

  return spcprt((const struct spcprm *)spc);
}

//----------------------------------------------------------------------------

// If null-terminated (using the Fortran CHAR(0) intrinsic), prefix may be of
// length less than but not exceeding 72 and trailing blanks are preserved.
// Otherwise, it must be of length 72 and trailing blanks are stripped off.

int spcperr_(int *spc, const char prefix[72])

{
  // This may or may not force the Fortran I/O buffers to be flushed.
  // If not, try CALL FLUSH(6) before calling SPCPERR in the Fortran code.
  fflush(NULL);

  char prefix_[73];
  wcsutil_strcvt(72, '\0', 1, prefix, prefix_);
  return wcserr_prt(((struct spcprm *)spc)->err, prefix_);
}

//----------------------------------------------------------------------------

int spcset_(int *spc)

{
  return spcset((struct spcprm *)spc);
}

//----------------------------------------------------------------------------

int spcx2s_(
  int *spc,
  const int *nx,
  const int *sspec,
  const int *sx,
  const double x[],
  double spec[],
  int stat[])

{
  return spcx2s((struct spcprm *)spc, *nx, *sx, *sspec, x, spec, stat);
}

//----------------------------------------------------------------------------

int spcs2x_(
  int *spc,
  const int *nspec,
  const int *sspec,
  const int *sx,
  const double spec[],
  double x[],
  int stat[])

{
  return spcs2x((struct spcprm *)spc, *nspec, *sspec, *sx, spec, x, stat);
}

//----------------------------------------------------------------------------

int spctype_(
  const char ctypei[8],
  char stype[4],
  char scode[3],
  char sname[21],
  char units[7],
  char ptype[1],
  char xtype[1],
  int *restreq,
  iptr err)

{
  char ctypei_[9];
  wcsutil_strcvt(8, ' ', 1, ctypei, ctypei_);

  char stype_[5], scode_[4], sname_[22], units_[8];
  int status = spctype(ctypei_, stype_, scode_, sname_, units_, ptype, xtype,
                       restreq, (struct wcserr **)err);

  wcsutil_strcvt( 4, ' ', 0, stype_, stype);
  wcsutil_strcvt( 3, ' ', 0, scode_, scode);
  wcsutil_strcvt(21, ' ', 0, sname_, sname);
  wcsutil_strcvt( 7, ' ', 0, units_, units);

  return status;
}

// : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : :

int spctyp_(
  const char ctypei[8],
  char stype[4],
  char scode[3],
  char sname[21],
  char units[7],
  char ptype[1],
  char xtype[1],
  int *restreq)

{
  return spctype_(ctypei, stype, scode, sname, units, ptype, xtype, restreq,
                  0x0);
}

//----------------------------------------------------------------------------

int spcspxe_(
  const char ctypeS[8],
  const double *crvalS,
  const double *restfrq,
  const double *restwav,
  char ptype[1],
  char xtype[1],
  int *restreq,
  double *crvalX,
  double *dXdS,
  iptr err)

{
  char ctypeS_[9];
  wcsutil_strcvt(8, ' ', 1, ctypeS, ctypeS_);

  return spcspxe(ctypeS_, *crvalS, *restfrq, *restwav, ptype, xtype, restreq,
                 crvalX, dXdS, (struct wcserr **)err);
}

// : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : :

int spcspx_(
  const char ctypeS[8],
  const double *crvalS,
  const double *restfrq,
  const double *restwav,
  char ptype[1],
  char xtype[1],
  int *restreq,
  double *crvalX,
  double *dXdS)

{
  return spcspxe_(ctypeS, crvalS, restfrq, restwav, ptype, xtype, restreq,
                  crvalX, dXdS, 0x0);
}

//----------------------------------------------------------------------------

int spcxpse_(
  const char ctypeS[8],
  const double *crvalX,
  const double *restfrq,
  const double *restwav,
  char ptype[1],
  char xtype[1],
  int *restreq,
  double *crvalS,
  double *dSdX,
  iptr err)

{
  char ctypeS_[9];
  wcsutil_strcvt(8, ' ', 1, ctypeS, ctypeS_);

  return spcxpse(ctypeS_, *crvalX, *restfrq, *restwav, ptype, xtype, restreq,
                 crvalS, dSdX, (struct wcserr **)err);
}

// : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : :

int spcxps_(
  const char ctypeS[8],
  const double *crvalX,
  const double *restfrq,
  const double *restwav,
  char ptype[1],
  char xtype[1],
  int *restreq,
  double *crvalS,
  double *dSdX)

{
  return spcxpse_(ctypeS, crvalX, restfrq, restwav, ptype, xtype, restreq,
                  crvalS, dSdX, 0x0);
}

//----------------------------------------------------------------------------

int spctrne_(
  const char ctypeS1[8],
  const double *crvalS1,
  const double *cdeltS1,
  const double *restfrq,
  const double *restwav,
  char   ctypeS2[8],
  double *crvalS2,
  double *cdeltS2,
  iptr err)

{
  char ctypeS1_[9], ctypeS2_[9];
  wcsutil_strcvt(8, ' ', 1, ctypeS1, ctypeS1_);
  wcsutil_strcvt(8, ' ', 1, ctypeS2, ctypeS2_);

  int status = spctrne(ctypeS1_, *crvalS1, *cdeltS1, *restfrq, *restwav,
                       ctypeS2_,  crvalS2,  cdeltS2, (struct wcserr **)err);

  wcsutil_strcvt(8, ' ', 0, ctypeS2_, ctypeS2);

  return status;
}

// : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : :

int spctrn_(
  const char ctypeS1[8],
  const double *crvalS1,
  const double *cdeltS1,
  const double *restfrq,
  const double *restwav,
  char   ctypeS2[8],
  double *crvalS2,
  double *cdeltS2)

{
  return spctrne_(ctypeS1, crvalS1, cdeltS1, restfrq, restwav, ctypeS2,
                  crvalS2, cdeltS2, 0x0);
}

//----------------------------------------------------------------------------

int spcaips_(
  const char ctypeA[8],
  int *velref,
  char ctype[8],
  char specsys[8])

{
  char ctypeA_[9];
  wcsutil_strcvt(8, ' ', 1, ctypeA, ctypeA_);

  char ctype_[9], specsys_[9];
  int status = spcaips(ctypeA_, *velref, ctype_, specsys_);

  wcsutil_strcvt(8, ' ', 0, ctype_,   ctype);
  wcsutil_strcvt(8, ' ', 0, specsys_, specsys);

  return status;
}
