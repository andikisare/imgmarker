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
* $Id: spc.inc,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

*     Functions.
      EXTERNAL  SPCPUT,  SPCPTC,  SPCPTD,  SPCPTI,
     :          SPCGET,  SPCGTC,  SPCGTD,  SPCGTI,
     :          SPCINI,  SPCFREE, SPCSIZE, SPCENQ,  SPCPRT,  SPCPERR,
     :          SPCSET,  SPCX2S,  SPCS2X,
     :          SPCTYPE, SPCSPXE, SPCXPSE, SPCTRNE, SPCAIPS

      INTEGER   SPCPUT,  SPCPTC,  SPCPTD,  SPCPTI,
     :          SPCGET,  SPCGTC,  SPCGTD,  SPCGTI,
     :          SPCINI,  SPCFREE, SPCSIZE, SPCENQ,  SPCPRT,  SPCPERR,
     :          SPCSET,  SPCX2S,  SPCS2X,
     :          SPCTYPE, SPCSPXE, SPCXPSE, SPCTRNE, SPCAIPS

*     Deprecated functions.
      EXTERNAL  SPCTYP, SPCSPX, SPCXPS, SPCTRN
      INTEGER   SPCTYP, SPCSPX, SPCXPS, SPCTRN

*     Length of the SPCPRM data structure (INTEGER array) on 64-bit
*     machines.  Only needs to be 44 on 32-bit machines.
      INTEGER   SPCLEN
      PARAMETER (SPCLEN = 50)

*     Codes for SPC data structure elements used by SPCPUT and SPCGET.
      INTEGER   SPC_FLAG, SPC_TYPE, SPC_CODE, SPC_CRVAL, SPC_RESTFRQ,
     :          SPC_RESTWAV, SPC_PV

      PARAMETER (SPC_FLAG    = 100)
      PARAMETER (SPC_TYPE    = 101)
      PARAMETER (SPC_CODE    = 102)
      PARAMETER (SPC_CRVAL   = 103)
      PARAMETER (SPC_RESTFRQ = 104)
      PARAMETER (SPC_RESTWAV = 105)
      PARAMETER (SPC_PV      = 106)

*     Codes for SPC data structure elements used by SPCGET (only).
      INTEGER   SPC_W, SPC_ISGRISM, SPC_ERR

      PARAMETER (SPC_W       = 200)
      PARAMETER (SPC_ISGRISM = 201)
      PARAMETER (SPC_ERR     = 202)

*     Codes used by SPCENQ.
      INTEGER   SPCENQ_SET, SPCENQ_BYP

      PARAMETER (SPCENQ_SET = 2)
      PARAMETER (SPCENQ_BYP = 4)

*     Error codes and messages.
      INTEGER   SPCERR_NO_CHANGE, SPCERR_SUCCESS, SPCERR_NULL_POINTER,
     :          SPCERR_BAD_SPEC_PARAMS, SPCERR_BAD_X, SPCERR_BAD_SPEC

      PARAMETER (SPCERR_NO_CHANGE       = -1)
      PARAMETER (SPCERR_SUCCESS         =  0)
      PARAMETER (SPCERR_NULL_POINTER    =  1)
      PARAMETER (SPCERR_BAD_SPEC_PARAMS =  2)
      PARAMETER (SPCERR_BAD_X           =  3)
      PARAMETER (SPCERR_BAD_SPEC        =  4)

      CHARACTER SPC_ERRMSG(-1:4)*80
      COMMON /SPC_DATA/ SPC_ERRMSG
