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
* $Id: wcserr.inc,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

*     Functions.
      EXTERNAL  WCSERR_GET, WCSERR_GTC, WCSERR_GTI,
     :          WCSERR_ENABLE, WCSERR_SIZE, WCSERR_PRT, WCSERR_CLEAR

      INTEGER   WCSERR_GET, WCSERR_GTC, WCSERR_GTI,
     :          WCSERR_ENABLE, WCSERR_SIZE, WCSERR_PRT, WCSERR_CLEAR

*     Length of the WCSERR data structure (INTEGER array) on 64-bit
*     machines.  Only needs to be 5 on 32-bit machines.
      INTEGER   ERRLEN
      PARAMETER (ERRLEN = 8)

*     Codes for WCSERR data structure elements used by WCSERR_GET.
      INTEGER   WCSERR_STATUS, WCSERR_LINE_NO, WCSERR_FUNCTION,
     :          WCSERR_FILE, WCSERR_MSG

      PARAMETER (WCSERR_STATUS   = 200)
      PARAMETER (WCSERR_LINE_NO  = 201)
      PARAMETER (WCSERR_FUNCTION = 202)
      PARAMETER (WCSERR_FILE     = 203)
      PARAMETER (WCSERR_MSG      = 204)

*     Size of character variable that can hold the largest messages.
      INTEGER   WCSERR_MSG_LENGTH
      PARAMETER (WCSERR_MSG_LENGTH = 512)
