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
* $Id: wcsfix_data.f,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=======================================================================

      BLOCK DATA WCSFIX_BLOCK_DATA

      CHARACTER WCSFIX_ERRMSG(-1:10)*80

      COMMON /WCSFIX_DATA/ WCSFIX_ERRMSG

      DATA WCSFIX_ERRMSG /
     :  'No change (not an error)',
     :  'Success',
     :  'Null wcsprm pointer passed',
     :  'Memory allocation failed',
     :  'Linear transformation matrix is singular',
     :  'Inconsistent or unrecognized coordinate axis types',
     :  'Invalid parameter value',
     :  'Invalid coordinate transformation parameters',
     :  'Ill-conditioned coordinate transformation parameters',
     :  'All of the corner pixel coordinates are invalid',
     :  'Could not determine reference pixel coordinate',
     :  'Could not determine reference pixel value'/

      END
