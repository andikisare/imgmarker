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
* $Id: twcsmix.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TWCS2
*-----------------------------------------------------------------------
*
* TWCS2 tests WCSMIX for closure on the 1 degree celestial graticule for
* a number of selected projections.  Points with good solutions are
* marked with a white dot on a graphical display of the projection while
* bad solutions are flagged with a red circle.
*
*-----------------------------------------------------------------------
*     Number of axes.
      INTEGER   N
      PARAMETER (N = 4)

      INTEGER   I, J, K, NAXIS, NPV, PVI(4), PVM(4)
      DOUBLE PRECISION CDELT(N), CRPIX(N), CRVAL(N), LATPOLE, LONPOLE,
     :          PC(N,N), PV(4), RESTFRQ, RESTWAV
      CHARACTER CTYPE(N)*72

      DOUBLE PRECISION TOL
      PARAMETER (TOL = 1D-9)

      COMMON /HEADER/ NAXIS, NPV, CRPIX, PC, CDELT, CRVAL, LONPOLE,
     :                LATPOLE, RESTFRQ, RESTWAV, PVI, PVM, PV
      COMMON /HEADCH/ CTYPE

      DATA NAXIS   /N/
      DATA (CRPIX(J), J=1,N)
     :             /513D0,   0D0,   0D0,   0D0/
      DATA ((PC(I,J),J=1,N),I=1,N)
     :             /1.1D0,    0D0,    0D0,    0D0,
     :                0D0,  1.0D0,    0D0,  0.1D0,
     :                0D0,    0D0,  1.0D0,    0D0,
     :                0D0,  0.2D0,    0D0,  1.0D0/
      DATA (CDELT(I), I=1,N)
     :             /-9.635265432D-6, 1D0, 1D0, -1D0/
      DATA (CTYPE(I), I=1,N)
     :           /'WAVE-F2W', 'XLAT-xxx ', 'TIME    ', 'XLON-xxx '/
      DATA (CRVAL(I), I=1,N)
     :             /0.214982042D0, -30D0, -2D3, 150D0/
      DATA LONPOLE /150D0/
      DATA LATPOLE /999D0/
      DATA RESTFRQ /1.42040575D9/
      DATA RESTWAV /0D0/

*     Set PVi_m keyvalues for the longitude axis (I = 4) so that the
*     fiducial native coordinates are at the native pole, i.e.
*     (phi0,theta0) = (0,90), but without any fiducial offset.  We do
*     this as a test, and also so that all projections will be
*     exercised with the same obliquity parameters.
      DATA (PVI(K), PVM(K), PV(K), K=1,2)
     :             /4, 1,  0D0,
     :              4, 2, 90D0/

*     PVi_m keyvalues for the latitude axis (I = 2).  Value may be reset
*     below.
      DATA (PVI(K), PVM(K), PV(K), K=3,4)
     :             /2, 1, 0D0,
     :              2, 2, 0D0/
*-----------------------------------------------------------------------
      WRITE (*, 10)
 10   FORMAT ('Testing WCSLIB wcsmix routine (twcsmix.f)',/,
     :        '-----------------------------------------')

*     PGPLOT initialization.
      CALL PGBEG (0, '/xwindow', 1, 1)

*     Define pen colours.
      CALL PGSCR (0, 0.00, 0.00, 0.00)
      CALL PGSCR (1, 1.00, 1.00, 0.00)
      CALL PGSCR (2, 1.00, 1.00, 1.00)
      CALL PGSCR (3, 0.50, 0.50, 0.80)
      CALL PGSCR (4, 0.80, 0.50, 0.50)
      CALL PGSCR (5, 0.80, 0.80, 0.80)
      CALL PGSCR (6, 0.50, 0.50, 0.80)
      CALL PGSCR (7, 0.80, 0.50, 0.50)
      CALL PGSCR (8, 0.30, 0.50, 0.30)
      CALL PGSCR (9, 1.00, 0.75, 0.00)

*     ARC: zenithal/azimuthal equidistant.
      CTYPE(2)(6:8) = 'ARC'
      CTYPE(4)(6:8) = 'ARC'
      NPV = 2
      CALL MIXEX (TOL, -190.0, 190.0, -190.0, 190.0)

*     ZEA: zenithal/azimuthal equal area.
      CTYPE(2)(6:8) = 'ZEA'
      CTYPE(4)(6:8) = 'ZEA'
      NPV = 2
      CALL MIXEX (TOL, -120.0, 120.0, -120.0, 120.0)

