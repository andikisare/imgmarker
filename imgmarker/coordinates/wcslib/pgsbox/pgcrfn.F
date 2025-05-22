*=======================================================================
*
* PGSBOX 8.4 - draw curvilinear coordinate axes for PGPLOT.
* Copyright (C) 1997-2024, Mark Calabretta
*
* This file is part of PGSBOX.
*
* PGSBOX is free software: you can redistribute it and/or modify it
* under the terms of the GNU Lesser General Public License as published
* by the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* PGSBOX is distributed in the hope that it will be useful, but WITHOUT
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
* FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
* License for more details.
*
* You should have received a copy of the GNU Lesser General Public
* License along with PGSBOX.  If not, see http://www.gnu.org/licenses.
*
* Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
* http://www.atnf.csiro.au/people/Mark.Calabretta
* $Id: pgcrfn.F,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
*=======================================================================
*
* PGCRFN defines separable pairs of non-linear coordinate systems for
* PGSBOX.
*
* Given:
*   OPCODE    I         Transformation code:
*                         +2: Compute a set of pixel coordinates that
*                             describe a path between this and the
*                             previous pair of world coordinates
*                             remembered from the last call with
*                             OPCODE = +1 or +2.
*                         +1: Compute pixel coordinates from world
*                             coordinates.
*                          0: Initialize.
*                         -1: Compute world coordinates from pixel
*                             coordinates.
*
*   NLC       I         Number of elements in FCODE (=8).
*
*   NLI       I         Number of elements in NLIPRM (=2).
*
*   NLD       I         Number of elements in NLDPRM.
*
*   FCODE     C(NLC)*1  Character array (contains the CTYPE array,
*                       see below).
*
* Given and/or returned:
*   NLIPRM    I(NLI)    Integer coefficients (see below).
*
*   NLDPRM    D(2,NLD)  Double precision coefficients (see below).
*
*   WORLD     D(2)      World coordinates.
*                       Given if OPCODE > 0, returned if OPCODE < 0.
*
*   PIXEL     D(2)      Pixel coordinates.
*                       Given if OPCODE < 0, returned if OPCODE > 0.
*
*   CONTRL    I         Control flag for OPCODE = +2 (ignored, always
*                       set to 0 on return).
*
*   CONTXT    D(20)     Context elements (ignored).
*
* Returned:
*   IERR      I         Status return value:
*                         0: Success.
*                         1: Invalid parameters.
*                         2: Invalid world coordinate.
*                         3: Invalid pixel coordinate.
*
* Notes:
*   PGCRFN assumes a simple 2-D image.  The FCODE array contains
*   two four-character mnemonics that select function types:
*
*     "Lin "   Linear
*     "Log "   Logarithmic
*     "Pow "   Power law
*
*   The first two elements of NLIPRM are set on initialization to
*   offsets used by computed GO TOs for each function type.
*
*   Note that PGCRFN treats NLDPRM as an array of dimension two.
*   The NLDPRM are used as follows:
*
*     Type   WORLD(J) =
*      Lin     NLDPRM(J,3) + S
*      Log     NLDPRM(J,3) * LOG10(S)
*      Pow     (NLDPRM(J,3) + S)**NLDPRM(J,4)
*
*   Where in each case S = NLDPRM(J,2)*(PIXEL(J) - NLDPRM(J,1))
*
*=======================================================================
#ifdef BINDC
#define PGCRFN PGCRFN_F
#endif

      SUBROUTINE PGCRFN (OPCODE, NLC, NLI, NLD, FCODE, NLIPRM, NLDPRM,
     :   WORLD, PIXEL, CONTRL, CONTXT, IERR)
*-----------------------------------------------------------------------
      INTEGER   CONTRL, IERR, J, NLC, NLD, NLI, OPCODE, NLIPRM(NLI)
      DOUBLE PRECISION CONTXT(20), NLDPRM(2,NLD), PIXEL(2), S, WORLD(2)
      CHARACTER FCODE(2)*4, FCODES*20

      DATA FCODES(1:20)  /'Lin Log Pow         '/
*-----------------------------------------------------------------------
*     Circumvent "unused dummy argument" compiler warnings.
      CONTXT(1) = 0D0

      IERR = 0

      IF (OPCODE.GT.0) THEN
*       Compute pixel coordinates from world coordinates.
        DO 200 J = 1, 2
          GO TO (110, 120, 130) NLIPRM(J)
          IERR = 1
          RETURN

*         Linear.
 110      S = WORLD(J) - NLDPRM(J,3)
          GO TO 190

*         Logarithmic to base 10.
 120      S = 10D0**(WORLD(J)/NLDPRM(J,3))
          GO TO 190

*         Power.
 130      S = WORLD(J)**(1D0/NLDPRM(J,4)) - NLDPRM(J,3)

 190      PIXEL(J) = NLDPRM(J,1) + S/NLDPRM(J,2)
 200    CONTINUE

        CONTRL = 0

      ELSE IF (OPCODE.EQ.0) THEN
*       Initialize.
        IF (NLC.LT.8 .OR. NLI.LT.2 .OR. NLD.LT.3) THEN
          IERR = 1
          RETURN
        END IF

*       Compute pointers.
        NLIPRM(1) = (INDEX(FCODES,FCODE(1)) + 3)/4
        NLIPRM(2) = (INDEX(FCODES,FCODE(2)) + 3)/4
        IF (NLIPRM(1).EQ.0 .OR. NLIPRM(2).EQ.0) THEN
          IERR = 1
          RETURN
        END IF

        CONTRL = 0

      ELSE IF (OPCODE.EQ.-1) THEN
*       Compute world coordinates from pixel coordinates.
        DO 300 J = 1, 2
          S = NLDPRM(J,2)*(PIXEL(J) - NLDPRM(J,1))

          GO TO (210, 220, 230) NLIPRM(J)
          IERR = 1
          RETURN

*         Linear.
 210      WORLD(J) = NLDPRM(J,3) + S
          GO TO 300

*         Logarithmic to base 10.
 220      IF (S.LE.0D0) THEN
            IERR = 1
            RETURN
          END IF
          WORLD(J) = NLDPRM(J,3)*LOG10(S)
          GO TO 300

*         Power.
 230      S = S + NLDPRM(J,3)
          IF (S.LE.0D0 .AND. MOD(NLDPRM(J,4),1D0).NE.0D0) THEN
            IERR = 1
            RETURN
          END IF
          WORLD(J) = S**NLDPRM(J,4)
 300    CONTINUE

      ELSE
        IERR = 1
      END IF


      RETURN
      END
