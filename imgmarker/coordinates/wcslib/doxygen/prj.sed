/^[^*]/{p;d;}

s|PVi_\([0-4]\)a|<TT><B>PV</B>i<B>_\1</B>a</TT>|g

s| prjprm| #prjprm|g

s|???set()|<B>&</B>|g
s|???x2s()|<B>&</B>|g
s|???s2x()|<B>&</B>|g

s|AIR|<TT><B>&</B></TT>|g
s|AIT|<TT><B>&</B></TT>|g
s|ARC|<TT><B>&</B></TT>|g
s|AZP|<TT><B>&</B></TT>|g
s|BON|<TT><B>&</B></TT>|g
s|CAR|<TT><B>&</B></TT>|g
s|CEA|<TT><B>&</B></TT>|g
s|COD|<TT><B>&</B></TT>|g
s|COE|<TT><B>&</B></TT>|g
s|COO|<TT><B>&</B></TT>|g
s|COP|<TT><B>&</B></TT>|g
s|CSC|<TT><B>&</B></TT>|g
s|CYP|<TT><B>&</B></TT>|g
s|HPX|<TT><B>&</B></TT>|g
s|MER|<TT><B>&</B></TT>|g
s|MOL|<TT><B>&</B></TT>|g
s|PAR|<TT><B>&</B></TT>|g
s|PCO|<TT><B>&</B></TT>|g
s|QSC|<TT><B>&</B></TT>|g
s|SFL|<TT><B>&</B></TT>|g
s|SIN|<TT><B>&</B></TT>|g
s|STG|<TT><B>&</B></TT>|g
s|SZP|<TT><B>&</B></TT>|g
s|TAN|<TT><B>&</B></TT>|g
s|TSC|<TT><B>&</B></TT>|g
s|ZEA|<TT><B>&</B></TT>|g
s|ZPN|<TT><B>&</B></TT>|g

s| i | <TT>i</TT> |g

s|carree|car\&eacute;e|g

s|\[-90,90\]|@f$[-90^\\circ,90^\\circ]@f$|g
s|\[-180,180\]|@f$[-180^\\circ,180^\\circ]@f$|g
s|180/pi|@f$180^\\circ/\\pi@f$|g
s|\([1-9][0-9]*\) degrees|@f$\1^\\circ@f$|g
s| 1 degree | @f$1^\\circ@f$ degree |g
s| 1E-10 degree | @f$0^\\circ.0000000001@f$ |g

s| phi\([ .]\)| @f$\\phi@f$\1|g
s| phi, | @f$\\phi@f$, |g
s| theta\([ .]\)| @f$\\theta@f$\1|g
s| theta, | @f$\\theta@f$, |g
s|phi_0|@f$\\phi_0@f$|g
s|theta_0|@f$\\theta_0@f$|g
s|(phi,theta)|@f$(\\phi,\\theta)@f$|g
s|(x,y)|@f$(x,y)@f$|g
s| x, | @f$x@f$,|g
s| x\([ .]\)| @f$x@f$\1|g
s| y, | @f$y@f$,|g
s| y\([ .]\)| @f$y@f$\1|g
