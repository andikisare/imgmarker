*=======================================================================
*
* PGSBOX 8.4 - draw curvilinear coordinate axes for PGPLOT.
* Copyright (C) 1997-2024, Mark Calabretta
*
* This file is part of PGSBOX.
*
* PGSBOX is free software: you can redistribute it and/or modify it
* under the terms of the GNU Lesser General Public License as published
* by the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* PGSBOX is distributed in the hope that it will be useful, but WITHOUT
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
* FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
* License for more details.
*
* You should have received a copy of the GNU Lesser General Public
* License along with PGSBOX.  If not, see http://www.gnu.org/licenses.
*
* Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
* http://www.atnf.csiro.au/people/Mark.Calabretta
* $Id: pgtest.f,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
*=======================================================================
      PROGRAM PGTEST
*=======================================================================
      LOGICAL   LARGE
      INTEGER   C0(7), CI(7), GCODE(2), IC, IERR, J, NAXIS(2),
     :          NLIPRM(2), STATUS
      REAL      BLC(2), SCL, TRC(2)
      DOUBLE PRECISION CACHE(4,0:256), DEC0, GRID1(0:8), GRID2(0:8),
     :          NLDPRM(8), ROTN, TIKLEN
      CHARACTER CTYPE(2)*72, DEVTYP*16, ESCAPE*1, FCODE(2)*4,
     :          IDENTS(3)*80, NLCPRM(1)*1, OPT(2)*1

      DOUBLE PRECISION D2R, PI
      PARAMETER (PI = 3.141592653589793238462643D0)
      PARAMETER (D2R = PI/180D0)

      INCLUDE 'wcs.inc'
      INTEGER   WCS(WCSLEN)

      EXTERNAL LNGVEL
      EXTERNAL FSCAN
      EXTERNAL PGCRFN
      EXTERNAL PGWCSL
*-----------------------------------------------------------------------
*     Setup.
      NAXIS(1) = 512
      NAXIS(2) = 512

      BLC(1) = 0.5
      BLC(2) = 0.5
      TRC(1) = NAXIS(1) + 0.5
      TRC(2) = NAXIS(2) + 0.5

      ESCAPE = CHAR(92)

*     CALL PGBEG (0, '?', 1, 1)
      call pgbeg (0, '/xw', 1, 1)

      CALL PGQINF ('TYPE', DEVTYP, J)
      IF (DEVTYP.EQ.'PS'  .OR.
     :    DEVTYP.EQ.'VPS' .OR.
     :    DEVTYP.EQ.'CPS' .OR.
     :    DEVTYP.EQ.'VCPS') THEN
*       Switch black and white.
        CALL PGSCR (0, 1.0, 1.0, 1.0)
        CALL PGSCR (1, 0.0, 0.0, 0.0)
      END IF

      LARGE = DEVTYP.EQ.'XWINDOW'
      IF (LARGE) THEN
        SCL = 1.0
        CALL PGVSTD ()
      ELSE
        SCL = 0.7
        CALL PGVSIZ (1.0, 3.0, 1.0, 3.0)
      END IF

*     Yellow.
      CALL PGSCR (2, 1.0, 1.0, 0.0)
*     White.
      CALL PGSCR (3, 1.0, 1.0, 1.0)
*     Pale blue.
      CALL PGSCR (4, 0.5, 0.5, 0.8)
*     Pale red.
      CALL PGSCR (5, 0.8, 0.5, 0.5)
*     Grey.
      CALL PGSCR (6, 0.7, 0.7, 0.7)
*     Dark green.
      CALL PGSCR (7, 0.3, 0.5, 0.3)

      C0(1) = -1
      C0(2) = -1
      C0(3) = -1
      C0(4) = -1
      C0(5) = -1
      C0(6) = -1
      C0(7) = -1

      CALL PGWNAD (0.0, 1.0, 0.0, 1.0)
      CALL PGASK (.TRUE.)
      CALL PGPAGE ()

      STATUS = WCSPTI (WCS, WCS_FLAG, -1, 0, 0)

*-----------------------------------------------------------------------

*     Longitude-velocity map; the y-axis is regularly spaced in
*     frequency but is to be labelled as a true relativistic velocity.
*       - PGSBOX uses subroutine LNGVEL.
*       - Separable (i.e. orthogonal), non-linear coordinate system.
*       - Automatic choice of coordinate increments.
*       - Extraction of a common scaling factor.
*       - Automatic choice of what edges to label.
*       - Request for tickmarks (internal) for one coordinate and grid
*         lines for the other.
*       - Simple two-colour grid using two calls with deferred
*         labelling on the first call.
*       - Degree labelling.
*       - Suppression of zero arcmin and arcsec fields in sexagesimal
*         degree format.

      WRITE (*, '(/,A)') 'Longitude-velocity map'

*     Reference pixel coordinates.
      NLDPRM(1) =   1D0
      NLDPRM(2) = 256D0

*     Reference pixel values.
      NLDPRM(3) = 0D0
      NLDPRM(4) = 1.420D9

*     Coordinate increments.
      NLDPRM(5) = 360D0/(NAXIS(1)-1)
      NLDPRM(6) = 4D6

*     Rest frequency.
      NLDPRM(7) = 1.420D9

*     Annotation.
      IDENTS(1) = 'galactic longitude'
      IDENTS(2) = 'velocity (m/s)'
      IDENTS(3) = 'HI line'

      OPT(1) = 'F'
      OPT(2) = ' '

*     Normal size lettering.
      CALL PGSCH (1.0*SCL)

*     Yellow tick marks for longitude and grid lines for velocity.
      CALL PGSCI (2)
      GCODE(1) = 1
      GCODE(2) = 2

