/^[^*]/{p;d;}

/^\*/s| fitskey| #fitskey|g

s|CONTINUE|<TT><B>&</B></TT>|g
s|END|<TT><B>&</B></TT>|g
s|ABCD.*89-_|<TT><B>&</B></TT>|g
s|"= "|''<TT><B>= </B></TT>''|g
s|'='|'<TT><B>=</B></TT>'|g
s|'/'|'<TT><B>/</B></TT>'|g
s|'&'|'<TT><B>\&</B></TT>'|g
s|(')|(<TT><B>'</B></TT>)|g

