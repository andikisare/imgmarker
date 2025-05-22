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
  $Id: sundazel.c,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
*=============================================================================
* Usage: sundazel [<option>] [<yyyymmdd>]
*-----------------------------------------------------------------------------
* sundazel computes the local time of the Sun's passage through the specified
* apparent longitude or latitude in a user-defined coordinate system.  It can
* also perform several other Solar related calculations.  Refer to the usage
* notes below.
*---------------------------------------------------------------------------*/

char usage[] =
"Usage: sundazel [<option>] [<yyyymmdd>]\n"
"\n"
"sundazel computes the local time of the Sun's passage through the\n"
"specified apparent longitude or latitude in a user-defined coordinate\n"
"system, for the specified location on the specified date (default today).\n"
"\n"
"The Sun's apparent hour angle, azimuth, elevation, and the longitude and\n"
"latitude in user coordinates are also printed, in degrees.  Refraction is\n"
"accounted for.\n"
"\n"
"sundazel may also be used to compute the time of sunrise and set, the\n"
"Sun's right ascension and declination, and the Equation of Time.\n"
"\n"
"Options:\n"
"  -p <option>\n"
"       The Solar passage required and, if relevant, the coordinate value\n"
"       in degrees:\n"
"         sunrise           Sunrise.\n"
"         sunset            Sunset.\n"
"         lng=<lng>         Longitude of the Sun in the user-defined\n"
"                           coordinate system.\n"
"         lat=<lat>         Latitude of the Sun in the user-defined\n"
"                           coordinate system.\n"
"  -l <lng>,<lat>\n"
"       Longitude and latitude of the observer.\n"
"  -t <tz>\n"
"       The observer's time zone, positive east of Greenwich (hr).\n"
"  -u <az>,<el>,<zlng>\n"
"       Azimuth and elevation of the pole of the user-defined coordinate\n"
"       system, and the longitude of the zenith (deg).  See below.\n"
"  -n   Set the user-defined coordinate system as one with pole due north\n"
"       on the horizon, with zero of longitude at the zenith.\n"
"  -w   Set the user-defined coordinate system as one with pole due west\n"
"       on the horizon, with zero of longitude at the zenith.\n"
"  -v   Also print the Sun's right ascension, declination (deg), and the\n"
"       Equation of Time (min).\n"
"\n"
"The user-defined coordinate system is a right-handed spherical coordinate\n"
"system with its pole at the specified azimuth and elevation, and with\n"
"zenith having the specified longitude.  If omitted, the default is a\n"
"right-handed system with its pole at the zenith and prime meridian due\n"
"north, i.e. similar to azimuth and elevation except that longitude\n"
"increases in the reverse sense to azimuth, i.e. from north through west\n"
"rather than north through east.\n"
"\n"
"Setting a range of azimuth or elevation often provides a poor criterion\n"
"for timing the passage of the Sun, for example in determining when it\n"
"shines directly through a skylight, or when an awning casts a shadow on a\n"
"particular point on the ground.  In such cases the projection of the\n"
"skylight or awning from the ground onto the sky should be considered.\n"
"Some other coordinate system may provide a better fit to the region of the\n"
"sky thereby defined.  For example, the passage of the Sun across a\n"
"skylight oriented at azimuth alpha might be handled via a coordinate\n"
"system with pole on the horizon at that azimuth and considering the Sun's\n"
"passage through a range of longitude in this system.  Perhaps better might\n"
"be to use a coordinate system with pole at alpha-90 and considering a\n"
"range of latitude.\n"
"\n"
"Sunrise and sunset correspond to first/last contact of the Sun's limb on\n"
"the horizon, corresponding to apparent elevation -0.27 deg (true elevation\n"
"-0.79 deg).  If no options are specified, the default is to calculate the\n"
"time of sunset.  If more than one p option is specified, only the last is\n"
"effective.\n";

// To get the declaration of localtime_r() from time.h.
#define _POSIX_C_SOURCE 199506L

#include <math.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Default values of the observer's geographic longitude (east +ve), latitude,
// and time zone offset (hr).
#ifndef OBSLNG
#define OBSLNG 0.0
#endif
#ifndef OBSLAT
#define OBSLAT 0.0
#endif
#ifndef OBSTZ
#define OBSTZ  0.0
#endif

int sundazel(char *mode, double obslng, double obslat, double obstz,
  double pole_az, double pole_el, double zlng, int year, int month, int day,
  double coord, double *ra, double *dec, double *eot, double *utc, double *ha,
  double *az, double *el, double *lng, double *lat);

int refract(double el, double *corr);

int eulrot(double euler[5], int mode, double lng1, double lat1,
  double *lng2, double *lat2, double *rotn);

int xeuler(double euler1[5], int mode1, double euler2[5], int mode2,
  double euler3[5]);

int eulerhy(double euler[5], int mode, double chi, double psi, int *nvalid,
  double alpha[2]);

int xyzalpha(double x, double y, double z, double alpha[2]);

double normang (int mode, double angle);

