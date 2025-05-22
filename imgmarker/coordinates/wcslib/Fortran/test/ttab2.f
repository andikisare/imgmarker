*=======================================================================
*
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
* $Id: ttab2.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TTAB2
*-----------------------------------------------------------------------
*
* TTAB2 tests the -TAB routines using PGPLOT for graphical display.  It
* demonstrates the nature of linear interpolation in 2 dimensions by
* contouring the interior a single 2 x 2 interpolation element as the
* values in each corner change.
*
*-----------------------------------------------------------------------

*     Set up a 2 x 2 lookup table.
      INTEGER   K1, K2, M
      PARAMETER (M = 2, K1 = 2, K2 = 2)

      INTEGER   K(2), MAP(2)
      DOUBLE PRECISION CRVAL(2)
      DATA K     /K1, K2/
      DATA MAP   /0, 1/
      DATA CRVAL /0D0, 0D0/

*     Number of subdivisions on each side of the interpolation element.
      INTEGER   NP
      REAL      SCL
      PARAMETER (NP = 128)
      PARAMETER (SCL = 2.0/(NP-1))

      INTEGER   I, IM, IK, J, L, L1, L2, L3, LSTEP, STAT(NP*NP), STATUS
      REAL      ARRAY(NP,NP), CLEV(-10:20), LTM(6), V0, V1, W
      DOUBLE PRECISION X(M,NP,NP), WORLD(M,NP,NP)
      CHARACTER TEXT*80

*     On some systems, such as Sun Sparc, the struct MUST be aligned
*     on a double precision boundary, done here using an equivalence.
*     Failure to do this may result in mysterious "bus errors".
      INCLUDE 'tab.inc'
      INTEGER   TAB(TABLEN)
      DOUBLE PRECISION DUMMY
      EQUIVALENCE (TAB,DUMMY)
*-----------------------------------------------------------------------

      WRITE (*, 10)
 10   FORMAT (
     :   'Testing WCSLIB coordinate lookup table routines (ttab2.f)',/,
     :   '---------------------------------------------------------')


*     PGPLOT initialization.
      CALL PGBEG (0, '/xwindow', 1, 1)
      CALL PGVSTD ()
      CALL PGSCH (0.7)

*     The viewport is slightly oversized.
      CALL PGWNAD (-0.65, 1.65, -0.65, 1.65)

      DO 20 L = -10, 20
        CLEV(L) = 0.2*L
 20   CONTINUE

      LTM(1) = -SCL*(1.0 + (NP-1)/4.0)
      LTM(2) =  SCL
      LTM(3) =  0.0
      LTM(4) = -SCL*(1.0 + (NP-1)/4.0)
      LTM(5) =  0.0
      LTM(6) =  SCL


*     Set up the lookup table.
      STATUS = TABPTI (TAB, TAB_FLAG, -1, 0, 0)
      STATUS = TABINI(M, K, TAB)
      IF (STATUS.NE.0) THEN
        WRITE (*, 30) STATUS
 30     FORMAT ('TABINI ERROR',I2,'.')
        GO TO 999
      END IF

      STATUS = TABPTI (TAB, TAB_M, M, 0, 0)
      DO 50 IM = 1, M
        STATUS = TABPTI (TAB, TAB_K,     K(IM),     IM, 0)
        STATUS = TABPTI (TAB, TAB_MAP,   MAP(IM),   IM, 0)
        STATUS = TABPTD (TAB, TAB_CRVAL, CRVAL(IM), IM, 0)

        DO 40 IK = 1, K(IM)
          STATUS = TABPTD (TAB, TAB_INDEX, DBLE(IK-1), IM, IK)
 40     CONTINUE
 50   CONTINUE

*     Subdivide the interpolation element.
      DO 70 I = 1, NP
        DO 60 J = 1, NP
          X(1,J,I) = (J-1)*(K1-1.0)*SCL - 0.5 - CRVAL(1)
          X(2,J,I) = (I-1)*(K2-1.0)*SCL - 0.5 - CRVAL(2)
 60     CONTINUE
 70   CONTINUE

*     The first coordinate element is static.
      STATUS = TABPTD (TAB, TAB_COORD, 0D0, 1, 0)
      STATUS = TABPTD (TAB, TAB_COORD, 0D0, 3, 0)
      STATUS = TABPTD (TAB, TAB_COORD, 0D0, 5, 0)
      STATUS = TABPTD (TAB, TAB_COORD, 0D0, 7, 0)

*     (k1,k2) = (1,1).
      STATUS = TABPTD (TAB, TAB_COORD, 0D0, 2, 0)

*     The second coordinate element varies in three of the corners.
      DO 170 L3 = 0, 100, 20
*       (k1,k2) = (2,2).
        STATUS = TABPTD (TAB, TAB_COORD, 0.01D0*L3, 8, 0)

        DO 160 L2 = 0, 100, 20
*         (k1,k2) = (1,2).
          STATUS = TABPTD (TAB, TAB_COORD, 0.01D0*L2, 6, 0)

          CALL PGPAGE ()
          DO 150 L1 = 0, 100, 2
*           (k1,k2) = (2,1).
            STATUS = TABPTD (TAB, TAB_COORD, 0.01D0*L1, 4, 0)

*           Compute coordinates within the interpolation element.
            STATUS = TABX2S (TAB, NP*NP, 2, X, WORLD, STAT)
            IF (STATUS.NE.0) THEN
              WRITE (*, 80) STATUS
 80           FORMAT ('TABX2S ERROR',I2,'.')
            END IF

