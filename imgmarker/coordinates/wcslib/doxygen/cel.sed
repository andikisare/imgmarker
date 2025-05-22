/^[^*]/{p;d;}

/^\*/s| celprm| #celprm|g

s|PVi_\([0-4]\)a|<TT><B>PV</B>i<B>_\1</B>a</TT>|g

s|UNDEFINED|<B><TT>&</TT></B>|g

s|delta_p|@f$\\delta_{\\mathrm p}@f$|g
s|phi_0|@f$\\phi_0@f$|g
s|phi_p|@f$\\phi_{\\mathrm p}@f$|g
s|theta_0|@f$\\theta_0@f$|g
s|theta_p|@f$\\theta_{\\mathrm p}@f$|g
s|(lng,lat)|@f$(\\alpha,\\delta)@f$|g
s|(phi,theta)|@f$(\\phi,\\theta)@f$|g
s|(x,y)|@f$(x,y)@f$|g
s|X-|@f$X@f$-|g
s|Z-|@f$Z@f$-|g
s|Z'-|@f$Z'@f$-|g
s|+/-|@f$\\pm@f$|g
s|\([1-9][0-9]*\) degrees|@f$\1^\\circ@f$|g
