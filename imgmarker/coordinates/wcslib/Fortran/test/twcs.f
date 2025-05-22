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
* $Id: twcs.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TWCS
*-----------------------------------------------------------------------
*
* TWCS1 tests WCSS2P and WCSP2S for closure on an oblique 2-D slice
* through a 4-D image with celestial, spectral and logarithmic
* coordinate axes.
*
*-----------------------------------------------------------------------
      INCLUDE 'cel.inc'
      INCLUDE 'prj.inc'
      INCLUDE 'wcs.inc'
      INCLUDE 'wcserr.inc'
      INCLUDE 'wcsmath.inc'

      DOUBLE PRECISION TOL
      PARAMETER (TOL = 1D-10)

      INTEGER   NELEM
      PARAMETER (NELEM = 9)

      LOGICAL   PASSED
      INTEGER   CHECK_ERROR, ETEST, I, J, K, LAT, LATIDX, LNG, LNGIDX,
     :          NFAIL(0:3), SPCIDX, STAT(0:360), STATUS, TEST_ERRORS
      DOUBLE PRECISION FREQ, IMG(NELEM,0:360), LAT1, LNG1, PHI(0:360),
     :          PIXEL1(NELEM,0:360), PIXEL2(NELEM,0:360), R, RESID,
     :          RESMAX, THETA(0:360), TIME, WORLD1(NELEM,0:360),
     :          WORLD2(NELEM,0:360)
      CHARACTER VERS*8

*     On some systems, such as Sun Sparc, the struct MUST be aligned
*     on a double precision boundary, done here using an equivalence.
*     Failure to do this may result in mysterious "bus errors".
      INTEGER   WCS(WCSLEN)
      DOUBLE PRECISION DUMMY
      EQUIVALENCE (WCS,DUMMY)

*     Number of axes.
      INTEGER   N
      PARAMETER (N = 4)

*     WCS header parameters.
      INTEGER   NAXIS, NPV, PVI(3), PVM(3)
      DOUBLE PRECISION CDELT(N), CRPIX(N), CRVAL(N), LATPOLE, LONPOLE,
     :          PC(N,N), PV(3), RESTFRQ, RESTWAV
      CHARACTER CTYPE(N)*72

      COMMON /HEADER/ NAXIS, NPV, CRPIX, PC, CDELT, CRVAL, LONPOLE,
     :                LATPOLE, RESTFRQ, RESTWAV, PVI, PVM, PV
      COMMON /HEADCH/ CTYPE

      DATA NAXIS   /N/
      DATA (CRPIX(J), J=1,N)
     :             /513D0,   0D0,   0D0,   0D0/
      DATA ((PC(I,J),J=1,N),I=1,N)
     :             /1.1D0,   0D0,   0D0,   0D0,
     :                0D0, 1.0D0,   0D0, 0.1D0,
     :                0D0,   0D0, 1.0D0,   0D0,
     :                0D0, 0.2D0,   0D0, 1.0D0/
      DATA (CDELT(I), I=1,N)
     :             /-9.635265432D-6, 1D0, 0.1D0, -1D0/
      DATA (CTYPE(I), I=1,N)
     :           /'WAVE-F2W', 'XLAT-BON', 'TIME-LOG', 'XLON-BON'/
      DATA (CRVAL(I), I=1,N)
     :             /0.214982042D0, -30D0, 1D0, 150D0/
      DATA LONPOLE /150D0/
      DATA LATPOLE /999D0/
      DATA RESTFRQ /1.42040575D9/
      DATA RESTWAV /0D0/

*     Set PVi_m keyvalues for the longitude axis (I = 4).  For test
*     purposes, these are set so that the fiducial native coordinates
*     are at the native pole, i.e. so that (phi0,theta0) = (0,90), but
*     without any fiducial offset, i.e. iwith PVi_0a == 0 (by default).
      DATA NPV     /3/
      DATA (PVI(K), PVM(K), PV(K), K=1,2)
     :             /4, 1,  0D0,
     :              4, 2, 90D0/

*     PVi_m keyvalues for the latitude axis (I = 2).
      DATA PVI(3), PVM(3), PV(3)
     :             /2, 1, -30D0/


