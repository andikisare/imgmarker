/^[^*]/{p;d;}

s|PVi_\([0-4]\)a|<TT><B>PV</B>i<B>_\1</B>a</TT>|g

s| <= | @f$\\leq@f$ |g
s|(K_1, K_2,... K_M)|@f$&@f$|g
s| K_1 \* K_2 \* ... \* K_M |@f$K_1 K_2 \\ldots K_M@f$|g
s| compressed K_1 | compressed @f$K_1@f$ |g
s|Upsilon_m|@f$\\&@f$|g
