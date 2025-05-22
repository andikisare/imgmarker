/^[^*]/{p;d;}

# Standard bintable keywords (see also doxextr.sed).
s|\([ >]\)CROTAi|\1<TT><B>CROTA</B>i</TT>|g
s|\([ >]\)DAVGn|\1<TT><B>DAVG</B>n</TT>|g
s|\([ >]\)EQUIna|\1<TT><B>EQUI</B>na</TT>|g
s|\([ >]\)LATPna|\1<TT><B>LATP</B>na</TT>|g
s|\([ >]\)LONPna|\1<TT><B>LONP</B>na</TT>|g
s|\([ >]\)MJDAn|\1<TT><B>MJDA</B>n</TT>|g
s|\([ >]\)MJDOBn|\1<TT><B>MJDOB</B>n</TT>|g
s|\([ >]\)OBSGXn|\1<TT><B>OBSGX</B>n</TT>|g
s|\([ >]\)OBSGYn|\1<TT><B>OBSGY</B>n</TT>|g
s|\([ >]\)OBSGZn|\1<TT><B>OBSGZ</B>n</TT>|g
s|\([ >]\)RADEna|\1<TT><B>RADE</B>na</TT>|g
s|\([ >]\)RFRQna|\1<TT><B>RFRQ</B>na</TT>|g
s|\([ >]\)RWAVna|\1<TT><B>RWAV</B>na</TT>|g
s|\([ >]\)SOBSna|\1<TT><B>SOBS</B>na</TT>|g
s|\([ >]\)SPECna|\1<TT><B>SPEC</B>na</TT>|g
s|\([ >]\)SSRCna|\1<TT><B>SSRC</B>na</TT>|g
s|\([ >]\)TCDEna|\1<TT><B>TCDE</B>na</TT>|g
s|\([ >]\)TCDLTn|\1<TT><B>TCDLT</B>n</TT>|g
s|\([ >]\)TCNAna|\1<TT><B>TCNA</B>na</TT>|g
s|\([ >]\)TCPERn|\1<TT><B>TCPER</B>n</TT>|g
s|\([ >]\)TCPRna|\1<TT><B>TCPR</B>na</TT>|g
s|\([ >]\)TCRDna|\1<TT><B>TCRD</B>na</TT>|g
s|\([ >]\)TCRPXn|\1<TT><B>TCRPX</B>n</TT>|g
s|\([ >]\)TCRPna|\1<TT><B>TCRP</B>na</TT>|g
s|\([ >]\)TCRVLn|\1<TT><B>TCRVL</B>n</TT>|g
s|\([ >]\)TCRVna|\1<TT><B>TCRV</B>na</TT>|g
s|\([ >]\)TCSYna|\1<TT><B>TCSY</B>na</TT>|g
s|\([ >]\)TCTYPn|\1<TT><B>TCTYP</B>n</TT>|g
s|\([ >]\)TCTYna|\1<TT><B>TCTY</B>na</TT>|g
s|\([ >]\)TCUNIn|\1<TT><B>TCUNI</B>n</TT>|g
s|\([ >]\)TCUNna|\1<TT><B>TCUN</B>na</TT>|g
s|\([ >]\)TCZPHn|\1<TT><B>TCZPH</B>n</TT>|g
s|\([ >]\)TCZPna|\1<TT><B>TCZP</B>na</TT>|g
s|\([ >]\)TCn_ka|\1<TT><B>TC</B>n<B>_</B>ka</TT>|g
s|\([ >]\)TFIELDS|\1<TT><B>TFIELDS</B></TT>|g
s|\([ >]\)TFORM|\1<TT><B>TFORM</B></TT>|g
s|\([ >]\)TPn_ka|\1<TT><B>TP</B>n<B>_</B>ka</TT>|g
s|\([ >]\)TRDIRn|\1<TT><B>MJDA</B>n</TT>|g
s|\([ >]\)TRPOSn|\1<TT><B>MJDA</B>n</TT>|g
s|\([ >]\)TSn_ma|\1<TT><B>TS</B>n<B>_</B>ma</TT>|g
s|\([ >]\)TVn_ma|\1<TT><B>TV</B>n<B>_</B>ma</TT>|g
s|\([ >]\)TWCSna|\1<TT><B>TWCS</B>na</TT>|g
s|\([ >]\)VANGna|\1<TT><B>VANG</B>na</TT>|g
s|\([ >]\)VSYSna|\1<TT><B>VSYS</B>na</TT>|g
s|\([ >]\)WCAXna|\1<TT><B>WCAX</B>na</TT>|g
s|\([ >]\)WCSNna|\1<TT><B>WCSN</B>na</TT>|g
s|\([ >]\)iCDEna|\1<TT>i<B>CDE</B>na</TT>|g
s|\([ >]\)iCDLTn|\1<TT>i<B>CDLT</B>n</TT>|g
s|\([ >]\)iCNAna|\1<TT>i<B>CNA</B>na</TT>|g
s|\([ >]\)iCPERn|\1<TT>i<B>CPER</B>n</TT>|g
s|\([ >]\)iCPRna|\1<TT>i<B>CPR</B>na</TT>|g
s|\([ >]\)iCRDna|\1<TT>i<B>CRD</B>na</TT>|g
s|\([ >]\)iCROTn|\1<TT>i<B>CROT</B>n</TT>|g
s|\([ >]\)iCRVLn|\1<TT>i<B>CRVL</B>n</TT>|g
s|\([ >]\)iCRVna|\1<TT>i<B>CRV</B>na</TT>|g
s|\([ >]\)iCSYna|\1<TT>i<B>CSY</B>na</TT>|g
s|\([ >]\)iCTYPn|\1<TT>i<B>CTYP</B>n</TT>|g
s|\([ >]\)iCTYna|\1<TT>i<B>CTY</B>na</TT>|g
s|\([ >]\)iCUNIn|\1<TT>i<B>CUNI</B>n</TT>|g
s|\([ >]\)iCUNna|\1<TT>i<B>CUN</B>na</TT>|g
s|\([ >]\)iCZPHn|\1<TT><B>TCZPH</B>n</TT>|g
s|\([ >]\)iCZPna|\1<TT><B>TCZP</B>na</TT>|g
s|\([ >]\)iSn_ma|\1<TT>i<B>S</B>n<B>_</B>ma</TT>|g
s|\([ >]\)iVn_ma|\1<TT>i<B>V</B>n<B>_</B>ma</TT>|g
s|\([ >]\)ijCDna|\1<TT>ij<B>CD</B>na</TT>|g
s|\([ >]\)ijPCna|\1<TT>ij<B>PC</B>na</TT>|g
s|\([ >]\)jCRPXn|\1<TT>j<B>CRPX</B>n</TT>|g
s|\([ >]\)jCRPna|\1<TT>j<B>CRP</B>na</TT>|g