*     Defer labelling.
      IC = -1
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, -1, 0, C0, GCODE, 2D0,
     :  0, GRID1, 0, GRID2, .FALSE., LNGVEL, 1, 1, 7, ' ', NLIPRM,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw fiducial grid lines in white and do labelling.
      CALL PGSCI (1)
      GCODE(1) = 2
      GCODE(2) = 2
      GRID1(1) = 180D0
      GRID2(1) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 0, 0, C0, GCODE, 0D0,
     :  1, GRID1, 1, GRID2, .FALSE., LNGVEL, 1, 1, 7, ' ', NLIPRM,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------

*     Azimuth-frequency scan; this sort of output might be obtained from
*     an antenna that scans in azimuth with a receiver that scans
*     simultaneously in frequency.
*       - PGSBOX uses subroutine FSCAN.
*       - Non-separable (i.e. non-orthogonal) non-linear coordinate
*         system.
*       - Automatic choice of what edges to label; results in labelling
*         the bottom, left and right sides of the plot.
*       - Cyclic labelling.  FSCAN returns the azimuth in the range
*         0 - 720 degrees but PGSBOX is set to normalize this to two
*         cycles of 0 - 360 degrees.
*       - Logarithmic labelling.
*       - Automatic choice of coordinate increments but with request
*         for all grid lines for the logarithmic coordinate.
*       - Degree labelling.
*       - Suppression of common zero arcmin and arcsec fields in
*         sexagesimal degree format.

      WRITE (*, '(/,A)') 'Azimuth-frequency scan'

*     Reference pixel coordinates.
      NLDPRM(1) = 0.5D0
      NLDPRM(2) = 0.5D0

*     Reference pixel values.
      NLDPRM(3) = 0D0
      NLDPRM(4) = 8.5D0

*     Coordinate increments.
      NLDPRM(5) = 720D0/(NAXIS(1)+1)
      NLDPRM(6) = 0.002D0

*     Rate of change of NLDPRM(4) with x-pixel.
      NLDPRM(7) = -0.002D0

*     Annotation.
      IDENTS(1) = 'azimuth'
      IDENTS(2) = ESCAPE // 'gn/Hz'
      IDENTS(3) = 'Frequency/azimuth scan'

      OPT(1) = 'D'
      OPT(2) = 'L'

*     Normal size lettering.
      CALL PGSCH (1.0*SCL)

*     Draw full grid lines.
      CALL PGSCI (1)
      GCODE(1) = 2
      GCODE(2) = 2

*     Setting LABDEN = 9900 forces all logarithmic grid lines to be
*     drawn.
      IC = -1
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 0, 9900, C0, GCODE, 2D0,
     :  0, GRID1, 0, GRID2, .FALSE., FSCAN, 1, 1, 7, ' ', NLIPRM,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------

*     Z versus time plot.
*       - PGSBOX uses subroutine PGCRFN.
*       - Separable (i.e. orthogonal), non-linear coordinate system.
*       - Use of function PGCRFN for separable axis types.
*       - Automatic choice of what edges to label; results in labelling
*         the bottom and left sides of the plot.
*       - Automatic choice of coordinate increments.
*       - Logarithmic labelling over many orders of magnitude.
*       - Single-character annotation on a vertical axis is upright.

      WRITE (*, '(/,A)') 'Z versus time plot'

*     Function types.
      FCODE(1) = 'Lin '
      FCODE(2) = 'Log '

*     Reference pixel coordinates.
      NLDPRM(1) = 0.5D0
      NLDPRM(2) = -50D0

*     Coordinate increments.
      NLDPRM(3) = 0.04D0
      NLDPRM(4) = 0.02D0

*     Reference pixel values.
      NLDPRM(5) = -3.0D0
      NLDPRM(6) =  1.0D0

*     Annotation.
      IDENTS(1) = 'Age of universe (sec)'
      IDENTS(2) = 'Y'
      IDENTS(3) = ' '

      OPT(1) = 'L'
      OPT(2) = ' '

*     Normal size lettering.
      CALL PGSCH (1.0*SCL)

*     Draw ticks for the first coordinate, grid lines for the second.
      CALL PGSCI (1)
      GCODE(1) = 1
      GCODE(2) = 2

      IC = -1
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 0, 0, C0, GCODE, 2D0,
     :  0, GRID1, 0, GRID2, .FALSE., PGCRFN, 8, 2, 4, FCODE, NLIPRM,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------

*     Simple SIN projection near the south celestial pole.
*       - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
*       - Non-separable (i.e. non-orthogonal) curvilinear coordinate
*         system.
*       - Demonstrate parameter definition for PGWCSL.
*       - Discovery of grid lines that do not cross any axis.
*       - Automatic choice of what edges to label; results in labelling
*         all sides of the plot.
*       - Automatic choice of coordinate increments but with request
*         for increased grid density for each coordinate.
*       - Double precision accuracy.
*       - Cyclic coordinates.  PGWCSL returns the right ascension in
*         the range -180 to +180 degrees, i.e. with a discontinuity
*         at +/- 180 degrees.
*       - Labelling of degrees as time in the range 0 - 24h.
*       - Suppression of labels that would overlap one another.
*       - Sexagesimal degree labelling with automatically determined
*         precision.
*       - Suppression of common zero minute and second fields in
*         sexagesimal time format.

      WRITE (*, '(/,A)') 'Simple SIN projection'

      STATUS = WCSINI (2, WCS)

*     Set projection type to SIN.
      CTYPE(1) = 'RA---SIN'
      CTYPE(2) = 'DEC--SIN'
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(1), 1, 0)
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(2), 2, 0)

