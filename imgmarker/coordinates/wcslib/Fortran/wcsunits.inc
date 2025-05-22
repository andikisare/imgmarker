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
* $Id: wcsunits.inc,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

*     Functions.
      EXTERNAL  WCSUNITSE, WCSUTRNE, WCSULEXE
      INTEGER   WCSUNITSE, WCSUTRNE, WCSULEXE

*     Deprecated functions.
      EXTERNAL  WCSUNITS, WCSUTRN, WCSULEX
      INTEGER   WCSUNITS, WCSUTRN, WCSULEX

*     Array indices.
      INTEGER   WCSUNITS_PLANE_ANGLE, WCSUNITS_SOLID_ANGLE,
     :          WCSUNITS_CHARGE, WCSUNITS_MOLE, WCSUNITS_TEMPERATURE,
     :          WCSUNITS_LUMINTEN, WCSUNITS_MASS, WCSUNITS_LENGTH,
     :          WCSUNITS_TIME, WCSUNITS_BEAM, WCSUNITS_BIN,
     :          WCSUNITS_BIT, WCSUNITS_COUNT, WCSUNITS_MAGNITUDE,
     :          WCSUNITS_PIXEL, WCSUNITS_SOLRATIO, WCSUNITS_VOXEL,
     :          WCSUNITS_NTYPE

      PARAMETER (WCSUNITS_PLANE_ANGLE =  1)
      PARAMETER (WCSUNITS_SOLID_ANGLE =  2)
      PARAMETER (WCSUNITS_CHARGE      =  3)
      PARAMETER (WCSUNITS_MOLE        =  4)
      PARAMETER (WCSUNITS_TEMPERATURE =  5)
      PARAMETER (WCSUNITS_LUMINTEN    =  6)
      PARAMETER (WCSUNITS_MASS        =  7)
      PARAMETER (WCSUNITS_LENGTH      =  8)
      PARAMETER (WCSUNITS_TIME        =  9)
      PARAMETER (WCSUNITS_BEAM        = 10)
      PARAMETER (WCSUNITS_BIN         = 11)
      PARAMETER (WCSUNITS_BIT         = 12)
      PARAMETER (WCSUNITS_COUNT       = 13)
      PARAMETER (WCSUNITS_MAGNITUDE   = 14)
      PARAMETER (WCSUNITS_PIXEL       = 15)
      PARAMETER (WCSUNITS_SOLRATIO    = 16)
      PARAMETER (WCSUNITS_VOXEL       = 17)
      PARAMETER (WCSUNITS_NTYPE       = 17)

*     Error codes and messages.
      INTEGER   UNITSERR_SUCCESS, UNITSERR_BAD_NUM_MULTIPLIER,
     :          UNITSERR_DANGLING_BINOP, UNITSERR_BAD_INITIAL_SYMBOL,
     :          UNITSERR_FUNCTION_CONTEXT, UNITSERR_BAD_EXPON_SYMBOL,
     :          UNITSERR_UNBAL_BRACKET, UNITSERR_UNBAL_PAREN,
     :          UNITSERR_CONSEC_BINOPS, UNITSERR_PARSER_ERROR,
     :          UNITSERR_BAD_UNIT_SPEC, UNITSERR_BAD_FUNCS,
     :          UNITSERR_UNSAFE_TRANS

      PARAMETER (UNITSERR_SUCCESS            =  0)
      PARAMETER (UNITSERR_BAD_NUM_MULTIPLIER =  1)
      PARAMETER (UNITSERR_DANGLING_BINOP     =  2)
      PARAMETER (UNITSERR_BAD_INITIAL_SYMBOL =  3)
      PARAMETER (UNITSERR_FUNCTION_CONTEXT   =  4)
      PARAMETER (UNITSERR_BAD_EXPON_SYMBOL   =  5)
      PARAMETER (UNITSERR_UNBAL_BRACKET      =  6)
      PARAMETER (UNITSERR_UNBAL_PAREN        =  7)
      PARAMETER (UNITSERR_CONSEC_BINOPS      =  8)
      PARAMETER (UNITSERR_PARSER_ERROR       =  9)
      PARAMETER (UNITSERR_BAD_UNIT_SPEC      = 10)
      PARAMETER (UNITSERR_BAD_FUNCS          = 11)
      PARAMETER (UNITSERR_UNSAFE_TRANS       = 12)

      CHARACTER WCSUNITS_ERRMSG(0:12)*40,
     :          WCSUNITS_TYPES(WCSUNITS_NTYPE)*18,
     :          WCSUNITS_UNITS(WCSUNITS_NTYPE)*9
      COMMON /WCSUNITS_DATA/ WCSUNITS_ERRMSG, WCSUNITS_TYPES,
     :                       WCSUNITS_UNITS