*           Start a new plot.
            CALL PGBBUF ()
            CALL PGERAS ()
            CALL PGSCI (1)
            CALL PGSLW (3)
            CALL PGBOX ('BCNST', 0.0, 0, 'BCNSTV', 0.0, 0)
            CALL PGMTXT ('T', 0.7, 0.5, 0.5, '-TAB coordinates:  ' //
     :                   'linear interpolation / extrapolation in 2-D')

*           Draw the boundary of the interpolation element in red.
            CALL PGSCI (2)
            CALL PGMOVE (-0.5,  0.0)
            CALL PGDRAW ( 1.5,  0.0)

            CALL PGMOVE ( 1.0, -0.5)
            CALL PGDRAW ( 1.0,  1.5)

            CALL PGMOVE ( 1.5,  1.0)
            CALL PGDRAW (-0.5,  1.0)

            CALL PGMOVE ( 0.0,  1.5)
            CALL PGDRAW ( 0.0, -0.5)

*           Label the value of the coordinate element in each corner.
            WRITE (TEXT, '(F3.1)') 0.0
            CALL PGTEXT (-0.09, -0.05, TEXT)
            WRITE (TEXT, '(F4.2)') 0.01*L1
            CALL PGTEXT ( 1.02, -0.05, TEXT)
            WRITE (TEXT, '(F3.1)') 0.01*L2
            CALL PGTEXT (-0.13,  1.02, TEXT)
            WRITE (TEXT, '(F3.1)') 0.01*L3
            CALL PGTEXT ( 1.02,  1.02, TEXT)

            CALL PGSCI (1)

*           Contour labelling: bottom.
            V0 = REAL(WORLD(2,1,1))
            V1 = REAL(WORLD(2,NP,1))
            IF (V0.NE.V1) THEN
              IF (ABS(INT((V1-V0)/0.2)).LT.10) THEN
                LSTEP = 20
              ELSE
                LSTEP = 40
              END IF

              DO 90 L = -200, 300, LSTEP
                W = -0.5 + 2.0*(L*0.01 - V0)/(V1 - V0)
                IF (W.LT.-0.5 .OR. W.GT.1.5) GO TO 90

                WRITE (TEXT, '(F4.1)') L*0.01
                CALL PGPTXT (W+0.04, -0.56, 0.0, 1.0, TEXT)
 90           CONTINUE
            END IF

*           Contour labelling: left.
            V0 = REAL(WORLD(2,1,1))
            V1 = REAL(WORLD(2,1,NP))
            IF (V0.NE.V1) THEN
              IF (ABS(INT((V1-V0)/0.2)).LT.10) THEN
                LSTEP = 20
              ELSE
                LSTEP = 40
              END IF

              DO 100 L = -200, 300, LSTEP
                W = -0.5 + 2.0*(L*0.01 - V0)/(V1 - V0)
                IF (W.LT.-0.5 .OR. W.GT.1.5) GO TO 100

                WRITE (TEXT, '(F4.1)') L*0.01
                CALL PGPTXT (-0.52, W-0.02, 0.0, 1.0, TEXT)
 100          CONTINUE
            END IF

*           Contour labelling: right.
            V0 = REAL(WORLD(2,NP,1))
            V1 = REAL(WORLD(2,NP,NP))
            IF (V0.NE.V1) THEN
              IF (ABS(INT((V1-V0)/0.2)).LT.10) THEN
                LSTEP = 20
              ELSE
                LSTEP = 40
              END IF

              DO 110 L = -200, 300, LSTEP
                W = -0.5 + 2.0*(L*0.01 - V0)/(V1 - V0)
                IF (W.LT.-0.5 .OR. W.GT.1.5) GO TO 110

                WRITE (TEXT, '(F3.1)') L*0.01
                CALL PGPTXT (1.52, W-0.02, 0.0, 0.0, TEXT)
 110          CONTINUE
            END IF

*           Contour labelling: top.
            V0 = REAL(WORLD(2,1,NP))
            V1 = REAL(WORLD(2,NP,NP))
            IF (V0.NE.V1) THEN
              IF (ABS(INT((V1-V0)/0.2)).LT.10) THEN
                LSTEP = 20
              ELSE
                LSTEP = 40
              END IF

              DO 120 L = -200, 300, LSTEP
                W = -0.5 + 2.0*(L*0.01 - V0)/(V1 - V0)
                IF (W.LT.-0.5 .OR. W.GT.1.5) GO TO 120

                WRITE (TEXT, '(F3.1)') L*0.01
                CALL PGPTXT (W+0.04, 1.52, 0.0, 1.0, TEXT)
 120          CONTINUE
            END IF

*           Draw contours for the second coordinate element.
            DO 140 I = 1, NP
              DO 130 J = 1, NP
                ARRAY(J,I) = REAL(WORLD(2,J,I))
 130          CONTINUE
 140        CONTINUE

            CALL PGSLW (2)

            CALL PGSCI (4)
            CALL PGCONT (ARRAY, NP, NP, 1, NP, 1, NP, CLEV(-10), 10,
     :                   LTM)

            CALL PGSCI (7)
            CALL PGCONT (ARRAY, NP, NP, 1, NP, 1, NP, CLEV(0), 1, LTM)

            CALL PGSCI (5)
            CALL PGCONT (ARRAY, NP, NP, 1, NP, 1, NP, CLEV(1), 20, LTM)

            CALL PGEBUF ()
 150      CONTINUE
 160    CONTINUE
 170  CONTINUE

      CALL PGEND ()

 999  STATUS = TABFREE (TAB)

      END