*     For the wcserr tests.
      COMMON /ERRTST/ ETEST
      DATA ETEST /0/
*-----------------------------------------------------------------------
      CALL WCSLIB_VERSION (VERS, 8)
      WRITE (*, 10) VERS
 10   FORMAT ('WCSLIB version number: ',A,/)

      WRITE (*, 20)
 20   FORMAT ('Testing closure of WCSLIB world coordinate ',
     :        'transformation routines (twcs.f)',/,
     :        '-------------------------------------------',
     :        '--------------------------------',/)


*     This routine simulates the actions of a FITS header parser.
      STATUS = WCSPTI (WCS, WCS_FLAG, -1, 0, 0)
      CALL PARSER (WCS)

*     Test WCSENQ - note that the struct is unset.
      NFAIL(0) = 0
      IF (WCSENQ(WCS, WCSENQ_MEM).EQ.0) THEN
        NFAIL(0) = 1
        WRITE (*, 30)
 30     FORMAT ('Unexpected result from WCSENQ: memory.')
      END IF

*     Put the struct in bypass mode (as a test).
      STATUS = WCSPTI (WCS, WCS_FLAG, 1, 0, 0)
      STATUS = WCSSET (WCS)
      IF (STATUS.NE.0) THEN
        WRITE (*, 40) STATUS
 40     FORMAT ('WCSSET ERROR',I3)
      END IF

*     Test WCSENQ.
      IF (WCSENQ(WCS, WCSENQ_SET + WCSENQ_BYP).EQ.0) THEN
        NFAIL(0) = NFAIL(0) + 1
        WRITE (*, 50)
 50     FORMAT ('Unexpected result from WCSENQ: set and bypass.')
      END IF

      IF (WCSENQ(WCS, WCSENQ_CHK).EQ.0) THEN
        NFAIL(0) = NFAIL(0) + 1
        WRITE (*, 60) 'a'
 60     FORMAT ('Unexpected result from WCSENQ: checksum (',A,').')
      END IF

*     Further test for WCSENQ - an inconsequential change.
      STATUS = WCSPTD (WCS, WCS_LATPOLE, 999.001D0, 0, 0)
      IF (WCSENQ(WCS, WCSENQ_CHK).EQ.1) THEN
        NFAIL(0) = NFAIL(0) + 1
        WRITE (*, 60) 'b'
      END IF


      IF (NFAIL(0).GT.0) WRITE (*, '()')
      WRITE (*, 70) TOL
 70   FORMAT ('Reporting tolerance',1PG8.1,' pixel.')

*     Get indices.
      STATUS = WCSGTI (WCS, WCS_LNG,  LNGIDX)
      STATUS = WCSGTI (WCS, WCS_LAT,  LATIDX)
      STATUS = WCSGTI (WCS, WCS_SPEC, SPCIDX)

