/^[^*]/{p;d;}

s|CTYPEn|<TT><B>CTYPE</B>n</TT>|g
s|VELREF|<TT><B>&</B></TT>|g

s|'AFRQ'|'<TT><B>AFRQ</B></TT>'|g
s|'AWAV'|'<TT><B>AWAV</B></TT>'|g
s|'BETA'|'<TT><B>BETA</B></TT>'|g
s|'ENER'|'<TT><B>ENER</B></TT>'|g
s|'FREQ'|'<TT><B>FREQ</B></TT>'|g
s|'FELO'|'<TT><B>FELO</B></TT>'|g
s|'VELO'|'<TT><B>VELO</B></TT>'|g
s|'VOPT'|'<TT><B>VOPT</B></TT>'|g
s|'VRAD'|'<TT><B>VRAD</B></TT>'|g
s|'WAVE'|'<TT><B>WAVE</B></TT>'|g
s|'WAVN'|'<TT><B>WAVN</B></TT>'|g
s|'ZOPT'|'<TT><B>ZOPT</B></TT>'|g

s|'VELO-F2V'|<TT><B>&</B></TT>|g
s|'ZOPT-F2W'|<TT><B>&</B></TT>|g
s|'VRAD-V2F'|<TT><B>&</B></TT>|g
s|'VOPT-V2W'|<TT><B>&</B></TT>|g
s|'ZOPT-V2W'|<TT><B>&</B></TT>|g
s|'BETA-W2V'|<TT><B>&</B></TT>|g
s|'LOG'|'<TT><B>LOG</B></TT>'|g
s|'TAB'|'<TT><B>TAB</B></TT>'|g
s|'GRA'|'<TT><B>GRA</B></TT>'|g
s|'GRI'|'<TT><B>GRI</B></TT>'|g

s|X -> P -> S|@f$X\\leadsto P\\rightarrow S@f$|g
s|S -> P -> X|@f$S\\rightarrow P\\leadsto X@f$|g
s| \([PSX]\)\([ -.:]\)| @f$\1@f$\2|g

s| S | @f$S@f$ |g
s| G, | @f$G@f$, |g
s| m, | @f$m@f$, |g
s|alpha|@f$\\alpha@f$|g
s|n_r|@f$n_r@f$|g
s|n'_r|@f$n'_r@f$|g
s|epsilon|@f$\\epsilon@f$|g
s|theta|@f$\\theta@f$|g
s|lambda_r|@f$\\lambda_r@f$|g
s|dn/dlambda|@f$dn/d\\lambda@f$|g
s|dX/dS|@f$dX/dS@f$|g
s|dS/dX|@f$dS/dX@f$|g

s|restreq%3 != 0|\\code & \\endcode|g
