#-----------------------------------------------------------------------------
# GNU makefile for building PGSBOX 8.4
#
# Summary of the main targets
# ---------------------------
#   build:     Build the library.
#
#   clean:     Delete intermediate object files.
#
#   cleaner:   clean, and also delete the test executables.
#
#   cleanest (distclean, or realclean):  cleaner, and also delete the pgsbox
#              and WCSLIB object libraries.
#
#   check (or test): Compile and run the test programs.  By default they are
#              executed in batch mode; use
#
#                make MODE=interactive check
#
#              to run them interactively.
#
#   tests:     Compile the test programs (but don't run them).
#
# Notes:
#   1) If you need to make changes then preferably modify ../makedefs.in
#      instead and re-run configure.
#
#   2) In compiling the test programs, this makefile assumes that the
#      WCSLIB 8.4 sources reside in ../C and ../Fortran (as in the
#      distribution kit).
#
# Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
# http://www.atnf.csiro.au/people/Mark.Calabretta
# $Id: GNUmakefile,v 8.4 2024/10/28 13:56:18 mcalabre Exp $
#-----------------------------------------------------------------------------
# Get configure settings.
SUBDIR := pgsbox
include ../makedefs

PGSBOXLIB := libpgsbox-$(LIBVER).a
MODULES   := pgsbox.o \
             cpgsbox.o \
             pgwcsl.o \
             pgcrfn.o

ifdef BINDC
  # Using Fortran 2003 BIND(C) interoperability mechanism.
  MODULES  += pgsbox_bindc.o \
              pgwcsl_bindc.o \
              pgcrfn_bindc.o
  CPPFLAGS += -DBINDC
  FFLAGS   += -DBINDC
endif

WCSLIB  := ../C/$(WCSLIB)
LIBLOCK := lib.lock

# For building the sharable library.
PICLIB  := libpgsbox-PIC.a
WCSSHR  := ../C/$(SHRLIB)
SHRLIB  := $(subst libwcs,libpgsbox,$(SHRLIB))
SONAME  := $(subst libwcs,libpgsbox,$(SONAME))
SHRLD   := $(subst libwcs,libpgsbox,$(SHRLD))
SHRLN   := $(subst libwcs,libpgsbox,$(SHRLN))

CPPFLAGS += -I. -I.. -I../C

# Required by pgtest.
WCSLEEP := ../Fortran/wcsleep_f.o

vpath %.h   ..:../C
vpath %.in  ..
vpath %.inc ../Fortran

# Pattern rules
#--------------

$(PGSBOXLIB)(%.o) : %.f
	-@ echo ''
	   $(FC) -I../Fortran $(FFLAGS) -c $<
	 @ if [ ! -f $(LIBLOCK) ] ; then \
	     echo $(AR) r$(ARFLAGS) $(PGSBOXLIB) $% ; \
	     $(AR) r$(ARFLAGS) $(PGSBOXLIB) $% ; \
	     $(RM) $% ; \
	   fi

# Fortran source files with .F suffix are preprocessed.
$(PGSBOXLIB)(%.o) : %.F
	-@ echo ''
	   $(FC) -I../Fortran $(FFLAGS) -c $<
	 @ if [ ! -f $(LIBLOCK) ] ; then \
	     echo $(AR) r$(ARFLAGS) $(PGSBOXLIB) $% ; \
	     $(AR) r$(ARFLAGS) $(PGSBOXLIB) $% ; \
	     $(RM) $% ; \
	   fi

$(PGSBOXLIB)(%.o) : %.f90
	-@ echo ''
	   $(FC) -I../Fortran $(FFLAGS) -c $<
	 @ if [ ! -f $(LIBLOCK) ] ; then \
	     echo $(AR) r$(ARFLAGS) $(PGSBOXLIB) $% ; \
	     $(AR) r$(ARFLAGS) $(PGSBOXLIB) $% ; \
	     $(RM) $% ; \
	   fi

$(PGSBOXLIB)(%.o) : %.c
	-@ echo ''
	   $(CC) $(CPPFLAGS) $(CFLAGS) -c $<
	 @ if [ ! -f $(LIBLOCK) ] ; then \
	     echo $(AR) r$(ARFLAGS) $(PGSBOXLIB) $% ; \
	     $(AR) r$(ARFLAGS) $(PGSBOXLIB) $% ; \
	     $(RM) $% ; \
	   fi