*     CYP: cylindrical perspective.
      CTYPE(2)(6:8) = 'CYP'
      CTYPE(4)(6:8) = 'CYP'
      NPV = 4
      PV(3) = 3D0
      PV(4) = 0.8D0
      CALL MIXEX (TOL, -170.0, 170.0, -170.0, 170.0)

*     CEA: cylindrical equal area.
      CTYPE(2)(6:8) = 'CEA'
      CTYPE(4)(6:8) = 'CEA'
      NPV = 3
      PV(3) = 0.75D0
      CALL MIXEX (TOL, -200.0, 200.0, -200.0, 200.0)

*     CAR: plate carree.
      CTYPE(2)(6:8) = 'CAR'
      CTYPE(4)(6:8) = 'CAR'
      NPV = 2
      CALL MIXEX (TOL, -210.0, 210.0, -210.0, 210.0)

*     SFL: Sanson-Flamsteed.
      CTYPE(2)(6:8) = 'SFL'
      CTYPE(4)(6:8) = 'SFL'
      NPV = 2
      CALL MIXEX (TOL, -190.0, 190.0, -190.0, 190.0)

*     PAR: parabolic.
      CTYPE(2)(6:8) = 'PAR'
      CTYPE(4)(6:8) = 'PAR'
      NPV = 2
      CALL MIXEX (TOL, -190.0, 190.0, -190.0, 190.0)

*     MOL: Mollweide's projection.
      CTYPE(2)(6:8) = 'MOL'
      CTYPE(4)(6:8) = 'MOL'
      NPV = 2
      CALL MIXEX (TOL, -170.0, 170.0, -170.0, 170.0)

*     AIT: Hammer-Aitoff.
      CTYPE(2)(6:8) = 'AIT'
      CTYPE(4)(6:8) = 'AIT'
      NPV = 2
      CALL MIXEX (TOL, -170.0, 170.0, -170.0, 170.0)

*     COE: conic equal area.
      CTYPE(2)(6:8) = 'COE'
      CTYPE(4)(6:8) = 'COE'
      NPV = 4
      PV(3) = 60D0
      PV(4) = 15D0
      CALL MIXEX (TOL, -140.0, 140.0, -120.0, 160.0)

*     COD: conic equidistant.
      CTYPE(2)(6:8) = 'COD'
      CTYPE(4)(6:8) = 'COD'
      NPV = 4
      PV(3) = 60D0
      PV(4) = 15D0
      CALL MIXEX (TOL, -200.0, 200.0, -180.0, 220.0)

*     BON: Bonne's projection.
      CTYPE(2)(6:8) = 'BON'
      CTYPE(4)(6:8) = 'BON'
      NPV = 3
      PV(3) = 30D0
      CALL MIXEX (TOL, -160.0, 160.0, -160.0, 160.0)

*     PCO: polyconic.
      CTYPE(2)(6:8) = 'PCO'
      CTYPE(4)(6:8) = 'PCO'
      NPV = 2
      CALL MIXEX (TOL, -190.0, 190.0, -190.0, 190.0)

*     TSC: tangential spherical cube.
      CTYPE(2)(6:8) = 'TSC'
      CTYPE(4)(6:8) = 'TSC'
      NPV = 2
      CALL MIXEX (TOL, -340.0, 80.0, -210.0, 210.0)

*     QSC: quadrilateralized spherical cube.
      CTYPE(2)(6:8) = 'QSC'
      CTYPE(4)(6:8) = 'QSC'
      NPV = 2
      CALL MIXEX (TOL, -340.0, 80.0, -210.0, 210.0)

      CALL PGEND ()

      END


*-----------------------------------------------------------------------
      SUBROUTINE MIXEX (TOL, IMIN, IMAX, JMIN, JMAX)
*-----------------------------------------------------------------------
*   MIXEX tests WCSMIX.
*
*   Given:
*      TOL      D        Reporting tolerance, degrees.
*-----------------------------------------------------------------------
      INTEGER   DOID, ILAT, ILNG, LATIDX, LNGIDX, SPCIDX, STAT, STATUS
      REAL      IMAX, IMIN, IPT(1), JMAX, JMIN, JPT(1)
      DOUBLE PRECISION IMG(4), LAT1, LATSPN(2), LNGSPN(2), LNG1, PHI,
     :          PIX1(4), PIX2(4), PIX3(4), PIXLAT, PIXLNG, THETA, TOL,
     :          WORLD(4)
      CHARACTER PCODE*4

