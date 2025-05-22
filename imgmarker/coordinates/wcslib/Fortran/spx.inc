*=======================================================================
* WCSLIB 8.4 - an implementation of the FITS WCS standard.
* Copyright (C) 1995-2024, Mark Calabretta
*
* This file is part of WCSLIB.
*
* WCSLIB is free software: you can redistribute it and/or modify it
* under the terms of the GNU Lesser General Public License as published
* by the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* WCSLIB is distributed in the hope that it will be useful, but WITHOUT
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
* FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
* License for more details.
*
* You should have received a copy of the GNU Lesser General Public
* License along with WCSLIB.  If not, see http://www.gnu.org/licenses.
*
* Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
* http://www.atnf.csiro.au/people/Mark.Calabretta
* $Id: spx.inc,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

*     Functions.
      EXTERNAL SPECX, SPXGET, SPXGTI,
     :         FREQAFRQ, AFRQFREQ, FREQENER, ENERFREQ,
     :         FREQWAVN, WAVNFREQ, FREQVRAD, VRADFREQ,
     :         FREQWAVE, WAVEFREQ, FREQAWAV, AWAVFREQ,
     :         FREQVELO, VELOFREQ, WAVEVOPT, VOPTWAVE,
     :         WAVEZOPT, ZOPTWAVE, WAVEAWAV, AWAVWAVE,
     :         WAVEVELO, VELOWAVE, AWAVVELO, VELOAWAV,
     :         VELOBETA, BETAVELO
      INTEGER  SPECX, SPXGET, SPXGTI,
     :         FREQAFRQ, AFRQFREQ, FREQENER, ENERFREQ,
     :         FREQWAVN, WAVNFREQ, FREQVRAD, VRADFREQ,
     :         FREQWAVE, WAVEFREQ, FREQAWAV, AWAVFREQ,
     :         FREQVELO, VELOFREQ, WAVEVOPT, VOPTWAVE,
     :         WAVEZOPT, ZOPTWAVE, WAVEAWAV, AWAVWAVE,
     :         WAVEVELO, VELOWAVE, AWAVVELO, VELOAWAV,
     :         VELOBETA, BETAVELO

*     Length of the SPXPRM data structure (INTEGER array) on 64-bit
*     machines.  Only needs to be 82 on 32-bit machines.
      INTEGER   SPXLEN
      PARAMETER (SPXLEN = 84)

*     Spectral data structure.
      INTEGER   SPX_WAVETYPE,  SPX_VELOTYPE
      DOUBLE PRECISION
     :          SPX_RESTFRQ, SPX_RESTWAV, SPX_TYPES,
     :          SPX_FREQ, SPX_AFRQ, SPX_ENER,  SPX_WAVN,
     :          SPX_VRAD, SPX_WAVE, SPX_VOPT,  SPX_ZOPT,
     :          SPX_AWAV, SPX_VELO, SPX_BETA,
     :          SPX_DFREQAFRQ, SPX_DAFRQFREQ, SPX_DFREQENER,
     :          SPX_DENERFREQ, SPX_DFREQWAVN, SPX_DWAVNFREQ,
     :          SPX_DFREQVRAD, SPX_DVRADFREQ, SPX_DFREQWAVE,
     :          SPX_DWAVEFREQ, SPX_DFREQAWAV, SPX_DAWAVFREQ,
     :          SPX_DFREQVELO, SPX_DVELOFREQ, SPX_DWAVEVOPT,
     :          SPX_DVOPTWAVE, SPX_DWAVEZOPT, SPX_DZOPTWAVE,
     :          SPX_DWAVEAWAV, SPX_DAWAVWAVE, SPX_DWAVEVELO,
     :          SPX_DVELOWAVE, SPX_DAWAVVELO, SPX_DVELOAWAV,
     :          SPX_DVELOBETA, SPX_DBETAVELO

