#-----------------------------------------------------------------------------
# GNU makefile for WCSLIB 8.4 utilities: fitshdr, HPXcvt, wcsgrid and wcsware.
#
# Summary of the main targets
# ---------------------------
#   build:     Build all utilities.
#   clean (or cleaner): Delete intermediate object files.
#   distclean (or realclean): cleaner, and also delete the executables.
#   cleanest: distclean, and also delete the man pages.
#
# Notes:
#   1: If you need to make changes then preferably modify ../makedefs.in
#      instead and re-run configure.
#
#   2: In compiling these utilities, this makefile assumes that the WCSLIB 8.4
#      sources reside in ../{pgsbox,C} (as in the distribution kit).
#
# Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
# http://www.atnf.csiro.au/people/Mark.Calabretta
# $Id: GNUmakefile,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
#-----------------------------------------------------------------------------
# Get configure settings.
SUBDIR := utils
include ../makedefs

UTILS := tofits fitshdr sundazel

ifneq "$(CFITSIOINC)" ""
ifneq "$(CFITSIOLIB)" ""
  UTILS += HPXcvt wcsware

  ifneq "$(PGPLOTINC)" ""
  ifneq "$(PGPLOTLIB)" ""
    UTILS += wcsgrid
  endif
  endif
endif
endif

MAN := $(addsuffix .1,$(UTILS))

WCSLIB    := ../C/$(WCSLIB)
PGSBOXLIB := ../pgsbox/libpgsbox-$(LIBVER).a

ifneq "$(GETWCSTAB)" ""
  GETWCSTAB := ../C/$(GETWCSTAB)
endif

CPPFLAGS += -I.. -I../C

OBSFLAGS := -DOBSLNG=$(OBSLNG) -DOBSLAT=$(OBSLAT) -DOBSTZ=$(OBSTZ)

vpath %.h  ..:../C:../pgsbox
vpath %.in ..


# Static and static pattern rules
#--------------------------------

.PHONY : build clean cleaner cleanest distclean install man realclean \
         uninstall

build : $(UTILS)

tofits : tofits.c
	-@ echo ''
	   $(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) -o $@ $<

fitshdr : fitshdr.c
	-@ echo ''
	   $(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@.o $<
	   $(LD) -o $@ $@.o $(LDFLAGS) $(LIBS)
	-@ $(RM) $@.o

sundazel : sundazel.c
	-@ echo ''
	   $(CC) $(CPPFLAGS) $(OBSFLAGS) $(CFLAGS) -c -o $@.o $<
	   $(LD) -o $@ $@.o $(LDFLAGS) $(LIBS)
	-@ $(RM) $@.o

HPXcvt : HPXcvt.c
	-@ echo ''
	   $(CC) $(CPPFLAGS) $(CFITSIOINC) $(CFLAGS) -c -o $@.o $<
	   $(LD) -o $@ $@.o $(LDFLAGS) $(CFITSIOLIB) $(LIBS)
	-@ $(RM) $@.o

wcsware : wcsware.c $(GETWCSTAB) $(WCSLIB)
	-@ echo ''
	   $(CC) -DDO_CFITSIO $(CPPFLAGS) -I../pgsbox -I../C $(CFITSIOINC) \
	     $(CFLAGS) -c -o $@.o $<
	   $(LD) -o $@ $@.o $(GETWCSTAB) $(LDFLAGS) $(CFITSIOLIB) $(WCSLIB) \
	     $(FLIBS) $(LIBS)
	-@ $(RM) $@.o

wcsgrid : wcsgrid.c $(GETWCSTAB) $(PGSBOXLIB) $(WCSLIB)
	-@ echo ''
	   $(CC) -DDO_CFITSIO $(CPPFLAGS) -I../pgsbox -I../C $(PGPLOTINC) \
	     $(CFITSIOINC) $(CFLAGS) -c -o $@.o $<
	   $(LD) -o $@ $@.o $(GETWCSTAB) $(LDFLAGS) $(PGSBOXLIB) \
	     $(PGPLOTLIB) $(CFITSIOLIB) $(WCSLIB) $(FLIBS) $(LIBS)
	-@ $(RM) $@.o

../C/getwcstab.o :
	   $(MAKE) -C ../C $(@F)

clean cleaner :
	-  $(RM) -r *.o *.i a.out core *.dSYM $(EXTRA_CLEAN)

distclean realclean : cleaner
	-  $(RM) $(UTILS)

cleanest : distclean
	-  $(RM) $(MAN)

$(PGSBOXLIB) :
	-@ echo ''
	   $(MAKE) -C ../pgsbox lib

$(WCSLIB) :
	-@ echo ''
	   $(MAKE) -C ../C lib

install : build
	-  if [ ! -d "$(BINDIR)" ] ; then \
	     $(INSTALL) -d -m 775 $(BINDIR) ; \
	   fi
	   $(INSTALL) -m 755 $(UTILS) $(BINDIR)
	-  if [ ! -d "$(MANDIR)/man1" ] ; then \
	     $(INSTALL) -d -m 775 $(MANDIR)/man1 ; \
	   fi
	   $(INSTALL) -m 644 $(MAN) $(MANDIR)/man1

uninstall :
	-  cd $(BINDIR) && $(RM) $(UTILS)
	-  cd $(MANDIR) && $(RM) $(MAN)

GNUmakefile : ../makedefs ;

../makedefs ../wcsconfig.h ../wcsconfig_utils.h : makedefs.in wcsconfig.h.in \
    wcsconfig_utils.h.in ../config.status
	-@ $(RM) ../wcsconfig.h ../wcsconfig_utils.h
	   cd .. && ./config.status

man : $(MAN)

tofits.1 : tofits
	help2man --no-discard-stderr --version-string=$(LIBVER) \
	  -n "Turn a list of keyrecords to a valid FITS file" -N ./$< > $@

fitshdr.1 : fitshdr
	help2man --no-discard-stderr --version-string=$(LIBVER) \
	  -n "List headers from a FITS file" -N ./$< > $@

sundazel.1 : sundazel
	help2man --no-discard-stderr --version-string=$(LIBVER) \
	  -n "Compute the time of Solar passage" -N ./$< > $@

wcsware.1 : wcsware
	help2man --no-discard-stderr --version-string=$(LIBVER) \
	  -n "Extract FITS WCS keywords for an image" -N ./$< > $@

wcsgrid.1 : wcsgrid
	help2man --no-discard-stderr --version-string=$(LIBVER) \
	  -n "Extract FITS WCS keywords and plot graticule" -N ./$< > $@

HPXcvt.1 : HPXcvt
	help2man --no-discard-stderr --version-string=$(LIBVER) \
	  -n "Reorganise HEALPix data into a 2-D FITS image" -N ./$< > $@

# Dependency lists.
fitshdr : wcsconfig.h wcsconfig_utils.h
wcsware : getwcstab.h wcs.h wcsfix.h wcshdr.h
wcsgrid : cpgsbox.h getwcstab.h wcs.h wcsfix.h wcshdr.h