# Non-standard or deprecated.
s|\([ >]\)ALTRPIX|\1<TT><B>ALTRPIX</B></TT>|g
s|\([ >]\)ALTRVAL|\1<TT><B>ALTRVAL</B></TT>|g
s|\([ >]\)CD00i00j|\1<TT><B>CD00</B>i<B>00</B>j</TT>|g
s|\([ >]\)CROTAia|\1<TT><B>CROTA</B>ia</TT>|g
s|\([ >]\)CROTAn|\1<TT><B>CROTA</B>n</TT>|g
s|\([ >]\)DOBSn|\1<TT><B>DOBS</B>n</TT>|g
s|\([ >]\)EPOCHa|\1<TT><B>EPOCH</B>a</TT>|g
s|\([ >]\)EPOCH|\1<TT><B>EPOCH</B></TT>|g
s|\([ >]\)OBSGLn|\1<TT><B>OBSGL</B>n</TT>|g
s|\([ >]\)OBSGBn|\1<TT><B>OBSGB</B>n</TT>|g
s|\([ >]\)OBSGHn|\1<TT><B>OBSGH</B>n</TT>|g
s|\([ >]\)PC00i00j|\1<TT><B>PC00</B>i<B>00</B>j</TT>|g
s|\([ >]\)PROJPn|\1<TT><B>PROJP</B>n</TT>|g
s|\([ >]\)RADECSYS|\1<TT><B>RADECSYS</B></TT>|g
s|\([ >]\)RESTFREQ|\1<TT><B>RESTFREQ</B></TT>|g
s|\([ >]\)TCDLTna|\1<TT><B>TCDLT</B>na</TT>|g
s|\([ >]\)TCDn_ka|\1<TT><B>TCD</B>n<B>_</B>ka</TT>|g
s|\([ >]\)TCNAMn|\1<TT><B>TCNAM</B>n</TT>|g
s|\([ >]\)TCNAMna|\1<TT><B>TCNAM</B>na</TT>|g
s|\([ >]\)TCPERna|\1<TT><B>TCPER</B>na</TT>|g
s|\([ >]\)TCRDEn|\1<TT><B>TCRDE</B>n</TT>|g
s|\([ >]\)TCRDEna|\1<TT><B>TCRDE</B>na</TT>|g
s|\([ >]\)TCROTna|\1<TT><B>TCROT</B>na</TT>|g
s|\([ >]\)TCRPXna|\1<TT><B>TCRPX</B>na</TT>|g
s|\([ >]\)TCRVLna|\1<TT><B>TCRVL</B>na</TT>|g
s|\([ >]\)TCSYEn|\1<TT><B>TCSYE</B>n</TT>|g
s|\([ >]\)TCSYEna|\1<TT><B>TCSYE</B>na</TT>|g
s|\([ >]\)TCTYPn|\1<TT><B>TCTYP</B>n</TT>|g
s|\([ >]\)TCTYPna|\1<TT><B>TCTYP</B>na</TT>|g
s|\([ >]\)TCUNIna|\1<TT><B>TCUNI</B>na</TT>|g
s|\([ >]\)TCZPHna|\1<TT><B>TCZPH</B>na</TT>|g
s|\([ >]\)TPCn_ka|\1<TT><B>TPC</B>n<B>_</B>ka</TT>|g
s|\([ >]\)TPSn_ma|\1<TT><B>TPS</B>n<B>_</B>ma</TT>|g
s|\([ >]\)TPVn_ma|\1<TT><B>TPV</B>n<B>_</B>ma</TT>|g
s|\([ >]\)VELREFa|\1<TT><B>VELREF</B>a</TT>|g
s|\([ >]\)VELREF|\1<TT><B>VELREF</B></TT>|g
s|\([ >]\)VSOURCEa|\1<TT><B>VSOURCE</B>a</TT>|g
s|\([ >]\)VSOUna|\1<TT><B>VSOU</B>na</TT>|g
s|\([ >]\)ZSOUna|\1<TT><B>ZSOU</B>na</TT>|g
s|\([ >]\)iCDLTna|\1<TT>i<B>CDLT</B>na</TT>|g
s|\([ >]\)iCNAMn|\1<TT>i<B>CNAM</B>n</TT>|g
s|\([ >]\)iCNAMna|\1<TT>i<B>CNAM</B>na</TT>|g
s|\([ >]\)iCPERna|\1<TT><B>TCPER</B>na</TT>|g
s|\([ >]\)iCRDEn|\1<TT>i<B>CRDE</B>n</TT>|g
s|\([ >]\)iCRDEna|\1<TT>i<B>CRDE</B>na</TT>|g
s|\([ >]\)iCROTna|\1<TT>i<B>CROT</B>na</TT>|g
s|\([ >]\)iCRVLna|\1<TT>i<B>CRVL</B>na</TT>|g
s|\([ >]\)iCSYEn|\1<TT>i<B>CSYE</B>n</TT>|g
s|\([ >]\)iCSYEna|\1<TT>i<B>CSYE</B>na</TT>|g
s|\([ >]\)iCTYPn|\1<TT>i<B>CTYP</B>n</TT>|g
s|\([ >]\)iCTYPna|\1<TT>i<B>CTYP</B>na</TT>|g
s|\([ >]\)iCUNIna|\1<TT>i<B>CUNI</B>na</TT>|g
s|\([ >]\)iCZPHna|\1<TT><B>TCZPH</B>na</TT>|g
s|\([ >]\)iPSn_ma|\1<TT>i<B>PS</B>n<B>_</B>ma</TT>|g
s|\([ >]\)iPVn_ma|\1<TT>i<B>PV</B>n<B>_</B>ma</TT>|g
s|\([ >]\)jCRPXna|\1<TT>j<B>CRPX</B>na</TT>|g

