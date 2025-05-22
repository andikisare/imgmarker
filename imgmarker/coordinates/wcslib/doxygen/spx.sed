/^[^*]/{p;d;}

s|AFRQ|<TT><B>&</B></TT>|g
s|AWAV|<TT><B>&</B></TT>|g
s|BETA|<TT><B>&</B></TT>|g
s|ENER|<TT><B>&</B></TT>|g
s|FREQ|<TT><B>&</B></TT>|g
s|VELO|<TT><B>&</B></TT>|g
s|VOPT|<TT><B>&</B></TT>|g
s|VRAD|<TT><B>&</B></TT>|g
s|WAVE|<TT><B>&</B></TT>|g
s|WAVN|<TT><B>&</B></TT>|g
s|ZOPT|<TT><B>&</B></TT>|g

s|velotype)|<EM>velotype</EM>)|g
s|(wavetype|(<EM>wavetype</EM>|g

s|= 1 / 2\*pi|@f$= 1 / 2 \\pi@f$|g
s|= 2\*pi|@f$= 2 \\pi@f$|g
s|= c,|@f$= c@f$,|g
s|= 1/c|@f$= 1/c@f$|g
s|= h,|@f$= h@f$,|g
s|= 1/h|@f$= 1/h@f$|g
s|= v/c|@f$\\beta = v/c@f$|g
