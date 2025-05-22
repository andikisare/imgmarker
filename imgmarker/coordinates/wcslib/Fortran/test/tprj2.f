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
* $Id: tprj2.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TPRJ2
*-----------------------------------------------------------------------
*
* TPRJ2 tests projection routines by plotting test graticules using
* PGPLOT.
*
*-----------------------------------------------------------------------
      INTEGER   J
      DOUBLE PRECISION PV(0:29)

      DOUBLE PRECISION PI
      PARAMETER (PI = 3.141592653589793238462643D0)
*-----------------------------------------------------------------------
      WRITE (*, 10)
 10   FORMAT (
     :  'Testing WCSLIB spherical projection routines (tprj2.f)',/,
     :  '------------------------------------------------------')

      DO 20 J = 0, 29
        PV(J) = 0D0
 20   CONTINUE

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

 30   FORMAT(/,A,' projection')
 40   FORMAT(/,A,' projection',/,'Parameters:',5F12.5,/,5F12.5)

*     AZP: zenithal/azimuthal perspective.
      PV(1) =  2D0
      PV(2) = 30D0
      WRITE (*, 40) 'Zenithal/azimuthal perspective', (PV(J), J=1,2)
      CALL PRJPLT ('AZP', 90, -90, PV)

*     SZP: zenithal/azimuthal perspective.
      PV(1) =   2D0
      PV(2) = 210D0
      PV(3) =  60D0
      WRITE (*, 40) 'Slant zenithal perspective', (PV(J), J=1,3)
      CALL PRJPLT ('SZP', 90, -90, PV)

*     TAN: gnomonic.
      WRITE (*, 30) 'Gnomonic'
      CALL PRJPLT ('TAN', 90,   5, PV)

*     STG: stereographic.
      WRITE (*, 30) 'Stereographic'
      CALL PRJPLT ('STG', 90, -85, PV)

*     SIN: orthographic.
      PV(1) = -0.3D0
      PV(2) =  0.5D0
      WRITE (*, 40) 'Orthographic/synthesis', (PV(J), J=1,2)
      CALL PRJPLT ('SIN', 90, -90, PV)

*     ARC: zenithal/azimuthal equidistant.
      WRITE (*, 30) 'Zenithal/azimuthal equidistant'
      CALL PRJPLT ('ARC', 90, -90, PV)

*     ZPN: zenithal/azimuthal polynomial.
      PV(0) =  0.05000D0
      PV(1) =  0.95000D0
      PV(2) = -0.02500D0
      PV(3) = -0.15833D0
      PV(4) =  0.00208D0
      PV(5) =  0.00792D0
      PV(6) = -0.00007D0
      PV(7) = -0.00019D0
      PV(8) =  0.00000D0
      PV(9) =  0.00000D0
      WRITE (*, 40) 'Zenithal/azimuthal polynomial', (PV(J), J=0,9)
      CALL PRJPLT ('ZPN', 90,  10, PV)

*     ZEA: zenithal/azimuthal equal area.
      WRITE (*, 30) 'Zenithal/azimuthal equal area'
      CALL PRJPLT ('ZEA', 90, -90, PV)

*     AIR: Airy's zenithal projection.
      PV(1) = 45D0
      WRITE (*, 40) 'Airy''s zenithal', PV(1)
      CALL PRJPLT ('AIR', 90, -85, PV)

*     CYP: cylindrical perspective.
      PV(1) = 3.0D0
      PV(2) = 0.8D0
      WRITE (*, 40) 'Cylindrical perspective', (PV(J), J=1,2)
      CALL PRJPLT ('CYP', 90, -90, PV)

*     CEA: cylindrical equal area.
      PV(1) = 0.75D0
      WRITE (*, 40) 'Cylindrical equal area', PV(1)
      CALL PRJPLT ('CEA', 90, -90, PV)

*     CAR: plate carree.
      WRITE (*, 30) 'Plate carree'
      CALL PRJPLT ('CAR', 90, -90, PV)

*     MER: Mercator's.
      WRITE (*, 30) 'Mercator''s'
      CALL PRJPLT ('MER', 85, -85, PV)

