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
  $Id: wcsware.c,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
*=============================================================================
* Usage: wcsware [<option>]... [<fitsfile>]
*-----------------------------------------------------------------------------
* wcsware extracts the WCS keywords for an image from the specified FITS file,
* constructs wcsprm structs for each coordinate representation found and
* performs a variety of operations using them.  Refer to the usage notes
* below.
*---------------------------------------------------------------------------*/

char usage[] =
"Usage: wcsware [<option>]... [<fitsfile>]\n"
"\n"
"wcsware extracts the WCS keywords for an image from the specified FITS\n"
"file, constructs wcsprm structs for each coordinate representation found\n"
"and performs a variety of operations using them.  It features a \"lint\"\n"
"capability as one of its more useful operations.\n\n"
"By default, all known extensions to the FITS WCS standard are allowed,\n"
"including deprecated usage.  However, in \"lint\" mode, strict conformance\n"
"to the standard is enforced.\n\n"
"The FITS file may be specified according to the syntax understood by\n"
"cfitsio, for example \"file.fits.gz+1\" refers to the first extension (the\n"
"second HDU) of a gzip'd FITS file.  Use \"-\" or omit the file name for\n"
"input from stdin.\n"
"\n"
"Options:\n"
"  -a<alt>      Specify an alternate coordinate representation (ignored if\n"
"               there is only one).  Can also be specified as a 0-relative\n"
"               index in the range 0 to 26, where alternates are sequenced\n"
"               alphabetically following the primary representation.\n"
"  -b           Use wcsbth() for primary image headers, normally wcspih()\n"
"               is used.  (Implies -i.)\n"
"  -c           Apply wcspcx() to the wcsprm struct to decompose CDi_ja\n"
"               into PCi_ja and CDELTia.\n"
"  -cp          As for -c, and also unscramble axes.\n"
"  -C           As for -c, decompose CDi_ja if present, otherwise recompose\n"
"               PCi_ja and CDELTia.\n"
"  -Cp          As for -C, and also unscramble axes.\n"
"  -f           Apply wcsfix() to the header.\n"
"  -h<hdu>      Move to HDU number (1-relative) which is expected to\n"
"               contain an image array.  Overrides cfitsio extended\n"
"               filename syntax.  Also useful for input from stdin.\n"
"  -i           Allow image header WCS keywords in binary table headers.\n"
"  -l           Validate (lint) the WCS keyrecords in the specified FITS\n"
"               header for conformance to the WCS standard.  (Implies -s.)\n"
"  -m           Apply wcstrim() to the wcsprm struct.\n"
"  -o           Use wcshdo() to translate the wcsprm struct into a FITS\n"
"               header and print it.\n"
"  -p           Print the struct(s) using wcsprt() (default operation).\n"
"  -P           Same as -p but don't print a default struct.\n"
"  -r           Require strict adherence to the FITS WCS standard, though\n"
"               allowing the deprecated AIPS-convention keywords, CROTAn,\n"
"               EPOCH, and VELREF, and also some other deprecated usage.\n"
"               (Must follow -l if relaxed linting is required.)\n"
"  -s           Require strict adherence to the FITS WCS standard,\n"
"               disallowing all deprecated features.\n"
"  -t           Terse (with -l), report rejected WCS keyrecords only.\n"
"  -v           Verbose (with -l), report recognised WCS keyrecords as well.\n"
"  -w           Convert world coordinates, obtained from stdin, to pixel\n"
"               coordinates using wcss2p().\n"
"  -x           Convert pixel coordinates, obtained from stdin, to world\n"
"               coordinates using wcsp2s().\n"
"  -z           Print the size of the wcsprm struct, including allocated\n"
"               memory.\n";

#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <fitsio.h>

#include <tab.h>
#include <wcs.h>
#include <wcshdr.h>
#include <wcsfix.h>
#include <wcsprintf.h>
#include <getwcstab.h>

int main(int argc, char **argv)

