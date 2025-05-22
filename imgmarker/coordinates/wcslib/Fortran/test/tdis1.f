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
* $Id: tdis1.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TDIS1
*-----------------------------------------------------------------------
*
* TDIS1 tests the WCSLIB distortion functions for closure.  Input comes
* from TPV7.fits.  The test is done via LINP2X and LINX2P.
*
* WCSP, which is meant to hold an address, is declared as an INTEGER
* array of length 2 to accomodate 64-bit machines for which
* sizeof(void *) = 2*sizeof(int).
*-----------------------------------------------------------------------
      INTEGER   AXMAX, NMAX
      PARAMETER (AXMAX = 4)
      PARAMETER (NMAX  = 4096)

      DOUBLE PRECISION ATOL, FTOL
      PARAMETER (ATOL = 1E-9)
      PARAMETER (FTOL = 1E-10)

      LOGICAL   GOTEND
      INTEGER   IBLOCK, IKEYRC, ILAT, ILNG, INC, J, K, N, NAXIS(AXMAX),
     :          NAXIS1, NAXIS2, NCLOS, NFAIL, NKEYRC, NREJECT, NTEST,
     :          NWCS, P1, P2, STATUS, WCSP(2)
      DOUBLE PRECISION ABSMAX, CRPIX(AXMAX), DP1, DP2, IMG(2,NMAX), PX,
     :          PX0(2,NMAX), PX1(2,NMAX), RELMAX, RESID
      CHARACTER KEYREC*80, HEADER*28801, INFILE*9

*     On some systems, such as Sun Sparc, the structs MUST be aligned
*     on a double precision boundary, done here using an equivalence.
*     Failure to do this may result in mysterious "bus errors".
      INCLUDE 'wcserr.inc'
      INCLUDE 'wcshdr.inc'
      INCLUDE 'wcs.inc'
      INCLUDE 'lin.inc'
      INTEGER   WCS(WCSLEN), LIN(LINLEN), ILIN
      EQUIVALENCE (LIN, ILIN)
      DOUBLE PRECISION DUMMY1, DUMMY2
      EQUIVALENCE (WCS, DUMMY1)
      EQUIVALENCE (LIN, DUMMY2)

      DATA INFILE /'TPV7.fits'/
*-----------------------------------------------------------------------
      STATUS = WCSERR_ENABLE (1)

      WRITE (*, 10)
 10   FORMAT (
     :  'Testing closure of WCSLIB distortion routines (tdis1.f)',/,
     :  '-------------------------------------------------------')

*     Open the FITS WCS test header for formatted, direct I/O.
      OPEN (UNIT=1, FILE=INFILE, FORM='FORMATTED', ACCESS='DIRECT',
     :      RECL=80, IOSTAT=STATUS)
      IF (STATUS.NE.0) THEN
        WRITE (*, 20) STATUS, INFILE
 20     FORMAT ('ERROR',I3,' opening ',A)
        GO TO 999
      END IF

*     Read in the FITS header, excluding COMMENT and HISTORY keyrecords.
      K = 1
      NKEYRC = 0
      GOTEND = .FALSE.
      DO 50 IBLOCK = 0, 100
        DO 40 IKEYRC = 1, 36
          READ (1, '(A80)', REC=36*IBLOCK+IKEYRC, IOSTAT=STATUS) KEYREC
          IF (STATUS.NE.0) THEN
            WRITE (*, 30) STATUS
 30         FORMAT ('ERROR',I3,' reading header.')
            GO TO 999
          END IF

          IF (KEYREC(:8).EQ.'        ') GO TO 40
          IF (KEYREC(:8).EQ.'COMMENT ') GO TO 40
          IF (KEYREC(:8).EQ.'HISTORY ') GO TO 40

          IF (KEYREC(:5).EQ.'NAXIS') THEN
            IF  (KEYREC(6:6).NE.' ') THEN
              READ (KEYREC(6:6), '(I1)') J
              READ (KEYREC(11:), *) NAXIS(J)
              GO TO 40
            END IF
          END IF

          HEADER(K:) = KEYREC
          K = K + 80
          NKEYRC = NKEYRC + 1

          IF (KEYREC(:10).EQ.'END       ') THEN
*           An END keyrecord was read, but read the rest of the block.
            GOTEND = .TRUE.
          END IF
 40     CONTINUE

        IF (GOTEND) GO TO 60
 50   CONTINUE

 60   CLOSE (UNIT=1)


*     Parse the header.
      CALL FLUSH (6)
      STATUS = WCSPIH (HEADER, NKEYRC, WCSHDR_none, 2, NREJECT, NWCS,
     :                 WCSP)
      IF (STATUS.NE.0) GO TO 999

*     Copy into our WCSPRM struct.
      STATUS = WCSVCOPY (WCSP, 0, WCS)
      IF (STATUS.NE.0) GO TO 999

*     Translate the TPV "projection" into a sequent distortion.
      STATUS = WCSSET (WCS)
      IF (STATUS.NE.0) THEN
        STATUS = WCSPERR (WCS, CHAR(0))
        GO TO 999
      END IF