*     SFL: Sanson-Flamsteed.
      WRITE (*, 30) 'Sanson-Flamsteed (global sinusoid)'
      CALL PRJPLT ('SFL', 90, -90, PV)

*     PAR: parabolic.
      WRITE (*, 30) 'Parabolic'
      CALL PRJPLT ('PAR', 90, -90, PV)

*     MOL: Mollweide's projection.
      WRITE (*, 30) 'Mollweide''s'
      CALL PRJPLT ('MOL', 90, -90, PV)

*     AIT: Hammer-Aitoff.
      WRITE (*, 30) 'Hammer-Aitoff'
      CALL PRJPLT ('AIT', 90, -90, PV)

*     COP: conic perspective.
      PV(1) =  60D0
      PV(2) =  15D0
      WRITE (*, 40) 'Conic perspective', (PV(J), J=1,2)
      CALL PRJPLT ('COP', 90, -25, PV)

*     COE: conic equal area.
      PV(1) =  60D0
      PV(2) = -15D0
      WRITE (*, 40) 'Conic equal area', (PV(J), J=1,2)
      CALL PRJPLT ('COE', 90, -90, PV)

*     COD: conic equidistant.
      PV(1) = -60D0
      PV(2) =  15D0
      WRITE (*, 40) 'Conic equidistant', (PV(J), J=1,2)
      CALL PRJPLT ('COD', 90, -90, PV)

*     COO: conic orthomorphic.
      PV(1) = -60D0
      PV(2) = -15D0
      WRITE (*, 40) 'Conic orthomorphic', (PV(J), J=1,2)
      CALL PRJPLT ('COO', 85, -90, PV)

*     BON: Bonne's projection.
      PV(1) = 30D0
      WRITE (*, 40) 'Bonne''s', PV(1)
      CALL PRJPLT ('BON', 90, -90, PV)

*     PCO: polyconic.
      WRITE (*, 30) 'Polyconic'
      CALL PRJPLT ('PCO', 90, -90, PV)

*     TSC: tangential spherical cube.
      WRITE (*, 30) 'Tangential spherical cube'
      CALL PRJPLT ('TSC', 90, -90, PV)

*     CSC: COBE quadrilateralized spherical cube.
      WRITE (*, 30) 'COBE quadrilateralized spherical cube'
      CALL PRJPLT ('CSC', 90, -90, PV)

*     QSC: quadrilateralized spherical cube.
      WRITE (*, 30) 'Quadrilateralized spherical cube'
      CALL PRJPLT ('QSC', 90, -90, PV)

*     HPX: HEALPix projection.
      PV(1) = 4D0
      PV(2) = 3D0
      WRITE (*, 40) 'HEALPix', (PV(J), J=1,2)
      CALL PRJPLT ('HPX', 90, -90, PV)

*     XPH: HEALPix polar, aka "butterfly" projection.
      WRITE (*, 40) 'Butterfly', (PV(J), J=1,2)
      CALL PRJPLT ('XPH', 90, -90, PV)

      CALL PGASK (0)
      CALL PGEND

      END


      SUBROUTINE PRJPLT (PCODE, NORTH, SOUTH, PV)
*-----------------------------------------------------------------------
*   PRJPLT draws a 15 degree coordinate graticule.
*
*   Given:
*      PCODE    C*3      Projection code.
*      NORTH    I        Northern cutoff latitude, degrees.
*      SOUTH    I        Southern cutoff latitude, degrees.
*      PV       D(0:29)  Projection parameters.
*-----------------------------------------------------------------------
      LOGICAL   CUBIC, HEALPX, INTRRP
      INTEGER   CI, H, ILAT, ILNG, J, K, LEN, NORTH, SOUTH, STAT(361),
     :          STATUS
      REAL      HX, HY, SX, SY, XR(512), XR0, YR(512), YR0
      DOUBLE PRECISION LAT(361), LNG(361), PV(0:29), X(361), X0, Y(361),
     :          Y0
      CHARACTER PCODE*3