#define PI  3.141592653589793238462643
#define D2R (PI/180.0)
#define R2D (180.0/PI)

#define cosd(X) cos((X)*D2R)
#define sind(X) sin((X)*D2R)
#define tand(X) tan((X)*D2R)
#define acosd(X) acos(X)*R2D
#define asind(X) asin(X)*R2D
#define atand(X) atan(X)*R2D
#define atan2d(Y,X) atan2(Y,X)*R2D


int main(int argc, char **argv)

{
  // Parse options.
  char   *ident = 0x0, mode[16];
  int    date = 0, verbose = 0;
  double obslng = OBSLNG, obslat = OBSLAT, obstz = OBSTZ;
  double coord = 0.0, pole_az = 0.0, pole_el = 90.0, zlng = 180.0;

  strcpy(mode, "sunset");

  int i;
  for (i = 1; i < argc && argv[i][0] == '-'; i++) {
    switch (argv[i][1]) {
    case 'p':
      if (++i < argc) {
        int j;
        for (j = 0; j < 16; j++) {
          if (argv[i][j] == '=' || argv[i][j] == '\0') break;
        }

        if (j == 16) goto usage;

        strncpy(mode, argv[i], j);
        mode[j] = '\0';

        if (strcmp(mode, "sunrise") == 0 ||
            strcmp(mode, "sunset")  == 0) {
          // No coordinate value.
          ident = "elevation";
          break;
        }

        if (strcmp(mode, "lng") == 0) {
          ident = "longitude";
        } else if (strcmp(mode, "lat") == 0) {
          ident = "latitude";
        } else {
          goto usage;
        }

        // Set the coordinate value.
        if (argv[i][j] == '=') {
          j++;
          coord = atof(argv[i]+j);
        } else {
          goto usage;
        }

      } else {
        goto usage;
      }

      break;

    case 'l':
      if (++i < argc) {
        sscanf(argv[i], "%lf,%lf", &obslng, &obslat);

      } else {
        goto usage;
      }

      break;

    case 't':
      if (++i < argc) {
        sscanf(argv[i], "%lf", &obstz);

      } else {
        goto usage;
      }

      break;

    case 'u':
      if (++i < argc) {
        sscanf(argv[i], "%lf,%lf,%lf", &pole_az, &pole_el, &zlng);

      } else {
        goto usage;
      }

      break;

    case 'n':
      pole_az = 0.0;
      pole_el = 0.0;
      zlng    = 0.0;

      break;

    case 'w':
      pole_az = -90.0;
      pole_el =   0.0;
      zlng    =   0.0;

      break;

    case 'v':
      verbose = 1;
      break;

    default:
      goto usage;
    }
  }

  if (i < argc) {
    date = atoi(argv[i]);

    if (++i < argc) goto usage;
  }

  // Get the year, month, and day.
  int iy, im, id;
  if (date) {
    iy = date/10000;
    im = (date/100)%100;
    id = date%100;
  } else {
    // No date given, use today's date.
    time_t tloc = time(NULL);
    tzset();

    struct tm tmval;
    localtime_r(&tloc, &tmval);
    iy = tmval.tm_year + 1900;
    im = tmval.tm_mon + 1;
    id = tmval.tm_mday;
  }

  double ra, dec, eot, utc, ha, az, el, lng, lat;
  if (sundazel(mode, obslng, obslat, obstz, pole_az, pole_el, zlng, iy, im,
               id, coord, &ra, &dec, &eot, &utc, &ha, &az, &el, &lng, &lat)) {
    printf("The Sun does not attain the requested %s on %d-%02d-%02d.\n",
           ident, iy, im, id);

  } else {
    double aest = fmod((utc + obstz) + 0.5/60.0, 24.0);
    printf("  %02d:%02d%8.2f%8.2f%8.2f%8.2f%8.2f",
      (int)aest, (int)(60*fmod(aest,1.0)), ha, az, el, lng, lat);
    if (verbose) {
      printf("%8.2f%8.2f%8.2f", ra, dec, eot);
    }
    printf("\n");
  }

  return 0;

usage:
  fprintf(stderr, "%s", usage);
  return 1;
}

