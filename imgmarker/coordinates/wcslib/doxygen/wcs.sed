/^[^*]/{p;d;}

s|CROTAi|<TT><B>CROTA</B>i</TT>|g
s|EPOCH|<TT><B>&</B></TT>|g
s|VELREF|<TT><B>&</B></TT>|g

s|PVi_\([0-4]\)a|<B><TT>PV</TT>i<TT>_\1</TT>a</B>|g
s|'a'|'<B>a</B>'|g
s|axis i |axis <B>i</B> |g

s|\([^_]\)CUBEFACE|\1<TT><B>CUBEFACE</B></TT>|g
s|\([^_]\)STOKES|\1<TT><B>STOKES</B></TT>|g

s|'RA--'|'<TT><B>RA--</B></TT>'|g
s|'DEC-'|'<TT><B>DEC-</B></TT>'|g
s|'GLON'|'<TT><B>GLON</B></TT>'|g
s|'GLAT'|'<TT><B>GLAT</B></TT>'|g

s|CSC|<TT><B>&</B></TT>|g
s|GLS|<TT><B>&</B></TT>|g
s|NCP|<TT><B>&</B></TT>|g
s|QSC|<TT><B>&</B></TT>|g
s|SFL|<TT><B>&</B></TT>|g
s|SIN|<TT><B>&</B></TT>|g
s|TSC|<TT><B>&</B></TT>|g

s|'FREQ'|'<TT><B>FREQ</B></TT>'|g
s|'FELO-HEL'|<TT><B>&</B></TT>|g
s|'FREQ-LSR'|<TT><B>&</B></TT>|g
s|'ZOPT-F2W'|<TT><B>&</B></TT>|g

s|yyyy-mm-ddThh:mm:ss|<EM>yyyy-mm-dd</EM><TT><B>T</B></TT><EM>hh:mm:ss</EM>|g

s|(phi_0,theta_0)|@f$(\\phi_0,\\theta_0)@f$|
s|phi_p|@f$\\phi_{\\mathrm p}@f$|g
s|theta_p|@f$\\theta_{\\mathrm p}@f$|g
s| x-| @f$x@f$-|g
s| y-| @f$y@f$-|g

s/altlin |= [124];/\\code & \\endcode/
