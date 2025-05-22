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
* $Id: tspx.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TSPX
*-----------------------------------------------------------------------
*
* TSPEC tests the spectral transformation routines for closure.
*
*-----------------------------------------------------------------------
*     Length of spectral axis - see CLOSURE.
      INTEGER   NSPEC
      PARAMETER (NSPEC = 8001)

      INTEGER   CLOSURE, J, K, NFAIL, STAT(NSPEC), STATUS
      DOUBLE PRECISION AWAV(NSPEC), C, FREQ(NSPEC), RESTFRQ, RESTWAV,
     :          SPC1(NSPEC), SPC2(NSPEC), STEP, VELO(NSPEC), WAVE(NSPEC)

      INCLUDE 'spx.inc'

      DATA C /2.99792458D8/
*-----------------------------------------------------------------------
      WRITE (*, 10)
 10   FORMAT ('Testing closure of WCSLIB spectral transformation ',
     :        'routines (tspx.f)',/,
     :        '--------------------------------------------------',
     :        '-----------------')

      RESTFRQ = 1420.40595D6
      RESTWAV = C/RESTFRQ

*     Exercise SPECX.
      WRITE (*, 20)
 20   FORMAT (/,'Testing spectral cross-conversions (specx).',/)
      STATUS = SPECX('VELO', 4.3D5, RESTFRQ, RESTWAV, SPX)

      WRITE (*, 30) SPX(1), SPX(2), SPXI(1), SPXI(2), (SPX(J), J=4,14)
 30   FORMAT ('    restfrq:',1PE20.12,/,'    restwav:',1PE20.12,/,
     :        '   wavetype:',I3,/,      '   velotype:',I3,//,
     :        '       freq:',1PE20.12,/,'       afrq:',1PE20.12,/,
     :        '       ener:',1PE20.12,/,'       wavn:',1PE20.12,/,
     :        '       vrad:',1PE20.12,/,'       wave:',1PE20.12,/,
     :        '       vopt:',1PE20.12,/,'       zopt:',1PE20.12,/,
     :        '       awav:',1PE20.12,/,'       velo:',1PE20.12,/,
     :        '       beta:',1PE20.12,/)

      WRITE (*, 40) (SPX(J), J=15,40)
 40   FORMAT ('dfreq/dafrq:',1PE20.12,/,'dafrq/dfreq:',1PE20.12,/,
     :        'dfreq/dener:',1PE20.12,/,'dener/dfreq:',1PE20.12,/,
     :        'dfreq/dwavn:',1PE20.12,/,'dwavn/dfreq:',1PE20.12,/,
     :        'dfreq/dvrad:',1PE20.12,/,'dvrad/dfreq:',1PE20.12,/,
     :        'dfreq/dwave:',1PE20.12,/,'dwave/dfreq:',1PE20.12,/,
     :        'dfreq/dawav:',1PE20.12,/,'dawav/dfreq:',1PE20.12,/,
     :        'dfreq/dvelo:',1PE20.12,/,'dvelo/dfreq:',1PE20.12,/,
     :        'dwave/dvopt:',1PE20.12,/,'dvopt/dwave:',1PE20.12,/,
     :        'dwave/dzopt:',1PE20.12,/,'dzopt/dwave:',1PE20.12,/,
     :        'dwave/dawav:',1PE20.12,/,'dawav/dwave:',1PE20.12,/,
     :        'dwave/dvelo:',1PE20.12,/,'dvelo/dwave:',1PE20.12,/,
     :        'dawav/dvelo:',1PE20.12,/,'dvelo/dawav:',1PE20.12,/,
     :        'dvelo/dbeta:',1PE20.12,/,'dbeta/dvelo:',1PE20.12,/)

*     Construct a linear velocity spectrum.
      STEP = (2D0*C/NSPEC) / 2D0
      K = -NSPEC
      DO 50 J = 1, NSPEC
        VELO(J) = (K+1)*STEP
        K = K + 2
 50   CONTINUE

      WRITE (*, 60) VELO(1)*1D-3, VELO(NSPEC)*1D-3,
     :             (VELO(2) - VELO(1))*1D-3
 60   FORMAT (/,'Velocity range:',F12.3,' to',F11.3,' km/s, step:',
     :        F7.3,' km/s')

