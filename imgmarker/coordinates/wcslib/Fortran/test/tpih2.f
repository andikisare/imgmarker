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
* $Id: tpih2.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TPIH2
*-----------------------------------------------------------------------
*
* TPIH2 tests WCSPIH, the WCS FITS parser for image headers, by reading
* a test header and using PGSBOX to plot coordinate graticules for the
* resulting WCSPRM structs.
*
* Input comes from file 'pih.fits'.
*
* WCSP, which is meant to hold an address, is declared as an INTEGER
* array of length 2 to accomodate 64-bit machines for which
* sizeof(void *) = 2*sizeof(int).
*-----------------------------------------------------------------------
      LOGICAL   GOTEND
      INTEGER   C0(7), GCODE(2), I, IC, IERR, J, K, NAXIS(2),
     :          NKEYRC, NREJECT, NWCS, RELAX, WCSP(2)
      REAL      BLC(2), TRC(2)
      DOUBLE PRECISION CACHE(4,0:256), NLDPRM(1)
      CHARACTER KEYREC*80, DEVTYP*16, HEADER*28801, IDENTS(3)*80,
     :          INFILE*9, NLCPRM(1)*1, OPT(2)*1, WCSNAME*72

*     On some systems, such as Sun Sparc, the struct MUST be aligned
*     on a double precision boundary, done here using an equivalence.
*     Failure to do this may result in mysterious "bus errors".
      INCLUDE 'wcshdr.inc'
      INCLUDE 'wcs.inc'
      INTEGER   WCS(WCSLEN)
      DOUBLE PRECISION DUMMY
      EQUIVALENCE (WCS,DUMMY)

      EXTERNAL PGWCSL

      DATA INFILE /'pih.fits'/
      DATA C0     /7*-1/
*-----------------------------------------------------------------------
      WRITE (*, 10)
 10   FORMAT (
     :  'Testing WCSLIB parser for FITS image headers (tpih2.f)',/,
     :  '------------------------------------------------------',/)

*     Open the FITS WCS test header for formatted, direct I/O.
      OPEN (UNIT=1, FILE=INFILE, FORM='FORMATTED', ACCESS='DIRECT',
     :      RECL=80, IOSTAT=IERR)
      IF (IERR.NE.0) THEN
        WRITE (*, 20) IERR, INFILE
 20     FORMAT ('ERROR',I3,' opening ',A)
        GO TO 999
      END IF

*     Read in the FITS header, excluding COMMENT and HISTORY keyrecords.
      K = 1
      NKEYRC = 0
      GOTEND = .FALSE.
      DO 50 J = 0, 100
        DO 40 I = 1, 36
          READ (1, '(A80)', REC=36*J+I, IOSTAT=IERR) KEYREC
          IF (IERR.NE.0) THEN
            WRITE (*, 30) IERR
 30         FORMAT ('ERROR',I3,' reading header.')
            GO TO 999
          END IF

          IF (KEYREC(:8).EQ.'        ') GO TO 40
          IF (KEYREC(:8).EQ.'COMMENT ') GO TO 40
          IF (KEYREC(:8).EQ.'HISTORY ') GO TO 40

          HEADER(K:) = KEYREC
          K = K + 80
          NKEYRC = NKEYRC + 1

          IF (KEYREC(:8).EQ.'END     ') THEN
*           An END keyrecord was read, read the rest of the block.
            GOTEND = .TRUE.
          END IF
 40     CONTINUE

        IF (GOTEND) GO TO 60
 50   CONTINUE

 60   CLOSE (UNIT=1)

      HEADER(K:K) = CHAR (0)
      WRITE (*, 70) NKEYRC
 70   FORMAT ('Found',I4,' non-comment header keyrecords.')


*     WCSPIH will allocate memory for an array of NWCS intialized WCSPRM
*     structs.  This array will be returned via a "pointer", WCSP, that
*     may be passed to WCSVCOPY to extract a particular struct.
      RELAX  = WCSHDR_all
      IERR = WCSPIH (HEADER, NKEYRC, RELAX, 3, NREJECT, NWCS, WCSP)
      IF (IERR.NE.0) THEN
        WRITE (*, 80) IERR
 80     FORMAT ('WCSPIH ERROR',I2,'.')
        GO TO 999
      END IF

*     Plot setup.
      NAXIS(1) = 1024
      NAXIS(2) = 1024

      BLC(1) = 0.5
      BLC(2) = 0.5
      TRC(1) = NAXIS(1) + 0.5
      TRC(2) = NAXIS(2) + 0.5

      DEVTYP = '/XWINDOW'
      CALL PGBEG(0, DEVTYP, 1, 1)
      CALL PGVSTD()

      CALL PGWNAD(0.0, 1.0, 0.0, 1.0)
      CALL PGASK(1)
      CALL PGPAGE()

*     Annotation.
      IDENTS(1) = 'Right ascension'
      IDENTS(2) = 'Declination'

      OPT(1) = 'G'
      OPT(2) = 'E'

*     Compact lettering.
      CALL PGSCH(0.8)

*     Draw full grid lines.
      CALL PGSCI(1)
      GCODE(1) = 2
      GCODE(2) = 2

      DO 100 I = 0, NWCS-1
*       Copy into our WCSPRM struct.
        IERR = WCSVCOPY (WCSP, I, WCS)

        IERR = WCSSET (WCS)
        IF (IERR.NE.0) THEN
          WRITE (*, 90) IERR
 90       FORMAT ('WCSSET ERROR',I2,'.')
          GO TO 999
        END IF

*       Get WCSNAME out of the WCSPRM struct.
        IERR = WCSGTC (WCS, WCS_WCSNAME, WCSNAME)
        IDENTS(3) = WCSNAME
        WRITE (*, '(/,A)') WCSNAME

*       Draw the celestial grid.  The grid density is set for each
*       world coordinate by specifying LABDEN = 1224.
        IC = -1
        CALL PGSBOX(BLC, TRC, IDENTS, OPT, 0, 1224, C0, GCODE, 0D0, 0,
     :    0D0, 0, 0D0, .FALSE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :    NLDPRM, 256, IC, CACHE, IERR)

*       Draw the frame.
        CALL PGBOX('BC', 0.0, 0, 'BC', 0.0, 0)

        CALL WCSLEEP (500)
        CALL PGPAGE()

*       Free memory (doesn't free memory allocated by WCSPIH).
        IERR = WCSFREE (WCS)
 100  CONTINUE

*     Free the memory allocated by WCSPIH.
      IERR = WCSVFREE (NWCS, WCSP)

 999  CONTINUE
      END