$(PICLIB)(%.o) : $(PGSBOXLIB)(%.o)
	-@ echo ''
	 @ if [ -f $(%:.o=.f) ] ; then \
	     echo $(FC) -I../Fortran $(FFLAGS) $(SHRFLAGS) -c $(%:.o=.f) ; \
	     $(FC) -I../Fortran $(FFLAGS) $(SHRFLAGS) -c $(%:.o=.f) ; \
	   elif [ -f $(%:.o=.F) ] ; then \
	     echo $(FC) -I../Fortran $(FFLAGS) $(SHRFLAGS) -c $(%:.o=.F) ; \
	     $(FC) -I../Fortran $(FFLAGS) $(SHRFLAGS) -c $(%:.o=.F) ; \
	   elif [ -f $(%:.o=.f90) ] ; then \
	     echo $(FC) -I../Fortran $(FFLAGS) $(SHRFLAGS) -c $(%:.o=.f90) ; \
	     $(FC) -I../Fortran $(FFLAGS) $(SHRFLAGS) -c $(%:.o=.f90) ; \
	   else \
	     echo $(CC) $(CPPFLAGS) $(CFLAGS) $(SHRFLAGS) -c $(%:.o=.c) ; \
	     $(CC) $(CPPFLAGS) $(CFLAGS) $(SHRFLAGS) -c $(%:.o=.c) ; \
	   fi
	 @ if [ ! -f $(LIBLOCK) ] ; then \
	     echo $(AR) r$(ARFLAGS) $(PICLIB) $% ; \
	     $(AR) r$(ARFLAGS) $(PICLIB) $% ; \
	     $(RM) $% ; \
	   fi

%.i : %.c
	-@ echo ''
	-@ $(RM) $@
	   $(CPP) $(CPPFLAGS) $(CFLAGS) $< > $@

# Print out include file dependencies.
%.d : %.c
	-@ echo ''
	-@ $(CPP) $(CPPFLAGS) $(CFLAGS) $< | \
	   sed -n -e 's|^# 1 "\([^/].*\.h\)".*|\1|p' | \
	   sed -e 's|.*/||' | \
	   sort -u

# Static and static pattern rules
#--------------------------------

.PHONY : build check clean cleaner cleanest distclean install realclean test \
         tests uninstall wcslib

build : lib

lib :
	-@ echo ''
	-@ echo 'Building PGSBOX library...'
	 @ $(MAKE) --no-print-directory $(PGSBOXLIB)

$(PGSBOXLIB) : $(LIBLOCK) $(MODULES:%=$(PGSBOXLIB)(%))
	-@ echo ''
	 @ set *.o ; \
	     if [ "$$1" != "*.o" ] ; then \
	       echo $(AR) r$(ARFLAGS) $@ *.o ; \
	       $(AR) r$(ARFLAGS) $@ *.o ; \
	       echo $(RANLIB) $@ ; \
	       $(RANLIB) $@ ; \
	       $(RM) *.o ; \
	     fi
	-@ $(RM) $<
	 @ if [ "$(SHRLIB)" != "" ] ; then \
	     $(MAKE) --no-print-directory $(SHRLIB) ; \
	   fi

$(SHRLIB) : $(PICLIB)
	-@ echo ''
	-@ $(RM) -r tmp
	-  mkdir tmp && \
	     cd tmp && \
	     trap 'cd .. ; $(RM) -r tmp' 0 1 2 3 15 ; \
	     $(AR) x ../$(PICLIB) && \
	     $(SHRLD) -o $@ *.o ../$(WCSSHR) $(LDFLAGS) $(PGPLOTLIB) $(FLIBS) && \
	     mv $@ ..

$(PICLIB) : $(LIBLOCK) $(MODULES:%.o=$(PICLIB)(%.o))
	-@ echo ''
	 @ set *.o ; \
	     if [ "$$1" != "*.o" ] ; then \
	       echo $(AR) r$(ARFLAGS) $@ *.o ; \
	       $(AR) r$(ARFLAGS) $@ *.o ; \
	       $(RM) *.o ; \
	     fi
	-@ $(RM) $<

$(LIBLOCK) : FORCE
	 @ $(RM) *.o
	 @ touch $@

install : build
	   $(MAKE) -C ../Fortran install
	   if [ "$(ARFLAGS)" = U ] ; then \
	     $(RM) -r tmp ; \
	     mkdir tmp && \
	       cd tmp && \
	       trap 'cd .. ; $(RM) -r tmp' 0 1 2 3 15 ; \
	       $(AR) x ../$(PGSBOXLIB) && \
	       $(AR) rD $(PGSBOXLIB) *.o && \
	       $(INSTALL) -m 644 $(PGSBOXLIB) $(LIBDIR) ; \
	       cd .. ; \
	       $(RM) -r tmp ; \
	   else \
	     $(INSTALL) -m 644 $(PGSBOXLIB) $(LIBDIR) ; \
	   fi
	   $(RANLIB) $(LIBDIR)/$(PGSBOXLIB)
	-  $(RM) $(LIBDIR)/libpgsbox.a
	   $(LN_S) $(PGSBOXLIB) $(LIBDIR)/libpgsbox.a
	   if [ "$(SHRLIB)" != "" ] ; then \
	     $(INSTALL) -m 755 $(SHRLIB) $(LIBDIR) ; \
	     if [ -h "$(LIBDIR)/$(SONAME)" ] ; then \
	       $(RM) $(LIBDIR)/$(SONAME) ; \
	     fi ; \
	     $(LN_S) $(SHRLIB) $(LIBDIR)/$(SONAME) ; \
	     if [ "$(SHRLN)" != "" ] ; then \
	       if [ -h "$(LIBDIR)/$(SHRLN)" ] ; then \
	         $(RM) $(LIBDIR)/$(SHRLN) ; \
	       fi ; \
	       $(LN_S) $(SONAME) $(LIBDIR)/$(SHRLN) ; \
	     fi ; \
	   fi
	   $(INSTALL) -m 444 *.h $(INCDIR)