*     On some systems, such as Sun Sparc, the structs MUST be aligned
*     on a double precision boundary, done here using equivalences.
*     Failure to do this may result in mysterious "bus errors".
      INCLUDE 'wcs.inc'
      INCLUDE 'cel.inc'
      INCLUDE 'prj.inc'
      INTEGER   CEL(CELLEN), PRJ(PRJLEN), WCS(WCSLEN)
      DOUBLE PRECISION DUMMY1, DUMMY2, DUMMY3
      EQUIVALENCE (CEL,DUMMY1), (PRJ,DUMMY2), (WCS,DUMMY3)
*-----------------------------------------------------------------------
*     This routine simulates the actions of a FITS header parser.
      STATUS = WCSPTI (WCS, WCS_FLAG, -1, 0, 0)
      CALL PARSER (WCS)


*     Draw the coordinate graticule.
      CALL GRDPLT(WCS, IMIN, IMAX, JMIN, JMAX)


      STATUS = WCSGTI (WCS, WCS_CEL, CEL(1))
      STATUS = CELGTI (CEL, CEL_PRJ, PRJ(1))
      STATUS = PRJGTC (PRJ, PRJ_CODE, PCODE)
      WRITE (*, 10) PCODE, TOL
 10   FORMAT ('Testing ',A3,'; reporting tolerance',1PG8.1,' deg.')

      STATUS = WCSGTI (WCS, WCS_LNG, LNGIDX)
      STATUS = WCSGTI (WCS, WCS_LAT, LATIDX)
      STATUS = WCSGTI (WCS, WCS_SPEC, SPCIDX)
      WORLD(1) = 0D0
      WORLD(2) = 0D0
      WORLD(3) = 0D0
      WORLD(4) = 0D0
      WORLD(SPCIDX) = 2.99792458D8 / 1.42040595D9

      DO 80 ILAT = 90, -90, -1
        LAT1 = DBLE(ILAT)

        DO 70 ILNG = -180, 180, 15
          LNG1 = DBLE(ILNG)

          WORLD(LNGIDX) = LNG1
          WORLD(LATIDX) = LAT1
          STATUS = WCSS2P (WCS, 1, 4, WORLD(1), PHI, THETA, IMG(1),
     :                     PIX1(1), STAT)
          IF (STATUS.NE.0) THEN
            WRITE (*, 20) PCODE, LNG1, LAT1, STATUS
 20         FORMAT (A3,': LNG1 =',F20.15,'  LAT1 =',F20.15,
     :         '  ERROR',I3)
            GO TO 70
          END IF

          PIXLNG = PIX1(LNGIDX)
          PIXLAT = PIX1(LATIDX)

          IPT(1) = REAL(PIXLNG)
          JPT(1) = REAL(PIXLAT)
          CALL PGPT (1, IPT, JPT, -1)

          LNGSPN(1) = LNG1 - 9.3D0
          IF (LNGSPN(1).LT.-180D0) LNGSPN(1) = -180D0
          LNGSPN(2) = LNG1 + 4.1D0
          IF (LNGSPN(2).GT. 180D0) LNGSPN(2) =  180D0
          LATSPN(1) = LAT1 - 3.7D0
          IF (LATSPN(1).LT. -90D0) LATSPN(1) =  -90D0
          LATSPN(2) = LAT1 + 7.2D0
          IF (LATSPN(2).GT.  90D0) LATSPN(2) =   90D0

          DOID = 1

          PIX2(LNGIDX) = PIXLNG
          STATUS = WCSMIX (WCS, LNGIDX, 1, LATSPN, 1D0, 0, WORLD,
     :       PHI, THETA, IMG, PIX2)
          IF (STATUS.NE.0) THEN
            CALL ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
            WRITE (*, '(A,I2)') '  A: WCSMIX ERROR', STATUS
          ELSE
            STATUS = WCSS2P (WCS, 1, 0, WORLD(1), PHI, THETA, IMG(1),
     :                       PIX3(1), STAT)
            IF (STATUS.NE.0) THEN
              CALL ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
              WRITE (*, '(A,I2)') '  A: WCSS2P ERROR', STATUS
            ELSE IF (ABS(PIX3(LNGIDX)-PIXLNG).GT.TOL .AND.
     :              (ABS(WORLD(LATIDX)- LAT1).GT.TOL .OR.
     :               ABS(PIX2(LATIDX)-PIXLAT).GT.TOL)) THEN
              CALL ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
              WRITE (*, 30) WORLD(LNGIDX), WORLD(LATIDX), PHI,
     :                      THETA, PIX2(LNGIDX), PIX2(LATIDX)
 30           FORMAT ('  A: (LNG2) =',F20.15,'   LAT2  =',F20.15,/,
     :                '       PHI  =',F20.15,'  THETA  =',F20.15,/,
     :                '       (I2) =',F20.15,'     J2  =',F20.15)
            END IF
          END IF

          PIX2(LATIDX) = PIXLAT
          STATUS = WCSMIX (WCS, LATIDX, 1, LATSPN, 1D0, 0, WORLD,
     :                     PHI, THETA, IMG, PIX2)
          IF (STATUS.NE.0) THEN
            CALL ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
            WRITE (*, '(A,I2)') '  B: WCSMIX ERROR', STATUS
          ELSE
            STATUS = WCSS2P (WCS, 1, 0, WORLD(1), PHI, THETA,
     :                       IMG(1), PIX3(1), STAT)
            IF (STATUS.NE.0) THEN
              CALL ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
              WRITE (*, '(A,I2)') '  B: WCSS2P ERROR', STATUS
            ELSE IF (ABS(PIX3(LATIDX)-PIXLAT).GT.TOL .AND.
     :              (ABS(WORLD(LATIDX)- LAT1).GT.TOL .OR.
     :               ABS(PIX2(LNGIDX)-PIXLNG).GT.TOL)) THEN
              CALL ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
              WRITE (*, 40) WORLD(LNGIDX), WORLD(LATIDX), PHI,
     :                      THETA, PIX2(LNGIDX), PIX2(LATIDX)
 40           FORMAT ('  B: (LNG2) =',F20.15,'   LAT2  =',F20.15,/,
     :                '       PHI  =',F20.15,'  THETA  =',F20.15,/,
     :                '        I2  =',F20.15,'    (J2) =',F20.15)
            END IF
          END IF

          WORLD(LATIDX) = LAT1

          PIX2(LNGIDX) = PIXLNG
          STATUS = WCSMIX (WCS, LNGIDX, 2, LNGSPN, 1D0, 0, WORLD,
     :                     PHI, THETA, IMG, PIX2)
          IF (STATUS.NE.0) THEN
            CALL ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
            WRITE (*, '(A,I2)') '  C: WCSMIX ERROR', STATUS
          ELSE
            STATUS = WCSS2P (WCS, 1, 0, WORLD(1), PHI, THETA,
     :                       IMG(1), PIX3(1), STAT)
            IF (STATUS.NE.0) THEN
              CALL ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
              WRITE (*, '(A,I2)') '  C: WCSS2P ERROR', STATUS
            ELSE IF (ABS(PIX3(LNGIDX)-PIXLNG).GT.TOL .AND.
     :              (ABS(WORLD(LNGIDX)- LNG1).GT.TOL .OR.
     :               ABS(PIX2(LATIDX)-PIXLAT).GT.TOL)) THEN
              CALL ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
              WRITE (*, 50) WORLD(LNGIDX), WORLD(LATIDX), PHI,
     :                      THETA, PIX2(LNGIDX), PIX2(LATIDX)
 50           FORMAT ('  C:  LNG2  =',F20.15,'  (LAT2) =',F20.15,/,
     :                '       PHI  =',F20.15,'  THETA  =',F20.15,/,
     :                '       (I2) =',F20.15,'     J2  =',F20.15)
            END IF
          END IF

          PIX2(LATIDX) = PIXLAT
          STATUS = WCSMIX (WCS, LATIDX, 2, LNGSPN, 1D0, 0, WORLD,
     :                     PHI, THETA, IMG, PIX2)
          IF (STATUS.NE.0) THEN
            CALL ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
            WRITE (*, '(A,I2)') '  D: WCSMIX ERROR', STATUS
          ELSE
            STATUS = WCSS2P (WCS, 1, 0, WORLD(1), PHI, THETA, IMG(1),
     :                       PIX3(1), STAT)
            IF (STATUS.NE.0) THEN
              CALL ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
              WRITE (*, '(A,I2)') '  D: WCSS2P ERROR', STATUS
            ELSE IF (ABS(PIX3(LATIDX)-PIXLAT).GT.TOL .AND.
     :              (ABS(WORLD(LNGIDX)- LNG1).GT.TOL .OR.
     :               ABS(PIX2(LNGIDX)-PIXLNG).GT.TOL)) THEN
              CALL ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
              WRITE (*, 60) WORLD(LNGIDX), WORLD(LATIDX), PHI,
     :                      THETA, PIX2(LNGIDX), PIX2(LATIDX)
 60           FORMAT ('  D:  LNG2  =',F20.15,'  (LAT2) =',F20.15,/,
     :                '       PHI  =',F20.15,'  THETA  =',F20.15,/,
     :                '        I2  =',F20.15,'    (J2) =',F20.15)
            END IF
          END IF

 70     CONTINUE
 80   CONTINUE

      STATUS = WCSFREE (WCS)

      RETURN
      END


