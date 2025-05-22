/^[^*]/{p;d;}

/^\*/s| disprm| #disprm|g

s|A_ORDER|<TT><B>A_ORDER</B></TT>|g
s|A_p_q|<TT><B>A_</B>p<B>_</B>q</TT>|g
s|AP_p_q|<TT><B>AP_</B>p<B>_</B>q</TT>|g
s|B_ORDER|<TT><B>B_ORDER</B></TT>|g
s|B_p_q|<TT><B>B_</B>p<B>_</B>q</TT>|g
s|BP_p_q|<TT><B>BP_</B>p<B>_</B>q</TT>|g
s|CPDISja|<TT><B>CPDIS</B>ja</TT>|g
s|CQDISia|<TT><B>CQDIS</B>ia</TT>|g
s|CPERRja|<TT><B>CPERR</B>ja</TT>|g
s|CQERRia|<TT><B>CQERR</B>ia</TT>|g
s|DOCORR|<TT><B>DOCORR</B></TT>|g
s|DPja|<TT><B>DP</B>ja</TT>|g
s|DQia|<TT><B>DQ</B>ia</TT>|g
s|DVERRa|<TT><B>DVERR</B>a</TT>|g
s|PVi_\([0-4]\)a|<TT><B>PV</B>i<B>_\1</B>a</TT>|g

s|\.NAXES|<TT><B>&</B></TT>|g
s|\.AXIS\.|<TT><B>&</B></TT>|g

s|AMD[XY]|<TT><B>&</B></TT>|g

s|DSS|<TT><B>&</B></TT>|g
s|TAN|<TT><B>&</B></TT>|g
s|TNX|<TT><B>&</B></TT>|g
s|TPD|<TT><B>&</B></TT>|g
s|TPV|<TT><B>&</B></TT>|g
s|SIP|<TT><B>&</B></TT>|g
s|WAT|<TT><B>&</B></TT>|g
s|ZPN|<TT><B>&</B></TT>|g
s|ZPX|<TT><B>&</B></TT>|g

s|sqrt(xx + yy)|@f$\\sqrt(x^2 + y^2)@f$|g
s|(xx + yy)|@f$(x^2 + y^2)@f$|g
