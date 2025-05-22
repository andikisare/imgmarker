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
* $Id: tdis2.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TDIS2
*-----------------------------------------------------------------------
*
* TDIS2 tests the WCSLIB Fortran routines for manipulating the contents
* of a disprm struct.  Two disprm structs are used.  One, residing in a
* linprm struct, is referenced by "address" (DISP), and the other (DISL)
* resides locally in an INTEGER array.
*
* DISP and WCSP, which are meant to hold addresses, are declared as
* INTEGER arrays of length 2 to accomodate 64-bit machines for which
* sizeof(void *) = 2*sizeof(int).
*
* Test input comes from TPV7.fits.
*-----------------------------------------------------------------------
      INTEGER   DPMAX
      PARAMETER (DPMAX = 256)

      LOGICAL   GOTEND
      INTEGER   DISP(2), IBLOCK, IKEYRC, J, JK, JN, K, NAXIS, NDP,
     :          NKEYRC, NREJECT, NWCS, STATL, STATP, STATUS, WCSP(2)
      DOUBLE PRECISION MAXDIS(2), TOTDIS
      CHARACTER DTYPE(2)*72, KEYREC*80, HEADER*28801, INFILE*9

*     On some systems, such as Sun Sparc, the structs MUST be aligned
*     on a double precision boundary, done here using an equivalence.
*     Failure to do this may result in mysterious "bus errors".
      INCLUDE 'wcserr.inc'
      INCLUDE 'wcshdr.inc'
      INCLUDE 'wcs.inc'
      INCLUDE 'lin.inc'
      INCLUDE 'dis.inc'
      INTEGER   DP(DPMAX*DPLEN), WCS(WCSLEN), LIN(LINLEN), DISL(DISLEN)
      DOUBLE PRECISION DUMMY1, DUMMY2, DUMMY3, DUMMY4
      EQUIVALENCE (DUMMY1, DP)
      EQUIVALENCE (DUMMY2, WCS)
      EQUIVALENCE (DUMMY3, LIN)
      EQUIVALENCE (DUMMY4, DISL)

      DATA INFILE /'TPV7.fits'/