*     Reference pixel coordinates.
      STATUS = WCSPTD (WCS, WCS_CRPIX, 384D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRPIX, 256D0, 2, 0)

*     Coordinate increments.
      STATUS = WCSPTD (WCS, WCS_CDELT, -1D0/3600000D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CDELT,  1D0/3600000D0, 2, 0)

*     Spherical coordinate references.
      DEC0 = -89.99995D0
      STATUS = WCSPTD (WCS, WCS_CRVAL, 25D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRVAL, DEC0, 2, 0)

*     Set parameters for an NCP projection.
      DEC0 = DEC0*D2R
      STATUS = WCSPTD (WCS, WCS_PV, 0D0, 2, 1)
      STATUS = WCSPTD (WCS, WCS_PV, COS(DEC0)/SIN(DEC0), 2, 2)

*     Annotation.
      IDENTS(1) = 'Right ascension'
      IDENTS(2) = 'Declination'
      IDENTS(3) = 'WCS SIN projection'

      OPT(1) = 'G'
      OPT(2) = 'E'

*     Reduced size lettering.
      CALL PGSCH (0.8*SCL)

*     Draw full grid lines.
      CALL PGSCI (1)
      GCODE(1) = 2
      GCODE(2) = 2

*     Draw the celestial grid.  The grid density is set for each world
*     coordinate by specifying LABDEN = 1224.
      IC = -1
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 0, 1224, C0, GCODE, 0D0,
     :  0, GRID1, 0, GRID2, .FALSE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------

*     Conic equal area projection.
*       - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
*       - Non-separable (i.e. non-orthogonal) curvilinear coordinate
*         system.
*       - Coordinate system undefined in areas of the plot.
*       - Demonstrate parameter definition for PGWCSL.
*       - Discontinuous grid lines handled by PGWCSL.
*       - Discovery of grid lines that do not cross any axis.
*       - Colour control for grid and labelling.
*       - Reduced size lettering.
*       - Automatic choice of what edges to label; results in labelling
*         all sides of the plot.
*       - Automatic choice of coordinate increments.
*       - Cyclic coordinates.  PGWCSL returns the longitude in the
*         range -180 to +180 degrees, i.e. with a discontinuity at
*         +/- 180 degrees.
*       - Suppression of labels that would overlap one another.
*       - Suppression of common zero arcmin and arcsec fields in
*         sexagesimal degree format.

      WRITE (*, '(/,A)') 'Conic equal area projection'

      STATUS = WCSINI (2, WCS)

*     Set projection type to conic equal-area.
      CTYPE(1) = 'RA---COE'
      CTYPE(2) = 'DEC--COE'
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(1), 1, 0)
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(2), 2, 0)

*     Reference pixel coordinates.
      STATUS = WCSPTD (WCS, WCS_CRPIX, 256D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRPIX, 256D0, 2, 0)

*     Coordinate increments.
      STATUS = WCSPTD (WCS, WCS_CDELT, -1D0/3D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CDELT,  1D0/3D0, 2, 0)

*     Spherical coordinate references.
      STATUS = WCSPTD (WCS, WCS_CRVAL, 90D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRVAL, 30D0, 2, 0)
      STATUS = WCSPTD (WCS, WCS_LONPOLE, 150D0, 0, 0)

*     Middle latitude and offset from standard parallels.
      STATUS = WCSPTD (WCS, WCS_PV, 60D0, 2, 1)
      STATUS = WCSPTD (WCS, WCS_PV, 15D0, 2, 2)

*     Annotation.
      IDENTS(1) = 'longitude'
      IDENTS(2) = 'latitude'
      IDENTS(3) = 'WCS conic equal area projection'

      OPT(1) = 'E'
      OPT(2) = 'E'

*     Reduced size lettering.
      CALL PGSCH (0.8*SCL)

*     Draw full grid lines.
      GCODE(1) = 2
      GCODE(2) = 2

*     Use colour to associate grid lines and labels.
*     Meridians in red.
      CALL PGSCR (10, 0.5, 0.0, 0.0)
*     Parallels in blue.
      CALL PGSCR (11, 0.0, 0.2, 0.5)
*     Longitudes in red.
      CALL PGSCR (12, 0.8, 0.3, 0.0)
*     Latitudes in blue.
      CALL PGSCR (13, 0.0, 0.4, 0.7)
*     Longitude labels in red.
      CALL PGSCR (14, 0.8, 0.3, 0.0)
*     Latitude labels in blue.
      CALL PGSCR (15, 0.0, 0.4, 0.7)
*     Title in cyan.
      CALL PGSCR (16, 0.3, 1.0, 1.0)

      CI(1) = 10
      CI(2) = 11
      CI(3) = 12
      CI(4) = 13
      CI(5) = 14
      CI(6) = 15
      CI(7) = 16

*     Draw the celestial grid letting PGSBOX choose the increments.
      IC = -1
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 0, 0, CI, GCODE, 0D0,
     :  0, GRID1, 0, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Set parameters to draw the native grid.
      STATUS = WCSPTD (WCS, WCS_CRVAL,  0D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRVAL, 60D0, 2, 0)
      STATUS = WCSPTD (WCS, WCS_LONPOLE, 999D0, 0, 0)
      STATUS = WCSPTD (WCS, WCS_LATPOLE, 999D0, 0, 0)

*     We just want to delineate the boundary, in green.
      CALL PGSCI (7)
      GRID1(1) = -180D0
      GRID1(2) =  180D0
      GRID2(1) =  -90D0
      GRID2(2) =   90D0

      IC = -1
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, -1, 0, C0, GCODE, 0D0,
     :  2, GRID1, 2, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGSCI (1)
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------

