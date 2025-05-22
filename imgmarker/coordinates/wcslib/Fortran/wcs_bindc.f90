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
! $Id: wcs_bindc.f90,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
!=============================================================================

INTEGER FUNCTION WCSPTC (WCS, WHAT, VALUE, I, J)
  INTEGER :: WCS(*), WHAT
  CHARACTER :: VALUE(*)
  INTEGER :: I, J

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSPTC_C (WCS, WHAT, VALUE, I, J) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: WCS(*), WHAT
      CHARACTER(KIND=C_CHAR, LEN=1) :: VALUE(*)
      INTEGER(C_INT) :: I, J
    END FUNCTION WCSPTC_C
  END INTERFACE

  WCSPTC = WCSPTC_C (WCS, WHAT, VALUE, I, J)
END FUNCTION WCSPTC

!-----------------------------------------------------------------------------

INTEGER FUNCTION WCSGTC (WCS, WHAT, VALUE)
  INTEGER :: WCS(*), WHAT
  CHARACTER :: VALUE(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSGTC_C (WCS, WHAT, VALUE) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: WCS(*), WHAT
      CHARACTER(KIND=C_CHAR, LEN=1) :: VALUE(*)
    END FUNCTION WCSGTC_C
  END INTERFACE

  WCSGTC = WCSGTC_C (WCS, WHAT, VALUE)
END FUNCTION WCSGTC

!-----------------------------------------------------------------------------

INTEGER FUNCTION WCSPERR (WCS, PREFIX)
  INTEGER :: WCS(*)
  CHARACTER :: PREFIX(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSPERR_C (WCS, PREFIX) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: WCS(*)
      CHARACTER(KIND=C_CHAR, LEN=1) :: PREFIX(72)
    END FUNCTION WCSPERR_C
  END INTERFACE

  WCSPERR = WCSPERR_C (WCS, PREFIX)
END FUNCTION WCSPERR

!-----------------------------------------------------------------------------

INTEGER FUNCTION WCSCCS (WCS, LNG2P1, LAT2P1, LNG1P2, CLNG, CLAT, RADESYS, &
                         EQUINOX, ALT)
  INTEGER :: WCS(*)
  DOUBLE PRECISION :: LNG2P1, LAT2P1, LNG1P2
  CHARACTER :: CLNG(4), CLAT(4), RADESYS(71)
  DOUBLE PRECISION :: EQUINOX
  CHARACTER :: ALT(1)

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSCCS_C (WCS, LNG2P1, LAT2P1, LNG1P2, CLNG, &
                                      CLAT, RADESYS, EQUINOX, ALT) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: WCS(*)
      REAL(C_DOUBLE) :: LNG2P1, LAT2P1, LNG1P2
      CHARACTER(KIND=C_CHAR, LEN=1) :: CLNG(4), CLAT(4), RADESYS(71)
      REAL(C_DOUBLE) :: EQUINOX
      CHARACTER(KIND=C_CHAR, LEN=1) :: ALT(1)
    END FUNCTION WCSCCS_C
  END INTERFACE

  WCSCCS = WCSCCS_C (WCS, LNG2P1, LAT2P1, LNG1P2, CLNG, CLAT, RADESYS, &
                     EQUINOX, ALT)
END FUNCTION WCSCCS

!-----------------------------------------------------------------------------

INTEGER FUNCTION WCSSPTR (WCS, I, CTYPE)
  INTEGER :: WCS(*), I
  CHARACTER :: CTYPE(8)

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSSPTR_C (WCS, I, CTYPE) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: WCS(*), I
      CHARACTER(KIND=C_CHAR, LEN=1) :: CTYPE(8)
    END FUNCTION WCSSPTR_C
  END INTERFACE

  WCSSPTR = WCSSPTR_C (WCS, I, CTYPE)
END FUNCTION WCSSPTR

!-----------------------------------------------------------------------------

SUBROUTINE WCSLIB_VERSION (WCSVER, NCHR)
  CHARACTER :: WCSVER(*)
  INTEGER :: NCHR

  INTERFACE
    SUBROUTINE WCSLIB_VERSION_C (WCSVER, NCHR) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      CHARACTER(KIND=C_CHAR, LEN=1) :: WCSVER(*)
      INTEGER(C_INT) :: NCHR
    END SUBROUTINE WCSLIB_VERSION_C
  END INTERFACE

  CALL WCSLIB_VERSION_C (WCSVER, NCHR)
END SUBROUTINE WCSLIB_VERSION