//============================================================================
// sundazel() - Compute UTC of Solar passage
// -----------------------------------------
// sundazel() computes the UTC for the given Solar longitude or latitude.
//
// Corresponding to the computed UTC, also returned are the Solar right
// ascension, declination, the Equation of Time, the apparent Solar hour
// angle, longitude and latitude.
//
// Given:
//   mode      *char     String indicating the Solar passage for which UTC is
//                       to be computed:
//                           sunrise: Sunrise,
//                            sunset: Sunset.
//                               lng: Apparent longitude (deg),
//                               lat: Apparent latitude  (deg),
//   obslng    double    The observer's longitude (deg).
//   obslat    double    The observer's latitude (deg).
//   obstz     double    The observer's time zone (hr).
//   pole_az   double    Azimuth of the pole of the user-defined coordinate
//                       system (deg).
//   pole_el   double    Elevation of the pole of the user-defined coordinate
//                       system (deg).
//   zlng      double    Longitude of the zenith in the user-defined
//                       coordinate system (deg).
//   year      int       Year.
//   month     int       Month.
//   day       int       Day of month.
//   coord     double    The coordinate value corresponding to mode (deg).
//
// Returned:
//   ra        double*   Solar right ascension (deg).
//   dec       double*   Solar declination (deg).
//   eot       double*   Equation of Time (min).
//   utc       double*   UTC (hr), normalized in the range [-obstz, 24-obstz).
//   ha        double*   Apparent Solar hour angle (deg).
//   az        double*   Apparent Solar azimuth   (deg).
//   el        double*   Apparent Solar elevation (deg).
//   lng       double*   Apparent Solar longitude (deg).
//   lat       double*   Apparent Solar latitude  (deg).
//
// Function return value:
//             int       Status return value:
//                         0: Success.
//                         1: The Sun does not attain the requested longitude
//                            or latitude on the date specified.
//
// Notes:
//   1: Null pointers may be provided for any of the returned values that are
//      not required.
//
//   2: Atmospheric refraction is accounted for using a simple model.
//      Specify apparent elevation = 0 for the centre of the Sun observed to
//      be on the horizon.
//
//   3: Sunrise/set is taken as the time of first/last contact of the Sun's
//      limb with the horizon, whereas its apparent elevation refers to the
//      centre of its disk.  Thus its 16 arcmin mean radius must be taken into
//      account.  Set apparent elevation to -0°.2667 for sunrise/set on the
//      horizon for an observer at sea level.
//
//   4. An adjustment to the rise/set elevation may be needed to account for
//      the observer's altitude.
//
//   5: Twilight is defined to start and end when the Sun's elevation is
//         -6 deg: Civil twilight,
//        -12 deg: Nautical twilight,
//        -18 deg: Astronomical twilight.
//
//   6: Euler angles for transformations between systems:
//        (-ha,dec) -> (-az,el):
//           Phi_0 = 90, Theta = 90 - obslat, Phi = -90.
//
//        (-az,el) -> (lng,lat):
//           Phi_0 = 90 - pole_az, Theta = 90 - pole_el, Phi = zlng - 90.
//
//   7: Formulae from aa.usno.navy.mil/faq/docs/SunApprox.php
//                    aa.usno.navy.mil/faq/docs/GAST.php
//
//   8: Validated against ssd.jpl.nasa.gov/horizons.cgi
//                    and www.esrl.noaa.gov/gmd/grad/solcalc
//
//============================================================================

int sundazel(
  char   *mode,
  double obslng,
  double obslat,
  double obstz,
  double pole_az,
  double pole_el,
  double zlng,
  int    year,
  int    month,
  int    day,
  double coord,
  double *ra_,
  double *dec_,
  double *eot_,
  double *utc_,
  double *ha_,
  double *az_,
  double *el_,
  double *lng_,
  double *lat_)