*-----------------------------------------------------------------------
      SUBROUTINE ID (WCS, DOID, LNG1, LAT1, PIXLNG, PIXLAT)
*-----------------------------------------------------------------------
      INTEGER   DOID, STATUS
      REAL      IPT(1), JPT(1)
      DOUBLE PRECISION EULER(5), LNG1, LAT1, PHI, PIXLAT, PIXLNG, THETA
      CHARACTER PCODE*4

*     On some systems, such as Sun Sparc, the structs MUST be aligned
*     on a double precision boundary.  As a dummy argument, WCS should
*     already be aligned.  The others are aligned here using
*     equivalences.  Failure to do this may result in mysterious "bus
*     errors".
      INCLUDE 'wcs.inc'
      INCLUDE 'cel.inc'
      INCLUDE 'prj.inc'
      INTEGER   CEL(CELLEN), PRJ(PRJLEN), WCS(WCSLEN)
      DOUBLE PRECISION DUMMY1, DUMMY2
      EQUIVALENCE (CEL,DUMMY1), (PRJ,DUMMY2)
*-----------------------------------------------------------------------
      IF (DOID.NE.0) THEN
*       Compute native coordinates.
        STATUS = WCSGTI (WCS, WCS_CEL, CEL(1))
        STATUS = CELGTD (CEL, CEL_EULER, EULER)
        CALL SPHS2X (EULER, 1, 1, 1, 1, LNG1, LAT1, PHI, THETA)

        STATUS = CELGTI (CEL, CEL_PRJ, PRJ)
        STATUS = PRJGTC (PRJ, PRJ_CODE, PCODE)
        WRITE (*, 10) PCODE, LNG1, LAT1, PHI, THETA, PIXLNG, PIXLAT
 10     FORMAT (/,A3,':  LNG1  =',F20.15,'   LAT1  =',F20.15,/,
     :            '       PHI  =',F20.15,'  THETA  =',F20.15,/,
     :            '        I1  =',F20.15,'     J1  =',F20.15)
        DOID = 0

        CALL PGSCI (9)
        IPT(1) = REAL(PIXLNG)
        JPT(1) = REAL(PIXLAT)
        CALL PGPT (1, IPT, JPT, 21)
        CALL PGSCI (2)
      END IF

      RETURN
      END


