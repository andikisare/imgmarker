//----------------------------------------------------------------------------
// Utility routine for the WCSLIB Fortran test programs that draw plots, to
// pause for the specified number of milliseconds between plots.  Whihout a
// pause they just become a blur.  Required because the Fortran SLEEP()
// function takes a whole number of seconds, which slows the test suite too
// much.
//
// $Id: wcsleep_f.c,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
//----------------------------------------------------------------------------

// Needed to get nanosleep() from time.h.
#define _POSIX_C_SOURCE 199309L

#include <time.h>


int wcsleep_ (const int *millisec)

{
  // Scale milliseconds to nanoseconds.
  struct timespec nano = {(time_t)0, (*millisec)*1000000L};
  return nanosleep(&nano, 0x0);
}
