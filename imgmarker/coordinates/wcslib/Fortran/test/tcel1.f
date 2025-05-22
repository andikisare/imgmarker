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
* $Id: tcel1.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TCEL1
*-----------------------------------------------------------------------
*
* tcel1 tests the spherical projection driver routines supplied with
* WCSLIB by drawing native and celestial coordinate graticules for
* Bonne's projection.
*
*-----------------------------------------------------------------------
      INTEGER   CI, CRVAL1, CRVAL2, ILAT, ILNG, J, K, LATPOL, LNGPOL,
     :          STAT(361), STATUS
      REAL      XR(512), YR(512)
      DOUBLE PRECISION LAT(181), LNG(361), PHI(361), REF(4), THETA(361),
     :          X(361), Y(361)
      CHARACTER TEXT*72

*     On some systems, such as Sun Sparc, the structs MUST be aligned
*     on a double precision boundary, done here using a equivalences.
*     Failure to do this may result in mysterious "bus errors".
      INCLUDE 'cel.inc'
      INCLUDE 'prj.inc'
      INTEGER   CEL(CELLEN)
      INTEGER   NTV(CELLEN)
      INTEGER   PRJ(PRJLEN)
      DOUBLE PRECISION DUMMY1, DUMMY2, DUMMY3
      EQUIVALENCE (CEL,DUMMY1), (NTV,DUMMY2), (PRJ,DUMMY3)
*-----------------------------------------------------------------------
      WRITE (*, 10)
 10   FORMAT ('Testing WCSLIB celestial coordinate transformation ',
     :        'routines (tcel1.f)',/,
     :        '---------------------------------------------------',
     :        '------------------')

*     Initialize.
      STATUS = CELINI (NTV)

*     Reference angles for the native graticule (in fact, the defaults).
      STATUS = CELPTD (NTV, CEL_REF,   0D0, 1)
      STATUS = CELPTD (NTV, CEL_REF,   0D0, 2)

*     Set up Bonne's projection with conformal latitude at +35.
      STATUS = CELGTI (NTV, CEL_PRJ, PRJ)
      STATUS = PRJPTC (PRJ, PRJ_CODE, 'BON', 0)
      STATUS = PRJPTD (PRJ, PRJ_PV, 35D0, 1)
      STATUS = CELPTI (NTV, CEL_PRJ, PRJ(1), 0)


*     Celestial graticule.
      STATUS = CELINI (CEL)
      STATUS = CELPTI (CEL, CEL_PRJ, PRJ, 0)


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

*     Define PGPLOT viewport.
      CALL PGENV (-180.0, 180.0, -90.0, 140.0, 1, -2)

*     Loop over CRVAL2, LONPOLE, and LATPOLE with CRVAL1 incrementing by
*     15 degrees each time (it has an uninteresting effect).
      CRVAL1 = -180
      DO 190 CRVAL2 = -90, 90, 30
        DO 180 LNGPOL = -180, 180, 30
          DO 170 LATPOL = -1, 1, 2
*           For the celestial graticule, set the celestial
*           coordinates of the reference point of the projection
*           (which for Bonne's projection is at the intersection of
*           the native equator and prime meridian), the native
*           longitude of the celestial pole, and extra information
*           needed to determine the celestial latitude of the native
*           pole.  These correspond to FITS keywords CRVAL1, CRVAL2,
*           LONPOLE, and LATPOLE.
            STATUS = CELPTI (CEL, CEL_FLAG, 0, 0)
            STATUS = CELPTD (CEL, CEL_REF, DBLE(CRVAL1), 1)
            STATUS = CELPTD (CEL, CEL_REF, DBLE(CRVAL2), 2)
            STATUS = CELPTD (CEL, CEL_REF, DBLE(LNGPOL), 3)
            STATUS = CELPTD (CEL, CEL_REF, DBLE(LATPOL), 4)

*           Skip invalid values of LONPOLE.
            STATUS = CELSET (CEL)
            IF (STATUS.NE.0) GO TO 170

*           Skip redundant values of LATPOLE.
            STATUS = CELGTD (CEL, CEL_REF, REF)
            IF (LATPOL.EQ.1 .AND. ABS(REF(4)).LT.0.1D0) GO TO 170

*           Buffer PGPLOT output.
            CALL PGBBUF ()
            CALL PGERAS ()

*           Write a descriptive title.
            TEXT = 'Bonne''s projection (BON) - 15 degree graticule'
            WRITE (*, '(/,A)') TEXT
            CALL PGTEXT (-180.0, -100.0, TEXT)

            WRITE (TEXT, 20) REF(1), REF(2)
 20         FORMAT ('centred on celestial coordinates (',F7.2,',',F6.2,
     :        ')')
            WRITE (*, '(A)') TEXT
            CALL PGTEXT (-180.0, -110.0, TEXT)

            WRITE (TEXT, 30) REF(3), REF(4)
 30         FORMAT ('with north celestial pole at native coordinates (',
     :        F7.2,',',F7.2,')')
            WRITE (*, '(A)') TEXT
            CALL PGTEXT (-180.0, -120.0, TEXT)


*           Draw the native graticule faintly in the background.
            CALL PGSCI (8)

*           Draw native meridians of longitude.
            J = 1
            DO 40 ILAT = -90, 90
              LAT(J) = DBLE(ILAT)
              J = J + 1
 40         CONTINUE

            DO 60 ILNG = -180, 180, 15
              LNG(1) = DBLE(ILNG)
              IF (ILNG.EQ.-180) LNG(1) = -179.99D0
              IF (ILNG.EQ.+180) LNG(1) = +179.99D0

