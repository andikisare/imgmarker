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
* $Id: ttab1.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TTAB1
*-----------------------------------------------------------------------
*
* TTAB1 tests the -TAB routines for closure.
*
*-----------------------------------------------------------------------

      DOUBLE PRECISION TOL
      PARAMETER (TOL = 1D-8)

      INTEGER   K1, K2, M
      PARAMETER (M = 2, K1 = 32, K2 = 16)

      INTEGER   K(2), MAP(2)
      DOUBLE PRECISION CRVAL(2)
      DATA K     /K1, K2/
      DATA MAP   /0, 1/
      DATA CRVAL /1D0, -1D0/

      INTEGER   I, IK, IK1, IK2, IM, J, N, NFAIL, STAT0(128),
     :          STAT1(128), STATUS
      DOUBLE PRECISION CRPIX4, EPSILON, RESID, RESIDMAX, TIME(12),
     :          WORLD(M,11,11), XT0(12), XT1(12), X0(M,11,11),
     :          X1(M,11,11), Z

*     On some systems, such as Sun Sparc, the struct MUST be aligned
*     on a double precision boundary, done here using an equivalence.
*     Failure to do this may result in mysterious "bus errors".
      INCLUDE 'tab.inc'
      INTEGER   TAB(TABLEN)
      DOUBLE PRECISION DUMMY
      EQUIVALENCE (TAB,DUMMY)
*-----------------------------------------------------------------------

      WRITE (*, 10) TOL
 10   FORMAT ('Testing closure of WCSLIB tabular coordinate routines ',
     :        '(ttab1.f)',/,
     :        '------------------------------------------------------',
     :        '---------',//,
     :        'Reporting tolerance',1PG8.1,'.')

*     First a 1-dimensional table from Sect. 6.2.3 of Paper III.
      WRITE (*, '(/,A)') 'One-dimensional test:'
      STATUS = TABPTI (TAB, TAB_FLAG, -1, 0, 0)
      STATUS = TABINI (M, K, TAB)
      IF (STATUS.NE.0) THEN
        WRITE (*, 20) STATUS
 20     FORMAT ('TABINI ERROR',I2,'.')
        GO TO 999
      END IF

      STATUS = TABPTI (TAB, TAB_M,       1, 0, 0)
      STATUS = TABPTI (TAB, TAB_K,       8, 1, 0)
      STATUS = TABPTI (TAB, TAB_MAP,     0, 1, 0)
      STATUS = TABPTD (TAB, TAB_CRVAL, 0D0, 1, 0)

      STATUS = TABPTD (TAB, TAB_INDEX, 0D0, 1, 1)
      STATUS = TABPTD (TAB, TAB_INDEX, 1D0, 1, 2)
      STATUS = TABPTD (TAB, TAB_INDEX, 1D0, 1, 3)
      STATUS = TABPTD (TAB, TAB_INDEX, 2D0, 1, 4)
      STATUS = TABPTD (TAB, TAB_INDEX, 2D0, 1, 5)
      STATUS = TABPTD (TAB, TAB_INDEX, 3D0, 1, 6)
      STATUS = TABPTD (TAB, TAB_INDEX, 3D0, 1, 7)
      STATUS = TABPTD (TAB, TAB_INDEX, 4D0, 1, 8)

      STATUS = TABPTD (TAB, TAB_COORD, 1997.84512D0, 1, 0)
      STATUS = TABPTD (TAB, TAB_COORD, 1997.84631D0, 2, 0)
      STATUS = TABPTD (TAB, TAB_COORD, 1993.28451D0, 3, 0)
      STATUS = TABPTD (TAB, TAB_COORD, 1993.28456D0, 4, 0)
      STATUS = TABPTD (TAB, TAB_COORD, 2001.59234D0, 5, 0)
      STATUS = TABPTD (TAB, TAB_COORD, 2001.59239D0, 6, 0)
      STATUS = TABPTD (TAB, TAB_COORD, 2002.18265D0, 7, 0)
      STATUS = TABPTD (TAB, TAB_COORD, 2002.18301D0, 8, 0)

      EPSILON = 1D-3
      CRPIX4  = 0.5
      XT0(1)  = 0.5 + EPSILON - CRPIX4
      XT0(2)  = 1.0           - CRPIX4
      XT0(3)  = 1.5 - EPSILON - CRPIX4
      XT0(4)  = 1.5 + EPSILON - CRPIX4
      XT0(5)  = 2.0           - CRPIX4
      XT0(6)  = 2.5 - EPSILON - CRPIX4
      XT0(7)  = 2.5 + EPSILON - CRPIX4
      XT0(8)  = 3.0           - CRPIX4
      XT0(9)  = 3.5 - EPSILON - CRPIX4
      XT0(10) = 3.5 + EPSILON - CRPIX4
      XT0(11) = 4.0           - CRPIX4
      XT0(12) = 4.5 - EPSILON - CRPIX4

      STATUS = TABX2S (TAB, 12, 1, XT0, TIME, STAT0)
      IF (STATUS.NE.0) THEN
        WRITE (*, 30) STATUS
 30     FORMAT ('TABX2S ERROR',I2,'.')
      END IF

      STATUS = TABS2X (TAB, 12, 1, TIME, XT1, STAT1)
      IF (STATUS.NE.0) THEN
        WRITE (*, 40) STATUS
 40     FORMAT ('TABX2S ERROR',I2,'.')
      END IF

      WRITE (*, 50)
 50   FORMAT ('    x   ->   time   ->   x')
      DO 70 I = 1, 12
        WRITE (*, 60) XT0(I), TIME(I), XT1(I)
 60     FORMAT (F8.5,F12.5,F9.5)
 70   CONTINUE
      WRITE (*, '(/)')

