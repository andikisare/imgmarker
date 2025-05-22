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
* $Id: twcsfix.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TWCSFIX
*-----------------------------------------------------------------------
*
* TWCSFIX tests the translation routines for non-standard WCS keyvalues,
* the WCSFIX suite.  It also tests the change of celestial coordinate
* system routine, WCSCCS, and the spectral coordinate translation
* routine, WCSSPTR.
*
*-----------------------------------------------------------------------
      DOUBLE PRECISION TOL
      PARAMETER (TOL = 1D-10)

*     B1950.0 equatorial coordinates of the galactic pole.
*     CUNITia is set to ARCSEC below as an additional test.
      DOUBLE PRECISION DEC, RA
      PARAMETER (RA  = 192.2500D0 * 3600D0)
      PARAMETER (DEC = +27.4000D0 * 3600D0)

*     Number of axes.
      INTEGER   N
      PARAMETER (N = 3)

      INTEGER   I, J, NAXIS, VELREF
      DOUBLE PRECISION BEPOCH, CDELT(N), CRPIX(N), CRVAL(N), EQUINOX,
     :          IMGCRD(N), LATPOLE, LONPOLE, MJDBEG, OBSGEO_B, OBSGEO_H,
     :          OBSGEO_L, PC(N,N), PHI, PIXCRD(N), RESTFRQ, RESTWAV,
     :          THETA, WORLD(N)
      CHARACTER CTYPE(N)*72, CUNIT(N)*72, DATEAVG*72, DATEBEG*72,
     :          DATEEND*72, DATEOBS*72, RADESYS*72, SPECSYS*72

      COMMON /HEADER/ CRPIX, PC, CDELT, CRVAL, RESTFRQ, RESTWAV, BEPOCH,
     :          MJDBEG, OBSGEO_L, OBSGEO_B, OBSGEO_H, EQUINOX, NAXIS,
     :          VELREF
      COMMON /HEADCH/ CTYPE, CUNIT, DATEOBS, DATEBEG, DATEAVG, DATEEND,
     :          SPECSYS

*     On some systems, such as Sun Sparc, the struct MUST be aligned
*     on a double precision boundary, done here using an equivalence.
*     Failure to do this may result in mysterious "bus errors".
      INCLUDE 'wcs.inc'
      INCLUDE 'wcsfix.inc'
      INTEGER   STAT(WCSFIX_NWCS), STATUS
      CHARACTER CTYPES*9
      INTEGER   WCS0(WCSLEN), WCS1(WCSLEN)
      DOUBLE PRECISION DUMMY0, DUMMY1
      EQUIVALENCE (WCS0,DUMMY0)
      EQUIVALENCE (WCS1,DUMMY1)

      DATA NAXIS   /N/
      DATA (CRPIX(J), J=1,N)
     :             /90D0,   90D0,   1D0/
      DATA ((PC(I,J),J=1,N),I=1,N)
     :             /1D0, 0D0, 0D0,
     :              0D0, 1D0, 0D0,
     :              0D0, 0D0, 1D0/
      DATA (CDELT(I), I=1,N)
     :             /-1D0, 1D0, 19.68717093222D0/
      DATA (CUNIT(I), I=1,N)
     :             /'ARCSEC', 'ARCSEC', 'KM/SEC'/
      DATA (CTYPE(I), I=1,N)
     :             /'RA---NCP', 'DEC--NCP', 'FELO-HEL'/
      DATA (CRVAL(I), I=1,N)
     :             /RA, DEC, 5569.27104D0/
      DATA RESTFRQ /1.42040575D9/
      DATA RESTWAV /0D0/

*     N.B. non-standard date-time format.
      DATA DATEOBS /'1957/02/15 01:10:00'/
      DATA DATEBEG /'1957/02/15 01:10:00'/
      DATA DATEAVG /'1957/02/15 02:10:00'/
      DATA DATEEND /'1957/02/15 03:10:00'/

      DATA BEPOCH  / 1957.124382563D0/
      DATA MJDBEG  / 35884.048611D0/

      DATA OBSGEO_L /148.263510D0/
      DATA OBSGEO_B /-32.998406D0/
      DATA OBSGEO_H /   411.793D0/

      DATA EQUINOX /1950.0D0/

*     For testing SPCFIX.
      DATA VELREF  /2/
      DATA SPECSYS /'BARYCENT'/