*-----------------------------------------------------------------------
      SUBROUTINE GRDPLT (WCS, IMIN, IMAX, JMIN, JMAX)
*-----------------------------------------------------------------------
*     Number of axes.
      INTEGER   N, NELEM
      PARAMETER (N = 4, NELEM = 9)

      LOGICAL   CUBIC
      INTEGER   CATEG, CI, ILAT, ILNG, J, K, LATIDX, LNGIDX, SPCIDX,
     :          STAT(0:360), STATUS
      REAL      IMAX, IMIN, JMAX, JMIN, IR(0:1023), JR(0:1023)
      DOUBLE PRECISION FREQ, IMG(NELEM,0:360), LAT, LNG, PHI(0:360),
     :          PIX(NELEM,0:360), REF(4), STEP, THETA(0:360), W(10),
     :          WORLD(NELEM,0:360)
      CHARACTER PCODE*4, TEXT*80

*     On some systems, such as Sun Sparc, the structs MUST be aligned
*     on a double precision boundary.  As a dummy argument, WCS should
*     already be aligned.  The others are aligned here using
*     equivalences.  Failure to do this may result in mysterious "bus
*     errors".
      INCLUDE 'wcs.inc'
      INCLUDE 'cel.inc'
      INCLUDE 'prj.inc'
      INCLUDE 'lin.inc'
      INTEGER   CEL(CELLEN), LIN(LINLEN), PRJ(PRJLEN), WCS(WCSLEN)
      INTEGER   NATIVE(WCSLEN)
      DOUBLE PRECISION DUMMY1, DUMMY2, DUMMY3, DUMMY4
      EQUIVALENCE (CEL,DUMMY1), (LIN,DUMMY2), (PRJ,DUMMY3),
     :          (NATIVE,DUMMY4)
