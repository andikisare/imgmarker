!=============================================================================
!
! PGSBOX 8.4 - draw curvilinear coordinate axes for PGPLOT.
! Copyright (C) 1997-2024, Mark Calabretta
!
! This file is part of PGSBOX.
!
! PGSBOX is free software: you can redistribute it and/or modify it under the
! terms of the GNU Lesser General Public License as published by the Free
! Software Foundation, either version 3 of the License, or (at your option)
! any later version.
!
! PGSBOX is distributed in the hope that it will be useful, but WITHOUT ANY
! WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
! FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for
! more details.
!
! You should have received a copy of the GNU Lesser General Public License
! along with PGSBOX.  If not, see http://www.gnu.org/licenses.
!
! Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
! http://www.atnf.csiro.au/people/Mark.Calabretta
! $Id: pgwcsl_bindc.f90,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
!=============================================================================

SUBROUTINE PGWCSL_ (OPCODE, NLC, NLI, NLD, NLCPRM, WCS, NLDPRM, &
                    WORLD, PIXEL, CONTRL, CONTXT, IERR) BIND (C)

  ! For the sake of backwards compatibility, for applications written in C
  ! using cpgsbox(), a C-compatible interface must be maintained.
  USE, INTRINSIC :: ISO_C_BINDING

  INTEGER (KIND=C_INT) :: OPCODE, NLC, NLI, NLD
  CHARACTER (KIND=C_CHAR, LEN=1) :: NLCPRM(NLC)
  INTEGER (KIND=C_INT) :: WCS(NLI)
  REAL (KIND=C_DOUBLE) :: NLDPRM(NLD), WORLD(2), PIXEL(2)
  INTEGER (KIND=C_INT) :: CONTRL
  REAL (KIND=C_DOUBLE) :: CONTXT(20)
  INTEGER (KIND=C_INT) :: IERR

  INTERFACE
    SUBROUTINE PGWCSL_C (OPCODE, NLC, NLI, NLD, NLCPRM, WCS, NLDPRM, &
                         WORLD, PIXEL, CONTRL, CONTXT, IERR) BIND (C)

      USE, INTRINSIC :: ISO_C_BINDING

      INTEGER (KIND=C_INT) :: OPCODE, NLC, NLI, NLD
      CHARACTER (KIND=C_CHAR, LEN=1) :: NLCPRM(NLC)
      INTEGER (KIND=C_INT) :: WCS(NLI)
      REAL (KIND=C_DOUBLE) :: NLDPRM(NLD), WORLD(2), PIXEL(2)
      INTEGER (KIND=C_INT) :: CONTRL
      REAL (KIND=C_DOUBLE) :: CONTXT(20)
      INTEGER (KIND=C_INT) :: IERR
    END SUBROUTINE PGWCSL_C
  END INTERFACE

  CALL PGWCSL_C (OPCODE, NLC, NLI, NLD, NLCPRM, WCS, NLDPRM, &
                 WORLD, PIXEL, CONTRL, CONTXT, IERR)
  RETURN
END SUBROUTINE PGWCSL_