*     Henceforth, we will work with linprm.  Make a shallow copy.
      STATUS = WCSGTI (WCS, WCS_LIN, ILIN)
      IF (STATUS.NE.0) THEN
        STATUS = WCSPERR (WCS, CHAR(0))
        GO TO 999
      END IF


*     The image size determines the test domain.
      STATUS = WCSGTI (WCS, WCS_LNG, ILNG)
      STATUS = WCSGTI (WCS, WCS_LAT, ILAT)
      NAXIS1 = NAXIS(ILNG)
      NAXIS2 = NAXIS(ILAT)
      IF (NAXIS1.EQ.0 .OR. NAXIS2.EQ.0) THEN
        STATUS = WCSGTD (WCS, WCS_CRPIX, CRPIX)
        IF (NAXIS1.EQ.0) NAXIS1 = 2*INT(CRPIX(ILNG)) + 1
        IF (NAXIS2.EQ.0) NAXIS2 = 2*INT(CRPIX(ILAT)) + 1
      END IF

*     Limit the number of tests.
      INC = 1
      DO 100 WHILE ((NAXIS1/INC)*(NAXIS2/INC).GT.800000)
        INC = 2 * INC
 100  CONTINUE

      N = NAXIS1 / INC
      IF (2*N.GT.NMAX) N = NMAX / 2

      NTEST = 0
      NFAIL = 0
      NCLOS = 0
      ABSMAX = 0D0
      RELMAX = 0D0

      DO 200 P2 = 1, NAXIS2, INC
        K = 0
        DO 110 P1 = 1, NAXIS1, INC
          K = K + 1
          PX0(1,K) = DBLE(P1)
          PX0(2,K) = DBLE(P2)
 110    CONTINUE

        STATUS = LINP2X(LIN, N, 2, PX0, IMG)
        IF (STATUS.NE.0) THEN
          STATUS = LINPERR(LIN, CHAR(0))
          NFAIL = 1
          GO TO 210
        END IF

        STATUS = LINX2P(LIN, N, 2, IMG, PX1)
        IF (STATUS.NE.0) THEN
          STATUS = LINPERR(LIN, CHAR(0))
          NFAIL = 1
          GO TO 210
        END IF

*       Check closure.
        DO 140 K = 1, N
          DP1 = ABS(PX1(1,K) - PX0(1,K))
          DP2 = ABS(PX1(2,K) - PX0(2,K))

          RESID = MAX(DP1, DP2)
          IF (RESID.GT.ABSMAX) ABSMAX = RESID

          IF (RESID.GT.ATOL) THEN
            NCLOS = NCLOS + 1
            WRITE (*, 120) PX0(1,K), PX0(2,K), IMG(1,K), IMG(2,K),
     :                     PX1(1,K), PX1(2,K)
 120        FORMAT ('   Absolute closure error:',/,
     :              '    pix: ',F18.12,1X,F18.12,/,
     :              ' -> img: ',F18.12,1X,F18.12,/,
     :              ' -> pix: ',F18.12,1X,F18.12,/)
            GO TO 140
          END IF

          RESID = 0D0
          PX = ABS(PX0(1,K))
          IF (PX.GT.1D0) RESID = DP1/PX
          PX = ABS(PX0(2,K))
          IF (PX.GT.1D0) RESID = MAX(RESID, DP2/PX)
          IF (RESID.GT.RELMAX) RELMAX = RESID

          IF (RESID.GT.FTOL) THEN
            NCLOS = NCLOS + 1
            WRITE (*, 130) PX0(1,K), PX0(2,K), IMG(1,K), IMG(2,K),
     :                     PX1(1,K), PX1(2,K)
 130        FORMAT ('   Relative closure error:',/,
     :              '    pix: ',F18.12,1X,F18.12,/,
     :              ' -> img: ',F18.12,1X,F18.12,/,
     :              ' -> pix: ',F18.12,1X,F18.12,/)
          END IF
 140    CONTINUE

        NTEST = NTEST + N
 200  CONTINUE

 210  IF (NFAIL.NE.0) THEN
        WRITE (*, 220)
 220    FORMAT (/,'FAIL: The test failed to complete.')

      ELSE
        WRITE (*, 230) NTEST, ABSMAX, RELMAX
 230    FORMAT (
     :    'LINP2X/LINX2P with distortions:',/,
     :    '  Completed',I7,' closure tests.',/,
     :    '  Maximum absolute closure residual =',1P,E8.1,' pixel.',/,
     :    '  Maximum relative closure residual =',1P,E8.1,'.',/)

        IF (NCLOS.NE.0) THEN
        WRITE (*, 240) NCLOS
 240    FORMAT ('FAIL:',I5,' closure residuals exceed reporting ',
     :          'tolerance.')

        ELSE
        WRITE (*, 250)
 250    FORMAT ('PASS: All closure residuals are within reporting ',
     :          'tolerance.')
        END IF
      END IF


*     Free the memory allocated by WCSPIH.
 999  STATUS = WCSVFREE (NWCS, WCSP)

*     Free memory, allocated via the call to WCSSET, in the copy we made.
*     Also frees allocated memory in the shallow copy we made of linprm.
      STATUS = WCSFREE (WCS)

      END