{
  if (ra_  == 0x0 &&
      dec_ == 0x0 &&
      eot_ == 0x0 &&
      utc_ == 0x0 &&
      ha_  == 0x0 &&
      az_  == 0x0 &&
      el_  == 0x0 &&
      lng_ == 0x0 &&
      lat_ == 0x0) {
    // Nothing to do!
    return 0;
  }

  const double COSLAT = cosd(obslat);
  const double SINLAT = sind(obslat);

  // Euler angles for (-ha,dec) -> (-az,el).
  double euler1[5];
  euler1[0] =  90.0;
  euler1[1] =  90.0 - obslat;
  euler1[2] = -90.0;
  euler1[3] = cosd(euler1[1]);
  euler1[4] = sind(euler1[1]);

  // Euler angles for (-az,el) -> (lng,lat).
  double euler2[5];
  euler2[0] = 90.0 - pole_az;
  euler2[1] = 90.0 - pole_el;
  euler2[2] = zlng - 90.0;
  euler2[3] = cosd(euler2[1]);
  euler2[4] = sind(euler2[1]);

  // Euler angles for (-ha,dec) -> (lng,lat).
  double euler3[5];
  xeuler(euler1, 1, euler2, 1, euler3);

  // Compute the Julian Date at 0h UTC on the specified UTC date.
  // Adapted from SoFA routine iauCal2jd().
  int jm, jy;
  if (month < 1) {
    jy = year - 1 + month/12;
    jm = 12 + month%12;
  } else {
    jy = year + (month-1)/12;
    jm = (month-1)%12 + 1;
  }

  long km = (jm - 14)/12;
  double jd0 = (double)((1461L*(4800L + jy + km))/4L
                      + (367L*(jm - 2 - 12*km))/12L
                      - (3L*((4900L + jy + km)/100L))/4L
                      + day - 32075L) - 0.5;

  // Number of days since epoch J2000.0.
  double D0 = jd0 - 2451545.0;

  // Convert observer's longitude to hour.
  double lnghr = obslng / 15.0;

  // Set first approximation of UTC rise/set time to local noon (hr).
  double utc =  12.0 - lnghr;

  double L, alpha, delta, ha;
  for (int i = 0; i < 2; i++) {
    double D = D0 + utc/24.0;

    // Mean longitude of the Sun, corrected for aberration (deg).
    L = fmod(280.459 + 0.98564736*D, 360.0);
    if (L < 0.0) L += 360.0;

    // Mean anomaly of the Sun (deg).
    double g = fmod(357.529 + 0.98560028*D, 360.0);

    // Ecliptic longitude of the Sun (deg), accurate to 1 arcmin.
    double lambda = normang(360, L + 1.915*sind(g) + 0.020*sind(2.0*g));

    // Obliquity of the ecliptic (deg).
    double epsilon = 23.439 - 0.00000036*D;

    // Sun-Earth distance (AU).
    double R = 1.00014 - 0.01671*cosd(g) - 0.00014*cosd(2.0*g);

    // Solar radius (deg).
    double SD = 0.2666 / R;

    // True Solar right ascension and declination (deg).
    alpha = atan2d(cosd(epsilon)*sind(lambda), cosd(lambda));
    delta = asind(sind(epsilon)*sind(lambda));

    // Normalize the RA.
    alpha = normang(360, alpha);

    // Compute true hour angle at the specified coordinate (deg).
    if (strcmp(mode, "sunrise") == 0 || strcmp(mode, "sunset") == 0) {
      // Sunrise/set.
      double el = -SD;

      // Correct for refraction.
      double corr;
      refract(el, &corr);
      el -= corr;

      double sinel = sind(el);
      double cosha = (sinel - sind(delta)*SINLAT) / (cosd(delta)*COSLAT);

      // Does the Sun attain the specified apparent elevation?
      if (1.0 < fabs(cosha)) {
        // No solution.
        return 1;
      }

      ha = acosd(cosha);
      if (mode[3] == 'r') {
        // Sunrise.
        ha = -ha;
      }

    } else if (strcmp(mode, "lng") == 0) {
      // Sun at the specified apparent longitude.
      double lng = normang(180, coord);

      // Find Solar hour angle for given declination and apparent longitude.
      // The Euler angles are for (-ha,dec) -> (lng,lat).
      int nvalid;
      double alpha[2];
      if (eulerhy(euler3, 1, delta, lng, &nvalid, alpha)) {
        // No solution.
        return 1;
      }

      // Select the appropriate root.
      ha = -alpha[0];
      if (nvalid == 2) {
        // Two valid solutions, choose the one closer to zero.
        if (fabs(alpha[1]) < fabs(alpha[0])) {
          ha = -alpha[1];
        }
      }

    } else if (strcmp(mode, "lat") == 0) {
      // Sun at the specified apparent latitude.
      double lat = coord;

      // Find Solar hour angle for given declination and apparent latitude.
      // The Euler angles are for (-ha,dec) -> (lng,lat).
      int nvalid;
      double alpha[2];
      if (eulerhy(euler3, 2, delta, lat, &nvalid, alpha)) {
        // No solution.
        return 1;
      }

      // Select the appropriate root.
      ha = -alpha[0];
      if (nvalid == 2) {
        // Two valid solutions, choose the one closer to zero.
        if (fabs(alpha[1]) < fabs(alpha[0])) {
          ha = -alpha[1];
        }
      }

    } else {
      // Unrecognized mode.
      return 1;
    }

    // Normalize the hour angle.
    ha = normang(180, ha);

    // Local apparent sidereal time of specified coordinate.
    double last0 = fmod((alpha+ha)/15.0, 24.0);

    // Greenwich mean sidereal time corresponding to UTC (hr).
    double gmst = fmod(6.697374558 + 0.06570982441908*D0 + 1.00273790935*utc,
                       24.0);

    // Longitude of the ascending node of the Moon (deg).
    double omega = 125.04 - 0.052954*D;

    // Approximate nutation in longitude (hr).
    double dpsi = -0.000319*sind(omega) - 0.000024*sind(2.0*L);

    // Equation of the Equinoxes (hr).
    double eqeq = dpsi*cosd(epsilon);

    // Greenwich apparent sidereal time corresponding to UTC (hr).
    double gast = gmst + eqeq;

    // Local apparent sidereal time corresponding to UTC (hr).
    double last = fmod(gast + lnghr, 24.0);

    // UTC of specified coordinate.
    utc = fmod((utc + obstz) + (last0 - last)*1.00273790935, 24.0);
    if (utc < 0.0) utc += 24.0;
    utc -= obstz;
  }


  // Copy or compute values to be returned.
  // True Solar right ascension and declination (deg).
  if (ra_)  *ra_ = alpha;
  if (dec_) *dec_ = delta;

  // Equation of time (min).
  if (eot_) {
    *eot_ = (L - alpha) * 4.0;
    if (*eot_ < -720.0) {
      *eot_ += 1440.0;
    } else if (720.0 < *eot_) {
      *eot_ -= 1440.0;
    }
  }

  // UTC of required passage (hr).
  if (utc_) *utc_ = utc;

  // Compute apparent Solar coordinates.
  double az, el;
  eulrot(euler1, 1, -ha, delta, &az, &el, 0x0);
  az = -az;

  double corr;
  refract(el, &corr);
  el += corr;

  double dec;
  eulrot(euler1, -1, -az, el, &ha, &dec, 0x0);
  ha = -ha;

  double lng, lat;
  eulrot(euler3, 1, -ha, dec, &lng, &lat, 0x0);

  // Apparent hour angle.
  if (ha_) *ha_ = ha;

  // Apparent azimuth and elevation.
  if (az_) *az_ = az;
  if (el_) *el_ = el;

  // Apparent longitude and latitude.
  if (lng_) *lng_ = lng;
  if (lat_) *lat_ = lat;


  return 0;
}


