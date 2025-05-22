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
! $Id: wcshdr_bindc.f90,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
!=============================================================================

INTEGER FUNCTION WCSPIH (HEADER, NKEYS, RELAX, CTRL, NREJECT, NWCS, WCSP)
  CHARACTER :: HEADER(*)
  INTEGER :: NKEYS, RELAX, CTRL, NREJECT, NWCS, WCSP(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSPIH_C (HEADER, NKEYS, RELAX, CTRL, NREJECT, &
                                      NWCS, WCSP) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      CHARACTER(KIND=C_CHAR, LEN=1) :: HEADER(*)
      INTEGER(C_INT) :: NKEYS, RELAX, CTRL, NREJECT, NWCS, WCSP(*)
    END FUNCTION WCSPIH_C
  END INTERFACE

  WCSPIH = WCSPIH_C (HEADER, NKEYS, RELAX, CTRL, NREJECT, NWCS, WCSP)
END FUNCTION WCSPIH

!-----------------------------------------------------------------------------

INTEGER FUNCTION WCSBTH (HEADER, NKEYS, RELAX, CTRL, KEYSEL, COLSEL, &
                         NREJECT, NWCS, WCSP)
  CHARACTER :: HEADER(*)
  INTEGER :: NKEYS, RELAX, CTRL, KEYSEL, COLSEL, NREJECT, NWCS, WCSP(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION WCSBTH_C (HEADER, NKEYS, RELAX, CTRL, KEYSEL, &
                                      COLSEL, NREJECT, NWCS, WCSP) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      CHARACTER(KIND=C_CHAR, LEN=1) :: HEADER(*)
      INTEGER(C_INT) :: NKEYS, RELAX, CTRL, KEYSEL, COLSEL, NREJECT, NWCS, &
                        WCSP(*)
    END FUNCTION WCSBTH_C
  END INTERFACE

  WCSBTH = WCSBTH_C (HEADER, NKEYS, RELAX, CTRL, KEYSEL, COLSEL, NREJECT, &
                     NWCS, WCSP)
END FUNCTION WCSBTH
