!=============================================================================
! WCSLIB 8.4 - an implementation of the FITS WCS standard.
! Copyright (C) 1995-2024, Mark Calabretta
!
! This file is part of WCSLIB.
!
! WCSLIB is free software: you can redistribute it and/or modify it under the
! terms of the GNU Lesser General Public License as published by the Free
! Software Foundation, either version 3 of the License, or (at your option)
! any later version.
!
! WCSLIB is distributed in the hope that it will be useful, but WITHOUT ANY
! WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
! FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for
! more details.
!
! You should have received a copy of the GNU Lesser General Public License
! along with WCSLIB.  If not, see http://www.gnu.org/licenses.
!
! Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
! http://www.atnf.csiro.au/people/Mark.Calabretta
! $Id: wcsunits_bindc.f90,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
!=============================================================================

INTEGER FUNCTION WCSUNITSE (HAVE, WANT, SCALE, OFFSET, POWER, ERR)
  CHARACTER :: HAVE(72), WANT(72)
  DOUBLE PRECISION :: SCALE, OFFSET, POWER
  INTEGER :: ERR(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSUNITSE_C (HAVE, WANT, SCALE, OFFSET, POWER, &
                                         ERR) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      CHARACTER(KIND=C_CHAR, LEN=1) :: HAVE(72), WANT(72)
      REAL(C_DOUBLE) :: SCALE, OFFSET, POWER
      INTEGER(C_INT) :: ERR(*)
    END FUNCTION WCSUNITSE_C
  END INTERFACE

  WCSUNITSE = WCSUNITSE_C (HAVE, WANT, SCALE, OFFSET, POWER, ERR)
END FUNCTION WCSUNITSE

!-----------------------------------------------------------------------------

INTEGER FUNCTION WCSUNITS (HAVE, WANT, SCALE, OFFSET, POWER)
  CHARACTER :: HAVE(72), WANT(72)
  DOUBLE PRECISION :: SCALE, OFFSET, POWER

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSUNITS_C (HAVE, WANT, SCALE, OFFSET, POWER) &
                                        BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      CHARACTER(KIND=C_CHAR, LEN=1) :: HAVE(72), WANT(72)
      REAL(C_DOUBLE) :: SCALE, OFFSET, POWER
    END FUNCTION WCSUNITS_C
  END INTERFACE

  WCSUNITS = WCSUNITS_C (HAVE, WANT, SCALE, OFFSET, POWER)
END FUNCTION WCSUNITS

!-----------------------------------------------------------------------------

INTEGER FUNCTION WCSUTRNE (CTRL, UNITSTR, ERR)
  INTEGER :: CTRL
  CHARACTER :: UNITSTR(72)
  INTEGER :: ERR(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSUTRNE_C (CTRL, UNITSTR, ERR) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: CTRL
      CHARACTER(KIND=C_CHAR, LEN=1) :: UNITSTR(72)
      INTEGER(C_INT) :: ERR(*)
    END FUNCTION WCSUTRNE_C
  END INTERFACE

  WCSUTRNE = WCSUTRNE_C (CTRL, UNITSTR, ERR)
END FUNCTION WCSUTRNE

!-----------------------------------------------------------------------------

INTEGER FUNCTION WCSUTRN (CTRL, UNITSTR)
  INTEGER :: CTRL
  CHARACTER :: UNITSTR(72)

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSUTRN_C (CTRL, UNITSTR) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: CTRL
      CHARACTER(KIND=C_CHAR, LEN=1) :: UNITSTR(72)
    END FUNCTION WCSUTRN_C
  END INTERFACE

  WCSUTRN = WCSUTRN_C (CTRL, UNITSTR)
END FUNCTION WCSUTRN

!-----------------------------------------------------------------------------

INTEGER FUNCTION WCSULEXE (UNITSTR, FUNC, SCALE, UNITS, ERR)
  CHARACTER :: UNITSTR(72)
  INTEGER :: FUNC
  DOUBLE PRECISION :: SCALE, UNITS(*)
  INTEGER :: ERR(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSULEXE_C (UNITSTR, FUNC, SCALE, UNITS, ERR) &
                                        BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      CHARACTER(KIND=C_CHAR, LEN=1) :: UNITSTR(72)
      INTEGER(C_INT) :: FUNC
      REAL(C_DOUBLE) :: SCALE, UNITS(*)
      INTEGER(C_INT) :: ERR(*)
    END FUNCTION WCSULEXE_C
  END INTERFACE

  WCSULEXE = WCSULEXE_C (UNITSTR, FUNC, SCALE, UNITS, ERR)
END FUNCTION WCSULEXE

!-----------------------------------------------------------------------------

INTEGER FUNCTION WCSULEX (UNITSTR, FUNC, SCALE, UNITS)
  CHARACTER :: UNITSTR(72)
  INTEGER :: FUNC
  DOUBLE PRECISION :: SCALE, UNITS(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSULEX_C (UNITSTR, FUNC, SCALE, UNITS) &
                                        BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      CHARACTER(KIND=C_CHAR, LEN=1) :: UNITSTR(72)
      INTEGER(C_INT) :: FUNC
      REAL(C_DOUBLE) :: SCALE, UNITS(*)
    END FUNCTION WCSULEX_C
  END INTERFACE

  WCSULEX = WCSULEX_C (UNITSTR, FUNC, SCALE, UNITS)
END FUNCTION WCSULEX