*     Direct equivalences into the data structure (not indexing codes).
      DOUBLE PRECISION SPX(41)
      EQUIVALENCE (SPX( 1), SPX_RESTFRQ)
      EQUIVALENCE (SPX( 2), SPX_RESTWAV)
      EQUIVALENCE (SPX( 3), SPX_TYPES)
      EQUIVALENCE (SPX( 4), SPX_FREQ)
      EQUIVALENCE (SPX( 5), SPX_AFRQ)
      EQUIVALENCE (SPX( 6), SPX_ENER)
      EQUIVALENCE (SPX( 7), SPX_WAVN)
      EQUIVALENCE (SPX( 8), SPX_VRAD)
      EQUIVALENCE (SPX( 9), SPX_WAVE)
      EQUIVALENCE (SPX(10), SPX_VOPT)
      EQUIVALENCE (SPX(11), SPX_ZOPT)
      EQUIVALENCE (SPX(12), SPX_AWAV)
      EQUIVALENCE (SPX(13), SPX_VELO)
      EQUIVALENCE (SPX(14), SPX_BETA)
      EQUIVALENCE (SPX(15), SPX_DFREQAFRQ)
      EQUIVALENCE (SPX(16), SPX_DAFRQFREQ)
      EQUIVALENCE (SPX(17), SPX_DFREQENER)
      EQUIVALENCE (SPX(18), SPX_DENERFREQ)
      EQUIVALENCE (SPX(19), SPX_DFREQWAVN)
      EQUIVALENCE (SPX(20), SPX_DWAVNFREQ)
      EQUIVALENCE (SPX(21), SPX_DFREQVRAD)
      EQUIVALENCE (SPX(22), SPX_DVRADFREQ)
      EQUIVALENCE (SPX(23), SPX_DFREQWAVE)
      EQUIVALENCE (SPX(24), SPX_DWAVEFREQ)
      EQUIVALENCE (SPX(25), SPX_DFREQAWAV)
      EQUIVALENCE (SPX(26), SPX_DAWAVFREQ)
      EQUIVALENCE (SPX(27), SPX_DFREQVELO)
      EQUIVALENCE (SPX(28), SPX_DVELOFREQ)
      EQUIVALENCE (SPX(29), SPX_DWAVEVOPT)
      EQUIVALENCE (SPX(30), SPX_DVOPTWAVE)
      EQUIVALENCE (SPX(31), SPX_DWAVEZOPT)
      EQUIVALENCE (SPX(32), SPX_DZOPTWAVE)
      EQUIVALENCE (SPX(33), SPX_DWAVEAWAV)
      EQUIVALENCE (SPX(34), SPX_DAWAVWAVE)
      EQUIVALENCE (SPX(35), SPX_DWAVEVELO)
      EQUIVALENCE (SPX(36), SPX_DVELOWAVE)
      EQUIVALENCE (SPX(37), SPX_DAWAVVELO)
      EQUIVALENCE (SPX(38), SPX_DVELOAWAV)
      EQUIVALENCE (SPX(39), SPX_DVELOBETA)
      EQUIVALENCE (SPX(40), SPX_DBETAVELO)

      INTEGER   SPXI(2)
      EQUIVALENCE (SPXI,    SPX_TYPES)
      EQUIVALENCE (SPXI(1), SPX_WAVETYPE)
      EQUIVALENCE (SPXI(2), SPX_VELOTYPE)

*     Codes for SPX data structure elements used by SPXGET (only).
      INTEGER   SPX_ERR

      PARAMETER (SPX_ERR     = 200)

*     Error codes and messages.
      INTEGER   SPXERR_SUCCESS, SPXERR_NULL_POINTER,
     :          SPXERR_BAD_SPEC_PARAMS, SPXERR_BAD_SPEC_VAR,
     :          SPXERR_BAD_INSPEC_COORD

      PARAMETER (SPXERR_SUCCESS          = 0)
      PARAMETER (SPXERR_NULL_POINTER     = 1)
      PARAMETER (SPXERR_BAD_SPEC_PARAMS  = 2)
      PARAMETER (SPXERR_BAD_SPEC_VAR     = 3)
      PARAMETER (SPXERR_BAD_INSPEC_COORD = 4)

      CHARACTER SPX_ERRMSG(0:4)*80
      COMMON /SPX_DATA/ SPX_ERRMSG
