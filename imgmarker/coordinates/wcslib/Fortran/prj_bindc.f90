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
! $Id: prj_bindc.f90,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
!=============================================================================

INTEGER FUNCTION PRJPTC (PRJ, WHAT, VALUE, M)
  INTEGER :: PRJ(*), WHAT
  CHARACTER :: VALUE(*)
  INTEGER :: M

  INTERFACE
    INTEGER(C_INT) FUNCTION PRJPTC_C (PRJ, WHAT, VALUE, M) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: PRJ(*), WHAT
      CHARACTER(KIND=C_CHAR, LEN=1) :: VALUE(*)
      INTEGER(C_INT) :: M
    END FUNCTION PRJPTC_C
  END INTERFACE

  PRJPTC = PRJPTC_C (PRJ, WHAT, VALUE, M)
END FUNCTION PRJPTC

!-----------------------------------------------------------------------------

INTEGER FUNCTION PRJGTC (PRJ, WHAT, VALUE)
  INTEGER :: PRJ(*), WHAT
  CHARACTER :: VALUE(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION PRJGTC_C (PRJ, WHAT, VALUE) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: PRJ(*), WHAT
      CHARACTER(KIND=C_CHAR, LEN=1) :: VALUE(*)
    END FUNCTION PRJGTC_C
  END INTERFACE

  PRJGTC = PRJGTC_C (PRJ, WHAT, VALUE)
END FUNCTION PRJGTC

!-----------------------------------------------------------------------------

INTEGER FUNCTION PRJPERR (PRJ, PREFIX)
  INTEGER :: PRJ(*)
  CHARACTER :: PREFIX(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION PRJPERR_C (PRJ, PREFIX) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: PRJ(*)
      CHARACTER(KIND=C_CHAR, LEN=1) :: PREFIX(72)
    END FUNCTION PRJPERR_C
  END INTERFACE

  PRJPERR = PRJPERR_C (PRJ, PREFIX)
END FUNCTION PRJPERR
