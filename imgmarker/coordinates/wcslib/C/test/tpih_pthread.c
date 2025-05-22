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
  $Id: tpih_pthread.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=============================================================================
*
* tpih_pthread tests the thread safety of wcspih(), the WCS FITS parser for
* image headers.  It closely follows tpih1.c, launching multiple threads in
* rapid succession to read a test header.
*
* Input comes from file "pih.fits" read directly using fgets().
*
*---------------------------------------------------------------------------*/

#include <wcsconfig_tests.h>

#include<pthread.h>
#include<stdio.h>
#include<string.h>
#include<unistd.h>

#include <wcshdr.h>

#define NTHREAD 8

pthread_t threadId[NTHREAD];

void *threadFn(void *threadarg);

struct threadArg {
  char *header;
  int  nkeyrec;
  int  relax;
  int  ctrl;
};

struct threadRet {
  int status;
  int nreject;
  int nwcs;
  struct wcsprm *wcs;
} threadret[NTHREAD];


int main(void)
{
  char infile[] = "pih.fits";
  int nkeyrec = 0;

  // Set for unbuffered output so messages are printed immediately.
  setvbuf(stdout, NULL, _IONBF, 0);

  printf("Testing WCSLIB header parser for thread safety (tpih_pthread.c)\n"
         "---------------------------------------------------------------\n\n");

  // Read in the FITS header, excluding COMMENT and HISTORY keyrecords.
  FILE *fptr;
  if ((fptr = fopen(infile, "r")) == 0) {
    fprintf(stderr, "ERROR opening %s\n", infile);
    return 1;
  }

  char keyrec[81], header[288001];
  int k = 0;
  int gotend = 0;
  for (int iblock = 0; iblock < 100; iblock++) {
    for (int ikeyrec = 0; ikeyrec < 36; ikeyrec++) {
      if (fgets(keyrec, 81, fptr) == 0) {
        break;
      }

      // Cull COMMENT and HISTORY keyrecords.
      if (strncmp(keyrec, "        ", 8) == 0) continue;
      if (strncmp(keyrec, "COMMENT ", 8) == 0) continue;
      if (strncmp(keyrec, "HISTORY ", 8) == 0) continue;

      memcpy(header+k, keyrec, 80);
      k += 80;
      nkeyrec++;

      if (strncmp(keyrec, "END     ", 8) == 0) {
        // An END keyrecord was read, but read the rest of the block.
        gotend = 1;
      }
    }

    if (gotend) break;
  }
  fclose(fptr);

  fprintf(stderr, "Found %d non-comment header keyrecords.\n\n", nkeyrec);

  // The threadArg struct contains constant data shared by all threads.
  struct threadArg threadarg = {header, nkeyrec, WCSHDR_all, 0};
  for (int iloop = 0; iloop < 10; iloop++) {
    printf("\nPass %d:\n", iloop);

    // Launch multiple threads parsing the same header.
    for (int ithread = 0; ithread < NTHREAD; ithread++) {
      printf("Thread %d...\n", ithread);

      int status;
      if ((status = pthread_create(&(threadId[ithread]), NULL, &threadFn,
                                   &threadarg))) {
        printf("Failed to create thread %d: %s", ithread, strerror(status));
      } else {
        printf("Thread %d created successfully.\n", ithread);
      }
    }

    // Wait for each thread to finish.
    for (int ithread = 0; ithread < NTHREAD; ithread++) {
      struct threadRet *ret;
      pthread_join(threadId[ithread], (void**)&ret);
      printf("Thread %d status return: %d.\n", ithread, ret->status);

      // Free memory allocated by wcspih().
      wcsvfree(&ret->nwcs, &ret->wcs);
    }
  }

  return 0;
}


/*----------------------------------------------------------------------------
* Invoke wcspih() in a thread.
----------------------------------------------------------------------------*/

void *threadFn(void *threadarg)
{
  // Determine our thread index.
  pthread_t selfId = pthread_self();
  int ithread;
  for (ithread = 0; ithread < NTHREAD; ithread++) {
    if (pthread_equal(selfId, threadId[ithread])) {
      break;
    }
  }

  printf("Thread %d processing started.\n", ithread);

  // Invoke wcspih().
  struct threadArg *arg = (struct threadArg *)threadarg;
  struct threadRet *ret = threadret + ithread;
  ret->status = wcspih(arg->header, arg->nkeyrec, arg->relax, arg->ctrl,
                       &ret->nreject, &ret->nwcs, &ret->wcs);

  // Terminate the thread.
  printf("Thread %d processing finished.\n", ithread);
  pthread_exit(ret);

  return NULL;
}
