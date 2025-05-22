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
  $Id: wcs_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*===========================================================================*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <wcserr.h>
#include <wcsmath.h>
#include <wcsutil.h>
#include <wcs.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define wcsput_  F77_FUNC(wcsput,  WCSPUT)
#define wcsptc_  F77_FUNC(wcsptc,  WCSPTC)
#define wcsptd_  F77_FUNC(wcsptd,  WCSPTD)
#define wcspti_  F77_FUNC(wcspti,  WCSPTI)
#define wcsget_  F77_FUNC(wcsget,  WCSGET)
#define wcsgtc_  F77_FUNC(wcsgtc,  WCSGTC)
#define wcsgtd_  F77_FUNC(wcsgtd,  WCSGTD)
#define wcsgti_  F77_FUNC(wcsgti,  WCSGTI)

#define wcsnpv_  F77_FUNC(wcsnpv,  WCSNPV)
#define wcsnps_  F77_FUNC(wcsnps,  WCSNPS)
#define wcsini_  F77_FUNC(wcsini,  WCSINI)
#define wcsinit_ F77_FUNC(wcsinit, WCSINIT)
#define wcssub_  F77_FUNC(wcssub,  WCSSUB)
#define wcscompare_  F77_FUNC(wcscompare,  WCSCOMPARE)
#define wcsfree_ F77_FUNC(wcsfree, WCSFREE)
#define wcstrim_ F77_FUNC(wcstrim, WCSTRIM)
#define wcssize_ F77_FUNC(wcssize, WCSSIZE)
#define auxsize_ F77_FUNC(auxsize, AUXSIZE)
#define wcsenq_  F77_FUNC(wcsenq,  WCSENQ)
#define wcsprt_  F77_FUNC(wcsprt,  WCSPRT)
#define wcsperr_ F77_FUNC(wcsperr, WCSPERR)
#define wcsbchk_ F77_FUNC(wcsbchk, WCSBCHK)
#define wcsset_  F77_FUNC(wcsset,  WCSSET)
#define wcsp2s_  F77_FUNC(wcsp2s,  WCSP2S)
#define wcss2p_  F77_FUNC(wcss2p,  WCSS2P)
#define wcsmix_  F77_FUNC(wcsmix,  WCSMIX)
#define wcsccs_  F77_FUNC(wcsccs,  WCSCCS)
#define wcssptr_ F77_FUNC(wcssptr, WCSSPTR)
#define wcscopy_ F77_FUNC(wcscopy, WCSCOPY)
#define wcslib_version_ F77_FUNC(wcslib_version, WCSLIB_VERSION)

#ifdef BINDC
  #undef  wcsptc_
  #define wcsptc_ wcsptc_c

  #undef  wcsgtc_
  #define wcsgtc_ wcsgtc_c

  #undef  wcsperr_
  #define wcsperr_ wcsperr_c

  #undef  wcsccs_
  #define wcsccs_ wcsccs_c

  #undef  wcssptr_
  #define wcssptr_ wcssptr_c

  #undef  wcslib_version_
  #define wcslib_version_ wcslib_version_c
#endif

// Must match the value set in wcs.inc.
#define WCS_FLAG     100
#define WCS_NAXIS    101
#define WCS_CRPIX    102
#define WCS_PC       103
#define WCS_CDELT    104
#define WCS_CRVAL    105
#define WCS_CUNIT    106
#define WCS_CTYPE    107
#define WCS_LONPOLE  108
#define WCS_LATPOLE  109
#define WCS_RESTFRQ  110
#define WCS_RESTWAV  111
#define WCS_NPV      112
#define WCS_NPVMAX   113
#define WCS_PV       114
#define WCS_NPS      115
#define WCS_NPSMAX   116
#define WCS_PS       117
#define WCS_CD       118
#define WCS_CROTA    119
#define WCS_ALTLIN   120
#define WCS_VELREF   121

#define WCS_ALT      122
#define WCS_COLNUM   123
#define WCS_COLAX    124

#define WCS_CNAME    125
#define WCS_CRDER    126
#define WCS_CSYER    127
#define WCS_CZPHS    128
#define WCS_CPERI    129

#define WCS_WCSNAME  130

#define WCS_TIMESYS  131
#define WCS_TREFPOS  132
#define WCS_TREFDIR  133
#define WCS_PLEPHEM  134
#define WCS_TIMEUNIT 135
#define WCS_DATEREF  136
#define WCS_MJDREF   137
#define WCS_TIMEOFFS 138

