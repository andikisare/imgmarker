*=======================================================================
*
* PGSBOX 8.4 - draw curvilinear coordinate axes for PGPLOT.
* Copyright (C) 1997-2024, Mark Calabretta
*
* This file is part of PGSBOX.
*
* PGSBOX is free software: you can redistribute it and/or modify it
* under the terms of the GNU Lesser General Public License as published
* by the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* PGSBOX is distributed in the hope that it will be useful, but WITHOUT
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
* FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
* License for more details.
*
* You should have received a copy of the GNU Lesser General Public
* License along with PGSBOX.  If not, see http://www.gnu.org/licenses.
*
* Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
* http://www.atnf.csiro.au/people/Mark.Calabretta
* $Id: lngvel.F,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
*=======================================================================
*
* LNGVEL defines a longitude/velocity coordinate system for the PGSBOX
* test programs (only).
*
* The second (Y) axis is assumed to be equispaced in frequency but
* required to be labelled with the relativistic Doppler velocity.
*
* Given:
*   OPCODE    I         Transformation code:
*                         +2: Compute a set of pixel coordinates that
*                             describe a path between this and the
*                             previous pair of world coordinates
*                             remembered from the last call with
*                             OPCODE = +1 or +2.
*                         +1: Compute pixel coordinates from world
*                             coordinates.
*                          0: Initialize.
*                         -1: Compute world coordinates from pixel
*                             coordinates.
*
*   NLC       I         Number of elements in NLCPRM (=1).
*
*   NLI       I         Number of elements in NLIPRM (=1).
*
*   NLD       I         Number of elements in NLDPRM (=7).
*
*   NLCPRM    C(NLC)*1  Character array (not used).
*
*   NLIPRM    I(NLI)    Integer array (not used).
*
* Given and/or returned:
*   NLDPRM    D(NLD)    Double precision coefficients (see below).
*
*   WORLD     D(2)      World coordinates.  WORLD(1) and WORLD(2) are
*                       the longitude and velocity, in degrees and m/s.
*                       Given if OPCODE > 0, returned if OPCODE < 0.
*
*   PIXEL     D(2)      Pixel coordinates.
*                       Given if OPCODE < 0, returned if OPCODE > 0.
*
*   CONTRL    I         Control flag for OPCODE = +2 (ignored, always
*                       set to 0 on return).
*
*   CONTXT    D(20)     Context elements (ignored).
*
* Returned:
*   IERR      I         Status return value:
*                         0: Success.
*                         1: Invalid coordinate transformation
*                            parameters.
*
* Notes:
*   The NLDPRM array is constructed as follows:
*     - (1)  Axis 1 reference pixel coordinate
*     - (2)  Axis 2 reference pixel coordinate
*     - (3)  Axis 1 reference pixel value (degree)
*     - (4)  Axis 2 reference pixel value (Hz)
*     - (5)  Axis 1 coordinate increment (degree/pixel)
*     - (6)  Axis 2 coordinate increment (Hz/pixel)
*     - (7)  Rest frequency (Hz)
*
*=======================================================================
#ifdef BINDC
      SUBROUTINE LNGVEL_ (OPCODE, NLC, NLI, NLD, NLCPRM, NLIPRM,
     :  NLDPRM, WORLD, PIXEL, CONTRL, CONTXT, IERR) BIND (C)

      USE, INTRINSIC :: ISO_C_BINDING

      INTEGER (KIND=C_INT) :: OPCODE, NLC, NLI, NLD
      CHARACTER (KIND=C_CHAR, LEN=1) :: NLCPRM(NLC)
      INTEGER (KIND=C_INT) :: NLIPRM(NLI)
      REAL (KIND=C_DOUBLE) :: NLDPRM(NLD), WORLD(2), PIXEL(2)
      INTEGER (KIND=C_INT) :: CONTRL
      REAL (KIND=C_DOUBLE) :: CONTXT(20)
      INTEGER (KIND=C_INT) :: IERR
#else
      SUBROUTINE LNGVEL (OPCODE, NLC, NLI, NLD, NLCPRM, NLIPRM,
     :  NLDPRM, WORLD, PIXEL, CONTRL, CONTXT, IERR)

      INTEGER OPCODE, NLC, NLI, NLD
      CHARACTER NLCPRM(NLC)
      INTEGER NLIPRM(NLI)
      DOUBLE PRECISION NLDPRM(NLD), WORLD(2), PIXEL(2)
      INTEGER CONTRL
      DOUBLE PRECISION CONTXT(20)
      INTEGER IERR
#endif
*-----------------------------------------------------------------------
      INTEGER   IDUMMY
      DOUBLE PRECISION CVEL, FREQ, S
      CHARACTER CDUMMY

      PARAMETER (CVEL = 2.99792458D8)
*-----------------------------------------------------------------------
*     Circumvent "unused dummy argument" compiler warnings.
      CONTXT(1) = 0D0
      CDUMMY = NLCPRM(1)
      IDUMMY = NLIPRM(1)

      IERR = 0

      IF (OPCODE.GT.0) THEN
*       Compute pixel coordinates from world coordinates.
        PIXEL(1) =  NLDPRM(1) + (WORLD(1) - NLDPRM(3))/NLDPRM(5)

        S = (CVEL-WORLD(2))/(CVEL+WORLD(2))
        IF (S.LT.0D0) THEN
          IERR = 2
          RETURN
        END IF
        FREQ = NLDPRM(7)*SQRT(S)
        PIXEL(2) =  NLDPRM(2) + (FREQ - NLDPRM(4))/NLDPRM(6)

        CONTRL = 0

      ELSE IF (OPCODE.EQ.0) THEN
*       Initialize.
        IF (NLC.LT.1 .OR. NLI.LT.1 .OR. NLD.LT.7) IERR = 1
        IF (NLDPRM(5).EQ.0D0) IERR = 1
        IF (NLDPRM(6).EQ.0D0) IERR = 1
        IF (NLDPRM(7).EQ.0D0) IERR = 1

        CONTRL = 0

      ELSE IF (OPCODE.EQ.-1) THEN
*       Compute world coordinates from pixel coordinates.
        WORLD(1) = NLDPRM(3) + NLDPRM(5)*(PIXEL(1) - NLDPRM(1))
        FREQ     = NLDPRM(4) + NLDPRM(6)*(PIXEL(2) - NLDPRM(2))
        S = (FREQ/NLDPRM(7))**2
        WORLD(2) = CVEL*(1D0 - S)/(1D0 + S)

      ELSE
        IERR = 1
      END IF


      RETURN
      END
