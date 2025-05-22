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
* $Id: tunits.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      PROGRAM TUNITS
*-----------------------------------------------------------------------
*
* TUNITS tests WCSULEX, WCSUTRN, and WCSUNITS the FITS units
* specification parser, translator and converter.
*
*-----------------------------------------------------------------------

      INCLUDE 'wcsunits.inc'

      LOGICAL   INTRCT
      INTEGER   FUNC, I, NC, STATUS
      DOUBLE PRECISION OFFSET, POWER, SCALE, UNITS(WCSUNITS_NTYPE)
      CHARACTER HAVE*80, WANT*80
*-----------------------------------------------------------------------

      INTRCT = ISATTY(5)

      WRITE (*, 10)
 10   FORMAT ('Testing FITS unit specification parser (tunits.f)',/,
     :        '-------------------------------------------------')
      IF (INTRCT) WRITE (*, 20)
 20   FORMAT (/,'To test WCSULEX, enter <CR> when prompted with "Unit ',
     :          'string (want):".')

 30   CONTINUE
        IF (INTRCT) WRITE (*, '(/,A,$)') 'Unit string (have): '
        READ (*, '(A)', END=999) HAVE
        NC = LNBLNK(HAVE)
        IF (.NOT.INTRCT) WRITE (*, 40) HAVE(:NC)
 40     FORMAT (/,'Unit string (have): ',A)

        STATUS = WCSUTRN(7, HAVE)
        IF (STATUS.GE.0) THEN
          NC = LNBLNK(HAVE)
          WRITE (*, 50) HAVE(:NC)
 50       FORMAT ('       Translation: ',A,$)
          IF (STATUS.EQ.0) THEN
            WRITE (*, '()')
          ELSE
            NC = LNBLNK(WCSUNITS_ERRMSG(STATUS))
            WRITE (*, 60) WCSUNITS_ERRMSG(STATUS)(:NC)
 60         FORMAT ('   (WARNING: ',A,')')
          END IF
        END IF

        IF (INTRCT) WRITE (*, '(A,$)') 'Unit string (want): '
        READ (*, '(A)', END=999) WANT

        IF (WANT.NE.' ') THEN
          NC = LNBLNK(WANT)
          IF (.NOT.INTRCT) WRITE (*, 70) WANT(:NC)
 70       FORMAT ('Unit string (want): ',A)

          STATUS = WCSUTRN(7, WANT)
          IF (STATUS.GE.0) THEN
            NC = LNBLNK(WANT)
            WRITE (*, 50) WANT(:NC)
            IF (STATUS.EQ.0) THEN
              WRITE (*, '()')
            ELSE
              NC = LNBLNK(WCSUNITS_ERRMSG(STATUS))
              WRITE (*, 60) WCSUNITS_ERRMSG(STATUS)(:NC)
            END IF
          END IF

          WRITE (*, 80) HAVE(:LNBLNK(HAVE)), WANT(:LNBLNK(WANT))
 80       FORMAT ('Conversion: "',A,'" -> "',A,'"')

          STATUS = WCSUNITS (HAVE, WANT, SCALE, OFFSET, POWER)
          IF (STATUS.NE.0) THEN
            NC = LNBLNK(WCSUNITS_ERRMSG(STATUS))
            WRITE (*, 90) STATUS, WCSUNITS_ERRMSG(STATUS)(:NC)
 90         FORMAT ('WCSUNITS ERROR',I3,': ',A)
            GO TO 30
          END IF

          IF (POWER.EQ.1D0) THEN
            WRITE (*, '(A,$)') '            = '
          ELSE
            WRITE (*, '(A,$)') '            = ('
          END IF

          IF (SCALE.EQ.1.0) THEN
            WRITE (*, '(A,$)') 'value'
          ELSE
            WRITE (*, '(1PG14.8,A,$)') SCALE, ' * value'
          END IF

          IF (OFFSET.NE.0D0) THEN
            WRITE (*, '(A,1PG14.8,$)') ' + ', OFFSET
          END IF

          IF (POWER.EQ.1D0) THEN
            WRITE (*, '()')
          ELSE
            WRITE (*, '(A,1PG12.6)') ')^', POWER
          END IF

        ELSE
*         Parse the unit string.
          NC = LNBLNK(HAVE)
          WRITE (*, '(A,A,A)') '   Parsing: "', HAVE(:NC), '"'

          STATUS = WCSULEX (HAVE, FUNC, SCALE, UNITS)
          IF (STATUS.NE.0) THEN
            NC = LNBLNK(WCSUNITS_ERRMSG(STATUS))
            WRITE (*, 100) STATUS, WCSUNITS_ERRMSG(STATUS)(:NC)
 100        FORMAT ('WCSULEX ERROR',I3,': ',A,'.')
            GO TO 30
          END IF

          WRITE (*, '(1PG15.8,A)') SCALE, ' *'
          DO 110 I = 1, WCSUNITS_NTYPE
            IF (UNITS(I).NE.0.0) THEN
              NC = LNBLNK(WCSUNITS_TYPES(I))
              WRITE (*, '(F11.2,X,A,$)') UNITS(I),
     :          WCSUNITS_TYPES(I)(:NC)
              IF (WCSUNITS_UNITS(I).NE.' ') THEN
                NC = LNBLNK(WCSUNITS_UNITS(I))
                WRITE (*, '(A,A,A)') ' (', WCSUNITS_UNITS(I)(:NC),')'
              ELSE
                WRITE (*, '()')
              END IF
            END IF
 110      CONTINUE
        END IF
      GO TO 30

 999  WRITE (*, '()')

      END
