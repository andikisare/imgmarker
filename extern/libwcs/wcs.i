%feature("autodoc", "1");

%module(package="imgmarker.libwcs") wcs

%{
#include "wcs.h"
%}

struct WorldCoor *wcsinit(char *hstring); /* set up a WCS structure from a FITS image header */

%apply double *OUTPUT { double *xpix, double *ypix, int *offscl};
void wcs2pix(struct WorldCoor *wcs, double xpos, double ypos, double *xpix, double *ypix, int *offscl);		/* Convert World Coordinates to pixel coordinates */
%apply double *OUTPUT { double *xpos, double *ypos};
void pix2wcs(struct WorldCoor *wcs, double xpix, double ypix, double *xpos, double *ypos);		/* Convert pixel coordinates to World Coordinates */

struct WorldCoor {
  double    xref;       /* X reference coordinate value (deg) */
  double    yref;       /* Y reference coordinate value (deg) */
  double    xrefpix;    /* X reference pixel */
  double    yrefpix;    /* Y reference pixel */
  double    xinc;       /* X coordinate increment (deg) */
  double    yinc;       /* Y coordinate increment (deg) */
  double    rot;        /* rotation around axis (deg) (N through E) */
  double    cd[4];      /* rotation matrix */
  double    dc[4];      /* inverse rotation matrix */
  double    equinox;    /* Equinox of coordinates default to 1950.0 */
  double    epoch;      /* Epoch of coordinates default to equinox */
  double    nxpix;      /* Number of pixels in X-dimension of image */
  double    nypix;      /* Number of pixels in Y-dimension of image */
  double    plate_ra;   /* Right ascension of plate center */
  double    plate_dec;  /* Declination of plate center */
  double    plate_scale;    /* Plate scale in arcsec/mm */
  double    x_pixel_offset; /* X pixel offset of image lower right */
  double    y_pixel_offset; /* Y pixel offset of image lower right */
  double    x_pixel_size;   /* X pixel_size */
  double    y_pixel_size;   /* Y pixel_size */
  double    ppo_coeff[6];   /* pixel to plate coefficients for DSS */
  double    x_coeff[20];    /* X coefficients for plate model */
  double    y_coeff[20];    /* Y coefficients for plate model */
  double    xpix;       /* X (RA) coordinate (pixels) */
  double    ypix;       /* Y (dec) coordinate (pixels) */
  double    zpix;       /* Z (face) coordinate (pixels) */
  double    xpos;       /* X (RA) coordinate (deg) */
  double    ypos;       /* Y (dec) coordinate (deg) */
  double    crpix[9];   /* Values of CRPIXn keywords */
  double    crval[9];   /* Values of CRVALn keywords */
  double    cdelt[9];   /* Values of CDELTn keywords */
  double    pc[81];     /* Values of PCiiijjj keywords */
  double    projp[10];  /* Constants for various projections */
  int       pvfail;     /* If non-zero, significant inaccuracy likely to occur in projection */
  double    projppv[2*MAXPV]; /* SCAMP constants for the PV coordinates */
  struct poly   *inv_x;     /* SCAMP projection correction polynom in x */
  struct poly   *inv_y;     /* SCAMP projection correction polynom in y */
  double    longpole;   /* Longitude of North Pole in degrees */
  double    latpole;    /* Latitude of North Pole in degrees */
  double    rodeg;      /* Radius of the projection generating sphere */
  double    imrot;      /* Rotation angle of north pole */
  double    pa_north;   /* Position angle of north (0=horizontal) */
  double    pa_east;    /* Position angle of east (0=horizontal) */
  double    radvel;     /* Radial velocity (km/sec away from observer)*/
  double    zvel;       /* Radial velocity (v/c away from observer)*/
  double    zpzd;       /* Colat of FIP (degs) */
  double    zpr;        /* Radius of FIP (degs) */
  int       imflip;     /* If not 0, image is reflected around axis */
  int       prjcode;    /* projection code (-1-32) */
  int       latbase;    /* Latitude base 90 (NPA), 0 (LAT), -90 (SPA) */
  int       ncoeff1;    /* Number of x-axis plate fit coefficients */
  int       ncoeff2;    /* Number of y-axis plate fit coefficients */
  int       zpnp;        /* ZP polynomial order (0-9) */
  int       changesys;  /* 1 for FK4->FK5, 2 for FK5->FK4 */
                /* 3 for FK4->galactic, 4 for FK5->galactic */
  int       printsys;   /* 1 to print coordinate system, else 0 */
  int       ndec;       /* Number of decimal places in PIX2WCST */
  int       degout;     /* 1 to always print degrees in PIX2WCST */
  int       tabsys;     /* 1 to put tab between RA & Dec, else 0 */
  int       rotmat;     /* 0 if CDELT, CROTA; 1 if CD */
  int       coorflip;   /* 0 if x=RA, y=Dec; 1 if x=Dec, y=RA */
  int       offscl;     /* 0 if OK, 1 if offscale */
  int       wcson;      /* 1 if WCS is set, else 0 */
  int       naxis;      /* Number of axes in image (for WCSLIB 3.0) */
  int       naxes;      /* Number of axes in image */
  int       wcsproj;    /* WCS_OLD: AIPS worldpos() and worldpix()
                   WCS_NEW: Mark Calabretta's WCSLIB subroutines
                   WCS_BEST: WCSLIB for all but CAR,COE,NCP
                   WCS_ALT:  AIPS for all but CAR,COE,NCP */
  int       linmode;    /* 0=system only, 1=units, 2=system+units */
  int       detector;   /* Instrument detector number */
  char      instrument[32]; /* Instrument name */
  char      ctype[9][9];    /* Values of CTYPEn keywords */
  char      c1type[9];  /*  1st coordinate type code:
                    RA--, GLON, ELON */
  char      c2type[9];  /*  2nd coordinate type code:
                    DEC-, GLAT, ELAT */
  char      ptype[9];   /*  projection type code:
                    SIN, TAN, ARC, NCP, GLS, MER, AIT, etc */
  char      units[9][32];   /* Units if LINEAR */
  char      radecsys[32];   /* Reference frame: FK4, FK4-NO-E, FK5, GAPPT*/
  char      radecout[32];   /* Output reference frame: FK4,FK5,GAL,ECL */
  char      radecin[32];    /* Input reference frame: FK4,FK5,GAL,ECL */
  double    eqin;       /* Input equinox (match sysin if 0.0) */
  double    eqout;      /* Output equinox (match sysout if 0.0) */
  int       sysin;      /* Input coordinate system code */
  int       syswcs;     /* WCS coordinate system code */
  int       sysout;     /* Output coordinate system code */
                /* WCS_B1950, WCS_J2000, WCS_ICRS, WCS_GALACTIC,
                 * WCS_ECLIPTIC, WCS_LINEAR, WCS_ALTAZ  */
  char      center[32]; /* Center coordinates (with frame) */
  struct wcsprm wcsl;       /* WCSLIB main projection parameters */
  struct linprm lin;        /* WCSLIB image/pixel conversion parameters */
  struct celprm cel;        /* WCSLIB projection type */
  struct prjprm prj;        /* WCSLIB projection parameters */
  struct IRAFsurface *lngcor;   /* RA/longitude correction structure */
  struct IRAFsurface *latcor;   /* Dec/latitude correction structure */
  int       distcode;   /* Distortion code 0=none 1=SIRTF */
  struct Distort distort;   /* SIRTF distortion coefficients */
  char *command_format[10]; /* WCS command formats */
                /* where %s is replaced by WCS coordinates */
                /* where %f is replaced by the image filename */
                /* where %x is replaced by image coordinates */
  double    ltm[4];     /* Image rotation matrix */
  double    ltv[2];     /* Image offset */
  int       idpix[2];   /* First pixel to use in image (x, y) */
  int       ndpix[2];   /* Number of pixels to use in image (x, y) */
  struct WorldCoor *wcs;    /* WCS upon which this WCS depends */
  struct WorldCoor *wcsdep; /* WCS depending on this WCS */
  char      *wcsname;   /* WCS name (defaults to NULL pointer) */
  char      wcschar;    /* WCS character (A-Z, null, space) */
  int       logwcs;     /* 1 if DC-FLAG is set for log wavelength */
};