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
* $Id: wcsfix.inc,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

*     Functions.
      EXTERNAL  WCSFIX, CDFIX, DATFIX, OBSFIX, UNITFIX, SPCFIX, CELFIX,
     :          CYLFIX, WCSPCX

      INTEGER   WCSFIX, CDFIX, DATFIX, OBSFIX, UNITFIX, SPCFIX, CELFIX,
     :          CYLFIX, WCSPCX

*     Flag bits for the RELAX argument.
      INTEGER   WCSFIX_CD, WCSFIX_DAT, WCSFIX_OBS, WCSFIX_UNIT,
     :          WCSFIX_CEL, WCSFIX_SPC, WCSFIX_CYL, WCSFIX_NWCS

      PARAMETER (WCSFIX_CD   = 1)
      PARAMETER (WCSFIX_DAT  = 2)
      PARAMETER (WCSFIX_OBS  = 3)
      PARAMETER (WCSFIX_UNIT = 4)
      PARAMETER (WCSFIX_CEL  = 5)
      PARAMETER (WCSFIX_SPC  = 6)
      PARAMETER (WCSFIX_CYL  = 7)
      PARAMETER (WCSFIX_NWCS = 7)

*     Error codes and messages.
      INTEGER   FIXERR_NO_CHANGE, FIXERR_SUCCESS, FIXERR_NULL_POINTER,
     :          FIXERR_MEMORY, FIXERR_SINGULAR_MTX, FIXERR_BAD_CTYPE,
     :          FIXERR_BAD_PARAM, FIXERR_BAD_COORD_TRANS,
     :          FIXERR_ILL_COORD_TRANS, FIXERR_BAD_CORNER_PIX,
     :          FIXERR_NO_REF_PIX_COORD, FIXERR_NO_REF_PIX_VAL

      PARAMETER (FIXERR_NO_CHANGE        = -1)
      PARAMETER (FIXERR_SUCCESS          =  0)
      PARAMETER (FIXERR_NULL_POINTER     =  1)
      PARAMETER (FIXERR_MEMORY           =  2)
      PARAMETER (FIXERR_SINGULAR_MTX     =  3)
      PARAMETER (FIXERR_BAD_CTYPE        =  4)
      PARAMETER (FIXERR_BAD_PARAM        =  5)
      PARAMETER (FIXERR_BAD_COORD_TRANS  =  6)
      PARAMETER (FIXERR_ILL_COORD_TRANS  =  7)
      PARAMETER (FIXERR_BAD_CORNER_PIX   =  8)
      PARAMETER (FIXERR_NO_REF_PIX_COORD =  9)
      PARAMETER (FIXERR_NO_REF_PIX_VAL   = 10)

      CHARACTER WCSFIX_ERRMSG(-1:10)*80
      COMMON /WCSFIX_DATA/ WCSFIX_ERRMSG