uninstall :
	-  cd $(LIBDIR) && $(RM) $(PGSBOXLIB) $(SHRLN) $(SONAME) $(SHRLIB)

clean :
	-  $(RM) *.o $(LIBLOCK) *.i a.out core *.dSYM
	-  $(RM) -r $(EXTRA_CLEAN)

cleaner : clean
	-  $(RM) pgtest cpgtest

cleanest distclean realclean : cleaner
	-  $(RM) $(PICLIB) libpgsbox-*.a libpgsbox.so.* libpgsbox.*.dylib

check test : tests
	-@ echo ''
	-@ $(TIMER)
	-@ echo 'Running the PGSBOX test program, PGTEST:'
	-@ if [ '$(MODE)' = interactive ] ; then \
	     ./pgtest ; \
	   else \
	     ./pgtest < /dev/null ; \
	   fi
	-@ echo ''
	-@ echo ''
	-@ $(TIMER)
	-@ echo 'Running the cpgsbox() test program, cpgtest:'
	-@ if [ '$(MODE)' = interactive ] ; then \
	     ./cpgtest ; \
	   else \
	     ./cpgtest < /dev/null ; \
	   fi

tests : wcslib pgtest cpgtest

wcslib : $(WCSLIB)

$(WCSLIB) :
	-@ echo ''
	   $(MAKE) -C ../Fortran lib

$(WCSLEEP) :
	-@ echo ''
	   $(MAKE) -C ../Fortran $(@F)

pgtest : pgtest.f fscan.F lngvel.F $(PGSBOXLIB) $(WCSLIB) $(WCSLEEP)
	-@ $(RM) $@
	-@ echo ''
	   $(FC) -I../Fortran $(FFLAGS) -o $@ $^ $(LDFLAGS) \
	     $(PGPLOTLIB) $(LIBS)

cpgtest : cpgtest.c fscan.F lngvel.F $(PGSBOXLIB) $(WCSLIB)
	-@ $(RM) $@
	-@ echo ''
	   $(FC) -I../Fortran $(FFLAGS) -c fscan.F lngvel.F
	   $(CC) $(CPPFLAGS) $(PGPLOTINC) $(CFLAGS) -o $@ $(^:.F=.o) \
	     $(LDFLAGS) $(PGPLOTLIB) $(FLIBS) $(LIBS)
	-@ $(RM) fscan.o lngvel.o

GNUmakefile : ../makedefs ;

../makedefs ../wcsconfig_f77.h : makedefs.in wcsconfig_f77.h.in \
    ../config.status
	-@ $(RM) ../wcsconfig_f77.h
	   cd .. && ./config.status

show ::
	-@ echo 'For building libpgsbox...'
	-@ echo '  PGSBOXLIB   := $(PGSBOXLIB)'
	-@ echo '  PICLIB      := $(PICLIB)'
	-@ echo '  WCSSHR      := $(WCSSHR)'
	-@ echo '  SHRLIB      := $(SHRLIB)'
	-@ echo '  SONAME      := $(SONAME)'
	-@ echo '  SHRFLAGS    := $(SHRFLAGS)'
	-@ echo '  SHRLD       := $(SHRLD)'
	-@ echo '  SHRLN       := $(SHRLN)'
	-@ echo ''
	-@ echo '  BINDC       := $(BINDC)'
	-@ echo '  MODULES     := $(MODULES)'

# Dependencies
#-------------

$(PGSBOXLIB)(cpgsbox.o) : cpgsbox.h wcsconfig_f77.h
$(PGSBOXLIB)(pgwcsl.o)  : cel.h lin.h prj.h spc.h sph.h spx.h wcs.h \
                          wcsconfig_f77.h

pgtest.o  : wcs.inc
cpgtest.o : cel.h cpgsbox.h lin.h prj.h spc.h spx.h wcs.h wcsconfig_f77.h \
            wcserr.h wcsfix.h