s|'TAB'|<TT>'<B>TAB</B>'</TT>|g
s|'T'|<TT>'<B>T</B>'</TT>|g

s|'{DATE,|<TT><B>'</B>{<B>DATE</B></TT>,|g
s|,MJD}-|,<TT><B>MJD</B>}<B>-</B></TT>|g
s|{OBS,|{<TT><B>OBS</B>,|g
s|,BEG,|,<B>BEG</B>,|g
s|,AVG,|,<B>AVG</B>,|g
s|,END}'|,<B>END</B>}<B>'</B></TT>|g
s|'OBSGEO-|<TT><B>'OBSGEO-</B>|g
s|{X,|{<B>X</B>,|g
s|,Y,|,<B>Y</B>,|g
s|,Z,|,<B>Z</B>,|g
s|,L,|,<B>L</B>,|g
s|,B,|,<B>B</B>,|g
s|,H}'|,<B>H</B>}<B>'</B></TT>|g

s|WCSHDR_|#&|g
s|WCSHDO_|#&|g

/^\*/s|tabprm|#&|g
/^\*/s|wcsprm|#&|g
/^\*/s|wtbarr[^.]|#&|g

s|fits_hdr2str()|<VAR>&</VAR>|g

s|m = n <= 9|<TT>m = n</TT> @f$\\le@f$ 9|
s| ARE NOT | <B><EM>are not</EM></B> |
s| ARE | <B><EM>are</EM></B> |
s|"relax"|<VAR>relax</VAR>|
