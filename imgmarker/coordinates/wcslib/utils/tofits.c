/*============================================================================
  WCSLIB 8.4 - an implementation of the FITS WCS standard.
  Copyright (C) 1995-2024, Mark Calabretta

  This file is part of WCSLIB.

  WCSLIB is free software: you can redistribute it and/or modify it under the
  terms of the GNU Lesser General Public License as published by the Free
  Software Foundation, either version 3 of the License, or (at your option)
  any later version.

  WCSLIB is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
  FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for
  more details.

  You should have received a copy of the GNU Lesser General Public License
  along with WCSLIB.  If not, see http://www.gnu.org/licenses.

  Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
  http://www.atnf.csiro.au/people/Mark.Calabretta
  $Id: tofits.c,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
*=============================================================================
* Usage: tofits [< <infile>] [> <outfile>]
*-----------------------------------------------------------------------------
* tofits turns a list of FITS header keyrecords, one per line, into a proper
* FITS header.  Refer to the usage notes below.
*===========================================================================*/

char usage[] =
"tofits turns a list of FITS header keyrecords, one per line, into a proper\n"
"FITS header by padding them with blanks to 80 characters and stripping out\n"
"newline characters.  It also pads the header to an integral number of 2880-\n"
"byte blocks if necessary.\n"
"\n"
"The input byte stream is assumed to be ASCII-encoded.  Characters outside\n"
"the set of text characters allowed by FITS (ASCII 0x20 to 0x7E) are ignored\n"
"with the sole exception that a byte with value 0xA0 (non-breaking space in\n"
"all variants of ISO/IEC 8859) is translated to an ordinary space (0x20).\n"
"Thus input encoded in ISO/IEC 8859 or UTF-8 should be interpreted correctly,\n"
"with any illegal characters in keycomments simply being ignored.\n"
"\n"
"tofits has no options and operates as a filter, reading from stdin and\n"
"writing to stdout, e.g.\n"
"\n"
"    tofits < infile > outfile\n"
"\n"
"Input lines beginning with '#' are treated as comments.\n";

#include <stdio.h>

int main(int argc, char **argv)

{
  // Avert nuisance compiler warnings about unused parameters.
  (void)argv;

  // Print usage if any arguments are given.
  if (argc > 1) {
    fprintf(stderr, "%s", usage);
    return 1;
  }

  int c, i = 0, nkeyrec = 0;

  while ((c = getchar()) != EOF) {
    if (c == 0xA0) {
      // Translate non-breaking space.
      c = 0x20;
    }

    if (c == '\n') {
      // Blank-fill the keyrecord.
      while (i++ < 80) {
        putchar(' ');
      }
      i = 0;
      nkeyrec++;

    } else if (c == '#' && i == 0) {
      // Discard comments.
      while ((c = getchar()) != EOF) {
        if (c == '\n') break;
      }

    } else if (c < 0x20 || 0x7E < c) {
      // ASCII escape code or 8-bit ASCII, ignore it.
      continue;

    } else {
      putchar(c);
      i++;
    }
  }

  // Pad to a multiple of 2880-bytes.
  if (nkeyrec %= 36) {
    while (nkeyrec++ < 36) {
      i = 0;
      while (i++ < 80) {
        putchar(' ');
      }
    }
  }

  return 0;
}