*-----------------------------------------------------------------------
      STATUS = WCSERR_ENABLE (1)

      WRITE (*, 10)
 10   FORMAT (
     :  'Testing WCSLIB Fortran disprm access routines (tdis2.f)',/,
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
 30         FORMAT ('ERROR',I5,' reading header.')
            GO TO 999
          END IF

          IF (KEYREC(:8).EQ.'        ') GO TO 40
          IF (KEYREC(:8).EQ.'COMMENT ') GO TO 40
          IF (KEYREC(:8).EQ.'HISTORY ') GO TO 40

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
      CALL FLUSH(6)
      STATUS = WCSPIH (HEADER, NKEYRC, WCSHDR_none, 2, NREJECT, NWCS,
     :                 WCSP)
      IF (STATUS.NE.0) GO TO 999

*     Copy into our WCSPRM struct.
      STATUS = WCSVCOPY (WCSP, 0, WCS)
      IF (STATUS.NE.0) GO TO 999

*     WCSSET translates the TPV "projection" into a sequent distortion.
      STATUS = WCSSET (WCS)
      IF (STATUS.NE.0) THEN
        STATUS = WCSPERR (WCS, CHAR(0))
        GO TO 999
      END IF

*     Make a shallow copy of the linprm struct.
      STATUS = WCSGTI (WCS, WCS_LIN, LIN)
      IF (STATUS.NE.0) THEN
        STATUS = WCSPERR (WCS, CHAR(0))
        GO TO 999
      END IF

*     Extract a "pointer" to the disprm struct.
      STATUS = LINGTI (LIN, LIN_DISSEQ, DISP)
      IF (STATUS.NE.0) THEN
        STATUS = LINPERR (LIN, CHAR(0))
        GO TO 999
      END IF

*     Add a little texture.  The first argument of DISPTD (and DISPRT,
*     DISGET, etc.) is unity to indicate that DISP is a "pointer".
      STATP = DISPTD (1, DISP, DIS_TOTDIS, 3.0000D0, 0, 0)
      IF (STATP.NE.0) GO TO 998
      STATP = DISPTD (1, DISP, DIS_MAXDIS, 2.0010D0, 1, 0)
      IF (STATP.NE.0) GO TO 998
      STATP = DISPTD (1, DISP, DIS_MAXDIS, 2.0020D0, 2, 0)
      IF (STATP.NE.0) GO TO 998

*     Print its contents.
      CALL FLUSH(6)
      STATP = DISPRT (1, DISP)
      IF (STATP.NE.0) GO TO 998

      WRITE (*, 70)
 70   FORMAT (/,'------------------------------------',
     :          '------------------------------------')


*   Copy it the long way first to test the various PUT and GET routines.
*     Start by reading everything from the first.
      STATP = DISGTI (1, DISP, DIS_NAXIS,  NAXIS)
      IF (STATP.NE.0) GO TO 998
      STATP = DISGTC (1, DISP, DIS_DTYPE,  DTYPE)
      IF (STATP.NE.0) GO TO 998
      STATP = DISGTI (1, DISP, DIS_NDP,    NDP)
      IF (STATP.NE.0) GO TO 998
      STATP = DISGTI (1, DISP, DIS_DP,     DP(1))
      IF (STATP.NE.0) GO TO 998
      STATP = DISGTD (1, DISP, DIS_TOTDIS, TOTDIS)
      IF (STATP.NE.0) GO TO 998
      STATP = DISGTD (1, DISP, DIS_MAXDIS, MAXDIS(1))
      IF (STATP.NE.0) GO TO 998

*     Initialize the destination.  The first argument of DISPUT (and
*     DISINI, etc.) is zero to indicate that DISL is an array (struct).
      STATL = DISPTI (0, DISL, DIS_FLAG, -1, 0, 0)
      IF (STATL.NE.0) GO TO 997
      STATL = DISINI (0, NAXIS, DISL)
      IF (STATL.NE.0) GO TO 997

*     Copy to the destination.
      JK = 0
      JN = 0
      DO 110 J = 1, NAXIS
        STATL = DISPTC (0, DISL, DIS_DTYPE, DTYPE, J, 0)
        IF (STATL.NE.0) GO TO 997
 110  CONTINUE

      DO 120 K = 1, NDP*DPLEN, DPLEN
        STATL = DISPTI (0, DISL, DIS_DP, DP(K), 0, 0)
 120  CONTINUE

      STATL = DISPTD (0, DISL, DIS_TOTDIS, TOTDIS, J, 0)
      IF (STATL.NE.0) GO TO 997

      DO 130 J = 1, NAXIS
        STATL = DISPTD (0, DISL, DIS_MAXDIS, MAXDIS(J), J, 0)
        IF (STATL.NE.0) GO TO 997
 130  CONTINUE

      STATL = DISSET (0, DISL)
      IF (STATL.NE.0) GO TO 997

*     Print the second.
      CALL FLUSH(6)
      STATL = DISPRT (0, DISL)
      IF (STATL.NE.0) GO TO 997

      WRITE (*, 70)


*   Now copy it the fast way.
*     DISCPY's first argument indicates that the source, DISP, is a
*     "pointer", and the destination, DISL, a local array.  DISCPY
*     will invoke DISINI on the destination, reusing memory allocated
*     previously by DISINI and DISSET.
      STATL = DISCPY (1, DISP, DISL)
      IF (STATL.NE.0) GO TO 997

*     A reset is required before printing.
      STATL = DISSET (0, DISL)
      IF (STATL.NE.0) GO TO 997

*     Print the copy.
      CALL FLUSH(6)
      STATL = DISPRT (0, DISL)
      IF (STATL.NE.0) GO TO 997


*   Cleanup.
 997  IF (STATL.NE.0) THEN
        STATUS = DISPERR (0, DISL, CHAR(0))
      END IF

*     Free memory allocated in the disprm struct.
      STATUS = DISFREE (0, DISL)

 998  IF (STATP.NE.0) THEN
        STATUS = DISPERR (1, DISP, CHAR(0))
      END IF

*     Free memory allocated by WCSPIH, WCSINI, etc.
 999  STATUS = WCSVFREE (NWCS, WCSP)

*     Free memory, allocated via the call to WCSSET, in the copy we made.
*     Also frees allocated memory in the shallow copy we made of linprm.
      STATUS = WCSFREE (WCS)

      END
