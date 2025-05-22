/*============================================================================
  WCSLIB 8.3 - an implementation of the FITS WCS standard.
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
  $Id$
*=============================================================================
*
* twcs_pthread tests the thread safety of wcsset() when invoked explicitly
* from within multiple threads.
*
*---------------------------------------------------------------------------*/

#include<pthread.h>
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>

#include <wcs.h>
#include <wcserr.h>

#define NTHREAD 4
#define NPXPTHR 100000
#define NPIX NPXPTHR*NTHREAD

// Pixel-world-pixel closure tolerance.
const double TOL = 1e-8;

// Make these global as a convenient way to get them to the threads.
struct wcsprm wcs;
double pixcrd[2*NPIX];
double imgcrd[2*NPIX];
double phi[NPIX], theta[NPIX];
double world[2*NPIX];
int    stat[NPIX];
double pixcrd2[2*NPIX];

pthread_t threadId[NTHREAD];
void *threadFn(void *ithread);
int threadRet[NTHREAD];

int main(void)
{
  // Set for unbuffered output so messages are printed immediately.
  setvbuf(stdout, NULL, _IONBF, 0);

  printf("Testing wcsset() for thread safety (twcs_pthread.c)\n"
         "---------------------------------------------------\n");

  wcsinit(1, 2, &wcs, 0, 0, 0);
  wcs.naxis = 2;
  wcs.crpix[0] = -234.75;
  wcs.crpix[1] =    8.3393;
  wcs.cdelt[0] =   -0.066667;
  wcs.cdelt[1] =    0.066667;
  wcs.crval[0] =    0.0;
  wcs.crval[1] =  -90.0;
  sprintf(wcs.ctype[0], "RA---AIR");
  sprintf(wcs.ctype[1], "DEC--AIR");

  wcserr_enable(1);

  // Set up the wcsprm struct.  It only needs to be done once and normally
  // that would be the end of it.  However, threadFn() is going to call
  // wcsset() repeatedly for testing purposes.  Hence the struct is put into
  // bypass mode by setting wcsprm::flag = 1.  That will stop wcsset()
  // altering it in one thread while it's being used by another.
  wcs.flag = 1;
  if (wcsset(&wcs)) {
    wcsperr(&wcs, "");
  }

  // Set up an array of random pixels.
  const double min = -1000.0;
  const double max =  1000.0;
  unsigned int seed = 292364782;
  for (int i = 0; i < 2*NPIX; ) {
    double r;

    r = (double)rand_r(&seed) / (double)RAND_MAX;
    pixcrd[i++] = min + r*(max - min);

    r = (double)rand_r(&seed) / (double)RAND_MAX;
    pixcrd[i++] = min + r*(max - min);
  }

  int threadArg[NTHREAD];
  for (int iloop = 0; iloop < 10; iloop++) {
    // Launch multiple threads working on the pixel array.
    for (int ithread = 0; ithread < NTHREAD; ithread++) {
      threadArg[ithread] = ithread;

      int status;
      if ((status = pthread_create(&(threadId[ithread]), NULL, &threadFn,
                                   threadArg+ithread))) {
        printf("Failed to create thread %d: %s", ithread, strerror(status));
      }
    }

    // Wait for each thread to finish.
    int iFail = 0;
    for (int ithread = 0; ithread < NTHREAD; ithread++) {
      pthread_join(threadId[ithread], NULL);
      iFail += threadRet[ithread];
    }

    printf("Iteration %d: got %d closure errors.\n", iloop, iFail);
  }

  return 0;
}


//----------------------------------------------------------------------------
// Invoke wcsset(), wcsp2x(), and wcsx2p() in a thread.
//----------------------------------------------------------------------------

void *threadFn(void *threadArg)
{
  int ithread = *(int *)threadArg;

  // Compute offsets into the 1-D and 2-D arrays for this thread.
  int off1 = ithread * NPXPTHR;
  int off2 = off1 * 2;

  // Pixel to world coordinates.
  if (wcsp2s(&wcs, NPXPTHR, 2, pixcrd+off2, imgcrd+off2, phi+off1, theta+off1,
             world+off2, stat+off1)) {
    wcsperr(&wcs, "");
  }

  // Invoke wcsset().  This is unnecessary and undesirable - do not write code
  // like this!  It is done to test thread-safety in situations where it can't
  // be avoided, such as may occur when WCSLIB is wrapped by another language.
  if (wcsset(&wcs)) {
    wcsperr(&wcs, "");
  }

  // World to pixel coordinates.
  if (wcss2p(&wcs, NPXPTHR, 2, world+off2, phi+off1, theta+off1, imgcrd+off2,
             pixcrd2+off2, stat+off1)) {
    wcsperr(&wcs, "");
  }

  // Check closure.
  int *iFailp = threadRet + ithread;
  *iFailp = 0;
  double tol2 = TOL*TOL;
  for (int i = off2; i < off2 + 2*NPXPTHR; i++) {
    double r = pixcrd2[i] - pixcrd[i];
    double resid = r*r;

    i++;
    r = pixcrd2[i] - pixcrd[i];
    resid += r*r;

    if (resid > tol2) {
      (*iFailp)++;
    }
  }

  // Terminate the thread.
  pthread_exit(NULL);
}