//============================================================================
// refract() - Compute a correction for atmospheric refraction
// -----------------------------------------------------------
// refract() computes an approximate correction for atmospheric refraction.
//
// Given:
//   el        double    True (geometric) Solar elevation (deg).
//
// Returned:
//   corr      double*   Correction to be added to the true Solar elevation to
//                       give the apparent elevation (deg).
//
// Function return value:
//             int       Status return value:
//                         0: Success.
//
// Notes:
//   1: Formulae from www.esrl.noaa.gov/gmd/grad/solcalc/calcdetails.html
//
//============================================================================

int refract(
  double el,
  double *corr)

{
  // Compute the correction in arcsec.
  if (el < -0.575) {
    *corr = -20.744 / tand(el);

  } else if (el < 5.0) {
    *corr = 1735.0 - (518.2 - (103.4 - (12.79 - 0.711*el)*el)*el)*el;

  } else if (el < 85.0) {
    double cotel = 1.0 / tand(el);
    double cot2el = cotel*cotel;
    *corr = (58.1 - (0.07 - 0.000086*cot2el)*cot2el)*cotel;

  } else {
    *corr = 0.0;
  }

  // Arcsec to degrees.
  *corr /= 3600.0;

  return 0;
}


//============================================================================
// eulrot() - Apply Euler angle based spherical coordinate transformation
// ----------------------------------------------------------------------
// eulrot() applies the Euler angle based transformation of spherical
// coordinates.
//
// Given:
//   euler     double[5] Euler angles for the transformation:
//                         0: (PHI0) Longitude of the ascending node in the
//                            old system (deg).  The ascending node is the
//                            point of intersection of the equators of the
//                            two systems such that the equator of the new
//                            system crosses from south to north as viewed in
//                            the old system.
//                         1: (THETA) Angle between the poles of the two
//                            systems (deg).  THETA is positive for a positive
//                            rotation about the ascending node.
//                         2: (PHI) Longitude of the ascending node in the new
//                            system (deg).
//                         3: cos(THETA).
//                         4: sin(THETA).
//   mode      int       If -1, apply the transformation in the reverse
//                       direction.
//   lng1      double    Longitude in the old coordinate system (deg).
//   lat1      double    Latitude  in the old coordinate system (deg).
//
// Returned:
//   lng2      double*   Longitude in the new coordinate system (deg),
//                       normalized to the range (-180, 180] degrees.
//   lat2      double*   Latitude in the new coordinate system (deg),
//   rotn      double*   Position angle of the old pole at the specified
//                       point (deg).  May be given as a null pointer if the
//                       value is not required.
//
// Function return value:
//             int       Status return value:
//                         0: Success.
//
// Notes:
//   1: Longitude at the poles in the new system is consistent with that
//      specified in the old system.  This may be important when dealing with
//      map projections in which the poles are represented by finite line
//      segments.  Such is the case for cylindrical projections for example.
//----------------------------------------------------------------------------

int eulrot(
  double euler[5],
  int    mode,
  double lng1,
  double lat1,
  double *lng2,
  double *lat2,
  double *rotn)

{
  double phi0, phi, ctheta, stheta;
  if (mode != -1) {
    // Forward transformation.
    phi0   = euler[0];
    phi    = euler[2];
    ctheta = euler[3];
    stheta = euler[4];
  } else {
    // Reverse transformation.
    phi0   =  euler[2];
    phi    =  euler[0];
    ctheta =  euler[3];
    stheta = -euler[4];
  }

  // Compute trigonometric functions of the old coordinates.
  double lng1p  = lng1 - phi0;
  double clng1p = cosd(lng1p);
  double slng1p = sind(lng1p);
  double clat1  = cosd(lat1);
  double slat1  = sind(lat1);

  // Compute the longitude in the new system.
  double x = clat1*clng1p;
  double y = clat1*slng1p*ctheta + slat1*stheta;
  if (fabs(x) < 1e-12 && fabs(y) < 1e-12) {
    // Longitude at the poles in the new system is consistent with that
    // specified in the old system.
    *lng2 = phi + lng1p;
  } else {
    *lng2 = phi + atan2(y,x)*R2D;
  }

  *lng2 = normang(180, *lng2);

  // Latitude in the new system - circumvent rounding errors.
  double slat2 = slat1*ctheta - clat1*stheta*slng1p;
  if (1e-12 < 1.0-fabs(slat2)) {
    *lat2 = asind(slat2);
  } else {
    if (slat2 < 0.0) {
      *lat2 = -90.0;
    } else {
      *lat2 = +90.0;
    }
  }

  if (rotn) {
    // Compute the position angle of the old pole at this point.
    x = slng1p*stheta*slat1 + ctheta*clat1;
    y = clng1p*stheta;
    *rotn = atan2(y,x)*R2D;
  }

  return 0;
}