#define WCS_DATEOBS  139
#define WCS_DATEBEG  140
#define WCS_DATEAVG  141
#define WCS_DATEEND  142
#define WCS_MJDOBS   143
#define WCS_MJDBEG   144
#define WCS_MJDAVG   145
#define WCS_MJDEND   146
#define WCS_JEPOCH   147
#define WCS_BEPOCH   148
#define WCS_TSTART   149
#define WCS_TSTOP    150
#define WCS_XPOSURE  151
#define WCS_TELAPSE  152

#define WCS_TIMSYER  153
#define WCS_TIMRDER  154
#define WCS_TIMEDEL  155
#define WCS_TIMEPIXR 156

#define WCS_OBSGEO   157
#define WCS_OBSORBIT 158
#define WCS_RADESYS  159
#define WCS_EQUINOX  160
#define WCS_SPECSYS  161
#define WCS_SSYSOBS  162
#define WCS_VELOSYS  163
#define WCS_ZSOURCE  164
#define WCS_SSYSSRC  165
#define WCS_VELANGL  166

#define WCS_RSUN_REF 167
#define WCS_DSUN_OBS 168
#define WCS_CRLN_OBS 169
#define WCS_HGLN_OBS 170
#define WCS_HGLT_OBS 171
#define WCS_A_RADIUS 172
#define WCS_B_RADIUS 173
#define WCS_C_RADIUS 174
#define WCS_BLON_OBS 175
#define WCS_BLAT_OBS 176
#define WCS_BDIS_OBS 177

#define WCS_NTAB     200
#define WCS_NWTB     201
#define WCS_TAB      202
#define WCS_WTB      203
#define WCS_LNGTYP   204
#define WCS_LATTYP   205
#define WCS_LNG      206
#define WCS_LAT      207
#define WCS_SPEC     208
#define WCS_TIME     209
#define WCS_CUBEFACE 210
#define WCS_TYPES    211
#define WCS_LIN      212
#define WCS_CEL      213
#define WCS_SPC      214
#define WCS_ERR      215

//----------------------------------------------------------------------------

int wcsput_(
  int *wcs,
  const int *what,
  const void *value,
  const int *i,
  const int *j)

