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
! $Id: lin_bindc.f90,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
!=============================================================================

INTEGER FUNCTION LINPERR (LIN, PREFIX)
  INTEGER :: LIN(*)
  CHARACTER :: PREFIX(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION LINPERR_C (LIN, PREFIX) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: LIN(*)
      CHARACTER(KIND=C_CHAR, LEN=1) :: PREFIX(72)
    END FUNCTION LINPERR_C
  END INTERFACE

  LINPERR = LINPERR_C (LIN, PREFIX)
END FUNCTION LINPERR