*     Polyconic projection with colour-coded grid.
*       - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
*       - Non-separable (i.e. non-orthogonal) curvilinear coordinate
*         system.
*       - Coordinate system undefined in areas of the plot.
*       - Demonstrate parameter definition for PGWCSL.
*       - Discontinuous grid lines handled by PGWCSL.
*       - Colour coded labelling.
*       - Colour coded grid implemented by the caller.
*       - Basic management of the axis-crossing table (see code).
*       - Reduced size lettering.
*       - Tick marks external to the frame.
*       - User selection of what edges to label with request for both
*         coordinates to be labelled on bottom, left and top edges.
*       - User selection of grid lines to plot.
*       - Concatenation of annotation at bottom and left; automatically
*         suppressed at the top since only one coordinate is labelled
*         there.
*       - Suppression of labels that would overlap one another.
*       - Degree labelling.
*       - Labelling of degrees as time in the range -12 - +12h.
*       - Suppression of common zero minute and second fields in
*         sexagesimal time format.

      WRITE (*, '(/,A)') 'Polyconic projection with colour-coded grid'

      STATUS = WCSINI (2, WCS)

*     Set projection type to polyconic.
      CTYPE(1) = 'RA---PCO'
      CTYPE(2) = 'DEC--PCO'
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(1), 1, 0)
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(2), 2, 0)

*     Reference pixel coordinates.
      STATUS = WCSPTD (WCS, WCS_CRPIX, 192D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRPIX, 640D0, 2, 0)

*     Rotate 30 degrees.
      ROTN = 30D0*D2R
      STATUS = WCSPTD (WCS, WCS_PC,  COS(ROTN), 1, 1)
      STATUS = WCSPTD (WCS, WCS_PC,  SIN(ROTN), 1, 2)
      STATUS = WCSPTD (WCS, WCS_PC, -SIN(ROTN), 2, 1)
      STATUS = WCSPTD (WCS, WCS_PC,  COS(ROTN), 2, 2)

*     Coordinate increments.
      STATUS = WCSPTD (WCS, WCS_CDELT, -1D0/5D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CDELT,  1D0/5D0, 2, 0)

*     Spherical coordinate references.
      STATUS = WCSPTD (WCS, WCS_CRVAL, 332D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRVAL,  40D0, 2, 0)
      STATUS = WCSPTD (WCS, WCS_LONPOLE, -30D0, 0, 0)

*     Annotation.
      IDENTS(1) = 'Hour angle'
      IDENTS(2) = 'Declination'
      IDENTS(3) = 'WCS polyconic projection'

      OPT(1) = 'H'
      OPT(2) = 'B'

*     Reduced size lettering.
      CALL PGSCH (0.9*SCL)

*     Draw external (TIKLEN < 0) tick marks every 5 degrees.
      CALL PGSCI (6)
      GCODE(1) = 1
      GCODE(2) = 1
      TIKLEN = -2D0

      IC = -1
      GRID1(0) = 5D0
      GRID2(0) = 5D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, -1, 0, C0, GCODE, TIKLEN,
     :  0, GRID1, 0, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Resetting the table index to zero causes information about the
*     tick marks to be discarded.
      IC = 0

*     Draw full grid lines in yellow rather than tick marks.
      CALL PGSCI (2)
      GCODE(1) = 2
      GCODE(2) = 2

*     Draw the primary meridian and equator.
      GRID1(1) = 0D0
      GRID2(1) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, -1, 0, C0, GCODE, 0D0,
     :  1, GRID1, 1, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     At this point the axis-crossing table will have entries for the
*     primary meridian and equator.  Labelling was deferred in the
*     previous call, and the table is passed intact on the second call
*     to accumulate further axis-crossings.

*     Draw 90 degree meridians and poles in white.
      CALL PGSCI (3)
      GRID1(1) =  90D0
      GRID1(2) = 180D0
      GRID1(3) = 270D0
      GRID2(1) = -90D0
      GRID2(2) =  90D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, -1, 0, C0, GCODE, 0D0,
     :  3, GRID1, 2, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the first set of 15 degree meridians and parallels in blue.
      CALL PGSCI (4)
      GRID1(1) =  15D0
      GRID1(2) =  60D0
      GRID1(3) = 105D0
      GRID1(4) = 150D0
      GRID1(5) = 195D0
      GRID1(6) = 240D0
      GRID1(7) = 285D0
      GRID1(8) = 330D0
      GRID2(1) = -75D0
      GRID2(2) = -30D0
      GRID2(3) =  15D0
      GRID2(4) =  60D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, -1, 0, C0, GCODE, 0D0,
     :  8, GRID1, 4, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the second set of 15 degree meridians and parallels in red.
      CALL PGSCI (5)
      GRID1(1) =  30D0
      GRID1(2) =  75D0
      GRID1(3) = 120D0
      GRID1(4) = 165D0
      GRID1(5) = 210D0
      GRID1(6) = 255D0
      GRID1(7) = 300D0
      GRID1(8) = 345D0
      GRID2(1) = -60D0
      GRID2(2) = -15D0
      GRID2(3) =  30D0
      GRID2(4) =  75D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, -1, 0, C0, GCODE, 0D0,
     :  8, GRID1, 4, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     The axis-crossing table has now accumulated information for all of
*     the preceding meridians and parallels but no labels have been
*     produced.  It will acquire information for the the next set of
*     meridians and parallels before being processed by this call to
*     PGSBOX which finally produces the labels.

*     Draw the 45 degree meridians and parallels in grey and use colour
*     to differentiate grid labels.
*     Meridians and parallels in grey.
      CALL PGSCR (10, 0.7, 0.7, 0.7)
      CALL PGSCR (11, 0.7, 0.7, 0.7)
