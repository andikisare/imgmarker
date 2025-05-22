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
! $Id: cel_bindc.f90,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
!=============================================================================

INTEGER FUNCTION CELPTC (CEL, WHAT, VALUE, I)
  INTEGER :: CEL(*), WHAT
  CHARACTER :: VALUE(*)
  INTEGER :: I

  INTERFACE
    INTEGER(C_INT) FUNCTION CELPTC_C (CEL, WHAT, VALUE, I) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: CEL(*), WHAT
      CHARACTER(KIND=C_CHAR, LEN=1) :: VALUE(*)
      INTEGER(C_INT) :: I
    END FUNCTION CELPTC_C
  END INTERFACE

  CELPTC = CELPTC_C (CEL, WHAT, VALUE, I)
END FUNCTION CELPTC

!-----------------------------------------------------------------------------

INTEGER FUNCTION CELGTC (CEL, WHAT, VALUE)
  INTEGER :: CEL(*), WHAT
  CHARACTER :: VALUE(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION CELGTC_C (CEL, WHAT, VALUE) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: CEL(*), WHAT
      CHARACTER(KIND=C_CHAR, LEN=1) :: VALUE(*)
    END FUNCTION CELGTC_C
  END INTERFACE

  CELGTC = CELGTC_C (CEL, WHAT, VALUE)
END FUNCTION CELGTC

!-----------------------------------------------------------------------------

INTEGER FUNCTION CELPERR (CEL, PREFIX)
  INTEGER :: CEL(*)
  CHARACTER :: PREFIX(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION CELPERR_C (CEL, PREFIX) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: CEL(*)
      CHARACTER(KIND=C_CHAR, LEN=1) :: PREFIX(72)
    END FUNCTION CELPERR_C
  END INTERFACE

  CELPERR = CELPERR_C (CEL, PREFIX)
END FUNCTION CELPERR