*     Convert it to frequency.
      STATUS = VELOFREQ(RESTFRQ, NSPEC, 1, 1, VELO, FREQ, STAT)

*     Test closure of all two-way combinations.
      NFAIL = 0
      NFAIL = NFAIL + CLOSURE ('freq', 'afrq', 0D0,
     :                         FREQAFRQ, AFRQFREQ, FREQ, SPC1)
      NFAIL = NFAIL + CLOSURE ('afrq', 'freq', 0D0,
     :                         AFRQFREQ, FREQAFRQ, SPC1, SPC2)

      NFAIL = NFAIL + CLOSURE ('freq', 'ener', 0D0,
     :                         FREQENER, ENERFREQ, FREQ, SPC1)
      NFAIL = NFAIL + CLOSURE ('ener', 'freq', 0D0,
     :                         ENERFREQ, FREQENER, SPC1, SPC2)

      NFAIL = NFAIL + CLOSURE ('freq', 'wavn', 0D0,
     :                         FREQWAVN, WAVNFREQ, FREQ, SPC1)
      NFAIL = NFAIL + CLOSURE ('wavn', 'freq', 0D0,
     :                         WAVNFREQ, FREQWAVN, SPC1, SPC2)

      NFAIL = NFAIL + CLOSURE ('freq', 'vrad', RESTFRQ,
     :                         FREQVRAD, VRADFREQ, FREQ, SPC1)
      NFAIL = NFAIL + CLOSURE ('vrad', 'freq', RESTFRQ,
     :                         VRADFREQ, FREQVRAD, SPC1, SPC2)

      NFAIL = NFAIL + CLOSURE ('freq', 'wave', 0D0,
     :                         FREQWAVE, WAVEFREQ, FREQ, WAVE)
      NFAIL = NFAIL + CLOSURE ('wave', 'freq', 0D0,
     :                         WAVEFREQ, FREQWAVE, WAVE, SPC2)

      NFAIL = NFAIL + CLOSURE ('freq', 'awav', 0D0,
     :                         FREQAWAV, AWAVFREQ, FREQ, AWAV)
      NFAIL = NFAIL + CLOSURE ('awav', 'freq', 0D0,
     :                         AWAVFREQ, FREQAWAV, AWAV, SPC2)

      NFAIL = NFAIL + CLOSURE ('freq', 'velo', RESTFRQ,
     :                         FREQVELO, VELOFREQ, FREQ, VELO)
      NFAIL = NFAIL + CLOSURE ('velo', 'freq', RESTFRQ,
     :                         VELOFREQ, FREQVELO, VELO, SPC2)

      NFAIL = NFAIL + CLOSURE ('wave', 'vopt', RESTWAV,
     :                         WAVEVOPT, VOPTWAVE, WAVE, SPC1)
      NFAIL = NFAIL + CLOSURE ('vopt', 'wave', RESTWAV,
     :                         VOPTWAVE, WAVEVOPT, SPC1, SPC2)

      NFAIL = NFAIL + CLOSURE ('wave', 'zopt', RESTWAV,
     :                         WAVEZOPT, ZOPTWAVE, WAVE, SPC1)
      NFAIL = NFAIL + CLOSURE ('zopt', 'wave', RESTWAV,
     :                         ZOPTWAVE, WAVEZOPT, SPC1, SPC2)

      NFAIL = NFAIL + CLOSURE ('wave', 'awav', 0D0,
     :                         WAVEAWAV, AWAVWAVE, WAVE, SPC1)
      NFAIL = NFAIL + CLOSURE ('awav', 'wave', 0D0,
     :                         AWAVWAVE, WAVEAWAV, SPC1, SPC2)

      NFAIL = NFAIL + CLOSURE ('wave', 'velo', RESTWAV,
     :                         WAVEVELO, VELOWAVE, WAVE, SPC1)
      NFAIL = NFAIL + CLOSURE ('velo', 'wave', RESTWAV,
     :                         VELOWAVE, WAVEVELO, SPC1, SPC2)

      NFAIL = NFAIL + CLOSURE ('awav', 'velo', RESTWAV,
     :                         AWAVVELO, VELOAWAV, AWAV, SPC1)
      NFAIL = NFAIL + CLOSURE ('velo', 'awav', RESTWAV,
     :                         VELOAWAV, AWAVVELO, SPC1, SPC2)

      NFAIL = NFAIL + CLOSURE ('velo', 'beta', 0D0,
     :                         VELOBETA, BETAVELO, VELO, SPC1)
      NFAIL = NFAIL + CLOSURE ('beta', 'velo', 0D0,
     :                         BETAVELO, VELOBETA, SPC1, SPC2)


      IF (NFAIL.NE.0) THEN
        WRITE (*, 70) NFAIL
 70     FORMAT (/,'FAIL:',I5,' closure residuals exceed reporting ',
     :    'tolerance.')
      ELSE
        WRITE (*, 80)
 80     FORMAT (/,'PASS: All closure residuals are within reporting ',
     :    'tolerance.')
      END IF

      END

