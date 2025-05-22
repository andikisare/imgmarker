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
* $Id: cel.inc,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

*     Functions.
      EXTERNAL  CELPUT, CELPTC,  CELPTD,  CELPTI,
     :          CELGET, CELGTC,  CELGTD,  CELGTI,
     :          CELINI, CELFREE, CELSIZE, CELENQ, CELPRT, CELPERR,
     :          CELSET, CELX2S,  CELS2X

      INTEGER   CELPUT, CELPTC,  CELPTD,  CELPTI,
     :          CELGET, CELGTC,  CELGTD,  CELGTI,
     :          CELINI, CELFREE, CELSIZE, CELENQ, CELPRT, CELPERR,
     :          CELSET, CELX2S,  CELS2X

*     Length of the CELPRM data structure (INTEGER array) on 64-bit
*     machines.  Only needs to be 144 on 32-bit machines.
      INTEGER   CELLEN
      PARAMETER (CELLEN = 150)

*     Codes for CEL data structure elements used by CELPUT and CELGET.
      INTEGER   CEL_FLAG, CEL_OFFSET, CEL_PHI0, CEL_THETA0, CEL_REF,
     :          CEL_PRJ

      PARAMETER (CEL_FLAG   = 100)
      PARAMETER (CEL_OFFSET = 101)
      PARAMETER (CEL_PHI0   = 102)
      PARAMETER (CEL_THETA0 = 103)
      PARAMETER (CEL_REF    = 104)
      PARAMETER (CEL_PRJ    = 105)

*     Codes for CEL data structure elements used by CELGET (only).
      INTEGER   CEL_EULER, CEL_LATPRQ, CEL_ISOLAT, CEL_ERR

      PARAMETER (CEL_EULER  = 200)
      PARAMETER (CEL_LATPRQ = 201)
      PARAMETER (CEL_ISOLAT = 202)
      PARAMETER (CEL_ERR    = 203)

*     Codes used by CELENQ.
      INTEGER   CELENQ_SET, CELENQ_BYP

      PARAMETER (CELENQ_SET = 2)
      PARAMETER (CELENQ_BYP = 4)

*     Error codes and messages.
      INTEGER   CELERR_SUCCESS, CELERR_NULL_POINTER, CELERR_BAD_PARAM,
     :          CELERR_BAD_COORD_TRANS, CELERR_ILL_COORD_TRANS,
     :          CELERR_BAD_PIX, CELERR_BAD_WORLD

      PARAMETER (CELERR_SUCCESS         = 0)
      PARAMETER (CELERR_NULL_POINTER    = 1)
      PARAMETER (CELERR_BAD_PARAM       = 2)
      PARAMETER (CELERR_BAD_COORD_TRANS = 3)
      PARAMETER (CELERR_ILL_COORD_TRANS = 4)
      PARAMETER (CELERR_BAD_PIX         = 5)
      PARAMETER (CELERR_BAD_WORLD       = 6)

      CHARACTER CEL_ERRMSG(0:6)*80
      COMMON /CEL_DATA/ CEL_ERRMSG