*     Longitudes tinged red.
      CALL PGSCR (12, 1.0, 0.9, 0.6)
*     Latitudes tinged green.
      CALL PGSCR (13, 0.8, 1.0, 0.9)
*     Longitude labels tinged red.
      CALL PGSCR (14, 1.0, 0.9, 0.6)
*     Latitude labels tinged green.
      CALL PGSCR (15, 0.8, 1.0, 0.9)
*     Title in white.
      CALL PGSCR (16, 1.0, 1.0, 1.0)

      CI(1) = 10
      CI(2) = 11
      CI(3) = 12
      CI(4) = 13
      CI(5) = 14
      CI(6) = 15
      CI(7) = 16

      CALL PGSCI (6)

*     Tell PGSBOX what edges to label.
      GRID1(1) =  45D0
      GRID1(2) = 135D0
      GRID1(3) = 225D0
      GRID1(4) = 315D0
      GRID2(1) = -45D0
      GRID2(2) =  45D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 2333, 0, CI, GCODE, 0D0,
     :  4, GRID1, 2, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Native grid in green (delineates boundary).
      CALL PGSCI (7)
      GRID1(1) = -180D0
      GRID1(2) =  180D0
      GRID2(1) = -999D0

      STATUS = WCSPTD (WCS, WCS_CRVAL, 0D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRVAL, 0D0, 2, 0)
      STATUS = WCSPTD (WCS, WCS_LONPOLE, 999D0, 0, 0)

      IC = -1
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, -1, 0, C0, GCODE, 0D0,
     :  2, GRID1, 1, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGSCI (1)
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------

*     Plate Carree projection.
*       - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
*       - Rectangular image.
*       - Dual coordinate grids.
*       - Non-separable (i.e. non-orthogonal) curvilinear coordinate
*         system.
*       - Demonstrate parameter definition for PGWCSL.
*       - Discontinuous grid lines handled by PGWCSL.
*       - Colour coding of grid and labelling.
*       - Reduced size lettering.
*       - Manual labelling control.
*       - Manual and automatic choice of coordinate increments.
*       - Cyclic coordinates.  PGWCSL returns the longitude in the
*         range -180 to +180 degrees, i.e. with a discontinuity at
*         +/- 180 degrees.
*       - Suppression of labels that would overlap one another.

      WRITE (*, '(/,A)') 'Plate Carree projection'

      NAXIS(1) = 181
      NAXIS(2) =  91

      BLC(1) = 0.5
      BLC(2) = 0.5
      TRC(1) = NAXIS(1) + 0.5
      TRC(2) = NAXIS(2) + 0.5

*     Reset viewport for rectangular image.

      IF (LARGE) THEN
        CALL PGVSTD ()
      ELSE
        CALL PGVSIZ (1.0, 3.0, 1.0, 3.0)
      END IF
      CALL PGWNAD (0.0, 1.0, 0.0, REAL(NAXIS(2))/REAL(NAXIS(1)))

      STATUS = WCSINI (2, WCS)

*     Set projection type to plate carree.
      CTYPE(1) = 'GLON-CAR'
      CTYPE(2) = 'GLAT-CAR'
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(1), 1, 0)
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(2), 2, 0)

*     Reference pixel coordinates.
      STATUS = WCSPTD (WCS, WCS_CRPIX, 226D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRPIX,  46D0, 2, 0)

*     Linear transformation matrix.
      ROTN = 15D0*D2R
      STATUS = WCSPTD (WCS, WCS_PC,  COS(ROTN), 1, 1)
      STATUS = WCSPTD (WCS, WCS_PC,  SIN(ROTN), 1, 2)
      STATUS = WCSPTD (WCS, WCS_PC, -SIN(ROTN), 2, 1)
      STATUS = WCSPTD (WCS, WCS_PC,  COS(ROTN), 2, 2)

*     Coordinate increments.
      STATUS = WCSPTD (WCS, WCS_CDELT, -1D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CDELT,  1D0, 2, 0)

*     Set parameters to draw the native grid.
      STATUS = WCSPTD (WCS, WCS_CRVAL, 0D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRVAL, 0D0, 2, 0)

*     The reference pixel was defined so that the native longitude runs
*     from 225 deg to 45 deg and this will cause the grid to be
*     truncated at the 180 deg boundary.  However, being a cylindrical
*     projection it is possible to recentre it in longitude.  CYLFIX
*     will modify CRPIX, CRVAL, and LONPOLE to suit.

      CALL CYLFIX (NAXIS, WCS)

*     Annotation.
      IDENTS(1) = ' '
      IDENTS(2) = ' '
      IDENTS(3) = 'WCS plate caree projection'

      OPT(1) = 'C'
      OPT(2) = 'C'

*     Reduced size lettering.
      CALL PGSCH (0.8*SCL)

*     Draw full grid lines.
      GCODE(1) = 2
      GCODE(2) = 2

*     Draw native grid in green.
      CALL PGSCR (16, 0.0, 0.2, 0.0)
*     Title in cyan.
      CALL PGSCR (17, 0.3, 1.0, 1.0)

      CI(1) = 16
      CI(2) = 16
      CI(3) =  7
      CI(4) =  7
      CI(5) = -1
      CI(6) = -1
      CI(7) = 17

      IC = -1
      GRID1(0) = 15D0
      GRID2(0) = 15D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 2100, 0, CI, GCODE, 0D0,
     :  0, GRID1, 0, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Reset CRPIX previously modified by CYLFIX.
      STATUS = WCSPTD (WCS, WCS_CRPIX, 226D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRPIX,  46D0, 2, 0)