*-----------------------------------------------------------------------
      WRITE (*, 10)
 10   FORMAT ('Testing WCSLIB translator for non-standard usage ',
     :        '(twcsfix.f)',/,
     :        '-------------------------------------------------',
     :        '-----------',/)

*     This routine simulates the actions of a FITS header parser.
      STATUS = WCSPTI (WCS0, WCS_FLAG, -1, 0, 0)
      CALL PARSER (WCS0)

*     Fix non-standard WCS keyvalues.
      STATUS = WCSFIX (7, 0, WCS0, STAT)
      WRITE (*, 20) (STAT(I), I=1,WCSFIX_NWCS)
 20   FORMAT ('WCSFIX status returns: (',I2,6(',',I2),')',/)

      IF (STATUS.NE.0) THEN
        WRITE (*, 30) STATUS
 30     FORMAT ('WCSFIX ERROR',I2,'.')
        GO TO 999
      END IF

*     Extract information from the FITS header.
      STATUS = WCSSET (WCS0)
      IF (STATUS.NE.0) THEN
        STATUS = WCSPERR(WCS0, CHAR(0))
        GO TO 999
      END IF

      CALL FLUSH(6)
      STATUS = WCSPRT (WCS0)
      WRITE (*, 40)
 40   FORMAT (/,'------------------------------------',
     :          '------------------------------------')

*     Make a copy of the wcsprm struct.
      STATUS = WCSPTI (WCS1, WCS_FLAG, -1, 0, 0)
      STATUS = WCSSUB (WCS0, -1, -1, WCS1)
      IF (STATUS.NE.0) THEN
        STATUS = WCSPERR (WCS1, CHAR(0))
        GO TO 999
      END IF

*     Transform equatorial B1950 to galactic coordinates.  The WCS has
*     been constructed with the galactic pole coincident with the native
*     pole of the projection in order to test the resolution of an
*     indeterminacy.
      RADESYS = CHAR(0)
      STATUS = WCSCCS (WCS1, 123.0D0, 27.4D0, 192.25D0, 'GLON', 'GLAT',
     :                 RADESYS, 0D0, 'G')
      IF (STATUS.NE.0) THEN
        STATUS = WCSPERR (WCS1, CHAR(0))
        GO TO 999
      END IF

*     Should now have a 'VOPT-F2W' axis, translate it to frequency.
      CTYPES = 'FREQ-???'
      I = -1
      STATUS = WCSSPTR (WCS1, I, CTYPES)
      IF (STATUS.NE.0) THEN
        STATUS = WCSPERR(WCS1, CHAR(0))
        GO TO 999
      END IF

      STATUS = WCSSET (WCS1)
      IF (STATUS.NE.0) THEN
        STATUS = WCSPERR(WCS1, CHAR(0))
        GO TO 999
      END IF

      CALL FLUSH(6)
      STATUS = WCSPRT (WCS1)

*     Print before-and-afters.
      WRITE (*, 50) (CRPIX(I), I=1,N)
 50   FORMAT (/,'Original and new coordinates of reference point ('
     :        2(F4.1,', '),F3.1,'), lonpole, and latpole:')
      STATUS = WCSGTD (WCS0, WCS_CRVAL,   CRVAL(1))
      STATUS = WCSGTD (WCS0, WCS_LONPOLE, LONPOLE)
      STATUS = WCSGTD (WCS0, WCS_LATPOLE, LATPOLE)
      WRITE (*, 60) (CRVAL(I), I=1,N), LONPOLE, LATPOLE
 60   FORMAT (2(F14.6,', '),F14.2,', ',F14.6,', ',F14.6)

      STATUS = WCSGTD (WCS1, WCS_CRVAL,   CRVAL(1))
      STATUS = WCSGTD (WCS1, WCS_LONPOLE, LONPOLE)
      STATUS = WCSGTD (WCS1, WCS_LATPOLE, LATPOLE)
      WRITE (*, 60) (CRVAL(I), I=1,N), LONPOLE, LATPOLE

