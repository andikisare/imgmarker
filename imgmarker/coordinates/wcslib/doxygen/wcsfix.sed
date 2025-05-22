/^[^*]/{p;d;}

s|CD00i00j|<TT><B>&</B></TT>|g
s|EPOCH|<TT><B>&</B></TT>|g
s|PC00i00j|<TT><B>&</B></TT>|g
s|PROJPn|<TT><B>&</B></TT>|g
s|VELREF|<TT><B>&</B></TT>|g
s|VSOURCEa|<TT><B>&</B></TT>|g

s|GLS|<TT><B>&</B></TT>|g
s|NCP|<TT><B>&</B></TT>|g
s|SIN|<TT><B>&</B></TT>|g

s|FREQ\([^-]\)|<TT><B>FREQ</B></TT>\1|g
s|FELO\([^-]\)|<TT><B>FELO</B></TT>\1|g
s|VELO\([^-]\)|<TT><B>VELO</B></TT>\1|g
s|\([^-]\)OBS|\1<TT><B>OBS</B></TT>|g
s|\([^-]\)LSR|\1<TT><B>LSR</B></TT>|g
s|\([^-]\)HEL|\1<TT><B>HEL</B></TT>|g

s|'VELO-OBS'|<TT><B>&</B></TT>|g
s|'FELO-HEL'|<TT><B>&</B></TT>|g
s|'FREQ-LSR'|<TT><B>&</B></TT>|g

s|'DEG'|'<TT><B>DEG</B></TT>'|g
s|'deg'|'<TT><B>deg</B></TT>'|g

s|CLDJ|<VAR>&</VAR>|g
s|DJCL|<VAR>&</VAR>|g

s|yyyy-mm-ddThh:mm:ss|<EM>yyyy-mm-dd</EM><TT><B>T</B></TT><EM>hh:mm:ss</EM>|g