{
  int k;
  const char *cvalp;
  const int  *ivalp;
  const double *dvalp;
  struct wcsprm *wcsp;

  // Cast pointers.
  wcsp  = (struct wcsprm *)wcs;
  cvalp = (const char *)value;
  ivalp = (const int *)value;
  dvalp = (const double *)value;

  // Preserve bypass mode.
  int flag = 0;
  if (wcsp->flag == 1 || wcsp->flag < 0) flag = 1;

  // Convert 1-relative FITS axis numbers to 0-relative C array indices.
  int i0 = *i - 1;
  int j0 = *j - 1;

  switch (*what) {
  case WCS_FLAG:
    wcsp->flag = *ivalp;
    break;
  case WCS_NAXIS:
    wcsp->naxis = *ivalp;
    wcsp->flag = flag;
    break;
  case WCS_CRPIX:
    wcsp->crpix[i0] = *dvalp;
    wcsp->flag = flag;
    break;
  case WCS_PC:
    k = (i0)*(wcsp->naxis) + (j0);
    *(wcsp->pc+k) = *dvalp;
    wcsp->flag = flag;
    break;
  case WCS_CDELT:
    wcsp->cdelt[i0] = *dvalp;
    wcsp->flag = flag;
    break;
  case WCS_CRVAL:
    wcsp->crval[i0] = *dvalp;
    wcsp->flag = flag;
    break;
  case WCS_CUNIT:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->cunit[i0]);
    wcsp->flag = flag;
    break;
  case WCS_CTYPE:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->ctype[i0]);
    wcsp->flag = flag;
    break;
  case WCS_LONPOLE:
    wcsp->lonpole = *dvalp;
    wcsp->flag = flag;
    break;
  case WCS_LATPOLE:
    wcsp->latpole = *dvalp;
    wcsp->flag = flag;
    break;
  case WCS_RESTFRQ:
    wcsp->restfrq = *dvalp;
    wcsp->flag = flag;
    break;
  case WCS_RESTWAV:
    wcsp->restwav = *dvalp;
    wcsp->flag = flag;
    break;
  case WCS_NPV:
  case WCS_NPVMAX:
    return 1;
    break;
  case WCS_PV:
    (wcsp->pv + wcsp->npv)->i = *i;
    (wcsp->pv + wcsp->npv)->m = *j;
    (wcsp->pv + wcsp->npv)->value = *dvalp;
    (wcsp->npv)++;
    wcsp->flag = flag;
    break;
  case WCS_NPS:
  case WCS_NPSMAX:
    return 1;
    break;
  case WCS_PS:
    (wcsp->ps + wcsp->nps)->i = *i;
    (wcsp->ps + wcsp->nps)->m = *j;
    wcsutil_strcvt(72, '\0', 0, cvalp, (wcsp->ps + wcsp->nps)->value);
    (wcsp->nps)++;
    wcsp->flag = flag;
    break;
  case WCS_CD:
    k = (i0)*(wcsp->naxis) + (j0);
    *(wcsp->cd+k) = *dvalp;
    wcsp->flag = flag;
    break;
  case WCS_CROTA:
    wcsp->crota[i0] = *dvalp;
    wcsp->flag = flag;
    break;
  case WCS_ALTLIN:
    wcsp->altlin = *ivalp;
    wcsp->flag = flag;
    break;
  case WCS_VELREF:
    wcsp->velref = *ivalp;
    break;

  case WCS_ALT:
    wcsp->alt[0] = cvalp[0];
    memset((wcsp->alt)+1, '\0', 3);
    break;
  case WCS_COLNUM:
    wcsp->colnum = *ivalp;
    break;
  case WCS_COLAX:
    wcsp->colax[i0] = *ivalp;
    break;

  case WCS_CNAME:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->cname[i0]);
    break;
  case WCS_CRDER:
    wcsp->crder[i0] = *dvalp;
    break;
  case WCS_CSYER:
    wcsp->csyer[i0] = *dvalp;
    break;
  case WCS_CZPHS:
    wcsp->czphs[i0] = *dvalp;
    break;
  case WCS_CPERI:
    wcsp->cperi[i0] = *dvalp;
    break;

  case WCS_WCSNAME:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->wcsname);
    break;

  case WCS_TIMESYS:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->timesys);
    break;
  case WCS_TREFPOS:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->trefpos);
    break;
  case WCS_TREFDIR:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->trefdir);
    break;
  case WCS_PLEPHEM:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->plephem);
    break;
  case WCS_TIMEUNIT:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->timeunit);
    break;
  case WCS_DATEREF:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->dateref);
    break;
  case WCS_MJDREF:
    wcsp->mjdref[i0] = *dvalp;
    break;
  case WCS_TIMEOFFS:
    wcsp->timeoffs = *dvalp;
    break;

  case WCS_DATEOBS:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->dateobs);
    break;
  case WCS_DATEBEG:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->datebeg);
    break;
  case WCS_DATEAVG:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->dateavg);
    break;
  case WCS_DATEEND:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->dateend);
    break;
  case WCS_MJDOBS:
    wcsp->mjdobs = *dvalp;
    break;
  case WCS_MJDBEG:
    wcsp->mjdbeg = *dvalp;
    break;
  case WCS_MJDAVG:
    wcsp->mjdavg = *dvalp;
    break;
  case WCS_MJDEND:
    wcsp->mjdend = *dvalp;
    break;
  case WCS_JEPOCH:
    wcsp->jepoch = *dvalp;
    break;
  case WCS_BEPOCH:
    wcsp->bepoch = *dvalp;
    break;
  case WCS_TSTART:
    wcsp->tstart = *dvalp;
    break;
  case WCS_TSTOP:
    wcsp->tstop = *dvalp;
    break;
  case WCS_XPOSURE:
    wcsp->xposure = *dvalp;
    break;
  case WCS_TELAPSE:
    wcsp->telapse = *dvalp;
    break;

  case WCS_TIMSYER:
    wcsp->timsyer = *dvalp;
    break;
  case WCS_TIMRDER:
    wcsp->timrder = *dvalp;
    break;
  case WCS_TIMEDEL:
    wcsp->timedel = *dvalp;
    break;
  case WCS_TIMEPIXR:
    wcsp->timepixr = *dvalp;
    break;

  case WCS_OBSGEO:
    wcsp->obsgeo[i0] = *dvalp;
    break;
  case WCS_OBSORBIT:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->obsorbit);
    break;
  case WCS_RADESYS:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->radesys);
    break;
  case WCS_EQUINOX:
    wcsp->equinox = *dvalp;
    break;
  case WCS_SPECSYS:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->specsys);
    break;
  case WCS_SSYSOBS:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->ssysobs);
    break;
  case WCS_VELOSYS:
    wcsp->velosys = *dvalp;
    break;
  case WCS_ZSOURCE:
    wcsp->zsource = *dvalp;
    break;
  case WCS_SSYSSRC:
    wcsutil_strcvt(72, '\0', 0, cvalp, wcsp->ssyssrc);
    break;
  case WCS_VELANGL:
    wcsp->velangl = *dvalp;
    break;

  case WCS_RSUN_REF:
  case WCS_DSUN_OBS:
  case WCS_CRLN_OBS:
  case WCS_HGLN_OBS:
  case WCS_HGLT_OBS:
  case WCS_A_RADIUS:
  case WCS_B_RADIUS:
  case WCS_C_RADIUS:
  case WCS_BLON_OBS:
  case WCS_BLAT_OBS:
  case WCS_BDIS_OBS:
    if (wcsp->aux == 0x0) {
      if (wcsauxi(1, wcsp)) {
        return 2;
      }
    }

    switch (*what) {
    case WCS_RSUN_REF:
      wcsp->aux->rsun_ref = *dvalp;
      break;
    case WCS_DSUN_OBS:
      wcsp->aux->dsun_obs = *dvalp;
      break;
    case WCS_CRLN_OBS:
      wcsp->aux->crln_obs = *dvalp;
      break;
    case WCS_HGLN_OBS:
      wcsp->aux->hgln_obs = *dvalp;
      break;
    case WCS_HGLT_OBS:
      wcsp->aux->hglt_obs = *dvalp;
      break;
    case WCS_A_RADIUS:
      wcsp->aux->a_radius = *dvalp;
      break;
    case WCS_B_RADIUS:
      wcsp->aux->b_radius = *dvalp;
      break;
    case WCS_C_RADIUS:
      wcsp->aux->c_radius = *dvalp;
      break;
    case WCS_BLON_OBS:
      wcsp->aux->blon_obs = *dvalp;
      break;
    case WCS_BLAT_OBS:
      wcsp->aux->blat_obs = *dvalp;
      break;
    case WCS_BDIS_OBS:
      wcsp->aux->bdis_obs = *dvalp;
      break;
    }

    break;
  default:
    return 1;
  }

  return 0;
}