*-----------------------------------------------------------------------
*     Initialize non-celestial world coordinates.
      STATUS = WCSGTI (WCS, WCS_LNG, LNGIDX)
      STATUS = WCSGTI (WCS, WCS_LAT, LATIDX)
      STATUS = WCSGTI (WCS, WCS_SPEC, SPCIDX)

      FREQ = 1.42040595D9 - 180D0 * 62500D0
      DO 10 J = 0, 360
        WORLD(1,J) = 0D0
        WORLD(2,J) = 0D0
        WORLD(3,J) = 0D0
        WORLD(4,J) = 0D0

        WORLD(SPCIDX,J) = 2.99792458D8 / FREQ
        FREQ = FREQ + 62500D0
 10   CONTINUE


*     Define PGPLOT viewport.
      CALL PGENV (IMIN, IMAX, JMIN, JMAX, 1, -2)

      STATUS = WCSGTI (WCS, WCS_CEL, CEL(1))
      STATUS = CELGTI (CEL, CEL_PRJ, PRJ)
      STATUS = PRJGTI (PRJ, PRJ_CATEGORY, CATEG)
      CUBIC = CATEG.EQ.7
      IF (CUBIC) THEN
*       Some sort of quad-cube projection.
        CALL PGSCI (8)

*       Draw the map boundary.
        DO 20 J = 0, 8
          IMG(1,J) = 0D0
          IMG(2,J) = 0D0
          IMG(3,J) = 0D0
          IMG(4,J) = 0D0
 20     CONTINUE

        STATUS = PRJGTD (PRJ, PRJ_W, W)
        IMG(LNGIDX,0) = -W(1)
        IMG(LATIDX,0) =  W(1)
        IMG(LNGIDX,1) = -W(1)
        IMG(LATIDX,1) =  W(1)*3D0
        IMG(LNGIDX,2) =  W(1)
        IMG(LATIDX,2) =  W(1)*3D0
        IMG(LNGIDX,3) =  W(1)
        IMG(LATIDX,3) = -W(1)*3D0
        IMG(LNGIDX,4) = -W(1)
        IMG(LATIDX,4) = -W(1)*3D0
        IMG(LNGIDX,5) = -W(1)
        IMG(LATIDX,5) =  W(1)
        IMG(LNGIDX,6) =  W(1)*7D0
        IMG(LATIDX,6) =  W(1)
        IMG(LNGIDX,7) =  W(1)*7D0
        IMG(LATIDX,7) = -W(1)
        IMG(LNGIDX,8) = -W(1)
        IMG(LATIDX,8) = -W(1)

        STATUS = WCSGTI (WCS, WCS_LIN, LIN(1))
        STATUS = LINX2P (LIN, 9, NELEM, IMG, PIX)

        DO 30 J = 0, 8
          IR(J) = REAL(PIX(LNGIDX,J))
          JR(J) = REAL(PIX(LATIDX,J))
 30     CONTINUE

        CALL PGLINE (9, IR, JR)
      END IF

      IF (CATEG.EQ.6) THEN
*       Polyconic.
        STEP = 10D0
      ELSE
        STEP = 15D0
      END IF


*     Draw the native coordinate graticule faintly in the background.
      STATUS = WCSPTI (NATIVE, WCS_FLAG, -1, 0, 0)
      STATUS = WCSCOPY (WCS, NATIVE)
      STATUS = WCSPTD (NATIVE, WCS_CRVAL,     0D0, LNGIDX, 0)
      STATUS = WCSPTD (NATIVE, WCS_CRVAL,    90D0, LATIDX, 0)
      STATUS = WCSPTD (NATIVE, WCS_LONPOLE, 180D0, 0, 0)
      STATUS = WCSSET (NATIVE)

      CALL PGSCI (8)

