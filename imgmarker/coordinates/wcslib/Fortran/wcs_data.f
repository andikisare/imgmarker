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
* $Id: wcs_data.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      BLOCK DATA WCS_BLOCK_DATA

      CHARACTER WCS_ERRMSG(0:13)*80

      COMMON /WCS_DATA/ WCS_ERRMSG

      DATA WCS_ERRMSG /
     :  'Success',
     :  'Null wcsprm pointer passed',
     :  'Memory allocation failed',
     :  'Linear transformation matrix is singular',
     :  'Inconsistent or unrecognized coordinate axis type',
     :  'Invalid parameter value',
     :  'Unrecognized coordinate transformation parameter',
     :  'Ill-conditioned coordinate transformation parameter',
     :  'One or more of the pixel coordinates were invalid',
     :  'One or more of the world coordinates were invalid',
     :  'Invalid world coordinate',
     :  'No solution found in the specified interval',
     :  'Invalid subimage specification',
     :  'Non-separable subimage coordinate system'/

      END