*     Galactic reference coordinates.
      STATUS = WCSPTD (WCS, WCS_CRVAL, 30D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRVAL, 35D0, 2, 0)
      STATUS = WCSPTD (WCS, WCS_LONPOLE, 999D0, 0, 0)

      CALL CYLFIX (NAXIS, WCS)

*     Annotation.
      IDENTS(1) = 'longitude'
      IDENTS(2) = 'latitude'
      IDENTS(3) = ' '

      OPT(1) = 'E'
      OPT(2) = 'E'

*     Use colour to associate grid lines and labels.
*     Meridians in red.
      CALL PGSCR (10, 0.5, 0.0, 0.0)
*     Parallels in blue.
      CALL PGSCR (11, 0.0, 0.2, 0.5)
*     Longitudes in red.
      CALL PGSCR (12, 0.8, 0.3, 0.0)
*     Latitudes in blue.
      CALL PGSCR (13, 0.0, 0.4, 0.7)
*     Longitude labels in red.
      CALL PGSCR (14, 0.8, 0.3, 0.0)
*     Latitude labels in blue.
      CALL PGSCR (15, 0.0, 0.4, 0.7)

      CI(1) = 10
      CI(2) = 11
      CI(3) = 12
      CI(4) = 13
      CI(5) = 14
      CI(6) = 15
      CI(7) = -1

*     Draw the celestial grid letting PGSBOX choose the increments.
      IC = -1
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 21, 0, CI, GCODE, 0D0,
     :  0, GRID1, 0, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGSCI (1)
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------

*     Plate Carree projection.
*       - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
*       - BLC, TRC unrelated to pixel coordinates.
*       - Demonstrate parameter definition for PGWCSL.
*       - Poles and 180 meridian projected along edges of the frame.
*       - Reduced size lettering.
*       - Manual and automatic choice of coordinate increments.
*       - Suppression of common zero minute and second fields in
*         sexagesimal time format.

      WRITE (*, '(/,A)') 'Plate Carree projection'

      BLC(1) = -180.0
      BLC(2) =  -90.0
      TRC(1) =  180.0
      TRC(2) =  +90.0

*     Reset viewport for rectangular image.

      IF (LARGE) THEN
        CALL PGVSTD ()
      ELSE
        CALL PGVSIZ (1.0, 3.0, 1.0, 3.0)
      END IF
      CALL PGWNAD (BLC(1), TRC(1), BLC(2), TRC(2))

      STATUS = WCSINI (2, WCS)

*     Set projection type to plate carree.
      CTYPE(1) = 'RA---CAR'
      CTYPE(2) = 'DEC--CAR'
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(1), 1, 0)
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(2), 2, 0)

*     Reference pixel coordinates.
      STATUS = WCSPTD (WCS, WCS_CRPIX, 0D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRPIX, 0D0, 2, 0)

*     Coordinate increments.
      STATUS = WCSPTD (WCS, WCS_CDELT, -1D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CDELT,  1D0, 2, 0)

*     Set parameters to draw the native grid.
      STATUS = WCSPTD (WCS, WCS_CRVAL, 0D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRVAL, 0D0, 2, 0)

*     Annotation.
      IDENTS(1) = 'Right ascension'
      IDENTS(2) = 'Declination'
      IDENTS(3) = 'WCS plate caree projection'

      OPT(1) = 'G'
      OPT(2) = 'E'

*     Reduced size lettering.
      CALL PGSCH (0.7*SCL)

*     Draw full grid lines.
      GCODE(1) = 2
      GCODE(2) = 2

      CALL PGSCI (1)

      IC = -1
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 2121, 1212, C0, GCODE, 0D0,
     :  0, GRID1, 0, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------

*     Cylindrical perspective projection.
*       - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
*       - BLC, TRC unrelated to pixel coordinates.
*       - Demonstrate parameter definition for PGWCSL.
*       - Reduced size lettering.
*       - Manual and automatic choice of coordinate increments.
*       - Suppression of common zero minute and second fields in
*         sexagesimal time format.

      WRITE (*, '(/,A)') 'Cylindrical perspective projection'

      BLC(1) = -180.0
      BLC(2) =  -90.0
      TRC(1) =  180.0
      TRC(2) =  +90.0

*     Reset viewport for rectangular image.

      IF (LARGE) THEN
        CALL PGVSTD ()
      ELSE
        CALL PGVSIZ (1.0, 3.0, 1.0, 3.0)
      END IF
      CALL PGWNAD (BLC(1), TRC(1), BLC(2), TRC(2))

      STATUS = WCSINI (2, WCS)

*     Set projection type to cylindrical perspective.
      CTYPE(1) = 'RA---CYP'
      CTYPE(2) = 'DEC--CYP'
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(1), 1, 0)
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(2), 2, 0)

*     Reference pixel coordinates.
      STATUS = WCSPTD (WCS, WCS_CRPIX, 0D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRPIX, 0D0, 2, 0)

*     Coordinate increments.
      STATUS = WCSPTD (WCS, WCS_CDELT, -1D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CDELT,  1D0, 2, 0)

*     Set parameters to draw the native grid.
      STATUS = WCSPTD (WCS, WCS_CRVAL,  45D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRVAL, -90D0, 2, 0)
      STATUS = WCSPTD (WCS, WCS_LONPOLE, 999D0, 0, 0)

*     mu and lambda projection parameters.
      STATUS = WCSPTD (WCS, WCS_PV, 0D0, 2, 1)
      STATUS = WCSPTD (WCS, WCS_PV, 1D0, 2, 2)

*     Annotation.
      IDENTS(1) = 'Right ascension'
      IDENTS(2) = 'Declination'
      IDENTS(3) = 'WCS cylindrical perspective projection'

      OPT(1) = 'G'
      OPT(2) = 'E'