//============================================================================
// xeuler() - Combine the Euler angles for two consecutive rotations into one
// --------------------------------------------------------------------------
// xeuler() combines the Euler angles for two consecutive rotations into one.
//
// Given:
//   euler1    double[5] Euler angles for the first rotation:
//                         0: (PHI0) Longitude of the ascending node in the
//                            old system (deg).  The ascending node is the
//                            point of intersection of the equators of the
//                            two systems such that the equator of the new
//                            system crosses from south to north as viewed in
//                            the old system.
//                         1: (THETA) Angle between the poles of the two
//                            systems (deg).  THETA is positive for a positive
//                            rotation about the ascending node.
//                         2: (PHI) Longitude of the ascending node in the new
//                            system (deg).
//                         3: cos(THETA).
//                         4: sin(THETA).
//   mode1     int       If -1, apply the first rotation in the reverse
//                       direction.
//   euler2    double[5] Euler angles for the second rotation (as for euler1).
//   mode2     int       If -1, apply the second rotation in the reverse
//                       direction.
//
// Returned:
//   euler3    double[5] Euler angles for the combined rotation (as for
//                       euler1).  euler3 may be the same array as euler1 or
//                       euler2.
//
// Function return value:
//             int       Status return value:
//                         0: Success.
//
// Notes:
//   1: The two rotations are applied successively to special points in the
//      original coordinate system.  In any rotation the north pole will be
//      transformed to polar angle 90 - THETA, and thus THETA, and likewise
//      PHI, for the combined rotation can be found easily.  Determination of
//      PHI0 is a little trickier, and requires the coordinates in the
//      original system of the north pole of the new system.  However, it is
//      straightforward to express the inverse of the combined rotation in
//      terms of the inverse of the two constituent rotations.
//
//   2: Note that rotations are not commutative.  Therefore, the order of the
//      two rotations is important.
//
//   3: If the Euler angles for a rotation are (PHI0, THETA, PHI) then for the
//      inverse rotation they are (PHI, -THETA, PHI0).
//
//   4: If R1, R2, and R are the rotations, and r1, r2, and r are their
//      inverses then R(x) = R2(R1(x)) and r(x) = r1(r2(x)).
//----------------------------------------------------------------------------

int xeuler(
  double euler1[5],
  int    mode1,
  double euler2[5],
  int    mode2,
  double euler3[5])

{
  // Apply the rotations in succession to the north pole of the first system.
  double lat1, lat2, lng1, lng2, rotn;
  eulrot(euler1, mode1,  0.0, 90.0, &lng1, &lat1, &rotn);
  eulrot(euler2, mode2, lng1, lat1, &lng2, &lat2, &rotn);


  // THETA can be obtained simply from the coordinates of the old north
  // pole in the new system.
  double theta = 90.0 - lat2;

  // Now determine PHI and PHI0.
  double phi0, phi;
  if (fabs(sind(theta)) < 1e-12) {
    // THETA equals zero is a special case.
    eulrot(euler1, mode1,  0.0,  0.0, &lng1, &lat1, &rotn);
    eulrot(euler2, mode2, lng1, lat1, &lng2, &lat2, &rotn);
    phi0 = 0.0;
    phi  = lng2;

  } else {
    // Otherwise, PHI is readily obtained in the same way as THETA.
    phi = normang(180, lng2 - 90.0);

    // The easiest way to find PHI0 is to apply the inverse transformation to
    // the north pole of the new coordinate system.
    double lng0, lat0;
    eulrot(euler2, -mode2,  0.0, 90.0, &lng1, &lat1, &rotn);
    eulrot(euler1, -mode1, lng1, lat1, &lng0, &lat0, &rotn);
    phi0 = normang(180, lng0 + 90.0);
  }

  // Setting euler3 could affect euler1 or euler2.
  euler3[0] = phi0;
  euler3[1] = theta;
  euler3[2] = phi;
  euler3[3] = cosd(theta);
  euler3[4] = sind(theta);

  return 0;
}

