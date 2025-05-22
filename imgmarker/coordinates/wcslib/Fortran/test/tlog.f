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
* $Id: tlog.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TLOG
*-----------------------------------------------------------------------
*
* TLOG tests the logarithmic coordinate transformation routines for
* closure.
*
*-----------------------------------------------------------------------
      DOUBLE PRECISION TOL
      PARAMETER (TOL = 2D-13)

      INTEGER   NCRD
      PARAMETER (NCRD = 8000)

      INTEGER   J, K, NFAIL, STAT1(NCRD), STAT2(NCRD), STATUS
      DOUBLE PRECISION CRVAL, LOGC(NCRD), RESID, RESMAX, STEP,
     :          X0(NCRD), X1(NCRD)

      DATA CRVAL /3.3D0/

      INCLUDE 'log.inc'
*-----------------------------------------------------------------------

      WRITE (*, 10)
 10   FORMAT ('Testing closure of WCSLIB logarithmic coordinate ',
     :        'routines (tlog.f)',/,
     :        '-------------------------------------------------',
     :        '-----------------')


*     Construct a logarithmic axis and test closure.
      STEP = (40D0/NCRD) / 2D0
      K = -NCRD
      DO 20 J = 1, NCRD
        X0(J) = K*STEP
        K = K + 2
 20   CONTINUE

      WRITE (*, 30) X0(1), X0(NCRD), X0(2) - X0(1)
 30   FORMAT (/,'Logarithmic range:',F6.1,' to',F5.1,', step:',F7.4)

*     Convert the first to the second.
      STATUS = LOGX2S(CRVAL, NCRD, 1, 1, X0, LOGC, STAT1)
      IF (STATUS.NE.0) THEN
        WRITE (*, 40) STATUS
 40     FORMAT ('LOGX2S ERROR',I2,'.')
      END IF

*     Convert the second back to the first.
      STATUS = LOGS2X(CRVAL, NCRD, 1, 1, LOGC, X1, STAT2)
      IF (STATUS.NE.0) THEN
        WRITE (*, 50) STATUS
 50     FORMAT ('LOGS2X ERROR',I2,'.')
      END IF


*     Test closure.
      NFAIL  = 0
      RESMAX = 0D0
      DO 90 J = 1, NCRD
        IF (STAT1(J).NE.0) THEN
          WRITE (*, 60) X0(J), STAT1(J)
 60       FORMAT ('LOGX2S: X =',1PE20.12,' -> log = ???, stat =',I2,'.')
          GO TO 90
        END IF

        IF (STAT2(J).NE.0) THEN
          WRITE (*, 70) X0(J), LOGC(J), STAT2(J)
 70       FORMAT ('LOGS2X: x =',1PE20.12,' -> log =',1PE20.12,
     :            ' -> x = ???, stat =',I2)
          GO TO 90
        END IF

        IF (X0(J).EQ.0D0) THEN
          RESID = ABS(X1(J) - X0(J))
        ELSE
          RESID = ABS((X1(J) - X0(J)) / X0(J))
          IF (RESID.GT.RESMAX) RESMAX = RESID
        END IF

        IF (RESID.GT.TOL) THEN
          NFAIL = NFAIL + 1
          WRITE (*, 80) X0(J), LOGC(J), X1(J), RESID
 80       FORMAT ('LOGX2S: x =',1PE20.12,' -> log =',1PE20.12,' ->',/,
     :            '        x =',1PE20.12,', resid =',1PE20.12)
        END IF
 90   CONTINUE

      IF (RESMAX.GT.TOL) THEN
        WRITE (*, *)
      END IF
      WRITE (*, 100) RESMAX
 100  FORMAT ('LOGX2S/LOGS2X: Maximum closure residual =',1PE8.1)


      IF (NFAIL.NE.0) THEN
        WRITE (*, 110) NFAIL
 110    FORMAT (/,'FAIL:',I5,' closure residuals exceed reporting ',
     :    'tolerance.')
      ELSE
        WRITE (*, 120)
 120    FORMAT (/,'PASS: All closure residuals are within reporting ',
     :    'tolerance.')
      END IF

      END
