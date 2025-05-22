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
* $Id: tspc.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TSPC
*-----------------------------------------------------------------------
*
* TSPC tests the spectral transformation driver routines for closure.
*
*-----------------------------------------------------------------------
*     Maximum length of spectral axis - see CLOSURE.
      INTEGER   NSPEC
      PARAMETER (NSPEC = 8001)

      INTEGER   CLOSURE, NAXISJ, NFAIL
      DOUBLE PRECISION C, CDELTX, CRPIXJ, CRVALX, MARS(0:6), RESTFRQ,
     :          RESTWAV, X1, X2

      COMMON /SPECTRO/ MARS

      DATA C /2.99792458D8/

*     KPNO MARS spectrograph grism parameters.
      DATA MARS /4.5D5, 1D0, 27D0, 1.765D0, -1.077D6, 3D0, 5D0/
*-----------------------------------------------------------------------
      WRITE (*, 10)
 10   FORMAT ('Testing closure of WCSLIB spectral transformation ',
     :        'routines (tspc.f)',/,
     :        '--------------------------------------------------',
     :        '-----------------')

      NFAIL = 0

*     PGPLOT initialization.
      CALL PGBEG (0, '/xwindow', 1, 1)

      NAXISJ = NSPEC
      CRPIXJ = NAXISJ/2 + 1

      RESTFRQ = 1420.40595D6
      RESTWAV = C/RESTFRQ
      X1 = 1D9
      X2 = 2D9
      CDELTX = (X2 - X1)/(NAXISJ - 1)
      CRVALX = X1 + (CRPIXJ - 1.0)*CDELTX
      WRITE (*, 20) X1*1D-9, X2*1D-9, CDELTX*1D-3
 20   FORMAT (/,'Linear frequency axis, span:',F4.1,' to',F4.1,
     :        ' (GHz), step:',F8.3,' (kHz)',/,'---------------------',
     :        '-----------------------------------------------------')
      NFAIL = NFAIL + CLOSURE('WAVE-F2W', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VOPT-F2W', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('ZOPT-F2W', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('AWAV-F2A', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VELO-F2V', RESTFRQ, 0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('BETA-F2V', RESTFRQ, 0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)


      RESTWAV = 700D-9
      RESTFRQ = C/RESTWAV
      X1 = 300D-9
      X2 = 900D-9
      CDELTX = (X2 - X1)/(NAXISJ - 1)
      CRVALX = X1 + (CRPIXJ - 1D0)*CDELTX
      WRITE (*, 30) INT(X1*1D9), INT(X2*1D9), CDELTX*1D9
 30   FORMAT (/,'Linear vacuum wavelength axis, span:',I4,' to',I4,
     :        ' (nm), step:',F9.6,' (nm)',/,'----------------------',
     :        '----------------------------------------------------')
      NFAIL = NFAIL + CLOSURE('FREQ-W2F', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('AFRQ-W2F', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('ENER-W2F', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('WAVN-W2F', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VRAD-W2F', RESTFRQ, 0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('AWAV-W2A', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VELO-W2V', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('BETA-W2V', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)


      WRITE (*, 40) INT(X1*1D9), INT(X2*1D9), CDELTX*1D9
 40   FORMAT (/,'Linear air wavelength axis, span:',I4,' to',I4,
     :        ' (nm), step:',F9.6,' (nm)',/,'----------------------',
     :        '----------------------------------------------------')
      NFAIL = NFAIL + CLOSURE('FREQ-A2F', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('AFRQ-A2F', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('ENER-A2F', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('WAVN-A2F', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VRAD-A2F', RESTFRQ, 0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('WAVE-A2W', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VOPT-A2W', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('ZOPT-A2W', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VELO-A2V', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('BETA-A2V', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)


      RESTFRQ = 1420.40595D6
      RESTWAV = C/RESTFRQ
      X1 = -0.96D0*C
      X2 =  0.96D0*C
      CDELTX = (X2 - X1)/(NAXISJ - 1)
      CRVALX = X1 + (CRPIXJ - 1D0)*CDELTX
      WRITE (*, 50) INT(X1), INT(X2), INT(CDELTX)
 50   FORMAT (/,'Linear velocity axis, span:',I11,' to',I10,
     :        ' m/s, step:',I6,' (m/s)',/,'-----------------------',
     :        '---------------------------------------------------')
      NFAIL = NFAIL + CLOSURE('FREQ-V2F', RESTFRQ, 0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('AFRQ-V2F', RESTFRQ, 0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('ENER-V2F', RESTFRQ, 0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('WAVN-V2F', RESTFRQ, 0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VRAD-V2F', RESTFRQ, 0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('WAVE-V2W', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VOPT-V2W', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('ZOPT-V2W', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('AWAV-V2A', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)


      RESTWAV = 650D-9
      RESTFRQ = C/RESTWAV
      X1 =  300D-9
      X2 = 1000D-9
      CDELTX = (X2 - X1)/(NAXISJ - 1)
      CRVALX = X1 + (CRPIXJ - 1D0)*CDELTX
      WRITE (*, 60) INT(X1*1D9), INT(X2*1D9), CDELTX*1D9
 60   FORMAT (/,'Vacuum wavelength grism axis, span:',I4,' to',I5,
     :        ' (nm), step:',F9.6,' (nm)',/,'----------------------',
     :        '----------------------------------------------------')
      NFAIL = NFAIL + CLOSURE('FREQ-GRI', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('AFRQ-GRI', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('ENER-GRI', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('WAVN-GRI', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VRAD-GRI', RESTFRQ, 0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('WAVE-GRI', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VOPT-GRI', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('ZOPT-GRI', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('AWAV-GRI', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VELO-GRI', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('BETA-GRI', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)


*     Reproduce Fig. 5 of Paper III.
      NAXISJ = 1700
      CRPIXJ = 719.8D0
      CRVALX = 7245.2D-10
      CDELTX = 2.956D-10
      RESTWAV = 8500D-10
      RESTFRQ = C/RESTWAV
      X1 = CRVALX + (1 - CRPIXJ)*CDELTX
      X2 = CRVALX + (NAXISJ - CRPIXJ)*CDELTX
      MARS(5) = 0D0
      MARS(6) = 0D0
      WRITE (*, 70) INT(X1*1D9), INT(X2*1D9), CDELTX*1D9
 70   FORMAT (/,'Air wavelength grism axis, span:',I4,' to',I5,
     :        ' (nm), step:',F9.6,' (nm)',/,'----------------------',
     :        '----------------------------------------------------')
      NFAIL = NFAIL + CLOSURE('AWAV-GRA', 0D0,     0D0, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)
      NFAIL = NFAIL + CLOSURE('VELO-GRA', 0D0, RESTWAV, NAXISJ, CRPIXJ,
     :                        CDELTX, CRVALX)

      CALL PGASK(0)
      CALL PGEND()


      IF (NFAIL.NE.0) THEN
        WRITE (*, 80) NFAIL
 80     FORMAT (/,'FAIL:',I5,' closure residuals exceed reporting ',
     :    'tolerance.')
      ELSE
        WRITE (*, 90)
 90     FORMAT (/,'PASS: All closure residuals are within reporting ',
     :    'tolerance.')
      END IF

      END

*=======================================================================

      INTEGER FUNCTION CLOSURE (CTYPES, RESTFRQ, RESTWAV, NAXISJ,
     :  CRPIXJ, CDELTX, CRVALX)

      INTEGER   NSPEC
      PARAMETER (NSPEC = 8001)

      INTEGER   J, NAXISJ, NFAIL, RESTREQ, STAT1(NSPEC), STAT2(NSPEC),
     :          STATUS
      REAL      TMP, X(NSPEC), XMIN, XMAX, Y(NSPEC), YMAX, YMIN
      DOUBLE PRECISION CDELTS, CDELTX, CLOS(NSPEC), CRPIXJ, CRVALS,
     :          CRVALX, DSDX, MARS(0:6), RESID, RESIDMAX, RESTFRQ,
     :          RESTWAV, SPEC1(NSPEC), SPEC2(NSPEC), TOL
      CHARACTER CTYPES*8, PTYPE, SCODE*3, SNAME*21, STYPE*8, TITLE*80,
     :          UNITS*7, XTYPE, YLAB*80

*     On some systems, such as Sun Sparc, the struct MUST be aligned
*     on a double precision boundary, done here using an equivalence.
*     Failure to do this may result in mysterious "bus errors".
      INCLUDE 'spx.inc'
      INCLUDE 'spc.inc'
      INTEGER   SPC(SPCLEN)
      DOUBLE PRECISION DUMMY
      EQUIVALENCE (SPC,DUMMY)

      COMMON /SPECTRO/ MARS

      DATA TOL /1D-11/
*-----------------------------------------------------------------------
      CLOSURE = 0

*     Get keyvalues for the required spectral axis type.
      STATUS = SPCXPS (CTYPES, CRVALX, RESTFRQ, RESTWAV, PTYPE, XTYPE,
     :                 RESTREQ, CRVALS, DSDX)
      IF (STATUS.NE.0) THEN
        WRITE (*, 10) STATUS, CTYPES
 10     FORMAT ('ERROR',I2,' from SPCXPS for',A,'.')
        RETURN
      END IF
      CDELTS = CDELTX * DSDX

      STATUS = SPCINI(SPC)

      IF (CTYPES(6:6).EQ.'G') THEN
*       KPNO MARS spectrograph grism parameters.
        STATUS = SPCPTD (SPC, SPC_PV, MARS(0), 0)
        STATUS = SPCPTD (SPC, SPC_PV, MARS(1), 1)
        STATUS = SPCPTD (SPC, SPC_PV, MARS(2), 2)
        STATUS = SPCPTD (SPC, SPC_PV, MARS(3), 3)
        STATUS = SPCPTD (SPC, SPC_PV, MARS(4), 4)
        STATUS = SPCPTD (SPC, SPC_PV, MARS(5), 5)
        STATUS = SPCPTD (SPC, SPC_PV, MARS(6), 6)
      END IF

*     Construct the axis.
      DO 20 J = 1, NAXISJ
        SPEC1(J) = (J - CRPIXJ)*CDELTS
 20   CONTINUE

      WRITE (*, 30) CTYPES, CRVALS+SPEC1(1), CRVALS+SPEC1(NAXISJ),
     :              CDELTS
 30   FORMAT (A,' (CRVALk+w) range: ',1PE13.6,' to ',1PE13.6,', step: ',
     :        1PE13.6)


*     Initialize.
      STATUS = SPCPTI (SPC, SPC_FLAG, 0, 0)
      STATUS = SPCPTD (SPC, SPC_CRVAL, CRVALS, 0)
      STATUS = SPCPTD (SPC, SPC_RESTFRQ, RESTFRQ, 0)
      STATUS = SPCPTD (SPC, SPC_RESTWAV, RESTWAV, 0)
      STATUS = SPCPTC (SPC, SPC_TYPE, CTYPES, 0)
      STATUS = SPCPTC (SPC, SPC_CODE, CTYPES(6:8), 0)

*     Convert the first to the second.
      STATUS = SPCX2S(SPC, NAXISJ, 1, 1, SPEC1, SPEC2, STAT1)
      IF (STATUS.NE.0) THEN
        WRITE (*, 40) STATUS
 40     FORMAT ('SPCX2S ERROR',I2,'.')
        RETURN
      END IF

*     Convert the second back to the first.
      STATUS = SPCS2X(SPC, NAXISJ, 1, 1, SPEC2, CLOS, STAT2)
      IF (STATUS.NE.0) THEN
        WRITE (*, 50) STATUS
 50     FORMAT ('SPCS2X ERROR',I2,'.')
        RETURN
      END IF


*     Test closure.
      NFAIL = 0
      RESIDMAX = 0D0
      STATUS = SPCGTC (SPC, SPC_TYPE, STYPE)
      DO 90 J = 1, NAXISJ
        IF (STAT1(J).NE.0) THEN
          WRITE (*, 60) CTYPES, SPEC1(J), STYPE, STAT1(J)
 60       FORMAT (A,': w =',1PE20.12,' -> ',A4,' = ???, stat = ',I2)
          GO TO 90
        END IF

        IF (STAT2(J).NE.0) THEN
          WRITE (*, 70) CTYPES, SPEC1(J), STYPE, SPEC2(J), STAT2(J)
 70       FORMAT (A,': w =',1PE20.12,' -> ',A4,' =',1PE20.12,
     :            ' -> w = ???, stat = ',I2)
          GO TO 90
        END IF

        RESID = ABS((CLOS(J) - SPEC1(J))/CDELTS)
        IF (RESID.GT.RESIDMAX) RESIDMAX = RESID

        IF (RESID.GT.TOL) THEN
          NFAIL = NFAIL + 1
          WRITE (*, 80) CTYPES, SPEC1(J), STYPE, SPEC2(J), CLOS(J),
     :                  RESID
 80       FORMAT (A,': w =',1PE20.12,' -> ',A4,' =',1PE20.12,' ->',/,
     :           '          w =',1PE20.12,',  resid =',1PE8.1)
        END IF
 90   CONTINUE

      WRITE (*, 100) CTYPES, RESIDMAX
 100  FORMAT (A,': Maximum closure residual =',1PE8.1,' pixel')


*     Draw graph.
      CALL PGBBUF()
      CALL PGERAS()

      XMIN = REAL(CRVALS + SPEC1(1))
      XMAX = REAL(CRVALS + SPEC1(NAXISJ))
      YMIN = REAL(SPEC2(1)) - XMIN
      YMAX = YMIN
      DO 110 J = 1, NAXISJ
        X(J) = REAL(J)
        Y(J) = REAL(SPEC2(J) - (CRVALS + SPEC1(J)))
        IF (Y(J).GT.YMAX) YMAX = Y(J)
        IF (Y(J).LT.YMIN) YMIN = Y(J)
 110  CONTINUE

      J = INT(CRPIXJ+1)
      IF (Y(J).LT.0D0) then
        TMP  = YMIN
        YMIN = YMAX
        YMAX = TMP
      END IF

      CALL PGASK(0)
      CALL PGENV(1.0, REAL(NAXISJ), YMIN, YMAX, 0, -1)

      CALL PGSCI(1)
      CALL PGBOX('ABNTS', 0.0, 0, 'BNTS', 0.0, 0)

      STATUS = SPCTYP (CTYPES, STYPE, SCODE, SNAME, UNITS, PTYPE, XTYPE,
     :                 RESTREQ)
      DO 120 J = 21, 1, -1
        IF (SNAME(J:J).NE.' ') GO TO 130
 120  CONTINUE
 130  YLAB  = SNAME(:J) // ' - correction ' // UNITS
      TITLE = CTYPES // ':  CRVALk + w ' // UNITS
      CALL PGLAB('Pixel coordinate', YLAB, TITLE)

      CALL PGAXIS('N', 0.0, YMAX, REAL(NAXISJ), YMAX, XMIN, XMAX, 0.0,
     :            0, -0.5, 0.0, 0.5, -0.5, 0.0)

      CALL PGAXIS('N', REAL(NAXISJ), ymin, REAL(NAXISJ), YMAX,
     :            REAL(YMIN/CDELTS), REAL(YMAX/CDELTS), 0.0, 0, 0.5,
     :            0.0, 0.5, 0.1, 0.0)
      CALL PGMTXT('R', 2.2, 0.5, 0.5, 'Pixel offset')

      CALL PGLINE(NAXISJ, X, Y)
      CALL PGSCI(7)
      CALL PGPT1(REAL(CRPIXJ), 0.0, 24)
      CALL PGEBUF()

      CALL WCSLEEP (200)
      WRITE (*, '(A,$)') 'Type <RETURN> for next page: '
      READ (*, *, END=140)
 140  WRITE (*, *)

      CLOSURE = NFAIL

      END