//============================================================================
// eulerhy() - hybrid coordinate calculations based on Euler angles
// ----------------------------------------------------------------
// eulerhy() inverts the Euler angle transformation formulae to perform hybrid
// coordinate calculations.  Specifically, given the Euler angles for the
// spherical rotation from (lng1,lat1) to (lng2,lat2), then
//   1. compute lng1 given lat1 and lng2,
//   2. compute lng1 given lat1 and lat2,
//   3. compute lat1 given lng1 and lng2,
//   4. compute lat1 given lng1 and lat2.
//
// The missing pairs, namely
//      compute lng1 given lng2 and lat2,
//      compute lat1 given lng2 and lat2,
// are, of course, handled by the normal Euler angle transformation formulae.
//
// Likewise, computing lng2 given lng1 and lat2, etc., are handled simply by
// using the Euler angles for the inverse spherical rotation, i.e. from
// (lng2,lat2) to (lng1,lat1).  See note 1 below.
//
// Given:
//   euler     double[5] Euler angles for the transformation:
//                         0: (PHI0) Longitude of the ascending node in the
//                            old system (deg).  The ascending node is the
//                            point of intersection of the equators of the
//                            two systems such that the equator of the new
//                            system crosses from south to north as viewed in
//                            the old system.
//                         1: (THETA) Angle between the poles of the two
//                            systems (deg).  THETA is positive for a positive
//                            rotation about the ascending node.
//                         2: (PHI) Longitude of the ascending node in the new
//                            system (deg).
//                         3: cos(THETA).
//                         4: sin(THETA).
//   mode      int       Mode of operation: if the spherical rotation is from
//                       (lng1,lat1) to (lng2,lat2):
//                         1: compute lng1 given lat1 and lng2,
//                         2: compute lng1 given lat1 and lat2,
//                         3: compute lat1 given lng1 and lng2,
//                         4: compute lat1 given lng1 and lat2.
//   chi,psi   double    The two given coordinates (deg), depending on the
//                       mode, in the order specified above.  E.g. for
//                       mode == 2, these are lat1 and lat2, for mode == 4,
//                       they are lng1 and lat2.
//
// Returned:
//   nvalid    int*      Number of valid solutions: 0, 1, or 2.
//   alpha[2]  double    The required coordinate (deg), normalized in the
//                       range (-180,+180].  E.g. for mode == 1, it is lng1.
//                       There may be 0, 1, or 2 valid solutions.  If there
//                       is only one valid solution it will be in alpha[0].
//
// Function return value:
//             int       Status return value:
//                         0: Success.
//                         1: No solution.
//                         2: Invalid parameter.
//
// Notes:
//   1: If the Euler angles for a rotation are (PHI0, THETA, PHI) then for the
//      inverse rotation they are (PHI, -THETA, PHI0).
//----------------------------------------------------------------------------

int eulerhy(
  double euler[5],
  int    mode,
  double chi,
  double psi,
  int    *nvalid,
  double alpha[2])

{
  const double TOL = 0.0001;

  const double phi0   = euler[0];
  const double phi    = euler[2];
  const double ctheta = euler[3];
  const double stheta = euler[4];

  int status = 1;
  *nvalid = 0;

  double x, y, z;
  if (mode == 1) {
    // Compute lng1 given lat1 and lng2,
    double lat1 = chi;
    double lng2 = psi;

    double lng2p  = lng2 - phi;
    double clat1  = cosd(lat1);
    double slat1  = sind(lat1);
    double clng2p = cosd(lng2p);
    double slng2p = sind(lng2p);

    x =  clat1*slng2p;
    y = -clat1*clng2p*ctheta;
    z =  slat1*clng2p*stheta;

    if (xyzalpha(x, y, z, alpha)) {
      // No solution.
      return 1;
    }

    // Check the solutions.
    lng2 = normang(180, lng2);
    for (int i = 0; i < 2; i++) {
      alpha[i] = normang(180, alpha[i] + phi0);
      double lng1 = alpha[i], lng, lat;
      eulrot(euler, 1, lng1, lat1, &lng, &lat, 0x0);

      lng = normang(180, lng);
      if (fabs(lng2-lng) < TOL) {
        // A valid root.
        (*nvalid)++;
        status = 0;
        if (i == 1 && *nvalid == 1) {
          alpha[0] = alpha[1];
        }
      }
    }

  } else if (mode == 2) {
    // Compute lng1 given lat1 and lat2,
    double lat1 = chi;
    double lat2 = psi;

    double clat1 = cosd(lat1);
    double slat1 = sind(lat1);
    double slat2 = sind(lat2);

    x = 0.0;
    y = clat1*stheta;
    z = slat1*ctheta - slat2;

    if (xyzalpha(x, y, z, alpha)) {
      // No solution.
      return 1;
    }

    // Check the solutions.
    for (int i = 0; i < 2; i++) {
      alpha[i] = normang(180, alpha[i] + phi0);
      double lng1 = alpha[i], lng, lat;
      eulrot(euler, 1, lng1, lat1, &lng, &lat, 0x0);

      if (fabs(lat2-lat) < TOL) {
        // A valid root.
        (*nvalid)++;
        status = 0;
        if (i == 1 && *nvalid == 1) {
          alpha[0] = alpha[1];
        }
      }
    }

  } else if (mode == 3) {
    // Compute lat1 given lng1 and lng2,
    double lng1 = chi;
    double lng2 = psi;

    double lng1p  = lng1 - phi0;
    double lng2p  = lng2 - phi;
    double clng1p = cosd(lng1p);
    double slng1p = sind(lng1p);
    double clng2p = cosd(lng2p);
    double slng2p = sind(lng2p);

    x = slng1p*clng2p*ctheta - clng1p*slng2p;
    y =        clng2p*stheta;
    z = 0.0;

    if (xyzalpha(x, y, z, alpha)) {
      // No solution.
      return 1;
    }

    // Check the solutions.
    lng2 = normang(180, lng2);
    for (int i = 0; i < 2; i++) {
      double lat1 = alpha[i], lng, lat;
      eulrot(euler, 1, lng1, lat1, &lng, &lat, 0x0);

      lng = normang(180, lng);
      if (fabs(lng2-lng) < TOL) {
        // A valid root.
        (*nvalid)++;
        status = 0;
        if (i == 1 && *nvalid == 1) {
          alpha[0] = alpha[1];
        }
      }
    }

  } else if (mode == 4) {
    // Compute lat1 given lng1 and lat2.
    double lng1 = chi;
    double lat2 = psi;

    double lng1p  = lng1 - phi0;
    double slng1p = sind(lng1p);
    double slat2  = sind(lat2);

    x = slng1p*stheta;
    y = -ctheta;
    z = -slat2;

    if (xyzalpha(x, y, z, alpha)) {
      // No solution.
      return 1;
    }

    // Check the solutions.
    for (int i = 0; i < 2; i++) {
      double lat1 = alpha[i], lng, lat;
      eulrot(euler, 1, lng1, lat1, &lng, &lat, 0x0);

      if (fabs(lat2-lat) < TOL) {
        // A valid root.
        (*nvalid)++;
        status = 0;
        if (i == 1 && *nvalid == 1) {
          alpha[0] = alpha[1];
        }
      }
    }

  } else {
    return 2;
  }

  return status;
}