*     Draw native meridians of longitude.
      DO 60 ILNG = -180, 180, 15
        LNG = DBLE(ILNG)
        IF (ILNG.EQ.-180) LNG = -179.99D0
        IF (ILNG.EQ.+180) LNG = +179.99D0

        J = 0
        DO 40 ILAT = -90, 90
          WORLD(LNGIDX,J) = LNG
          WORLD(LATIDX,J) = DBLE(ILAT)
          J = J + 1
 40     CONTINUE

        STATUS = WCSS2P (NATIVE, 181, NELEM, WORLD(1,0),
     :                   PHI(0), THETA(0), IMG(1,0), PIX(1,0), STAT(0))
        IF (STATUS.NE.0) GO TO 60

        J = 0
        K = 0
        DO 50 ILAT = -90, 90
          IF (CUBIC .AND. K.GT.0) THEN
            IF (ABS(PIX(LNGIDX,J)-IR(K-1)).GT.2D0 .OR.
     :          ABS(PIX(LATIDX,J)-JR(K-1)).GT.5D0) THEN
              IF (K.GT.1) CALL PGLINE (K, IR, JR)
              K = 0
            END IF
          END IF

          IR(K) = REAL(PIX(LNGIDX,J))
          JR(K) = REAL(PIX(LATIDX,J))
          J = J + 1
          K = K + 1
 50     CONTINUE

        CALL PGLINE (K, IR, JR)
 60   CONTINUE

*     Draw native parallels of latitude.
      DO 90 ILAT = -90, 90, 15
        LAT = DBLE(ILAT)

        J = 0
        DO 70 ILNG = -180, 180
          LNG = DBLE(ILNG)
          IF (ILNG.EQ.-180) LNG = -179.99D0
          IF (ILNG.EQ.+180) LNG = +179.99D0

          WORLD(LNGIDX,J) = LNG
          WORLD(LATIDX,J) = LAT
          J = J + 1
 70     CONTINUE

        STATUS = WCSS2P (NATIVE, 361, NELEM, WORLD(1,0),
     :                   PHI(0), THETA(0), IMG(1,0), PIX(1,0), STAT(0))
        IF (STATUS.NE.0) GO TO 90

        J = 0
        K = 0
        DO 80 ILNG = -180, 180
          IF (CUBIC .AND. K.GT.0) THEN
            IF (ABS(PIX(LNGIDX,J)-IR(K-1)).GT.2D0 .OR.
     :          ABS(PIX(LATIDX,J)-JR(K-1)).GT.5D0) THEN
              IF (K.GT.1) CALL PGLINE (K, IR, JR)
              K = 0
            END IF
          END IF

          IR(K) = REAL(PIX(LNGIDX,J))
          JR(K) = REAL(PIX(LATIDX,J))
          J = J + 1
          K = K + 1
 80     CONTINUE

        CALL PGLINE (K, IR, JR)
 90   CONTINUE

      STATUS = WCSFREE (NATIVE)


*     Draw a colour-coded celestial coordinate graticule.
      CI = 1

*     Draw celestial meridians of longitude.
      DO 120 ILNG = -180, 180, 15
        LNG = DBLE(ILNG)

        CI = CI + 1
        IF (CI.GT.7) CI = 2
        IF (ILNG.NE.0) THEN
          CALL PGSCI (CI)
        ELSE
          CALL PGSCI (1)
        END IF

        J = 0
        DO 100 ILAT = -90, 90
          LAT = DBLE(ILAT)

          WORLD(LNGIDX,J) = LNG
          WORLD(LATIDX,J) = LAT
          J = J + 1
 100    CONTINUE

        STATUS = WCSS2P (WCS, 181, NELEM, WORLD(1,0), PHI(0), THETA(0),
     :                   IMG(1,0), PIX(1,0), STAT(0))
        IF (STATUS.NE.0) GO TO 120

        J = 0
        K = 0
        DO 110 ILAT = -90, 90