int wcsptc_(int *wcs, const int *what, const char *value, const int *i,
  const int *j)
{
  return wcsput_(wcs, what, value, i, j);
}

int wcsptd_(int *wcs, const int *what, const double *value, const int *i,
  const int *j)
{
  return wcsput_(wcs, what, value, i, j);
}

int wcspti_(int *wcs, const int *what, const int *value, const int *i,
  const int *j)
{
  return wcsput_(wcs, what, value, i, j);
}

//----------------------------------------------------------------------------

int wcsget_(const int *wcs, const int *what, void *value)

{
  // Cast pointers.
  const struct wcsprm *wcsp = (const struct wcsprm *)wcs;
  char   *cvalp = (char *)value;
  int    *ivalp = (int *)value;
  double *dvalp = (double *)value;

  int naxis = wcsp->naxis;

  const int *iwcsp;
  switch (*what) {
  case WCS_FLAG:
    *ivalp = wcsp->flag;
    break;
  case WCS_NAXIS:
    *ivalp = naxis;
    break;
  case WCS_CRPIX:
    for (int i = 0; i < naxis; i++) {
      *(dvalp++) = wcsp->crpix[i];
    }
    break;
  case WCS_PC:
    // C row-major to FORTRAN column-major.
    for (int j = 0; j < naxis; j++) {
      const double *dwcsp = wcsp->pc + j;
      for (int i = 0; i < naxis; i++) {
        *(dvalp++) = *dwcsp;
        dwcsp += naxis;
      }
    }
    break;
  case WCS_CDELT:
    for (int i = 0; i < naxis; i++) {
      *(dvalp++) = wcsp->cdelt[i];
    }
    break;
  case WCS_CRVAL:
    for (int i = 0; i < naxis; i++) {
      *(dvalp++) = wcsp->crval[i];
    }
    break;
  case WCS_CUNIT:
    for (int i = 0; i < naxis; i++) {
      wcsutil_strcvt(72, ' ', 0, wcsp->cunit[i], cvalp);
      cvalp += 72;
    }
    break;
  case WCS_CTYPE:
    for (int i = 0; i < naxis; i++) {
      wcsutil_strcvt(72, ' ', 0, wcsp->ctype[i], cvalp);
      cvalp += 72;
    }
    break;
  case WCS_LONPOLE:
    *dvalp = wcsp->lonpole;
    break;
  case WCS_LATPOLE:
    *dvalp = wcsp->latpole;
    break;
  case WCS_RESTFRQ:
    *dvalp = wcsp->restfrq;
    break;
  case WCS_RESTWAV:
    *dvalp = wcsp->restwav;
    break;
  case WCS_NPV:
    *ivalp = wcsp->npv;
    break;
  case WCS_NPVMAX:
    *ivalp = wcsp->npvmax;
    break;
  case WCS_PV:
    for (int k = 0; k < wcsp->npv; k++) {
      *(dvalp++) = (wcsp->pv + k)->i;
      *(dvalp++) = (wcsp->pv + k)->m;
      *(dvalp++) = (wcsp->pv + k)->value;
    }
    break;
  case WCS_NPS:
    *ivalp = wcsp->nps;
    break;
  case WCS_NPSMAX:
    *ivalp = wcsp->npsmax;
    break;
  case WCS_PS:
    for (int k = 0; k < wcsp->nps; k++) {
      *(dvalp++) = (wcsp->ps + k)->i;
      *(dvalp++) = (wcsp->ps + k)->m;
      cvalp += 2*sizeof(double);
      wcsutil_strcvt(72, ' ', 0, (wcsp->ps + k)->value, cvalp);
      cvalp += 72;
    }
    break;
  case WCS_CD:
    // C row-major to FORTRAN column-major.
    for (int j = 0; j < naxis; j++) {
      const double *dwcsp = wcsp->cd + j;
      for (int i = 0; i < naxis; i++) {
        *(dvalp++) = *dwcsp;
        dwcsp += naxis;
      }
    }
    break;
  case WCS_CROTA:
    for (int i = 0; i < naxis; i++) {
      *(dvalp++) = wcsp->crota[i];
    }
    break;
  case WCS_ALTLIN:
    *ivalp = wcsp->altlin;
    break;
  case WCS_VELREF:
    *ivalp = wcsp->velref;
    break;

  case WCS_ALT:
    wcsutil_strcvt(4, ' ', 0, wcsp->alt, cvalp);
    break;
  case WCS_COLNUM:
    *ivalp = wcsp->colnum;
    break;
  case WCS_COLAX:
    for (int i = 0; i < naxis; i++) {
      *(ivalp++) = wcsp->colax[i];
    }
    break;

  case WCS_CNAME:
    for (int i = 0; i < naxis; i++) {
      wcsutil_strcvt(72, ' ', 0, wcsp->cname[i], cvalp);
      cvalp += 72;
    }
    break;
  case WCS_CRDER:
    for (int i = 0; i < naxis; i++) {
      *(dvalp++) = wcsp->crder[i];
    }
    break;
  case WCS_CSYER:
    for (int i = 0; i < naxis; i++) {
      *(dvalp++) = wcsp->csyer[i];
    }
    break;
  case WCS_CZPHS:
    for (int i = 0; i < naxis; i++) {
      *(dvalp++) = wcsp->czphs[i];
    }
    break;
  case WCS_CPERI:
    for (int i = 0; i < naxis; i++) {
      *(dvalp++) = wcsp->cperi[i];
    }
    break;

  case WCS_WCSNAME:
    wcsutil_strcvt(72, ' ', 0, wcsp->wcsname, cvalp);
    break;

  case WCS_TIMESYS:
    wcsutil_strcvt(72, ' ', 0, wcsp->timesys, cvalp);
    break;
  case WCS_TREFPOS:
    wcsutil_strcvt(72, ' ', 0, wcsp->trefpos, cvalp);
    break;
  case WCS_TREFDIR:
    wcsutil_strcvt(72, ' ', 0, wcsp->trefdir, cvalp);
    break;
  case WCS_PLEPHEM:
    wcsutil_strcvt(72, ' ', 0, wcsp->plephem, cvalp);
    break;
  case WCS_TIMEUNIT:
    wcsutil_strcvt(72, ' ', 0, wcsp->timeunit, cvalp);
    break;
  case WCS_DATEREF:
    wcsutil_strcvt(72, ' ', 0, wcsp->dateref, cvalp);
    break;
  case WCS_MJDREF:
    *(dvalp++) = wcsp->mjdref[0];
    *(dvalp++) = wcsp->mjdref[1];
    break;
  case WCS_TIMEOFFS:
    *dvalp = wcsp->timeoffs;
    break;

  case WCS_DATEOBS:
    wcsutil_strcvt(72, ' ', 0, wcsp->dateobs, cvalp);
    break;
  case WCS_DATEBEG:
    wcsutil_strcvt(72, ' ', 0, wcsp->datebeg, cvalp);
    break;
  case WCS_DATEAVG:
    wcsutil_strcvt(72, ' ', 0, wcsp->dateavg, cvalp);
    break;
  case WCS_DATEEND:
    wcsutil_strcvt(72, ' ', 0, wcsp->dateend, cvalp);
    break;
  case WCS_MJDOBS:
    *dvalp = wcsp->mjdobs;
    break;
  case WCS_MJDBEG:
    *dvalp = wcsp->mjdbeg;
    break;
  case WCS_MJDAVG:
    *dvalp = wcsp->mjdavg;
    break;
  case WCS_MJDEND:
    *dvalp = wcsp->mjdend;
    break;
  case WCS_JEPOCH:
    *dvalp = wcsp->jepoch;
    break;
  case WCS_BEPOCH:
    *dvalp = wcsp->bepoch;
    break;
  case WCS_TSTART:
    *dvalp = wcsp->tstart;
    break;
  case WCS_TSTOP:
    *dvalp = wcsp->tstop;
    break;
  case WCS_XPOSURE:
    *dvalp = wcsp->xposure;
    break;
  case WCS_TELAPSE:
    *dvalp = wcsp->telapse;
    break;

  case WCS_TIMSYER:
    *dvalp = wcsp->timsyer;
    break;
  case WCS_TIMRDER:
    *dvalp = wcsp->timrder;
    break;
  case WCS_TIMEDEL:
    *dvalp = wcsp->timedel;
    break;
  case WCS_TIMEPIXR:
    *dvalp = wcsp->timepixr;
    break;

  case WCS_OBSGEO:
    for (int i = 0; i < 6; i++) {
      *(dvalp++) = wcsp->obsgeo[i];
    }
    break;
  case WCS_OBSORBIT:
    wcsutil_strcvt(72, ' ', 0, wcsp->obsorbit, cvalp);
    break;
  case WCS_RADESYS:
    wcsutil_strcvt(72, ' ', 0, wcsp->radesys, cvalp);
    break;
  case WCS_EQUINOX:
    *dvalp = wcsp->equinox;
    break;
  case WCS_SPECSYS:
    wcsutil_strcvt(72, ' ', 0, wcsp->specsys, cvalp);
    break;
  case WCS_SSYSOBS:
    wcsutil_strcvt(72, ' ', 0, wcsp->ssysobs, cvalp);
    break;
  case WCS_VELOSYS:
    *dvalp = wcsp->velosys;
    break;
  case WCS_ZSOURCE:
    *dvalp = wcsp->zsource;
    break;
  case WCS_SSYSSRC:
    wcsutil_strcvt(72, ' ', 0, wcsp->ssyssrc, cvalp);
    break;
  case WCS_VELANGL:
    *dvalp = wcsp->velangl;
    break;

  case WCS_RSUN_REF:
    *dvalp = wcsp->aux ? wcsp->aux->rsun_ref : UNDEFINED;
    break;
  case WCS_DSUN_OBS:
    *dvalp = wcsp->aux ? wcsp->aux->dsun_obs : UNDEFINED;
    break;
  case WCS_CRLN_OBS:
    *dvalp = wcsp->aux ? wcsp->aux->crln_obs : UNDEFINED;
    break;
  case WCS_HGLN_OBS:
    *dvalp = wcsp->aux ? wcsp->aux->hgln_obs : UNDEFINED;
    break;
  case WCS_HGLT_OBS:
    *dvalp = wcsp->aux ? wcsp->aux->hglt_obs : UNDEFINED;
    break;
  case WCS_A_RADIUS:
    *dvalp = wcsp->aux ? wcsp->aux->a_radius : UNDEFINED;
    break;
  case WCS_B_RADIUS:
    *dvalp = wcsp->aux ? wcsp->aux->b_radius : UNDEFINED;
    break;
  case WCS_C_RADIUS:
    *dvalp = wcsp->aux ? wcsp->aux->c_radius : UNDEFINED;
    break;
  case WCS_BLON_OBS:
    *dvalp = wcsp->aux ? wcsp->aux->blon_obs : UNDEFINED;
    break;
  case WCS_BLAT_OBS:
    *dvalp = wcsp->aux ? wcsp->aux->blat_obs : UNDEFINED;
    break;
  case WCS_BDIS_OBS:
    *dvalp = wcsp->aux ? wcsp->aux->bdis_obs : UNDEFINED;
    break;

  case WCS_NTAB:
    *ivalp = wcsp->ntab;
    break;
  case WCS_NWTB:
    *ivalp = wcsp->nwtb;
    break;
  case WCS_TAB:
    *(void **)value = wcsp->tab;
    break;
  case WCS_WTB:
    *(void **)value = wcsp->wtb;
    break;
  case WCS_LNGTYP:
    wcsutil_strcvt(4, ' ', 0, wcsp->lngtyp, cvalp);
    break;
  case WCS_LATTYP:
    wcsutil_strcvt(4, ' ', 0, wcsp->lattyp, cvalp);
    break;
  case WCS_LNG:
    *ivalp = wcsp->lng + 1;
    break;
  case WCS_LAT:
    *ivalp = wcsp->lat + 1;
    break;
  case WCS_SPEC:
    *ivalp = wcsp->spec + 1;
    break;
  case WCS_TIME:
    *ivalp = wcsp->time + 1;
    break;
  case WCS_CUBEFACE:
    *ivalp = wcsp->cubeface;
    break;
  case WCS_TYPES:
    for (int i = 0; i < naxis; i++) {
      *(ivalp++) = wcsp->types[i];
    }
    break;
  case WCS_LIN:
    // Copy the contents of the linprm struct.
    iwcsp = (int *)(&(wcsp->lin));
    for (size_t l = 0; l < LINLEN; l++) {
      *(ivalp++) = *(iwcsp++);
    }
    break;
  case WCS_CEL:
    // Copy the contents of the celprm struct.
    iwcsp = (int *)(&(wcsp->cel));
    for (size_t l = 0; l < CELLEN; l++) {
      *(ivalp++) = *(iwcsp++);
    }
    break;
  case WCS_SPC:
    // Copy the contents of the spcprm struct.
    iwcsp = (int *)(&(wcsp->spc));
    for (size_t l = 0; l < SPCLEN; l++) {
      *(ivalp++) = *(iwcsp++);
    }
    break;
  case WCS_ERR:
    // Copy the contents of the wcserr struct.
    if (wcsp->err) {
    iwcsp = (int *)(wcsp->err);
      for (size_t l = 0; l < ERRLEN; l++) {
        *(ivalp++) = *(iwcsp++);
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

int wcsgtc_(const int *wcs, const int *what, char *value)
{
  return wcsget_(wcs, what, value);
}

int wcsgtd_(const int *wcs, const int *what, double *value)
{
  return wcsget_(wcs, what, value);
}

int wcsgti_(const int *wcs, const int *what, int *value)
{
  return wcsget_(wcs, what, value);
}

//----------------------------------------------------------------------------

int wcsnpv_(int *npvmax) { return wcsnpv(*npvmax); }
int wcsnps_(int *npsmax) { return wcsnps(*npsmax); }

//----------------------------------------------------------------------------

int wcsini_(const int *naxis, int *wcs)

{
  return wcsini(1, *naxis, (struct wcsprm *)wcs);
}

//----------------------------------------------------------------------------

int wcsinit_(
  const int *naxis,
  int *wcs,
  int *npvmax,
  int *npsmax,
  int *ndpmax)

{
  return wcsinit(1, *naxis, (struct wcsprm *)wcs, *npvmax, *npsmax, *ndpmax);
}

//----------------------------------------------------------------------------

int wcssub_(const int *wcssrc, int *nsub, int axes[], int *wcsdst)

{
  if (*nsub == -1 && *axes == -1) {
    // Interpreted as a signal that a deep copy is required.
    return wcssub(1, (const struct wcsprm *)wcssrc, 0x0, 0x0,
                  (struct wcsprm *)wcsdst);
  } else {
    // Beware that if *nsub == 0 it will be set on return so cannot be a
    // constant argument.
    return wcssub(1, (const struct wcsprm *)wcssrc, nsub, axes,
                  (struct wcsprm *)wcsdst);
  }
}

//----------------------------------------------------------------------------

int wcscompare_(
  const int *cmp,
  const double *tol,
  const int *wcs1,
  const int *wcs2,
  int *equal)

{
  return wcscompare(*cmp, *tol, (const struct wcsprm *)wcs1,
                    (const struct wcsprm *)wcs2, equal);
}

//----------------------------------------------------------------------------

int wcsfree_(int *wcs)

{
  return wcsfree((struct wcsprm *)wcs);
}

//----------------------------------------------------------------------------

int wcstrim_(int *wcs)

{
  return wcstrim((struct wcsprm *)wcs);
}

//----------------------------------------------------------------------------

int wcssize_(const int *wcs, int sizes[2])

{
  return wcssize((const struct wcsprm *)wcs, sizes);
}

//----------------------------------------------------------------------------

int auxsize_(const int *aux, int sizes[2])

{
  return auxsize((const struct auxprm *)aux, sizes);
}

//----------------------------------------------------------------------------

int wcsenq_(const int *wcs, int *enquiry)

{
  return wcsenq((const struct wcsprm *)wcs, *enquiry);
}

//----------------------------------------------------------------------------

int wcsprt_(const int *wcs)

{
  // This may or may not force the Fortran I/O buffers to be flushed.  If
  // not, try CALL FLUSH(6) before calling WCSPRT in the Fortran code.
  fflush(NULL);

  return wcsprt((const struct wcsprm *)wcs);
}

//----------------------------------------------------------------------------

// If null-terminated (using the Fortran CHAR(0) intrinsic), prefix may be of
// length less than but not exceeding 72 and trailing blanks are preserved.
// Otherwise, it must be of length 72 and trailing blanks are stripped off.

int wcsperr_(int *wcs, const char prefix[72])

{
  char prefix_[73];
  wcsutil_strcvt(72, '\0', 1, prefix, prefix_);

  // This may or may not force the Fortran I/O buffers to be flushed.
  // If not, try CALL FLUSH(6) before calling WCSPERR in the Fortran code.
  fflush(NULL);

  return wcsperr((struct wcsprm *)wcs, prefix_);
}

//----------------------------------------------------------------------------

int wcsbchk_(int *wcs, int *bounds)

{
  return wcsbchk((struct wcsprm *)wcs, *bounds);
}

//----------------------------------------------------------------------------

int wcsset_(int *wcs)

{
  return wcsset((struct wcsprm *)wcs);
}

//----------------------------------------------------------------------------

int wcsp2s_(
  int *wcs,
  const int *ncoord,
  const int *nelem,
  const double pixcrd[],
  double imgcrd[],
  double phi[],
  double theta[],
  double world[],
  int stat[])

{
  return wcsp2s((struct wcsprm *)wcs, *ncoord, *nelem, pixcrd, imgcrd, phi,
                theta, world, stat);
}

//----------------------------------------------------------------------------

int wcss2p_(
  int* wcs,
  const int *ncoord,
  const int *nelem,
  const double world[],
  double phi[],
  double theta[],
  double imgcrd[],
  double pixcrd[],
  int stat[])

{
  return wcss2p((struct wcsprm *)wcs, *ncoord, *nelem, world, phi, theta,
                imgcrd, pixcrd, stat);
}

//----------------------------------------------------------------------------

int wcsmix_(
  int *wcs,
  const int *mixpix,
  const int *mixcel,
  const double vspan[2],
  const double *vstep,
  int *viter,
  double world[],
  double phi[],
  double theta[],
  double imgcrd[],
  double pixcrd[])

{
  return wcsmix((struct wcsprm *)wcs, *mixpix-1, *mixcel, vspan, *vstep,
                *viter, world, phi, theta, imgcrd, pixcrd);
}

//----------------------------------------------------------------------------

int wcsccs_(
  int *wcs,
  const double *lng2p1,
  const double *lat2p1,
  const double *lng1p2,
  const char clng[4],
  const char clat[4],
  const char radesys[71],
  const double *equinox,
  const char alt[1])

{
  char clng_[5], clat_[5], radesys_[72];
  wcsutil_strcvt(4,  '\0', 1, clng, clng_);
  wcsutil_strcvt(4,  '\0', 1, clat, clat_);
  wcsutil_strcvt(71, '\0', 1, radesys, radesys_);

  int status = wcsccs((struct wcsprm *)wcs, *lng2p1, *lat2p1, *lng1p2, clng_,
                      clat_, radesys_, *equinox, alt);

  return status;
}

//----------------------------------------------------------------------------

int wcssptr_(
  int *wcs,
  int *i,
  char ctype[8])

{
  char ctype_[9];
  wcsutil_strcvt(8, ' ', 1, ctype, ctype_);

  int status = wcssptr((struct wcsprm *)wcs, i, ctype_);

  wcsutil_strcvt(8, ' ', 0, ctype_, ctype);

  return status;
}

//----------------------------------------------------------------------------

int wcscopy_(
  const int *wcssrc,
  int *wcsdst)

{
  return wcscopy(1, (const struct wcsprm *)wcssrc, (struct wcsprm *)wcsdst);
}

//----------------------------------------------------------------------------

void wcslib_version_(
  char *wcsver,
  int  *nchr)

{
  wcsutil_strcvt(*nchr, ' ', 0, wcslib_version(0x0), wcsver);
}