*     Test closure.
      NFAIL = 0
      RESIDMAX = 0D0
      DO 110 I = 1, 12
        IF (STAT0(I).NE.0) THEN
          WRITE (*, 80) XT0(I), STAT0(I)
 80       FORMAT ('   TABX2S: X =',F7.1,', STAT =',I2)
          GO TO 110
        END IF

        IF (STAT1(I).NE.0) THEN
          WRITE (*, 90) TIME(I), STAT1(I)
 90       FORMAT ('   TABS2X: T =',F7.1,', STAT =',I2)
          GO TO 110
        END IF

        RESID = ABS(XT1(I) - XT0(I))
        IF (RESID.GT.RESIDMAX) RESIDMAX = RESID

        IF (RESID.GT.TOL) THEN
          NFAIL = NFAIL + 1
          WRITE (*, 100) XT0(I), TIME(I), XT1(I)
 100      FORMAT ('   Closure error:',/,'      X = ',F20.15,/,
     :            '   -> T = ',F20.15,/,'   -> X = ',F20.15)
        END IF
 110  CONTINUE

      STATUS = TABFREE (TAB)


*     Now a 2-dimensional table.
      WRITE (*, '(A)') 'Two-dimensional test:'
      STATUS = TABPTI (TAB, TAB_FLAG, -1, 0, 0)
      STATUS = TABINI (M, K, TAB)
      IF (STATUS.NE.0) THEN
        WRITE (*, 120) STATUS
 120    FORMAT ('TABINI ERROR',I2,'.')
        GO TO 999
      END IF

      STATUS = TABPTI (TAB, TAB_M, M, 0, 0)
      DO 140 IM = 1, M
        STATUS = TABPTI (TAB, TAB_K,     K(IM),     IM, 0)
        STATUS = TABPTI (TAB, TAB_MAP,   MAP(IM),   IM, 0)
        STATUS = TABPTD (TAB, TAB_CRVAL, CRVAL(IM), IM, 0)

        DO 130 IK = 1, K(IM)
          STATUS = TABPTD (TAB, TAB_INDEX, DBLE(IK-1), IM, IK)
 130    CONTINUE
 140  CONTINUE

      N = 0
      Z = 1D0 / ((K1-1) * (K2-1))
      DO 160 IK2 = 0, K2-1
        DO 150 IK1 = 0, K1-1
          N = N + 1
          STATUS = TABPTD (TAB, TAB_COORD,  3D0*IK1*IK2*Z, N, 0)
          N = N + 1
          STATUS = TABPTD (TAB, TAB_COORD, -1D0*(K1-IK1-1)*IK2*Z +
     :                     0.01*IK1, N, 0)
 150    CONTINUE
 160  CONTINUE

      DO 180 I = 1, 11
        DO 170 J = 1, 11
          X0(1,J,I) = (J-1)*(K1-1)/10D0 - CRVAL(1)
          X0(2,J,I) = (I-1)*(K2-1)/10D0 - CRVAL(2)
 170    CONTINUE
 180  CONTINUE

      STATUS = TABX2S (TAB, 121, 2, X0, WORLD, STAT0)
      IF (STATUS.NE.0) THEN
        WRITE (*, 190) STATUS
 190    FORMAT ('TABX2S ERROR',I2,'.')
      END IF

      STATUS = TABS2X (TAB, 121, 2, WORLD, X1, STAT1)
      IF (STATUS.NE.0) THEN
        WRITE (*, 200) STATUS
 200    FORMAT ('TABX2S ERROR',I2,'.')
      END IF

*     Test closure.
      N = 0
      RESIDMAX = 0D0
      DO 260 I = 1, 11
        DO 250 J = 1, 11
          N = N + 1
          IF (STAT0(N).NE.0) THEN
            WRITE (*, 210) X0(1,J,I), X0(2,J,I), STAT0(N)
 210        FORMAT ('   TABX2S: X = (',F6.1,',',F6.1,'), STAT =',I2)
            GO TO 250
          END IF

          IF (STAT1(N).NE.0) THEN
            WRITE (*, 220) WORLD(1,J,I), WORLD(2,J,I), STAT1(N)
 220        FORMAT ('   TABS2X: S = (',F6.1,',',F6.1,'), STAT =',I2)
            GO TO 250
          END IF

          DO 240 IM = 1, M
            RESID = ABS(X1(IM,J,I) - X0(IM,J,I))
            IF (RESID.GT.RESIDMAX) RESIDMAX = RESID

            IF (RESID.GT.TOL) THEN
              NFAIL = NFAIL + 1
              WRITE (*, 230) X0(1,J,I), X0(2,J,I), WORLD(1,J,I),
     :                       WORLD(2,J,I), X1(1,J,I), X1(2,J,I)
 230          FORMAT ('   Closure error:',/,
     :                '      X = (',F20.15,',',F20.15,')',/,
     :                '   -> W = (',F20.15,',',F20.15,')',/,
     :                '   -> X = (',F20.15,',',F20.15,')')
              GO TO 250
            END IF
 240      CONTINUE
 250    CONTINUE
 260  CONTINUE

      WRITE (*, 270) RESIDMAX
 270  FORMAT (/,'TABX2S/TABS2X: Maximum closure residual =',1PE8.1)

      IF (NFAIL.NE.0) THEN
        WRITE (*, 280) NFAIL
 280    FORMAT (/,'FAIL:',I5,' closure residuals exceed reporting ',
     :    'tolerance.')
      ELSE
        WRITE (*, 290)
 290    FORMAT (/,'PASS: All closure residuals are within reporting ',
     :    'tolerance.')
      END IF


 999  STATUS = TABFREE (TAB)

      END
