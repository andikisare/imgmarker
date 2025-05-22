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
! $Id: dis_bindc.f90,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
!=============================================================================

INTEGER FUNCTION DISPTC (DEREF, DIS, WHAT, VALUE, I, K)
  INTEGER :: DEREF, DIS(*), WHAT
  CHARACTER :: VALUE(*)
  INTEGER :: I, K

  INTERFACE
    INTEGER(C_INT) FUNCTION DISPTC_C (DEREF, DIS, WHAT, VALUE, I, K) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: DEREF, DIS(*), WHAT
      CHARACTER(KIND=C_CHAR, LEN=1) :: VALUE(*)
      INTEGER(C_INT) :: I, K
    END FUNCTION DISPTC_C
  END INTERFACE

  DISPTC = DISPTC_C (DEREF, DIS, WHAT, VALUE, I, K)
END FUNCTION DISPTC

!-----------------------------------------------------------------------------

INTEGER FUNCTION DISGTC (DEREF, DIS, WHAT, VALUE)
  INTEGER :: DEREF, DIS(*), WHAT
  CHARACTER :: VALUE(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION DISGTC_C (DEREF, DIS, WHAT, VALUE) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: DEREF, DIS(*), WHAT
      CHARACTER(KIND=C_CHAR, LEN=1) :: VALUE(*)
    END FUNCTION DISGTC_C
  END INTERFACE

  DISGTC = DISGTC_C (DEREF, DIS, WHAT, VALUE)
END FUNCTION DISGTC

!-----------------------------------------------------------------------------

INTEGER FUNCTION DPFILL (DP, KEYWORD, FIELD, J, TYPE, IVAL, FVAL)
  INTEGER :: DP
  CHARACTER :: KEYWORD(*), FIELD(*)
  INTEGER :: J, TYPE, IVAL
  DOUBLE PRECISION FVAL

  INTERFACE
    INTEGER(C_INT) FUNCTION DPFILL_C (DP, KEYWORD, FIELD, J, TYPE, IVAL, &
                                      FVAL) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: DP
      CHARACTER(KIND=C_CHAR, LEN=1) :: KEYWORD(72), FIELD(72)
      INTEGER(C_INT) :: J, TYPE, IVAL
      REAL(C_DOUBLE) :: FVAL
    END FUNCTION DPFILL_C
  END INTERFACE

  DPFILL = DPFILL_C (DP, KEYWORD, FIELD, J, TYPE, IVAL, FVAL)
END FUNCTION DPFILL

!-----------------------------------------------------------------------------

INTEGER FUNCTION DISPERR (DEREF, DIS, PREFIX)
  INTEGER :: DEREF, DIS(*)
  CHARACTER :: PREFIX(*)

  INTERFACE
    INTEGER(C_INT) FUNCTION DISPERR_C (DEREF, DIS, PREFIX) BIND (C)
      USE, INTRINSIC :: ISO_C_BINDING
      INTEGER(C_INT) :: DEREF, DIS(*)
      CHARACTER(KIND=C_CHAR, LEN=1) :: PREFIX(72)
    END FUNCTION DISPERR_C
  END INTERFACE

  DISPERR = DISPERR_C (DEREF, DIS, PREFIX)
END FUNCTION DISPERR
