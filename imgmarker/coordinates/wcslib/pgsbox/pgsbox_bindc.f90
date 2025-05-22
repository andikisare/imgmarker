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
! $Id: pgsbox_bindc.f90,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
!=============================================================================

SUBROUTINE PGSBOK_C (BLC, TRC, IDENTS, OPT, LABCTL, LABDEN, CI, GCODE, &
                     TIKLEN, NG1, GRID1, NG2, GRID2, DOEQ, NLFUNC, NLC, NLI, &
                     NLD, NLCPRM, NLIPRM, NLDPRM, NC, IC, CACHE, IERR) BIND (C)

  USE ISO_C_BINDING

  REAL (KIND=C_FLOAT)  :: BLC(2), TRC(2)
  CHARACTER (KIND=C_CHAR, LEN=1) :: IDENTS(80,3), OPT(2)
  INTEGER (KIND=C_INT) :: LABCTL, LABDEN, CI(7), GCODE(2)
  REAL (KIND=C_DOUBLE) :: TIKLEN
  INTEGER (KIND=C_INT) :: NG1
  REAL (KIND=C_DOUBLE) :: GRID1(0:NG1)
  INTEGER (KIND=C_INT) :: NG2
  REAL (KIND=C_DOUBLE) :: GRID2(0:NG2)
  INTEGER (KIND=C_INT) :: DOEQ
  TYPE (C_FUNPTR), VALUE :: NLFUNC
  INTEGER (KIND=C_INT) :: NLC, NLI, NLD
  CHARACTER (KIND=C_CHAR, LEN=1) :: NLCPRM(NLC)
  INTEGER (KIND=C_INT) :: NLIPRM(NLI)
  REAL (KIND=C_DOUBLE) :: NLDPRM(NLD)
  INTEGER (KIND=C_INT) :: NC, IC
  REAL (KIND=C_DOUBLE) :: CACHE(4,0:NC)
  INTEGER (KIND=C_INT) :: IERR

  INTERFACE
    SUBROUTINE PGSBOX (BLC, TRC, IDENTS, OPT, LABCTL, LABDEN, CI, GCODE, &
                       TIKLEN, NG1, GRID1, NG2, GRID2, DOEQ, NLFUNC, NLC, &
                       NLI, NLD, NLCPRM, NLIPRM, NLDPRM, NC, IC, CACHE, IERR)
      REAL      :: BLC(2), TRC(2)
      CHARACTER :: IDENTS(80,3)*1, OPT(2)*1
      INTEGER   :: LABCTL, LABDEN, CI(7), GCODE(2)
      DOUBLE PRECISION :: TIKLEN
      INTEGER   :: NG1
      DOUBLE PRECISION :: GRID1(0:NG1)
      INTEGER   :: NG2
      DOUBLE PRECISION :: GRID2(0:NG2)
      LOGICAL   :: DOEQ
      EXTERNAL  :: NLFUNC
      INTEGER   :: NLC, NLI, NLD
      CHARACTER :: NLCPRM(NLC)
      INTEGER   :: NLIPRM(NLI)
      DOUBLE PRECISION :: NLDPRM(NLD)
      INTEGER   :: NC, IC
      DOUBLE PRECISION :: CACHE(4,0:NC)
      INTEGER   :: IERR
    END SUBROUTINE PGSBOX
  END INTERFACE

  ABSTRACT INTERFACE
    SUBROUTINE NLFUNC_I (OPCODE, NLC, NLI, NLD, NLCPRM, NLIPRM, NLDPRM, &
                         WORLD, XY, CONTRL, CONTXT, IERR)
      INTEGER, INTENT(IN) :: OPCODE, NLC, NLI, NLD
      CHARACTER :: NLCPRM(NLC)*1
      INTEGER   :: NLIPRM(NLI)
      DOUBLE PRECISION :: NLDPRM(NLD), WORLD(2), XY(2)
      INTEGER   :: CONTRL
      DOUBLE PRECISION :: CONTXT(20)
      INTEGER   :: IERR
    END SUBROUTINE NLFUNC_I
  END INTERFACE

  PROCEDURE(NLFUNC_I), POINTER :: NLFUNC_

  ! Do necessary translations.
  LOGICAL DOEQ_
  DOEQ_ = DOEQ .NE. 0

  CALL C_F_PROCPOINTER (NLFUNC, NLFUNC_)

  CALL PGSBOX (BLC, TRC, IDENTS, OPT, LABCTL, LABDEN, CI, GCODE, TIKLEN, &
               NG1, GRID1, NG2, GRID2, DOEQ_, NLFUNC_, NLC, NLI, NLD, &
               NLCPRM, NLIPRM, NLDPRM, NC, IC, CACHE, IERR)
  RETURN
END SUBROUTINE PGSBOK_C

!-----------------------------------------------------------------------------

SUBROUTINE PGLBOK_C (IDENTS, OPT, LABCTL, LABDEN, CI, GCODE, TIKLEN, NG1, &
                    GRID1, NG2, GRID2, DOEQ, NC, IC, CACHE, IERR) BIND (C)

  USE ISO_C_BINDING

  CHARACTER (KIND=C_CHAR, LEN=1) :: IDENTS(80,3), OPT(2)
  INTEGER (KIND=C_INT) :: LABCTL, LABDEN, CI(7), GCODE(2)
  REAL (KIND=C_DOUBLE) :: TIKLEN
  INTEGER (KIND=C_INT) :: NG1
  REAL (KIND=C_DOUBLE) :: GRID1(0:NG1)
  INTEGER (KIND=C_INT) :: NG2
  REAL (KIND=C_DOUBLE) :: GRID2(0:NG1)
  INTEGER (KIND=C_INT) :: DOEQ
  INTEGER (KIND=C_INT) :: NC, IC
  REAL (KIND=C_DOUBLE) :: CACHE(4,0:NC)
  INTEGER (KIND=C_INT) :: IERR

  INTERFACE
    SUBROUTINE PGLBOX (IDENTS, OPT, LABCTL, LABDEN, CI, GCODE, TIKLEN, &
                       NG1, GRID1, NG2, GRID2, DOEQ, NC, IC, CACHE, IERR)
      CHARACTER :: IDENTS(80,3)*1, OPT(2)*1
      INTEGER   :: LABCTL, LABDEN, CI(7), GCODE(2)
      DOUBLE PRECISION :: TIKLEN
      INTEGER   :: NG1
      DOUBLE PRECISION :: GRID1(0:NG1)
      INTEGER   :: NG2
      DOUBLE PRECISION :: GRID2(0:NG1)
      LOGICAL   :: DOEQ
      INTEGER   :: NC, IC
      DOUBLE PRECISION :: CACHE(4,0:NC)
      INTEGER   :: IERR
    END SUBROUTINE PGLBOX
  END INTERFACE

  ! Do necessary translations.
  LOGICAL DOEQ_
  DOEQ_ = DOEQ .NE. 0

  CALL PGLBOX (IDENTS, OPT, LABCTL, LABDEN, CI, GCODE, TIKLEN, &
               NG1, GRID1, NG2, GRID2, DOEQ_, NC, IC, CACHE, IERR)
  RETURN
END SUBROUTINE PGLBOK_C