*     Initialize non-celestial world coordinates.
      TIME = 1D0
      FREQ = 1.42040595D9 - 180D0 * 62500D0
      DO 80 K = 0, 360
        WORLD1(1,K) = 0D0
        WORLD1(2,K) = 0D0
        WORLD1(3,K) = 0D0
        WORLD1(4,K) = 0D0

        WORLD1(3,K) = TIME
        TIME = 1.01D0 * TIME

        WORLD1(SPCIDX,K) = 2.99792458D8 / FREQ
        FREQ = FREQ + 62500D0
 80   CONTINUE

      NFAIL(1) = 0
      RESMAX = 0D0
      DO 160 LAT = 90, -90, -1
        LAT1 = DBLE(LAT)

        K = 0
        DO 90 LNG = -180, 180
          LNG1 = DBLE(LNG)

          WORLD1(LNGIDX,K) = LNG1
          WORLD1(LATIDX,K) = LAT1
          K = K + 1
 90     CONTINUE

        STATUS = WCSS2P (WCS, 361, NELEM, WORLD1, PHI, THETA, IMG,
     :                   PIXEL1, STAT)
        IF (STATUS.NE.0) THEN
          WRITE (*, 100) STATUS, LAT1
 100      FORMAT (3X,'WCSS2P(1) ERROR',I3,' (LAT1 =',F20.15, ')')
          GO TO 160
        END IF

        STATUS = WCSP2S (WCS, 361, NELEM, PIXEL1, IMG, PHI, THETA,
     :                   WORLD2, STAT)
        IF (STATUS.NE.0) THEN
          WRITE (*, 110) STATUS, LAT1
 110      FORMAT (3X,'WCSP2S ERROR',I3,' (LAT1 =',F20.15, ')')
          GO TO 160
        END IF

        STATUS = WCSS2P (WCS, 361, NELEM, WORLD2, PHI, THETA, IMG,
     :                   PIXEL2, STAT)
        IF (STATUS.NE.0) THEN
          WRITE (*, 120) STATUS, LAT1
 120      FORMAT (3X,'WCSS2P(2) ERROR',I3,' (LAT1 =',F20.15, ')')
          GO TO 160
        END IF

        DO 150 K = 0, 360
          RESID = 0D0
          DO 130 I = 1, NAXIS
            R = PIXEL2(I,K) - PIXEL1(I,K)
            RESID = RESID + R*R
 130      CONTINUE

          RESID = SQRT(RESID)
          IF (RESID.GT.RESMAX) RESMAX = RESID

          IF (RESID.GT.TOL) THEN
            NFAIL(1) = NFAIL(1) + 1
            WRITE (*, 140) (WORLD1(I,K), I=1,NAXIS),
     :                     (PIXEL1(I,K), I=1,NAXIS),
     :                     (WORLD2(I,K), I=1,NAXIS),
     :                     (PIXEL2(I,K), I=1,NAXIS)
 140        FORMAT (/,'Closure error:',/,
     :                'world1:',4F18.12,/,
     :                'pixel1:',4F18.12,/,
     :                'world2:',4F18.12,/,
     :                'pixel2:',4F18.12)
          END IF

          LNG1 = LNG1 + 1D0
 150    CONTINUE
 160  CONTINUE

      WRITE (*, 170) RESMAX
 170  FORMAT ('WCSP2S/WCSS2P: Maximum closure residual =',1P,G8.1,
     :        ' pixel.')


*     Test WCSERR.
      WRITE (*, 180)
 180  FORMAT (/,'IGNORE messages marked with ''OK'', they test ',
     :          'WCSERR: ')

      STATUS = WCSERR_ENABLE(1)

*     Test 1 - take it out of bypass mode, so now WCSSET should fail.
      STATUS = WCSPTD (WCS, WCS_PV, UNDEFINED, PVI(3), PVM(3))
      STATUS = WCSPTI (WCS, WCS_FLAG, 0, 0, 0)
      STATUS = WCSSET (WCS)
      NFAIL(3) = CHECK_ERROR (WCS, STATUS, WCSERR_BAD_PARAM,
     :                        'Invalid parameter value')

      NFAIL(3) = NFAIL(3) + TEST_ERRORS()

      WRITE (*, '()')

      PASSED = .TRUE.
      IF (NFAIL(0).NE.0) THEN
        PASSED = .FALSE.
        WRITE (*, 190)
 190    FORMAT ('FAIL: Unexpected result from WCSENQ.')
      END IF

      IF (NFAIL(1).NE.0) THEN
        PASSED = .FALSE.
        WRITE (*, 200) NFAIL(1)
 200    FORMAT ('FAIL:',I5,' closure residuals exceed reporting ',
     :    'tolerance.')
      END IF

      IF (NFAIL(3).NE.0) THEN
        PASSED = .FALSE.
        WRITE (*, 210) NFAIL(3)
 210    FORMAT ('FAIL:',I5,' error messages differ from that ',
     :    'expected.')
      END IF

      IF (PASSED) THEN
        WRITE (*, 220)
 220    FORMAT (
     :    'PASS: All enquiry results returned as expected',/,
     :    'PASS: All closure residuals are within reporting ',
     :           'tolerance.',/,
     :    'PASS: All error messages reported as expected.')
      END IF


*     Clean up.
      STATUS = WCSFREE(WCS)

      END