*         Test for discontinuities.
          IF (K.GT.0) THEN
            IF (ABS(PIX(LNGIDX,J)-IR(K-1)).GT.STEP .OR.
     :          ABS(PIX(LATIDX,J)-JR(K-1)).GT.STEP) THEN
              IF (K.GT.1) CALL PGLINE (K, IR, JR)
              K = 0
            END IF
          END IF

          IR(K) = REAL(PIX(LNGIDX,J))
          JR(K) = REAL(PIX(LATIDX,J))
          J = J + 1
          K = K + 1
 110    CONTINUE

        CALL PGLINE (K, IR, JR)
 120  CONTINUE

*     Draw celestial parallels of latitude.
      CI = 1
      DO 150 ILAT = -90, 90, 15
        LAT = DBLE(ILAT)

        CI = CI + 1
        IF (CI.GT.7) CI = 2
        IF (ILAT.NE.0) THEN
          CALL PGSCI (CI)
        ELSE
          CALL PGSCI (1)
        END IF

        J = 0
        DO 130 ILNG = -180, 180
          WORLD(LNGIDX,J) = DBLE(ILNG)
          WORLD(LATIDX,J) = LAT
          J = J + 1
 130    CONTINUE

        STATUS = WCSS2P (WCS, 361, NELEM, WORLD(1,0), PHI(0), THETA(0),
     :                   IMG(1,0), PIX(1,0), STAT(0))
        IF (STATUS.NE.0) GO TO 150

        J = 0
        K = 0
        DO 140 ILNG = -180, 180
*         Test for discontinuities.
          IF (K.GT.0) THEN
            IF (ABS(PIX(LNGIDX,J)-IR(K-1)).GT.STEP .OR.
     :          ABS(PIX(LATIDX,J)-JR(K-1)).GT.STEP) THEN
              IF (K.GT.1) CALL PGLINE (K, IR, JR)
              K = 0
            END IF
          END IF

          IR(K) = REAL(PIX(LNGIDX,J))
          JR(K) = REAL(PIX(LATIDX,J))
          J = J + 1
          K = K + 1
 140    CONTINUE

        CALL PGLINE (K, IR, JR)
 150  CONTINUE


*     Write a descriptive title.
      CALL PGSCI (1)
      STATUS = PRJGTC (PRJ, PRJ_CODE, PCODE)
      TEXT = PCODE // 'projection - 15 degree graticule'
      WRITE (*, '(//,A)') TEXT
      CALL PGTEXT (IMIN, JMIN-10.0, TEXT)

      STATUS = CELGTD (CEL, CEL_REF, REF)
      WRITE (TEXT, 160) REF(1), REF(2)
 160  FORMAT ('centered on celestial coordinates (',F6.2,',',F6.2,')')
      WRITE (*, '(A)') TEXT
      CALL PGTEXT (IMIN, JMIN-20.0, TEXT)

      WRITE (TEXT, 170) REF(3), REF(4)
 170  FORMAT ('with celestial pole at native coordinates (',F7.2,
     :   ',',F7.2,')')
      WRITE (*, '(A)') TEXT
      CALL PGTEXT (IMIN, JMIN-30.0, TEXT)

      CALL PGSCI (2)


      RETURN
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

      INTEGER   I, J, K, NAXIS, NPV, PVI(4), PVM(4), STATUS, WCS(*)
      DOUBLE PRECISION CDELT(N), CRPIX(N), CRVAL(N), LATPOLE, LONPOLE,
     :          PC(N,N), PV(4), RESTFRQ, RESTWAV
      CHARACTER CTYPE(N)*72

      INCLUDE 'wcs.inc'

      COMMON /HEADER/ NAXIS, NPV, CRPIX, PC, CDELT, CRVAL, LONPOLE,
     :                LATPOLE, RESTFRQ, RESTWAV, PVI, PVM, PV
      COMMON /HEADCH/ CTYPE
*-----------------------------------------------------------------------
      STATUS = WCSPTI (WCS, WCS_FLAG, -1, 0, 0)
      STATUS = WCSINI (NAXIS, WCS)

      DO 20 I = 1, NAXIS
        STATUS = WCSPTD (WCS, WCS_CRPIX, CRPIX(I), I, 0)

        DO 10 J = 1, NAXIS
          STATUS = WCSPTD (WCS, WCS_PC, PC(I,J), I, J)
 10     CONTINUE

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

*     Extract information from the FITS header.
      STATUS = WCSSET (WCS)
      IF (STATUS.NE.0) THEN
        WRITE (*, 40) STATUS
 40     FORMAT ('WCSSET ERROR',I3)
      END IF

      RETURN
      END
