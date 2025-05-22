/^[^*]/{p;d;}

s|dist and pa|<VAR>dist</VAR> and <VAR>pa</VAR>|
s|lng and lat|<VAR>lng</VAR> and <VAR>lat</VAR>|
s|phi and theta|<VAR>phi</VAR> and <VAR>theta</VAR>|

s|\([1-9][0-9]*\) degrees|@f$\1^\\circ@f$|g
s|(lng0,+90-epsilon)|@f$(\\alpha_0,+90^\\circ-\\epsilon)@f$|
s|(lng0,-90+epsilon)|@f$(\\alpha_0,-90^\\circ+\\epsilon)@f$|
s| 0 or | @f$0^\\circ@f$ or |
s| epsilon| @f$\\epsilon@f$|g
s|cos(|@f$cos@f$(|g
s|sin(|@f$sin@f$(|g
