*=======================================================================
* WCSLIB 8.4 - an implementation of the FITS WCS standard.
* Copyright (C) 1995-2024, Mark Calabretta
*
* This file is part of WCSLIB.
*
* WCSLIB is free software: you can redistribute it and/or modify it
* under the terms of the GNU Lesser General Public License as published
* by the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* WCSLIB is distributed in the hope that it will be useful, but WITHOUT
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
* FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
* License for more details.
*
* You should have received a copy of the GNU Lesser General Public
* License along with WCSLIB.  If not, see http://www.gnu.org/licenses.
*
* Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
* http://www.atnf.csiro.au/people/Mark.Calabretta
* $Id: wcshdr.inc,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

*     Functions.
      EXTERNAL  WCSPIH, WCSBTH, WCSTAB, WCSIDX, WCSBDX, WCSVFREE,
     :          WCSVCOPY

      INTEGER   WCSPIH, WCSBTH, WCSTAB, WCSIDX, WCSBDX, WCSVFREE,
     :          WCSVCOPY

*     Flag bits for the RELAX argument.
      INTEGER   WCSHDR_none, WCSHDR_all, WCSHDR_reject, WCSHDR_strict

      PARAMETER (WCSHDR_none     = 0)
      PARAMETER (WCSHDR_all      = 2**20 - 1)
      PARAMETER (WCSHDR_reject   = 2**28)
      PARAMETER (WCSHDR_strict   = 2**29)

      INTEGER   WCSHDR_CROTAia,  WCSHDR_EPOCHa,   WCSHDR_VELREFa,
     :          WCSHDR_CD00i00j, WCSHDR_PC00i00j, WCSHDR_PROJPn,
     :          WCSHDR_CD0i_0ja, WCSHDR_PC0i_0ja, WCSHDR_PV0i_0ma,
     :          WCSHDR_PS0i_0ma, WCSHDR_RADECSYS, WCSHDR_VSOURCE,
     :          WCSHDR_DOBSn,    WCSHDR_LONGKEY,  WCSHDR_CNAMn,
     :          WCSHDR_AUXIMG,   WCSHDR_ALLIMG

      PARAMETER (WCSHDR_CROTAia  = 2**0)
      PARAMETER (WCSHDR_EPOCHa   = 2**1)
      PARAMETER (WCSHDR_VELREFa  = 2**2)
      PARAMETER (WCSHDR_CD00i00j = 2**3)
      PARAMETER (WCSHDR_PC00i00j = 2**4)
      PARAMETER (WCSHDR_PROJPn   = 2**5)
      PARAMETER (WCSHDR_CD0i_0ja = 2**6)
      PARAMETER (WCSHDR_PC0i_0ja = 2**7)
      PARAMETER (WCSHDR_PV0i_0ma = 2**8)
      PARAMETER (WCSHDR_PS0i_0ma = 2**9)
      PARAMETER (WCSHDR_RADECSYS = 2**10)
      PARAMETER (WCSHDR_VSOURCE  = 2**11)
      PARAMETER (WCSHDR_DOBSn    = 2**12)
      PARAMETER (WCSHDR_LONGKEY  = 2**13)
      PARAMETER (WCSHDR_CNAMn    = 2**14)
      PARAMETER (WCSHDR_AUXIMG   = 2**15)
      PARAMETER (WCSHDR_ALLIMG   = 2**16)

      INTEGER   WCSHDR_IMGHEAD, WCSHDR_BIMGARR, WCSHDR_PIXLIST

      PARAMETER (WCSHDR_IMGHEAD  = 2**21)
      PARAMETER (WCSHDR_BIMGARR  = 2**22)
      PARAMETER (WCSHDR_PIXLIST  = 2**23)

*     Error codes and messages.
      INTEGER   WCSHDRERR_SUCCESS, WCSHDRERR_NULL_POINTER,
     :          WCSHDRERR_MEMORY,  WCSHDRERR_BAD_COLUMN,
     :          WCSHDRERR_PARSER,  WCSHDRERR_BAD_TABULAR_PARAMS

      PARAMETER (WCSHDRERR_SUCCESS            = 0)
      PARAMETER (WCSHDRERR_NULL_POINTER       = 1)
      PARAMETER (WCSHDRERR_MEMORY             = 2)
      PARAMETER (WCSHDRERR_BAD_COLUMN         = 3)
      PARAMETER (WCSHDRERR_PARSER             = 4)
      PARAMETER (WCSHDRERR_BAD_TABULAR_PARAMS = 5)

      CHARACTER WCSHDR_ERRMSG(0:5)*80
      COMMON /WCSHDR_DATA/ WCSHDR_ERRMSG