{
  // Parse options.
  int allimg =  0;
  int ctrl   = -3;
  int dobth  =  0;
  int dofix  =  0;
  int dohdr  =  0;
  int dolint =  0;
  int dopcx  =  0;
  int doperm =  0;
  int dopix  =  0;
  int doprt  =  0;
  int dosize =  0;
  int dotrim =  0;
  int dowrld =  0;
  int hdunum =  0;
  int relax  = WCSHDR_all;
  int strict =  0;

  char *alt = 0x0;

  int iopt;
  for (iopt = 1; iopt < argc && argv[iopt][0] == '-'; iopt++) {
    if (!argv[iopt][1]) break;

    switch (argv[iopt][1]) {
    case 'a':
      // Select an alternate WCS.
      alt = argv[iopt]+2;
      break;

    case 'b':
      // Use wcsbth() for image headers.
      dobth  = 1;
      allimg = 1;
      break;

    case 'c':
      // Apply wcspcx().
      dopcx  = 1;
      doperm = (argv[iopt][2] == 'p');
      break;

    case 'C':
      // Apply wcspcx() with dopc == 1.
      dopcx  = 2;
      doperm = (argv[iopt][2] == 'p');
      break;

    case 'f':
      // Apply wcsfix().
      dofix  = 1;
      break;

    case 'h':
      // Move to HDU number.
      hdunum = atoi(argv[iopt]+2);
      if (hdunum < 0) {
        hdunum = 0;
        wcsfprintf(stderr, "wcsware: Invalid HDU number ignored.\n");
      }
      break;

    case 'i':
      // Allow image header keywords in bintables.
      allimg = 1;
      break;

    case 'l':
      // WCS lint.
      strict = 1;
      relax  = WCSHDR_strict;
      ctrl   = 3;
      dolint = 1;
      break;

    case 'm':
      // Apply wcstrim().
      dotrim = 1;
      break;

    case 'o':
      // Print header using wcshdo().
      dohdr = 1;
      break;

    case 'p':
      // Print structs.
      doprt  = 1;
      break;

    case 'P':
      // Print non-default structs.
      doprt  = -1;
      break;

    case 'r':
      // Strict, but allow some deprecated usage.
      strict = 0;
      relax  = WCSHDR_reject;
      break;

    case 's':
      // Strict, really strict.
      strict = 1;
      relax  = WCSHDR_strict;
      break;

    case 't':
      // Terse.
      ctrl   = 2;
      break;

    case 'v':
      // Verbose.
      ctrl   = 4;
      break;

    case 'w':
      // Convert world coordinates to pixel coordinates.
      dowrld = 1;
      break;

    case 'x':
      // Convert pixel coordinates to world coordinates.
      dopix  = 1;
      break;

    case 'z':
      // Print the full size of the wcsprm struct.
      dosize = 1;
      break;

    default:
      wcsfprintf(stderr, "%s", usage);
      return 1;
    }
  }

  if (allimg) {
    relax |= WCSHDR_ALLIMG;
  }

  char *infile;
  if (iopt < argc) {
    infile = argv[iopt++];

    if (iopt < argc) {
      wcsfprintf(stderr, "%s", usage);
      return 1;
    }
  } else {
    infile = "-";
  }

  if (!(dolint || dohdr || doprt || dopix || dowrld)) {
    doprt  = 1;
    dotrim = 1;
  }


  // Open the FITS file and move to the required HDU.
  int fitstat = 0;
  fitsfile *fptr;
  if (fits_open_file(&fptr, infile, READONLY, &fitstat)) goto cleanup;

  int hdutype;
  if (hdunum) {
    if (fits_movabs_hdu(fptr, hdunum, &hdutype, &fitstat)) goto cleanup;
  } else {
    if (fits_get_hdu_type(fptr, &hdutype, &fitstat)) goto cleanup;
  }

  // Read in the FITS header, excluding COMMENT and HISTORY keyrecords.
  char *header;
  int nkeyrec;
  if (fits_hdr2str(fptr, 1, NULL, 0, &header, &nkeyrec, &fitstat)) {
    goto cleanup;
  }


  // Interpret the WCS keywords.
  int keysel, nreject, nwcs, status;
  struct wcsprm *wcs;
  if ((hdutype == BINARY_TBL) ||
     ((hdutype == IMAGE_HDU) && dobth)) {
    keysel = (hdutype == BINARY_TBL) ? 0 : WCSHDR_IMGHEAD;
    if ((status = wcsbth(header, nkeyrec, relax, ctrl, keysel, 0x0, &nreject,
                    &nwcs, &wcs))) {
      wcsfprintf(stderr, "wcsbth ERROR %d: %s.\n", status,
                 wcshdr_errmsg[status]);
      goto cleanup;
    }
  } else if (hdutype == IMAGE_HDU) {
    if ((status = wcspih(header, nkeyrec, relax, ctrl, &nreject,
                    &nwcs, &wcs))) {
      wcsfprintf(stderr, "wcspih ERROR %d: %s.\n", status,
                 wcshdr_errmsg[status]);
      goto cleanup;
    }
  } else {
    wcsfprintf(stderr, "wcsware: Invalid FITS extension type.\n");
    goto cleanup;
  }

  free(header);

  if (nreject) {
    if (ctrl <= 3) {
      wcsprintf("\n%d WCS keyrecords were rejected.\n", nreject);
    }
    wcsprintf("\nThe rejected keyrecords do not conform%s to the FITS WCS "
              "standard.\n", strict?" strictly":"");
  } else if (nwcs == 0) {
    if (2 < ctrl) wcsprintf("\n");
    wcsprintf("No world coordinate systems found.\n");
    fits_close_file(fptr, &fitstat);
    return 0;

  } else if (2 < ctrl) {
    wcsprintf("\nNo invalid WCS keyrecords were found.\n");
  }


  // Sort out alternates.
  int  alts[27];
  struct wcsprm *wcsi = 0x0;
  if (alt) {
    int i = 0;

    if ('0' <= *alt && *alt <= '9') {
      if ((i = atoi(alt)) > nwcs-1) {
        wcsfprintf(stderr, "WARNING, no alternate coordinate "
          "representation \"%s\".\n", alt);
        goto cleanup;
      }

    } else {
      wcsidx(nwcs, &wcs, alts);

      int ialt = toupper(*alt);
      if (strlen(alt) > 1) {
        wcsfprintf(stderr, "WARNING, alternate specifier \"%s\" is "
          "invalid.\n", alt);
        goto cleanup;

      } else if (*alt == ' ') {
        if (alts[0] == -1) {
          wcsfprintf(stderr, "WARNING, no primary coordinate "
            "representation.\n");
          goto cleanup;
        }

      } else if (ialt < 'A' || ialt > 'Z') {
        wcsfprintf(stderr, "WARNING, alternate specifier \"%s\" is "
          "invalid.\n", alt);
        goto cleanup;

      } else {
        if ((i = alts[ialt - 'A' + 1]) == -1) {
          wcsfprintf(stderr, "WARNING, no alternate coordinate "
            "representation \"%s\".\n", alt);
          goto cleanup;
        }
      }
    }

    wcsi = wcs + i;
  }


  // Initialize and possibly print the structs.
  wcserr_enable(1);
  wcsprintf_set(stdout);

  for (int i = 0; i < nwcs; i++) {
    if (wcsi) {
      if ((wcs+i) != wcsi) continue;
    } else if (i) {
      wcsprintf("\nType <CR> for next: ");
      fgetc(stdin);
      wcsprintf("\n");
    }

    // Read -TAB arrays from the binary table extension (if necessary).
    if (fits_read_wcstab(fptr, wcs[i].nwtb, (wtbarr *)wcs[i].wtb,
                         &fitstat)) {
      goto cleanup;
    }

    // Translate non-standard WCS keyvalues?
    if (dofix) {
      int *stat = malloc(NWCSFIX * sizeof(int));
      if ((status = wcsfix(7, 0, wcs+i, stat))) {
        for (int j = 0; j < NWCSFIX; j++) {
          if (stat[j] > 0) {
             wcsfprintf(stderr, "wcsfix ERROR %d: %s.\n", status,
                        wcsfix_errmsg[stat[j]]);
          }
        }

        goto cleanup;
      }

      free(stat);
    }

    if ((status = wcsset(wcs+i))) {
      wcsperr(wcs+i, "");
      continue;
    }

    // Decompose CDi_ja, or recompose PCi_ja and CDELTia?
    if (dopcx) {
      if (dopcx == 1 || !((wcs+i)->altlin & 1)) {
        wcsprintf("Decomposing CDi_ja into PCi_ja and CDELTia");
      } else {
        wcsprintf("Recomposing PCi_ja and CDELTia");
      }

      if (doperm) {
        wcsprintf(" with axis permutation");
      }
      wcsprintf(".\n");

      double rotn[2];
      if (wcspcx(wcs+i, dopcx-1, doperm, rotn)) {
        wcsperr(wcs+i, "");
        continue;
      }

      wcsprintf("Rotation of celestial axis basis vectors (deg): "
        "%10.5f, %10.5f\n", rotn[0], rotn[1]);
    }

    // Apply wcstrim()?
    if (dotrim) {
      if (wcstrim(wcs+i)) {
        wcsperr(wcs+i, "");
        continue;
      }
    }

    // Extract WCSNAME from the wcsprm struct.
    char wcsname[72];
    strcpy(wcsname, wcs[i].wcsname);

    // Print the struct as a FITS header?
    if (dohdr) {
      if (wcshdo(WCSHDO_all, wcs+i, &nkeyrec, &header)) {
        wcsperr(wcs+i, "");
        continue;
      }

      char *hptr = header;
      wcsprintf("\n");
      for (int k = 0; k < nkeyrec; k++, hptr += 80) {
        wcsprintf("%.80s\n", hptr);
      }

      free(header);
    }

    // Print the struct?
    if (doprt) {
      if (doprt == 1 || strcmp(wcsname, "DEFAULTS")) {
        if (strlen(wcsname)) {
          wcsprintf("\n%s\n", wcsname);
        }

        wcsprintf("\n");
        wcsprt(wcs+i);
      }
    }

    // Print full size of the struct.
    if (dosize) {
      int sizes[2];
      wcssize(wcs+i, sizes);
      wcsprintf("\nSize of wcsprm struct: %4d (base), plus allocated memory: "
        "%4d, total: %4d (bytes).\n", sizes[0], sizes[1], sizes[0] + sizes[1]);
      wcsprintf("Constituent structs (prjprm is included in celprm):\n");

      auxsize((wcs+i)->aux, sizes);
      wcsprintf("        auxprm struct: %4d\n", sizes[0]);

      for (int itab = 0; itab < (wcs+i)->ntab; itab++) {
        tabsize((wcs+i)->tab + itab, sizes);
        wcsprintf("        tabprm struct: %4d (base), plus allocated memory: "
          "%4d, total: %4d (bytes).\n", sizes[0], sizes[1],
          sizes[0] + sizes[1]);
      }

      linsize(&((wcs+i)->lin), sizes);
      wcsprintf("        linprm struct: %4d (base), plus allocated memory: "
        "%4d, total: %4d (bytes).\n", sizes[0], sizes[1],
        sizes[0] + sizes[1]);

      celsize(&((wcs+i)->cel), sizes);
      wcsprintf("        celprm struct: %4d (base), plus allocated memory: "
        "%4d, total: %4d (bytes).\n", sizes[0], sizes[1],
        sizes[0] + sizes[1]);

      prjsize(&((wcs+i)->cel.prj), sizes);
      wcsprintf("        prjprm struct: %4d (base), plus allocated memory: "
        "%4d, total: %4d (bytes).\n", sizes[0], sizes[1],
        sizes[0] + sizes[1]);

      spcsize(&((wcs+i)->spc), sizes);
      wcsprintf("        spcprm struct: %4d (base), plus allocated memory: "
        "%4d, total: %4d (bytes).\n", sizes[0], sizes[1],
        sizes[0] + sizes[1]);
    }


    // Transform coordinates?
    if (dopix || dowrld) {
      if (strlen(wcsname)) {
        wcsprintf("\n%s\n", wcsname);
      }

      double *world  = 0x0;
      double *imgcrd = 0x0;
      double *pixcrd = 0x0;
      int    *stat   = 0x0;

      int nelem = wcs[i].naxis;
      world  = realloc(world,  nelem * sizeof(double));
      imgcrd = realloc(imgcrd, nelem * sizeof(double));
      pixcrd = realloc(pixcrd, nelem * sizeof(double));
      stat   = realloc(stat,   nelem * sizeof(int));

      if (dopix) {
        // Transform pixel coordinates.
        while (1) {
          wcsprintf("\nEnter %d pixel coordinate element%s: ", nelem,
            (nelem==1)?"":"s");
          int c = fgetc(stdin);
          if (c == EOF || c == '\n') {
            if (c == EOF) wcsprintf("\n");
            break;
          }
          ungetc(c, stdin);

          int ok;
          if ((ok = (scanf("%lf", pixcrd) == 1))) {
            for (int j = 1; j < nelem; j++) {
              if (scanf("%*[ ,]%lf", pixcrd+j) != 1) {
                ok = 0;
                break;
              }
            }
          }

          while (fgetc(stdin) != '\n');

          if (!ok) {
            wcsprintf("Input error, please try again.\n");
            continue;
          }

          wcsprintf("Pixel: ");
          for (int j = 0; j < nelem; j++) {
            wcsprintf("%s%14.9g", j?", ":"", pixcrd[j]);
          }
          wcsprintf("\n");

          double phi, theta;
          if ((status = wcsp2s(wcs+i, 1, nelem, pixcrd, imgcrd, &phi, &theta,
                               world, stat))) {
            wcsperr(wcs+i, "");

          } else {
            wcsprintf("Image: ");
            for (int j = 0; j < nelem; j++) {
              if (j == wcs[i].lng || j == wcs[i].lat) {
                // Print angles in fixed format.
                wcsprintf("%s%14.6f", j?", ":"", imgcrd[j]);
              } else {
                wcsprintf("%s%14.9g", j?", ":"", imgcrd[j]);
              }
            }

            wcsprintf("\nWorld: ");
            for (int j = 0; j < nelem; j++) {
              if (j == wcs[i].lng || j == wcs[i].lat) {
                // Print angles in fixed format.
                wcsprintf("%s%14.6f", j?", ":"", world[j]);
              } else {
                wcsprintf("%s%14.9g", j?", ":"", world[j]);
              }
            }
            wcsprintf("\n");
          }
        }
      }


      if (dowrld) {
        // Transform world coordinates.
        while (1) {
          wcsprintf("\nEnter %d world coordinate element%s: ", nelem,
            (nelem==1)?"":"s");
          int c = fgetc(stdin);
          if (c == EOF || c == '\n') {
            if (c == EOF) wcsprintf("\n");
            break;
          }
          ungetc(c, stdin);

          int ok;
          if ((ok = (scanf("%lf", world) == 1))) {
            for (int j = 1; j < nelem; j++) {
              if (scanf("%*[ ,]%lf", world+j) != 1) {
                ok = 0;
                break;
              }
            }
          }

          while (fgetc(stdin) != '\n');

          if (!ok) {
            wcsprintf("Input error, please try again.\n");
            continue;
          }

          wcsprintf("World: ");
          for (int j = 0; j < nelem; j++) {
            if (j == wcs[i].lng || j == wcs[i].lat) {
              // Print angles in fixed format.
              wcsprintf("%s%14.6f", j?", ":"", world[j]);
            } else {
              wcsprintf("%s%14.9g", j?", ":"", world[j]);
            }
          }
          wcsprintf("\n");

          double phi, theta;
          if ((status = wcss2p(wcs+i, 1, nelem, world, &phi, &theta, imgcrd,
                               pixcrd, stat))) {
            wcsperr(wcs+i, "");

          } else {
            wcsprintf("Image: ");
            for (int j = 0; j < nelem; j++) {
              if (j == wcs[i].lng || j == wcs[i].lat) {
                // Print angles in fixed format.
                wcsprintf("%s%14.6f", j?", ":"", imgcrd[j]);
              } else {
                wcsprintf("%s%14.9g", j?", ":"", imgcrd[j]);
              }
            }

            wcsprintf("\nPixel: ");
            for (int j = 0; j < nelem; j++) {
              wcsprintf("%s%14.9g", j?", ":"", pixcrd[j]);
            }
            wcsprintf("\n");
          }
        }
      }

      free(world);
      free(imgcrd);
      free(pixcrd);
      free(stat);
    }
  }

  fits_close_file(fptr, &fitstat);

  // Defeat spurious reporting of memory leaks.
  wcsvfree(&nwcs, &wcs);

  return 0;

cleanup:
  if (fitstat) fits_report_error(stderr, fitstat);
  fits_close_file(fptr, &fitstat);
  return 1;
}