*     Reduced size lettering.
      CALL PGSCH (0.7*SCL)

*     Draw full grid lines.
      GCODE(1) = 2
      GCODE(2) = 2

      CALL PGSCI (1)

      IC = -1
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 2121, 1212, C0, GCODE, 0D0,
     :  0, GRID1, 0, GRID2, .TRUE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------
*     Gnomonic projection.
*       - PGSBOX uses subroutine PGWCSL to interface to WCSLIB.
*       - Demonstrate parameter definition for PGWCSL.
*       - Reduced size lettering.
*       - Manual and automatic choice of coordinate increments.
*       - Suppression of common zero minute and second fields in
*         sexagesimal time format.

      WRITE (*, '(/,A)') 'TAN projection'

      NAXIS(1) = 100
      NAXIS(2) = 100

      BLC(1) = 0.5
      BLC(2) = 0.5
      TRC(1) = NAXIS(1) + 0.5
      TRC(2) = NAXIS(2) + 0.5

*     Reset viewport for rectangular image.
      IF (LARGE) THEN
        CALL PGVSTD ()
      ELSE
        CALL PGVSIZ (1.0, 3.0, 1.0, 3.0)
      END IF
      CALL PGWNAD (0.0, 1.0, 0.0, REAL(NAXIS(2))/REAL(NAXIS(1)))

      STATUS = WCSINI (2, WCS)

*     Set projection type to gnomonic.
      CTYPE(1) = 'RA---TAN'
      CTYPE(2) = 'DEC--TAN'
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(1), 1, 0)
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(2), 2, 0)

*     Reference pixel coordinates.
      STATUS = WCSPTD (WCS, WCS_CRPIX, 50.5D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRPIX,  1.0D0, 2, 0)

*     Coordinate increments.
      STATUS = WCSPTD (WCS, WCS_CDELT, 1D-3, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CDELT, 1D-3, 2, 0)

*     Set parameters to draw the native grid.
      STATUS = WCSPTD (WCS, WCS_CRVAL, -45.0D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRVAL, -89.7D0, 2, 0)
      STATUS = WCSPTD (WCS, WCS_LONPOLE, 999D0, 0, 0)

*     Annotation.
      IDENTS(1) = 'Right ascension'
      IDENTS(2) = 'Declination'
      IDENTS(3) = 'WCS TAN projection'

      OPT(1) = 'E'
      OPT(2) = 'E'

*     Reduced size lettering.
      CALL PGSCH (0.7*SCL)

*     Draw full grid lines.
      GCODE(1) = 2
      GCODE(2) = 2

      CALL PGSCI (1)

      IC = -1
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 0, 1212, C0, GCODE, 0D0,
     :  0, GRID1, 0, GRID2, .FALSE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------

*     Linear-linear plot with two types of alternative labelling.
*       - PGSBOX uses subroutine PGCRFN.
*       - Separable (i.e. orthogonal), linear coordinate system.
*       - Use of function PGCRFN for separable axis types.
*       - Alternative labelling and axis annotation.
*       - Direct manipulation of the axis-crossing table.
*       - Tick mark and grid line control.
*       - User selection of what edges to label.
*       - Automatic choice of coordinate increments.

      WRITE (*, '(/,A)') 'Linear plot with alternative labelling'

      IF (LARGE) THEN
        CALL PGVSTD ()
      ELSE
        CALL PGVSIZ (1.0, 3.0, 1.0, 3.0)
      END IF
      CALL PGWNAD (0.0, 1.0, 0.0, 1.0)

      NAXIS(1) = 512
      NAXIS(2) = 512

      BLC(1) = 0.5
      BLC(2) = 0.5
      TRC(1) = NAXIS(1) + 0.5
      TRC(2) = NAXIS(2) + 0.5

*     Function types.
      FCODE(1) = 'Lin '
      FCODE(2) = 'Lin '

*     Reference pixel coordinates.
      NLDPRM(1) = 0.5D0
      NLDPRM(2) = 0.5D0

*     Coordinate increments.
      NLDPRM(3) = 0.03D0
      NLDPRM(4) = 0.03D0

*     Reference pixel values.
      NLDPRM(5) = 20D0
      NLDPRM(6) =  0D0

*     Annotation.
      IDENTS(1) = 'temperature of frog (' // ESCAPE // 'uo' //
     :            ESCAPE // 'dC)'
      IDENTS(2) = 'distance hopped (m)'
      IDENTS(3) = ' '

      OPT(1) = ' '
      OPT(2) = ' '

*     Reduced size lettering.
      CALL PGSCH (0.8*SCL)

*     Draw tick marks at the bottom for the first coordinate, grid lines
*     for the second.  Setting GCODE(1) = -1 inhibits information being
*     stored for labels on the top edge while GCODE(2) = 2 causes
*     information to be stored for labels on the right edge even if
*     those labels are not actually produced.
      CALL PGSCI (1)
      GCODE(1) = -1
      GCODE(2) = 2

*     Set LABCTL = 21 to label the bottom and left edges only.
      IC = -1
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 21, 0, C0, GCODE, 2D0,
     :  0, GRID1, 0, GRID2, .FALSE., PGCRFN, 8, 2, 4, FCODE, NLIPRM,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Information for labels on the right edge was stored in the
*     crossing table on the first call to PGSBOX.  We now want to
*     manipulate it to convert metres to feet.  Note that while it's
*     a simple matter to draw alternative sets of tick marks on opposite
*     edges of the frame, as with the two temperature scales, we have
*     the slightly more difficult requirement of labelling grid lines
*     with different values at each end.
      DO 10 J = 1, IC
