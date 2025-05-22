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
* $Id: lin.inc,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

*     Functions.
      EXTERNAL  LINPUT,  LINPTD,  LINPTI, LINGET,  LINGTD, LINGTI,
     :          LININI,  LININIT, LINDIS, LINDIST, LINCPY, LINFREE,
     :          LINSIZE, LINENQ,  LINPRT,  LINPERR,
     :          LINSET,  LINP2X,  LINX2P, LINWARP

      INTEGER   LINPUT,  LINPTD,  LINPTI, LINGET,  LINGTD, LINGTI,
     :          LININI,  LININIT, LINDIS, LINDIST, LINCPY, LINFREE,
     :          LINSIZE, LINENQ,  LINPRT,  LINPERR,
     :          LINSET,  LINP2X,  LINX2P, LINWARP

*     Length of the LINPRM data structure (INTEGER array) on 64-bit
*     machines.  Only needs to be 22 on 32-bit machines.
      INTEGER   LINLEN
      PARAMETER (LINLEN = 36)

*     Codes for LIN data structure elements used by LINPUT and LINGET.
      INTEGER   LIN_FLAG, LIN_NAXIS, LIN_CRPIX, LIN_PC, LIN_CDELT,
     :          LIN_DISPRE, LIN_DISSEQ

      PARAMETER (LIN_FLAG   = 100)
      PARAMETER (LIN_NAXIS  = 101)
      PARAMETER (LIN_CRPIX  = 102)
      PARAMETER (LIN_PC     = 103)
      PARAMETER (LIN_CDELT  = 104)
      PARAMETER (LIN_DISPRE = 105)
      PARAMETER (LIN_DISSEQ = 106)

*     Codes for LIN data structure elements used by LINGET (only).
      INTEGER   LIN_PIXIMG, LIN_IMGPIX, LIN_INAXIS, LIN_UNITY,
     :          LIN_AFFINE, LIN_SIMPLE, LIN_ERR

      PARAMETER (LIN_PIXIMG = 200)
      PARAMETER (LIN_IMGPIX = 201)
      PARAMETER (LIN_INAXIS = 202)
      PARAMETER (LIN_UNITY  = 203)
      PARAMETER (LIN_AFFINE = 204)
      PARAMETER (LIN_SIMPLE = 205)
      PARAMETER (LIN_ERR    = 206)

*     Codes used by LINENQ.
      INTEGER   LINENQ_MEM, LINENQ_SET, LINENQ_BYP

      PARAMETER (LINENQ_MEM = 1)
      PARAMETER (LINENQ_SET = 2)
      PARAMETER (LINENQ_BYP = 4)

*     Error codes and messages.
      INTEGER   LINERR_SUCCESS, LINERR_NULL_POINTER, LINERR_MEMORY,
     :          LINERR_SINGULAR_MTX, LINERR_DISTORT_INIT,
     :          LINERR_DISTORT, LINERR_DEDISTORT

      PARAMETER (LINERR_SUCCESS      = 0)
      PARAMETER (LINERR_NULL_POINTER = 1)
      PARAMETER (LINERR_MEMORY       = 2)
      PARAMETER (LINERR_SINGULAR_MTX = 3)
      PARAMETER (LINERR_DISTORT_INIT = 4)
      PARAMETER (LINERR_DISTORT      = 5)
      PARAMETER (LINERR_DEDISTORT    = 6)

      CHARACTER LIN_ERRMSG(0:6)*80
      COMMON /LIN_DATA/ LIN_ERRMSG