*=======================================================================

      INTEGER FUNCTION CLOSURE (FROM, TO, PARM, FWD, REV, SPEC1, SPEC2)

      INTEGER   NSPEC
      PARAMETER (NSPEC = 8001)

      LOGICAL   SKIP
      INTEGER   J, NFAIL, STAT1(NSPEC), STAT2(NSPEC), STATUS
      DOUBLE PRECISION CLOS(NSPEC), PARM, RESID, RESIDMAX, SPEC1(NSPEC),
     :          SPEC2(NSPEC), TOL
      CHARACTER FROM*(*), TO*(*)

      PARAMETER (TOL = 1D-9)

      INTEGER  FWD, REV
      EXTERNAL FWD, REV

      SAVE SKIP
      DATA SKIP/.FALSE./
*-----------------------------------------------------------------------

*     Convert the first to the second.
      STATUS = FWD(PARM, NSPEC, 1, 1, SPEC1, SPEC2, STAT1)
      IF (STATUS.NE.0) THEN
        WRITE (*, 10) FROM, TO, STATUS
 10     FORMAT (A,A,' ERROR',I2,'.')
      END IF

*     Convert the second back to the first.
      STATUS = REV(PARM, NSPEC, 1, 1, SPEC2, CLOS, STAT2)
      IF (STATUS.NE.0) THEN
        WRITE (*, 10) TO, FROM, STATUS
      END IF

*     Test closure.
      NFAIL = 0
      RESIDMAX = 0.0
      DO 50 J = 1, NSPEC
        IF (STAT1(J).NE.0) THEN
          IF (SKIP) WRITE (*, *)
          WRITE (*, 20) FROM, TO, FROM, SPEC1(J), TO, STAT1(J)
 20       FORMAT (A,A,': ',A,' =',1PE19.12,' -> ',A,
     :            ' = ???, stat = ',I2)
          SKIP = .FALSE.
          GO TO 50
        END IF

        IF (STAT2(J).NE.0) THEN
          IF (SKIP) WRITE (*, *)
          WRITE (*, 30) TO, FROM, FROM, SPEC1(J), TO, SPEC2(J), FROM,
     :                  STAT2(J)
 30       FORMAT (A,A,': ',A,' =',1PE19.12,' -> ',A,' =',1PE19.12,
     :            ' -> ',A,' = ???, stat = ',I2)
          SKIP = .FALSE.
          GO TO 50
        END IF

        IF (SPEC1(J).EQ.0.0) THEN
          RESID = ABS(CLOS(J) - SPEC1(J))
        ELSE
          RESID = ABS((CLOS(J) - SPEC1(J))/SPEC1(J))
          IF (RESID.GT.RESIDMAX) RESIDMAX = RESID
        END IF

        IF (RESID.GT.TOL) THEN
          NFAIL = NFAIL + 1
          IF (SKIP) WRITE (*, *)
          WRITE (*, 40) FROM, TO, FROM, SPEC1(J), TO, SPEC2(J), FROM,
     :                  CLOS(J), RESID
 40       FORMAT (A,A,': ',A,' =',1PE19.12,' -> ',A,' =',1PE19.12,
     :            ' ->',/,'          ',A,' =',1PE19.12,',  resid =',
     :            1PE8.1)
          SKIP = .FALSE.
        END IF
 50   CONTINUE

      WRITE (*, 60) FROM, TO, RESIDMAX
 60   FORMAT (A,A,': Maximum closure residual =',1PE8.1)
      IF (RESIDMAX.GT.TOL) THEN
        WRITE (*, *)
        SKIP = .FALSE.
      ELSE
        SKIP = .TRUE.
      END IF

      CLOSURE = NFAIL

      END
