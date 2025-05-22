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
  $Id: fitshdr_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*===========================================================================*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <wcsutil.h>
#include <fitshdr.h>

// Fortran name mangling.
#include <wcsconfig_f77.h>
#define keyidput_ F77_FUNC(keyidput, KEYIDPUT)
#define keyidptc_ F77_FUNC(keyidptc, KEYIDPTC)
#define keyidget_ F77_FUNC(keyidget, KEYIDGET)
#define keyidgtc_ F77_FUNC(keyidgtc, KEYIDGTC)
#define keyidgti_ F77_FUNC(keyidgti, KEYIDGTI)
#define keyget_   F77_FUNC(keyget,   KEYGET)
#define keygtc_   F77_FUNC(keygtc,   KEYGTC)
#define keygtd_   F77_FUNC(keygtd,   KEYGTD)
#define keygti_   F77_FUNC(keygti,   KEYGTI)
#define freekeys_ F77_FUNC(freekeys, FREEKEYS)

#define fitshdr_  F77_FUNC(fitshdr,  FITSHDR)

#ifdef BINDC
  #undef  keyidptc_
  #define keyidptc_ keyidptc_c

  #undef  keyidgtc_
  #define keyidgtc_ keyidgtc_c

  #undef  keygtc_
  #define keygtc_ keygtc_c

  #undef  fitshdr_
  #define fitshdr_ fitshdr_c
#endif

// Must match the values set in fitshdr.inc.
#define KEYID_NAME   100
#define KEYID_COUNT  101
#define KEYID_IDX    102

#define KEY_KEYNO    200
#define KEY_KEYID    201
#define KEY_STATUS   202
#define KEY_KEYWORD  203
#define KEY_TYPE     204
#define KEY_KEYVALUE 205
#define KEY_ULEN     206
#define KEY_COMMENT  207

//----------------------------------------------------------------------------

int keyidput_(int *keyid, const int *i, const int *what, const void *value)

{
  const char *cvalp;
  struct fitskeyid *kidp;

  // Cast pointers.
  kidp  = (struct fitskeyid *)keyid + *i;
  cvalp = (const char *)value;

  switch (*what) {
  case KEYID_NAME:
    // Only eight characters need be given.
    wcsutil_strcvt(8, ' ', 1, cvalp, kidp->name);
    wcsutil_null_fill(12, kidp->name);
    break;
  default:
    return 1;
  }

  return 0;
}

int keyidptc_(int *keyid, const int *i, const int *what, const char *value)
{
  return keyidput_(keyid, i, what, value);
}

//----------------------------------------------------------------------------

int keyidget_(const int *keyid, const int *i, const int *what, void *value)

{
  char *cvalp;
  int  *ivalp;
  const struct fitskeyid *keyidp;

  // Cast pointers.
  keyidp = (const struct fitskeyid *)keyid + *i;
  cvalp = (char *)value;
  ivalp = (int *)value;

  switch (*what) {
  case KEYID_NAME:
    wcsutil_strcvt(12, ' ', 0, keyidp->name, cvalp);
    break;
  case KEYID_COUNT:
    *ivalp = keyidp->count;
    break;
  case KEYID_IDX:
    *(ivalp++) = keyidp->idx[0];
    *(ivalp++) = keyidp->idx[1];
    break;
  default:
    return 1;
  }

  return 0;
}

int keyidgtc_(const int *keyid, const int *i, const int *what, char *value)
{
  return keyidget_(keyid, i, what, value);
}

int keyidgti_(const int *keyid, const int *i, const int *what, int *value)
{
  return keyidget_(keyid, i, what, value);
}

//----------------------------------------------------------------------------


int keyget_(
  const int *keys,
  const int *i,
  const int *what,
  void *value,
  int  *nc)

{
  char   *cvalp, text[32];
  int    *ivalp, j;
  double *dvalp;
  const struct fitskey *keyp;

  // Cast pointers.
  keyp  = *((const struct fitskey **)keys) + *i;
  cvalp = (char *)value;
  ivalp = (int *)value;
  dvalp = (double *)value;

  *nc = 1;
  switch (*what) {
  case KEY_KEYNO:
    *ivalp = keyp->keyno;
    break;
  case KEY_KEYID:
    *ivalp = keyp->keyid;
    break;
  case KEY_STATUS:
    *ivalp = keyp->status;
    break;
  case KEY_KEYWORD:
    *nc = (int)(strlen(keyp->keyword));
    wcsutil_strcvt(12, ' ', 0, keyp->keyword, cvalp);
    break;
  case KEY_TYPE:
    *ivalp = keyp->type;
    break;
  case KEY_KEYVALUE:
    switch (abs(keyp->type)%10) {
    case 1:
    case 2:
      // Logical and 32-bit integer.
      *ivalp = keyp->keyvalue.i;
      break;
    case 3:
      // 64-bit integer.
      *nc = 3;
#ifdef WCSLIB_INT64
      sprintf(text, "%28.27lld", keyp->keyvalue.k);
      sscanf(text+1, "%9d%9d%9d", ivalp+2, ivalp+1, ivalp);
      if (*text == '-') {
        ivalp[0] *= -1;
        ivalp[1] *= -1;
        ivalp[2] *= -1;
      }
#else
      *(ivalp++) = keyp->keyvalue.k[0];
      *(ivalp++) = keyp->keyvalue.k[1];
      *(ivalp++) = keyp->keyvalue.k[2];
#endif
      break;
    case 4:
      // Very long integer.
      *nc = 8;
      for (j = 0; j < 8; j++) {
        *(ivalp++) = keyp->keyvalue.l[j];
      }
      break;
    case 5:
      // Floating point.
      *dvalp = keyp->keyvalue.f;
      break;
    case 6:
    case 7:
      // Integer complex and floating point complex.
      *nc = 2;
      *(dvalp++) = keyp->keyvalue.c[0];
      *(dvalp++) = keyp->keyvalue.c[1];
      break;
    case 8:
      // String or part of a continued string.
      *nc = (int)(strlen(keyp->keyvalue.s));
      wcsutil_strcvt(72, ' ', 0, keyp->keyvalue.s, cvalp);
      break;
    default:
      // No value.
      break;
    }
    break;
  case KEY_ULEN:
    *ivalp = keyp->ulen;
    break;
  case KEY_COMMENT:
    *nc = (int)(strlen(keyp->comment));
    wcsutil_strcvt(84, ' ', 0, keyp->comment, cvalp);
    break;
  default:
    return 1;
  }

  return 0;
}

int keygtc_(
  const int *keys,
  const int *i,
  const int *what,
  char *value,
  int *nc)
{
  return keyget_(keys, i, what, value, nc);
}

int keygtd_(
  const int *keys,
  const int *i,
  const int *what,
  double *value,
  int *nc)
{
  return keyget_(keys, i, what, value, nc);
}

int keygti_(
  const int *keys,
  const int *i,
  const int *what,
  int *value,
  int *nc)
{
  return keyget_(keys, i, what, value, nc);
}

//----------------------------------------------------------------------------

int freekeys_(int *keys)

{
  free(*((struct fitskey **)keys));
  *keys = 0;
  return 0;
}

//----------------------------------------------------------------------------

int fitshdr_(
  const char header[],
  const int *nkeyrec,
  const int *nkeyids,
  int *keyids,
  int *nreject,
  iptr keys)

{
  return fitshdr(header, *nkeyrec, *nkeyids, (struct fitskeyid *)keyids,
                 nreject, (struct fitskey **)keys);
}