*     On some systems, such as Sun Sparc, the struct MUST be aligned
*     on a double precision boundary, done here using an equivalence.
*     Failure to do this may result in mysterious "bus errors".
      INCLUDE 'prj.inc'
      INTEGER   PRJ(PRJLEN)
      DOUBLE PRECISION DUMMY
      EQUIVALENCE (PRJ,DUMMY)
*-----------------------------------------------------------------------
      STATUS = PRJINI(PRJ)

      DO 10 J = 0, 29
        STATUS = PRJPTD (PRJ, PRJ_PV, PV(J), J)
 10   CONTINUE

      STATUS = PRJPTC (PRJ, PRJ_CODE, PCODE, 0)

      WRITE (*, 20) PCODE, NORTH, SOUTH
 20   FORMAT ('Plotting ',A3,'; latitudes',I3,' to',I4,'.')

      CALL PGASK (0)

      STATUS = PRJSET(PRJ)
      STATUS = PRJGTI (PRJ, PRJ_CATEGORY, J)
      CUBIC  = J.EQ.PRJ_QUADCUBE
      HEALPX = J.EQ.PRJ_HEALPIX
      IF (CUBIC) THEN
*       Draw the perimeter of the quadcube projection.
        CALL PGENV (-335.0, 65.0, -200.0, 200.0, 1, -2)
        CALL PGSCI (2)
        CALL PGTEXT (-340.0, -220.0, PCODE // ' - 15 degree graticule')

        CALL PGSCI (8)

        STATUS = PRJGTD (PRJ, PRJ_X0, X0)
        STATUS = PRJGTD (PRJ, PRJ_Y0, Y0)

        XR0 = REAL(X0)
        YR0 = REAL(Y0)

        XR(1) =      45.0 + XR0
        YR(1) =      45.0 - YR0
        XR(2) =      45.0 + XR0
        YR(2) =  3.0*45.0 - YR0
        XR(3) =     -45.0 + XR0
        YR(3) =  3.0*45.0 - YR0
        XR(4) =     -45.0 + XR0
        YR(4) = -3.0*45.0 - YR0
        XR(5) =      45.0 + XR0
        YR(5) = -3.0*45.0 - YR0
        XR(6) =      45.0 + XR0
        YR(6) =      45.0 - YR0
        XR(7) = -7.0*45.0 + XR0
        YR(7) =      45.0 - YR0
        XR(8) = -7.0*45.0 + XR0
        YR(8) =     -45.0 - YR0
        XR(9) =      45.0 + XR0
        YR(9) =     -45.0 - YR0
        CALL PGLINE (9, XR, YR)

      ELSE
        CALL PGENV (-200.0, 200.0, -200.0, 200.0, 1, -2)
        CALL PGSCI (2)
        CALL PGTEXT (-240.0, -220.0, PCODE//' - 15 degree graticule')

        IF (HEALPX) THEN
          IF (PCODE.EQ.'HPX') THEN
*           Draw the perimeter of the HEALPix projection.
            CALL PGSCI (8)

            H = NINT(PV(1))
            SX = 180.0 / H
            SY = SX * NINT(PV(2) + 1D0) / 2.0

            STATUS = PRJGTD (PRJ, PRJ_X0, X0)
            STATUS = PRJGTD (PRJ, PRJ_Y0, Y0)

            XR0 = REAL(X0)
            YR0 = REAL(Y0)

            HX = 180.0 + XR0
            HY = SY - SX - YR0
            CALL PGMOVE (HX, HY)

            DO 30 J = 1, H
              HX = HX - SX
              HY = HY + SX
              CALL PGDRAW (HX, HY)

              HX = HX - SX
              HY = HY - SX
              CALL PGDRAW (HX, HY)
 30         CONTINUE

            HX = 180.0 + XR0
            HY = -SY + SX - YR0

            IF (MOD(INT(PV(2)),2).EQ.1) THEN
              K = 1
            ELSE
              K = -1
              HY = HY - SX
            END IF

            CALL PGMOVE (HX, HY)

            DO 40 J = 1, H
              HX = HX - SX
              HY = HY - K*SX
              CALL PGDRAW (HX, HY)

              HX = HX - SX
              HY = HY + K*SX
              CALL PGDRAW (HX, HY)
 40         CONTINUE

          ELSE IF (PCODE.EQ.'XPH') THEN
            DO 70 ILNG = -90, 180, 90
              LNG(1) = DBLE(ILNG) - 0.0001

              J = 1
              DO 50 ILAT = 90, -90, -1
                LAT(J) = DBLE(ILAT)
                J = J + 1
 50           CONTINUE

              STATUS = PRJS2X(PRJ, 1, 181, 1, 1, LNG, LAT, X, Y, STAT)

              DO 60 J = 1, 181
                XR(J) = -REAL(X(J))
                YR(J) =  REAL(Y(J))
 60           CONTINUE

              CALL PGLINE(181, XR, YR)
 70         CONTINUE
          END IF

        END IF
      END IF


      CI = 1
      DO 100 ILNG = -180, 180, 15
        CI = CI + 1
        IF (CI.GT.7) CI = 2

        LNG(1) = DBLE(ILNG)

        IF (ILNG.EQ.0) THEN
          CALL PGSCI (1)
        ELSE
          CALL PGSCI (CI)
        END IF

        J = 1
        DO 80 ILAT = NORTH, SOUTH, -1
          LAT(J) = DBLE(ILAT)
          J = J + 1
 80     CONTINUE

        LEN  = NORTH - SOUTH + 1
        STATUS = PRJS2X (PRJ, 1, LEN, 1, 1, LNG, LAT, X, Y, STAT)

        K = 0
        DO 90 J = 1, LEN
          IF (STAT(J).NE.0) THEN
            IF (K.GT.1) CALL PGLINE (K, XR, YR)
            K = 0
            GO TO 90
          END IF

          IF (CUBIC .AND. J.GT.1) THEN
            IF (ABS(X(J) - X(J-1)).GT.2D0 .OR.
     :          ABS(Y(J) - Y(J-1)).GT.5D0) THEN
              IF (K.GT.1) CALL PGLINE (K, XR, YR)
              K = 0
            END IF
          ELSE IF (HEALPX .AND. ILNG.EQ.180) THEN
            IF (X(J).GT.180D0) GO TO 90
          END IF

          K = K + 1
          XR(K) = -REAL(X(J))
          YR(K) =  REAL(Y(J))
 90     CONTINUE

        CALL PGLINE (K, XR, YR)
 100  CONTINUE

      CI = 1
      INTRRP = CUBIC .OR. HEALPX
      DO 130 ILAT = -90, 90, 15
        CI = CI + 1
        IF (CI.GT.7) CI = 2

        IF (ILAT.GT.NORTH) GO TO 130
        IF (ILAT.LT.SOUTH) GO TO 130

        LAT(1) = DBLE(ILAT)

        IF (ILAT.EQ.0) THEN
          CALL PGSCI (1)
        ELSE
          CALL PGSCI (CI)
        END IF

        ILNG = -180
        DO 110 J = 1, 361
          LNG(J) = DBLE(ILNG)
          ILNG = ILNG + 1
 110    CONTINUE

        STATUS = PRJS2X (PRJ, 361, 1, 1, 1, LNG, LAT, X, Y, STAT)

        K = 0
        DO 120 J = 1, 361
          IF (STAT(J).NE.0) THEN
            IF (K.GT.1) CALL PGLINE (K, XR, YR)
            K = 0
            GO TO 120
          END IF

          IF (INTRRP .AND. J.GT.1) THEN
            IF (ABS(X(J) - X(J-1)).GT.2D0 .OR.
     :          ABS(Y(J) - Y(J-1)).GT.5D0) THEN
              IF (K.GT.1) CALL PGLINE (K, XR, YR)
              K = 0
            END IF
          END IF

          K = K + 1
          XR(K) = -REAL(X(J))
          YR(K) =  REAL(Y(J))
 120    CONTINUE

        CALL PGLINE (K, XR, YR)
 130  CONTINUE

      CALL PGSCI(1)
      XR(1) = 0.0
      YR(1) = 0.0
      CALL PGPT (1, XR, YR, 21)

      CALL PGASK (1)
      CALL WCSLEEP (250)
      CALL PGPAGE()


      RETURN
      END
