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
  $Id: wcshdr_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*===========================================================================*/

#include <stdio.h>

#include <wcshdr.h>
#include <wcs.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define wcspih_   F77_FUNC(wcspih,   WCSPIH)
#define wcsbth_   F77_FUNC(wcsbth,   WCSBTH)
#define wcstab_   F77_FUNC(wcstab,   WCSTAB)
#define wcsidx_   F77_FUNC(wcsidx,   WCSIDX)
#define wcsbdx_   F77_FUNC(wcsbdx,   WCSBDX)
#define wcsvcopy_ F77_FUNC(wcsvcopy, WCSVCOPY)
#define wcsvfree_ F77_FUNC(wcsvfree, WCSVFREE)

#ifdef BINDC
  #undef  wcspih_
  #define wcspih_ wcspih_c

  #undef  wcsbth_
  #define wcsbth_ wcsbth_c
#endif

//----------------------------------------------------------------------------

int wcspih_(
  char header[],
  const int *nkeys,
  const int *relax,
  const int *ctrl,
  int *nreject,
  int *nwcs,
  iptr wcsp)

{
  // This may or may not force the Fortran I/O buffers to be flushed.  If
  // not, try CALL FLUSH(6) before calling WCSPIH in the Fortran code.
  fflush(NULL);

  return wcspih(header, *nkeys, *relax, *ctrl, nreject, nwcs,
    (struct wcsprm **)wcsp);
}

//----------------------------------------------------------------------------

int wcsbth_(
  char header[],
  const int *nkeys,
  const int *relax,
  const int *ctrl,
  const int *keysel,
  int *colsel,
  int *nreject,
  int *nwcs,
  iptr wcsp)

{
  // This may or may not force the Fortran I/O buffers to be flushed.  If
  // not, try CALL FLUSH(6) before calling WCSBTH in the Fortran code.
  fflush(NULL);

  return wcsbth(header, *nkeys, *relax, *ctrl, *keysel, colsel, nreject,
    nwcs, (struct wcsprm **)wcsp);
}

//----------------------------------------------------------------------------

int wcstab_(int *wcs)

{
  return wcstab((struct wcsprm *)wcs);
}

//----------------------------------------------------------------------------

int wcsidx_(int *nwcs, iptr wcsp, int alts[27])

{
  return wcsidx(*nwcs, (struct wcsprm **)wcsp, alts);
}

//----------------------------------------------------------------------------

int wcsbdx_(int *nwcs, iptr wcsp, int *type, short alts[1000][28])

{
  return wcsbdx(*nwcs, (struct wcsprm **)wcsp, *type, alts);
}

//----------------------------------------------------------------------------

int wcsvcopy_(const iptr wcspp, const int *i, int *wcs)

{
  struct wcsprm *wcsdst, *wcssrc;

  // Do a shallow copy.
  wcssrc = *((struct wcsprm **)wcspp) + *i;
  wcsdst = (struct wcsprm *)wcs;
  *wcsdst = *wcssrc;

  // Prevent wcsfree(wcsdst) freeing memory that is used by wcssrc.  On
  // the other hand, beware that wcsfree(wcssrc) will free the "given"
  // members of wcsdst for which memory was allocated by wcsini().

  // Don't take any error messages.
  wcsdst->err         = 0x0;
  wcsdst->lin.err     = 0x0;
  wcsdst->cel.err     = 0x0;
  wcsdst->spc.err     = 0x0;
  wcsdst->cel.prj.err = 0x0;

  // Don't take memory allocated by wcsini()...
  wcsdst->m_flag  = 0;
  wcsdst->m_naxis = 0;
  wcsdst->m_crpix = 0x0;
  wcsdst->m_pc    = 0x0;
  wcsdst->m_cdelt = 0x0;
  wcsdst->m_crval = 0x0;
  wcsdst->m_cunit = 0x0;
  wcsdst->m_ctype = 0x0;
  wcsdst->m_pv    = 0x0;
  wcsdst->m_ps    = 0x0;
  wcsdst->m_cd    = 0x0;
  wcsdst->m_crota = 0x0;
  wcsdst->m_colax = 0x0;
  wcsdst->m_cname = 0x0;
  wcsdst->m_crder = 0x0;
  wcsdst->m_csyer = 0x0;
  wcsdst->m_tab   = 0x0;
  wcsdst->m_wtb   = 0x0;

  // ...or by wcsset().
  wcsdst->types   = 0x0;
  wcsdst->flag    = 0;

  // Don't take memory allocated by linini()...
  wcsdst->lin.m_flag   = 0;
  wcsdst->lin.m_naxis  = 0x0;
  wcsdst->lin.m_crpix  = 0x0;
  wcsdst->lin.m_pc     = 0x0;
  wcsdst->lin.m_cdelt  = 0x0;
  wcsdst->lin.m_dispre = 0x0;
  wcsdst->lin.m_disseq = 0x0;

  // ...or by linset().
  wcsdst->lin.piximg   = 0x0;
  wcsdst->lin.imgpix   = 0x0;
  wcsdst->lin.flag     = 0;

  return 0;
}

//----------------------------------------------------------------------------

int wcsvfree_(int *nwcs, iptr wcspp)

{
  return wcsvfree(nwcs, (struct wcsprm **)wcspp);
}
