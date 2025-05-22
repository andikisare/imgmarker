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
! $Id: fitshdr_bindc.f90,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
!=============================================================================

INTEGER FUNCTION KEYIDPTC (KEYID, I, WHAT, VALUE)
  INTEGER :: KEYID(*), I, WHAT
  CHARACTER :: VALUE(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION KEYIDPTC_C (KEYID, I, WHAT, VALUE) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: KEYID(*), I, WHAT
      CHARACTER(KIND=C_CHAR, LEN=1) :: VALUE(*)
    END FUNCTION KEYIDPTC_C
  END INTERFACE

  KEYIDPTC = KEYIDPTC_C (KEYID, I, WHAT, VALUE)
END FUNCTION KEYIDPTC

!-----------------------------------------------------------------------------

INTEGER FUNCTION KEYIDGTC (KEYID, I, WHAT, VALUE)
  INTEGER :: KEYID(*), I, WHAT
  CHARACTER :: VALUE(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION KEYIDGTC_C (KEYID, I, WHAT, VALUE) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: KEYID(*), I, WHAT
      CHARACTER(KIND=C_CHAR, LEN=1) :: VALUE(*)
    END FUNCTION KEYIDGTC_C
  END INTERFACE

  KEYIDGTC = KEYIDGTC_C (KEYID, I, WHAT, VALUE)
END FUNCTION KEYIDGTC

!-----------------------------------------------------------------------------

INTEGER FUNCTION KEYGTC (KEYS, I, WHAT, VALUE, NC)
  INTEGER :: KEYS(*), I, WHAT
  CHARACTER :: VALUE(*)
  INTEGER :: NC

  INTERFACE
    INTEGER(C_INT) FUNCTION KEYGTC_C (KEYS, I, WHAT, VALUE, NC) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: KEYS(*), I, WHAT
      CHARACTER(KIND=C_CHAR, LEN=1) :: VALUE(*)
      INTEGER(C_INT) :: NC
    END FUNCTION KEYGTC_C
  END INTERFACE

  KEYGTC = KEYGTC_C (KEYS, I, WHAT, VALUE, NC)
END FUNCTION KEYGTC

!-----------------------------------------------------------------------------

INTEGER FUNCTION FITSHDR (HEADER, NKEYREC, NKEYIDS, KEYIDS, NREJECT, KEYS)
  CHARACTER :: HEADER(*)
  INTEGER :: NKEYREC, NKEYIDS, KEYIDS, NREJECT, KEYS(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION FITSHDR_C (HEADER, NKEYREC, NKEYIDS, KEYIDS, &
                                       NREJECT, KEYS) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      CHARACTER(KIND=C_CHAR, LEN=1) :: HEADER(*)
      INTEGER(C_INT) :: NKEYREC, NKEYIDS, KEYIDS, NREJECT, KEYS(*)
    END FUNCTION FITSHDR_C
  END INTERFACE

  FITSHDR = FITSHDR_C (HEADER, NKEYREC, NKEYIDS, KEYIDS, NREJECT, KEYS)
END FUNCTION FITSHDR
