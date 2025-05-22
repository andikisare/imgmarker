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
* $Id: tab.inc,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

*     Functions.
      EXTERNAL  TABPUT, TABPTD, TABPTI,  TABGET, TABGTD,  TABGTI,
     :          TABINI, TABMEM, TABCPY,  TABCMP, TABFREE, TABSIZE,
     :          TABENQ, TABPRT, TABPERR, TABSET, TABX2S, TABS2X

      INTEGER   TABPUT, TABPTD, TABPTI,  TABGET, TABGTD,  TABGTI,
     :          TABINI, TABMEM, TABCPY,  TABCMP, TABFREE, TABSIZE,
     :          TABENQ, TABPRT, TABPERR, TABSET, TABX2S, TABS2X

*     Length of the TABPRM data structure (INTEGER array) on 64-bit
*     machines.  Only needs to be 24 on 32-bit machines.
      INTEGER   TABLEN
      PARAMETER (TABLEN = 40)

*     Codes for TAB data structure elements used by TABPUT and TABGET.
      INTEGER   TAB_FLAG, TAB_M, TAB_K, TAB_MAP, TAB_CRVAL, TAB_INDEX,
     :          TAB_COORD

      PARAMETER (TAB_FLAG    = 100)
      PARAMETER (TAB_M       = 101)
      PARAMETER (TAB_K       = 102)
      PARAMETER (TAB_MAP     = 103)
      PARAMETER (TAB_CRVAL   = 104)
      PARAMETER (TAB_INDEX   = 105)
      PARAMETER (TAB_COORD   = 106)

*     Codes for TAB data structure elements used by TABGET (only).
      INTEGER   TAB_NC, TAB_SENSE, TAB_P0, TAB_DELTA, TAB_EXTREMA,
     :          TAB_ERR

      PARAMETER (TAB_NC      = 200)
      PARAMETER (TAB_SENSE   = 201)
      PARAMETER (TAB_P0      = 202)
      PARAMETER (TAB_DELTA   = 203)
      PARAMETER (TAB_EXTREMA = 204)
      PARAMETER (TAB_ERR     = 205)

*     Codes used by TABENQ.
      INTEGER   TABENQ_MEM, TABENQ_SET, TABENQ_BYP

      PARAMETER (TABENQ_MEM = 1)
      PARAMETER (TABENQ_SET = 2)
      PARAMETER (TABENQ_BYP = 4)

*     Error codes and messages.
      INTEGER   TABERR_SUCCESS, TABERR_NULL_POINTER, TABERR_MEMORY,
     :          TABERR_BAD_PARAMS, TABERR_BAD_X, TABERR_BAD_WORLD

      PARAMETER (TABERR_SUCCESS      = 0)
      PARAMETER (TABERR_NULL_POINTER = 1)
      PARAMETER (TABERR_MEMORY       = 2)
      PARAMETER (TABERR_BAD_PARAMS   = 3)
      PARAMETER (TABERR_BAD_X        = 4)
      PARAMETER (TABERR_BAD_WORLD    = 5)

      CHARACTER TAB_ERRMSG(0:5)*80
      COMMON /TAB_DATA/ TAB_ERRMSG