//============================================================================
// xyzalpha() - Solve the equation x*cos(alpha) + y*sin(alpha) = z for alpha
// -------------------------------------------------------------------------
// xyzalpha() solves the equation x*cos(alpha) + y*sin(alpha) = z for alpha.
// Used in inverting the Euler angle transformation formulae.
//
// Given:
//   x,y,z     double    The values of x, y, and z.
//
// Returned:
//   alpha     double[2] The two solutions for alpha (deg), normalized in
//                       the range (-180,+180].  The smaller solution is
//                       returned in alpha[0].
//
// Function return value:
//             int       Status return value:
//                         0: Success.
//                         1: No solution.
//
// Notes:
//   1: The solution is indeterminate, i.e. alpha may have any value, if
//      (x,y,z) == (0,0,0).  In this case both values of alpha are returned
//      as zero.
//
//   2: There are no solutions if x² + y² < z².
//----------------------------------------------------------------------------

int xyzalpha(
  double x,
  double y,
  double z,
  double alpha[2])

{
  double u;
  if (x == 0.0 && y == 0.0) {
    if (z == 0.0) {
      // Indeterminate.
      alpha[0] = 0.0;
      alpha[1] = 0.0;
      return 0;
    } else {
      // No solution.
      return 1;
    }
  } else if (y == 0.0 && x > 0.0) {
    u =   0.0;
  } else if (x == 0.0 && y > 0.0) {
    u =  90.0;
  } else if (y == 0.0 && x < 0.0) {
    u = 180.0;
  } else if (x == 0.0 && y < 0.0) {
    u = -90.0;
  } else {
    u = atan2d(y, x);
  }

  double r = sqrt(x*x + y*y), v;
  if (r < fabs(z)) {
    // No solution.
    return 1;
  } else if (z == r) {
    v =   0.0;
  } else if (z == 0.0) {
    v =  90.0;
  } else if (z == -r) {
    v = 180.0;
  } else {
    v = acosd(z/r);
  }

  // Compute the two solutions in range (-180,+180].
  alpha[0] = normang(180, u - v);
  alpha[1] = normang(180, u + v);

  // Ensure the smaller solution is returned in alpha[0].
  if (alpha[1] < alpha[0]) {
    double tmp = alpha[0];
    alpha[0] = alpha[1];
    alpha[1] = tmp;
  }

  return 0;
}


//============================================================================
// normang() - Normalize an angle in the required range
// -------------------------------------------------------------------------
// normang() normalizes an angle in the range (-180,+180], or [0,+360).
//
// Given:
//   mode      int       Required normalization range:
//                         180: (-180,+180],
//                         360: [0,+360).
//   angle     double    The angle (deg).
//
// Function return value:
//             double    The normalized angle (deg).
//----------------------------------------------------------------------------

double normang (int mode, double angle)

{
  angle = fmod(angle, 360.0);

  if (mode == 180) {
    if (angle <= -180.0) {
      angle += 360.0;
    } else if (180.0 < angle) {
      angle -= 360.0;
    }
  } else {
    if (angle < 0.0) angle += 360.0;
  }

  return angle;
}