*     Compute B1950 coordinates of a field point.
      PIXCRD(1) = 1000D0
      PIXCRD(2) = 1000D0
      PIXCRD(3) =    1D0
      WRITE (*, 70) (PIXCRD(I), I=1,N)
 70   FORMAT (/,'Original and new coordinates of field point (',
     :        2(F6.1,', '),F3.1,'):')

      STATUS = WCSP2S (WCS0, 1, N, PIXCRD, IMGCRD, PHI, THETA, WORLD,
     :                 STAT)
      IF (STATUS.NE.0) THEN
        STATUS = WCSPERR (WCS0, CHAR(0))
        GO TO 999
      END IF

      WRITE (*, 80) (WORLD(I), I=1,N)
 80   FORMAT (2(F14.6,', '),F14.2)

*     Compute galactic coordinates of the same field point.
      STATUS = WCSP2S (WCS1, 1, N, PIXCRD, IMGCRD, PHI, THETA, WORLD,
     :                 STAT)
      IF (STATUS.NE.0) THEN
        STATUS = WCSPERR (WCS1, CHAR(0))
        GO TO 999
      END IF

      WRITE (*, 80) (WORLD(I), I=1,N)

      STATUS = WCSFREE (WCS0)
      STATUS = WCSFREE (WCS1)


 999  CONTINUE
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
      PARAMETER (N = 3)

      INTEGER   I, J, NAXIS, STATUS, VELREF, WCS(*)
      DOUBLE PRECISION BEPOCH, CDELT(N), CRPIX(N), CRVAL(N), EQUINOX,
     :          MJDBEG, OBSGEO_B, OBSGEO_H, OBSGEO_L, PC(N,N), RESTFRQ,
     :          RESTWAV
      CHARACTER CTYPE(N)*72, CUNIT(N)*72, DATEAVG*72, DATEBEG*72,
     :          DATEEND*72, DATEOBS*72, SPECSYS*72

      COMMON /HEADER/ CRPIX, PC, CDELT, CRVAL, RESTFRQ, RESTWAV, BEPOCH,
     :          MJDBEG, OBSGEO_L, OBSGEO_B, OBSGEO_H, EQUINOX, NAXIS,
     :          VELREF
      COMMON /HEADCH/ CTYPE, CUNIT, DATEOBS, DATEBEG, DATEAVG, DATEEND,
     :          SPECSYS

      INCLUDE 'wcsunits.inc'
      INCLUDE 'wcs.inc'
*-----------------------------------------------------------------------
      STATUS = WCSNPV (2)
      STATUS = WCSINI (NAXIS, WCS)

      DO 20 I = 1, NAXIS
        STATUS = WCSPTD (WCS, WCS_CRPIX, CRPIX(I), I, 0)

        DO 10 J = 1, NAXIS
          STATUS = WCSPTD (WCS, WCS_PC, PC(I,J), I, J)
 10     CONTINUE

        STATUS = WCSPTD (WCS, WCS_CDELT, CDELT(I), I, 0)
        STATUS = WCSPTC (WCS, WCS_CUNIT, CUNIT(I), I, 0)
        STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(I), I, 0)
        STATUS = WCSPTD (WCS, WCS_CRVAL, CRVAL(I), I, 0)
 20   CONTINUE

      STATUS = WCSPTD (WCS, WCS_RESTFRQ, RESTFRQ, 0, 0)
      STATUS = WCSPTD (WCS, WCS_RESTWAV, RESTWAV, 0, 0)

      STATUS = WCSPTI (WCS, WCS_NPV, 1, 0, 0)
      STATUS = WCSPTD (WCS, WCS_PV, -1D0, -1, -1)

      STATUS = WCSPTI (WCS, WCS_VELREF, VELREF, 0, 0)

      STATUS = WCSPTC (WCS, WCS_DATEAVG, DATEAVG, 0, 0)
      STATUS = WCSPTC (WCS, WCS_DATEEND, DATEEND, 0, 0)

      STATUS = WCSPTD (WCS, WCS_BEPOCH,  BEPOCH,  0, 0)
      STATUS = WCSPTD (WCS, WCS_MJDBEG,  MJDBEG,  0, 0)

      STATUS = WCSPTD (WCS, WCS_OBSGEO, OBSGEO_L, 4, 0)
      STATUS = WCSPTD (WCS, WCS_OBSGEO, OBSGEO_B, 5, 0)
      STATUS = WCSPTD (WCS, WCS_OBSGEO, OBSGEO_H, 6, 0)

      STATUS = WCSPTD (WCS, WCS_EQUINOX, EQUINOX, 6, 0)

      STATUS = WCSPTC (WCS, WCS_SPECSYS, SPECSYS, 0, 0)

      RETURN
      END
