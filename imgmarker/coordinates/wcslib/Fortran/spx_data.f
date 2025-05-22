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
* $Id: spx_data.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      BLOCK DATA SPX_BLOCK_DATA

      CHARACTER SPX_ERRMSG(0:4)*80

      COMMON /SPX_DATA/ SPX_ERRMSG

      DATA SPX_ERRMSG /
     :  'Success',
     :  'Null spxprm pointer passed',
     :  'Invalid spectral parameters',
     :  'Invalid spectral variable',
     :  'One or more of the inspec coordinates were invalid'/

      END
