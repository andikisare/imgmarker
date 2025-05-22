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
* $Id: twcssub.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TWCSSUB
*-----------------------------------------------------------------------
*
* TWCSSUB tests WCSSUB which extracts the coordinate description for a
* subimage from a wcsprm struct.
*
*-----------------------------------------------------------------------
*     Number of axes.
      INTEGER   NAXIS
      PARAMETER (NAXIS = 4)

      INTEGER   AXES(NAXIS), I, J, K, NPS, NPV, NSUB, PSI(10), PSM(10),
     :          PVI(10), PVM(10), STATUS
      DOUBLE PRECISION CDELT(NAXIS), CRPIX(NAXIS), CRVAL(NAXIS),
     :          LATPOLE, LONPOLE, PC(NAXIS,NAXIS), PV(10), RESTFRQ,
     :          RESTWAV
      CHARACTER CNAME(NAXIS)*72, CTYPE(NAXIS)*72, CUNIT(NAXIS)*72,
     :          PS(10)*72

*     On some systems, such as Sun Sparc, the structs MUST be aligned
*     on a double precision boundary, done here using equivalences.
*     Failure to do this may result in mysterious "bus errors".
      INCLUDE 'wcs.inc'
      INCLUDE 'wcserr.inc'
      INTEGER   WCS(WCSLEN), WCSEXT(WCSLEN)
      DOUBLE PRECISION DUMMY1, DUMMY2
      EQUIVALENCE (WCS,DUMMY1), (WCSEXT,DUMMY2)

      DATA (CRPIX(J), J=1,NAXIS)
     :             / 1025D0,  64D0, 512D0,  513D0/
      DATA ((PC(I,J),J=1,NAXIS),I=1,NAXIS)
     :             /  1.1D0,   0D0,   0D0,   0D0,
     :                  0D0, 1.0D0,   0D0,   0D0,
     :                  0D0,   0D0, 1.0D0, 0.1D0,
     :                  0D0,   0D0, 0.2D0, 1.0D0/
      DATA (CDELT(I), I=1,NAXIS)
     :             /-9.2D-6,  10D0,   1D0,  -1D0/
      DATA (CUNIT(I), I=1,NAXIS)
     :             /'m', 's', 'deg', 'deg'/
      DATA (CTYPE(I), I=1,NAXIS)
     :             /'WAVE-F2W', 'TIME', 'XLAT-SZP', 'XLON-SZP'/
      DATA (CRVAL(I), I=1,NAXIS)
     :             /0.214982042D0, -2D3, -30D0, 150D0/
      DATA LONPOLE /150D0/
      DATA LATPOLE /999D0/
      DATA RESTFRQ /1.42040575D9/
      DATA RESTWAV /0D0/

      DATA (CNAME(I), I=1,NAXIS)
     :             /'Wavelength', 'Time', 'Latitude', 'Longitude'/

      PARAMETER (NPV = 4)
      DATA (PVI(K), PVM(K), PV(K), K=1,NPV)
     :             /1, 1,  -1D0,
     :              3, 1,   2D0,
     :              3, 2, 210D0,
     :              3, 3,  60D0/

      PARAMETER (NPS = 1)
      DATA (PSI(K), PSM(K), PS(K), K=1,NPS)
     :             /2, 1, 'UTC'/
*-----------------------------------------------------------------------
      STATUS = WCSPTI (WCS, WCS_FLAG, -1, 0, 0)
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
        STATUS = WCSPTC (WCS, WCS_CNAME, CNAME(I), I, 0)
 20   CONTINUE

      STATUS = WCSPTD (WCS, WCS_LONPOLE, LONPOLE, 0, 0)
      STATUS = WCSPTD (WCS, WCS_LATPOLE, LATPOLE, 0, 0)

      STATUS = WCSPTD (WCS, WCS_RESTFRQ, RESTFRQ, 0, 0)
      STATUS = WCSPTD (WCS, WCS_RESTWAV, RESTWAV, 0, 0)

      DO 30 K = 1, NPV
        STATUS = WCSPTD (WCS, WCS_PV, PV(K), PVI(K), PVM(K))
 30   CONTINUE

      DO 40 K = 1, NPS
        STATUS = WCSPTC (WCS, WCS_PS, PS(K), PSI(K), PSM(K))
 40   CONTINUE

*     Extract information from the FITS header.
      STATUS = WCSSET (WCS)
      IF (STATUS.NE.0) THEN
        WRITE (*, 50) STATUS
 50     FORMAT ('WCSSET ERROR',I3,'.')
        GO TO 999
      END IF

      WRITE (*, 60)
 60   FORMAT (
     :  'Testing WCSLIB subimage extraction subroutine (twcssub.f)',/,
     :  '---------------------------------------------------------',//,
     :  'Initial contents of wcsprm struct:')
      CALL FLUSH(6)
      STATUS = WCSPRT (WCS)


*     Extract the coordinate description for a subimage and add an axis.
      NSUB = 4
      AXES(1) = WCSSUB_LONGITUDE
      AXES(2) = WCSSUB_LATITUDE
      AXES(3) = -(WCSSUB_SPECTRAL + WCSSUB_STOKES)
      AXES(4) = 0
      WRITE (6, 70)
 70   FORMAT (//,'Extracted contents of wcsprm struct:')

      STATUS = WCSPTI (WCSEXT, WCS_FLAG, -1, 0, 0)
      STATUS = WCSSUB (WCS, NSUB, AXES, WCSEXT)

      CALL FLUSH(6)
      IF (STATUS.NE.0) THEN
        STATUS = WCSPERR (WCSEXT, CHAR(0))
      ELSE
        STATUS = WCSSET (WCSEXT)
        IF (STATUS.NE.0) THEN
          STATUS = WCSPERR (WCSEXT, CHAR(0))
        ELSE
          STATUS = WCSPRT (WCSEXT)
        END IF
      END IF


*     Set it up for failure by setting PC1_3 non-zero.
      STATUS = WCSPTD (WCS, WCS_PC, 1D0, 1, 3)
      NSUB = 2
      AXES(1) = 4
      AXES(2) = 3
      STATUS = WCSSUB(WCS, NSUB, AXES, WCSEXT)
      IF (STATUS.EQ.WCSERR_NON_SEPARABLE) THEN
        WRITE (6, 80) WCSERR_NON_SEPARABLE
 80     FORMAT (//,'Received wcssub status',I3,' as expected for a '
     :    'non-separable subimage',/,'coordinate system.')
      ELSE
        WRITE (6, 90) WCSERR_NON_SEPARABLE, STATUS
 90     FORMAT (//,'ERROR: expected wcssub status',I3,' for a non-',
     :    'separable subimage coordinate',/,'system, but received ',
     :    'status',I3,' instead.')
      END IF


      STATUS = WCSFREE (WCSEXT)
 999  STATUS = WCSFREE (WCS)

      END