*-----------------------------------------------------------------------
      SUBROUTINE PARSER (WCS)
*-----------------------------------------------------------------------
* In practice a parser would read the FITS header until it encountered
* the NAXIS keyword which must occur near the start, before any of the
* WCS keywords.  It would then use WCSINI to allocate memory for arrays
* in the WCSPRM "data structure" and set default values.
*
* In this simulation the header keyvalues are set in the main program in
* variables passed in COMMON.
*-----------------------------------------------------------------------
*     Number of axes.
      INTEGER   N
      PARAMETER (N = 4)

      INTEGER   I, J, K, NAXIS, NPV, PVI(3), PVM(3), STATUS, WCS(*)
      DOUBLE PRECISION CDELT(N), CRPIX(N), CRVAL(N), LATPOLE, LONPOLE,
     :          PC(N,N), PV(3), RESTFRQ, RESTWAV
      CHARACTER CTYPE(N)*72

      INCLUDE 'wcs.inc'

      COMMON /HEADER/ NAXIS, NPV, CRPIX, PC, CDELT, CRVAL, LONPOLE,
     :                LATPOLE, RESTFRQ, RESTWAV, PVI, PVM, PV
      COMMON /HEADCH/ CTYPE
*-----------------------------------------------------------------------
      STATUS = WCSINI (NAXIS, WCS)

      DO 20 I = 1, NAXIS
         STATUS = WCSPTD (WCS, WCS_CRPIX, CRPIX(I), I, 0)

         DO 10 J = 1, NAXIS
            STATUS = WCSPTD (WCS, WCS_PC, PC(I,J), I, J)
 10      CONTINUE

         STATUS = WCSPTD (WCS, WCS_CDELT, CDELT(I), I, 0)
         STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(I), I, 0)
         STATUS = WCSPTD (WCS, WCS_CRVAL, CRVAL(I), I, 0)
 20   CONTINUE

      STATUS = WCSPTD (WCS, WCS_LONPOLE, LONPOLE, 0, 0)
      STATUS = WCSPTD (WCS, WCS_LATPOLE, LATPOLE, 0, 0)

      STATUS = WCSPTD (WCS, WCS_RESTFRQ, RESTFRQ, 0, 0)
      STATUS = WCSPTD (WCS, WCS_RESTWAV, RESTWAV, 0, 0)

      DO 30 K = 1, NPV
         STATUS = WCSPTD (WCS, WCS_PV, PV(K), PVI(K), PVM(K))
 30   CONTINUE

      END

*-----------------------------------------------------------------------
      INTEGER FUNCTION TEST_ERRORS()
*-----------------------------------------------------------------------
      CHARACTER NULL*1
      PARAMETER (NULL = CHAR(0))

      INTEGER   CHECK_ERROR, ETEST, NFAIL, STATUS
      CHARACTER CTYPE*72

*     On some systems, such as Sun Sparc, the struct MUST be aligned
*     on a double precision boundary, done here using an equivalence.
*     Failure to do this may result in mysterious "bus errors".
      INCLUDE 'wcs.inc'
      INTEGER   WCS(WCSLEN)
      DOUBLE PRECISION DUMMY
      EQUIVALENCE (WCS,DUMMY)

      COMMON /ERRTST/ ETEST
*-----------------------------------------------------------------------
      NFAIL = 0

*     Test 2.
      STATUS = WCSPTI (WCS, WCS_FLAG, -1, 0, 0)
      STATUS = WCSINI (-32, WCS)
      NFAIL = NFAIL + CHECK_ERROR (WCS, STATUS, WCSERR_MEMORY,
     :          'naxis must not be negative (got -32)')

*     Test 3.
      STATUS = WCSPTI (WCS, WCS_FLAG, 0, 0, 0)
      STATUS = WCSINI (2, WCS)
      NFAIL = NFAIL + CHECK_ERROR (WCS, STATUS, WCSERR_SUCCESS, ' ')

*     Test 4; CTYPE strings handled with CHARACTER*72 variable.
      CTYPE = 'CUBEFACE'
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE, 1, 0)
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE, 2, 0)
      STATUS = WCSSET (WCS)
      NFAIL = NFAIL + CHECK_ERROR (WCS, STATUS, WCSERR_BAD_CTYPE,
     :          'Multiple CUBEFACE axes (in CTYPE1 and CTYPE2)')