*       Look for entries associated with the right edge of the frame.
        IF (CACHE(1,J).EQ.4D0) THEN
*         Convert to feet, rounding to the nearest 0.1.
          CACHE(4,J) = CACHE(4,J) * 1D3/(25.4*12D0)
          CACHE(4,J) = AINT(CACHE(4,J)*10D0 + 0.5D0)/10D0
        END IF
 10   CONTINUE

*     Annotation for the right edge.
      IDENTS(1) = ' '
      IDENTS(2) = '(feet)'

*     Set LABCTL = 12000 to label the right edge with the second
*     coordinate without redrawing the grid lines.
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 12000, 0, C0, GCODE, 2D0,
     :  0, GRID1, 0, GRID2, .FALSE., PGCRFN, 8, 2, 4, FCODE, NLIPRM,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     The alternative temperature scale in Fahrenheit is to be
*     constructed with a new set of tick marks.
      NLDPRM(3) = NLDPRM(3)*1.8D0
      NLDPRM(5) = NLDPRM(5)*1.8D0 + 32D0

*     Draw tick marks at the top for the first coordinate, don't redo
*     grid lines for the second.
      GCODE(1) = -100
      GCODE(2) = 0

*     Annotation for the top edge.
      IDENTS(1) = '(' // ESCAPE // 'uo' // ESCAPE // 'dF)'
      IDENTS(2) = ' '

*     Set LABCTL = 100 to label the top edge; Set IC = -1 to redetermine
*     the coordinate extrema.
      IC = -1
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 100, 0, C0, GCODE, 2D0,
     :  0, GRID1, 0, GRID2, .FALSE., PGCRFN, 8, 2, 4, FCODE, NLIPRM,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------

*     Calendar axes using subroutine PGLBOX.
*       - Separable (i.e. orthogonal), linear coordinate system.
*       - Use of PGLBOX for simple linear axis types.
*       - Automatic choice of what edges to label; results in labelling
*         the bottom and left sides of the plot.
*       - Automatic choice of coordinate increments.
*       - Calendar date axis labelling.
*       - Single-character annotation on a vertical axis is upright.

      WRITE (*, '(/,A)') 'Calendar axes using subroutine PGLBOX'

      CALL PGSWIN (51900.0, 52412.0, 51900.0, 57020.0)

*     Annotation.
      IDENTS(1) = 'Date started'
      IDENTS(2) = 'Date finished'
      IDENTS(3) = 'Calendar axes using subroutine PGLBOX'

      OPT(1) = 'Y'
      OPT(2) = 'Y'

*     Reduced size lettering.
      CALL PGSCH (0.7*SCL)

*     Draw tick marks on each axis.
      CALL PGSCI (1)
      GCODE(1) = 1
      GCODE(2) = 1

      IC = -1
      CALL PGLBOX (IDENTS, OPT, 0, 0, C0, GCODE, 2D0, 0, 0D0, 0, 0D0,
     :  .FALSE., 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------

*     Simple linear axes handled by PGWCSL.
*       - Separable (i.e. orthogonal), linear coordinate system.
*       - Automatic choice of what edges to label; results in labelling
*         the bottom and left sides of the plot.
*       - Automatic choice of coordinate increments.
*       - Tick marks and labels at the edges of the frame.
*       - Single-character annotation on a vertical axis is upright.

      WRITE (*, '(/,A)') 'Simple linear axes handled by pgwcsl()'

      NAXIS(1) = 3
      NAXIS(2) = 3

      BLC(1) = 0.5
      BLC(2) = 0.5
      TRC(1) = NAXIS(1) + 0.5
      TRC(2) = NAXIS(2) + 0.5

      STATUS = WCSINI (2, WCS)

      CTYPE(1) = 'X'
      CTYPE(2) = 'Y'
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(1), 1, 0)
      STATUS = WCSPTC (WCS, WCS_CTYPE, CTYPE(2), 2, 0)

*     Reference pixel coordinates.
      STATUS = WCSPTD (WCS, WCS_CRPIX, 2D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRPIX, 2D0, 2, 0)

*     Coordinate increments.
      STATUS = WCSPTD (WCS, WCS_CDELT, 1D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CDELT, 1D0, 2, 0)

*     Spherical coordinate references.
      STATUS = WCSPTD (WCS, WCS_CRVAL, 2D0, 1, 0)
      STATUS = WCSPTD (WCS, WCS_CRVAL, 2D0, 2, 0)

*     Annotation.
      IDENTS(1) = 'X'
      IDENTS(2) = 'Y'
      IDENTS(3) = 'Simple linear axes handled by pgwcsl()'

      OPT(1) = ' '
      OPT(2) = ' '

*     Reduced size lettering.
      CALL PGSCH (0.8*SCL)

*     Draw tick marks only.
      CALL PGSCI (1)
      GCODE(1) = 1
      GCODE(2) = 1

      IC = -1
      GRID1(0) = 0D0
      GRID2(0) = 0D0
      CALL PGSBOX (BLC, TRC, IDENTS, OPT, 0, 0, C0, GCODE, 2D0,
     :  0, GRID1, 0, GRID2, .FALSE., PGWCSL, 1, WCSLEN, 1, NLCPRM, WCS,
     :  NLDPRM, 256, IC, CACHE, IERR)

*     Draw the frame.
      CALL PGBOX ('BC', 0.0, 0, 'BC', 0.0, 0)

      CALL WCSLEEP (250)
      CALL PGPAGE ()

*-----------------------------------------------------------------------

      STATUS = WCSFREE (WCS)

      CALL PGASK (.FALSE.)
      CALL PGEND ()

      END