*             Dash the longitude of the celestial pole.
              IF (MOD(ILNG-LNGPOL,360).EQ.0) THEN
                CALL PGSLS (2)
                CALL PGSLW (5)
              END IF

              STATUS = CELS2X (NTV, 1, 181, 1, 1, LNG, LAT, PHI, THETA,
     :                         X, Y, STAT)

              K = 0
              DO 50 J = 1, 181
                IF (STAT(J).NE.0) THEN
                  IF (K.GT.1) CALL PGLINE (K, XR, YR)
                  K = 0
                  GO TO 50
                END IF

                K = K + 1
                XR(K) = -REAL(X(J))
                YR(K) =  REAL(Y(J))
 50           CONTINUE

              CALL PGLINE (K, XR, YR)
              CALL PGSLS (1)
              CALL PGSLW (1)
 60         CONTINUE

*           Draw native parallels of latitude.
            LNG(1)   = -179.99D0
            LNG(361) = +179.99D0
            J = 2
            ILNG = -179
            DO 70 ILNG = -179, 180
              LNG(J) = DBLE(ILNG)
              J = J + 1
 70         CONTINUE

            DO 90 ILAT = -90, 90, 15
              LAT(1) = DBLE(ILAT)

              STATUS = CELS2X (NTV, 361, 1, 1, 1, LNG, LAT, PHI, THETA,
     :                         X, Y, STAT)

              K = 0
              DO 80 J = 1, 361
                IF (STAT(J).NE.0) THEN
                  IF (K.GT.1) CALL PGLINE (K, XR, YR)
                  K = 0
                  GO TO 80
                END IF

                K = K + 1
                XR(K) = -REAL(X(J))
                YR(K) =  REAL(Y(J))
 80           CONTINUE

              CALL PGLINE (K, XR, YR)
 90         CONTINUE


*           Draw a colour-coded celestial coordinate graticule.
            CI = 1

*           Draw celestial meridians of longitude.
            J = 1
            DO 100 ILAT = -90, 90
              LAT(J) = DBLE(ILAT)
              J = J + 1
 100         CONTINUE

            DO 120 ILNG = -180, 180, 15
              LNG(1) = DBLE(ILNG)

              CI = CI + 1
              IF (CI.GT.7) CI = 2
              IF (ILNG.EQ.0) THEN
                CALL PGSCI (1)
              ELSE
                CALL PGSCI (CI)
              END IF

*             Dash the reference longitude.
              IF (MOD(ILNG-CRVAL1,360).EQ.0) THEN
                CALL PGSLS (2)
                CALL PGSLW (5)
              END IF

              STATUS = CELS2X (CEL, 1, 181, 1, 1, LNG, LAT, PHI, THETA,
     :                         X, Y, STAT)

              K = 0
              DO 110 J = 1, 181
                IF (STAT(J).NE.0) THEN
                  IF (K.GT.1) CALL PGLINE (K, XR, YR)
                  K = 0
                  GO TO 110
                END IF

*               Test for discontinuities.
                IF (J.GT.1) THEN
                  IF (ABS(X(J) - X(J-1)).GT.4D0 .OR.
     :                ABS(Y(J) - Y(J-1)).GT.4D0) THEN
                    IF (K.GT.1) CALL PGLINE (K, XR, YR)
                    K = 0
                  END IF
                END IF

                K = K + 1
                XR(K) = -REAL(X(J))
                YR(K) =  REAL(Y(J))
 110          CONTINUE

              CALL PGLINE (K, XR, YR)
              CALL PGSLS (1)
              CALL PGSLW (1)
 120        CONTINUE

*           Draw celestial parallels of latitude.
            J = 1
            DO 130 ILNG = -180, 180
              LNG(J) = DBLE(ILNG)
              J = J + 1
 130        CONTINUE

            CI = 1
            DO 150 ILAT = -90, 90, 15
              LAT(1) = DBLE(ILAT)

              CI = CI + 1
              IF (CI.GT.7) CI = 2
              IF (ILAT.EQ.0) THEN
                CALL PGSCI (1)
              ELSE
                CALL PGSCI (CI)
              END IF

*             Dash the reference latitude.
              IF (ILAT.EQ.CRVAL2) THEN
                CALL PGSLS (2)
                CALL PGSLW (5)
              END IF

              STATUS = CELS2X (CEL, 361, 1, 1, 1, LNG, LAT, PHI, THETA,
     :                         X, Y, STAT)

              K = 0
              DO 140 J = 1, 361
                IF (STAT(J).NE.0) THEN
                  IF (K.GT.1) CALL PGLINE (K, XR, YR)
                  K = 0
                  GO TO 140
                END IF

*               Test for discontinuities.
                IF (J.GT.1) THEN
                  IF (ABS(X(J) - X(J-1)).GT.4D0 .OR.
     :                ABS(Y(J) - Y(J-1)).GT.4D0) THEN
                    IF (K.GT.1) CALL PGLINE (K, XR, YR)
                    K = 0
                  END IF
                END IF

                K = K + 1
                XR(K) = -REAL(X(J))
                YR(K) =  REAL(Y(J))
 140          CONTINUE

              CALL PGLINE (K, XR, YR)
              CALL PGSLS (1)
              CALL PGSLW (1)
 150        CONTINUE

*           Flush PGPLOT buffer.
            CALL PGEBUF ()
            WRITE (*, '(A,$)') ' Type <RETURN> for next page: '
            READ (*, *, END=160)

*           Cycle through celestial longitudes.
 160        CRVAL1 = CRVAL1 + 15
            IF (CRVAL1.GT.180) CRVAL1 = -180

*           Skip boring celestial latitudes.
            IF (CRVAL2.EQ.0) GO TO 190
 170      CONTINUE
 180    CONTINUE
 190  CONTINUE

      CALL PGASK (0)
      CALL PGEND


      END