*     Test 5; CTYPE strings handled C-style, i.e. with trailing '\0'.
      STATUS = WCSPTI (WCS, WCS_FLAG, 0, 0, 0)
      STATUS = WCSINI (2, WCS)
      STATUS = WCSPTC (WCS, WCS_CTYPE, 'RA---FOO'//NULL, 1, 0)
      STATUS = WCSPTC (WCS, WCS_CTYPE, 'DEC--BAR'//NULL, 2, 0)
      STATUS = WCSSET (WCS)
      NFAIL = NFAIL + CHECK_ERROR (WCS, STATUS, WCSERR_BAD_CTYPE,
     :          'Unrecognized projection code (FOO in CTYPE1)')

*     Test 6.
      STATUS = WCSPTI (WCS, WCS_FLAG, 0, 0, 0)
      STATUS = WCSINI (2, WCS)
      STATUS = WCSPTC (WCS, WCS_CTYPE, 'RA---TAN'//NULL, 1, 0)
      STATUS = WCSPTC (WCS, WCS_CTYPE, 'FREQ-LOG'//NULL, 2, 0)
      STATUS = WCSSET (WCS)
      NFAIL = NFAIL + CHECK_ERROR (WCS, STATUS, WCSERR_BAD_CTYPE,
     :          'Unmatched celestial axes')

      STATUS = WCSFREE(WCS)

      TEST_ERRORS = NFAIL

      END

*-----------------------------------------------------------------------
      INTEGER FUNCTION CHECK_ERROR(WCS, STATUS, EXSTATUS, EXMSG)
*-----------------------------------------------------------------------
      INCLUDE 'wcs.inc'
      INCLUDE 'wcserr.inc'

      INTEGER   EXSTATUS, ILEN, ISTAT, ETEST, STATUS, WCS(WCSLEN)
      CHARACTER ERRMSG*(WCSERR_MSG_LENGTH), EXMSG*(*)

*     On some systems, such as Sun Sparc, the structs MUST be aligned
*     on a double precision boundary.  As a dummy argument, WCS should
*     already be aligned.  WCSERR is aligned here using an equivalence.
*     Failure to do this may result in mysterious "bus errors".
      INTEGER   WCSERR(ERRLEN)
      DOUBLE PRECISION DUMMY
      EQUIVALENCE (WCSERR,DUMMY)

      COMMON /ERRTST/ ETEST
*-----------------------------------------------------------------------
      IF (STATUS.NE.0) THEN
        ISTAT = WCSGTI (WCS, WCS_ERR, WCSERR(1))
        ISTAT = WCSERR_GTC (WCSERR, WCSERR_MSG, ERRMSG)
      ELSE
        ERRMSG = ' '
      END IF

      ETEST = ETEST + 1
      WRITE (*, 10) ETEST
 10   FORMAT (/,'Test ',I2,'...')

      IF (STATUS.EQ.EXSTATUS .AND. ERRMSG.EQ.EXMSG) THEN
        CALL FLUSH(6)
        ISTAT = WCSPERR (WCS, 'OK: '//CHAR(0))
        WRITE (*, *) '...succeeded.'
        CHECK_ERROR = 0
      ELSE
        WRITE (*, 20) EXSTATUS, EXMSG(:ILEN(EXMSG))
 20     FORMAT ('Expected error ',I2,': ''',A,''', got')
        CALL FLUSH(6)
        ISTAT = WCSPERR (WCS, CHAR(0))
        WRITE (*, *) '...failed.'
        CHECK_ERROR = 1
      END IF

      END

*-----------------------------------------------------------------------
      INTEGER FUNCTION ILEN(STRING)
*-----------------------------------------------------------------------
      CHARACTER STRING*(*)
*-----------------------------------------------------------------------
      DO 10 ILEN = LEN(STRING), 1, -1
        IF (STRING(ILEN:ILEN).NE. ' ') RETURN
 10   CONTINUE

      ILEN = 0
      END
