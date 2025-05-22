/*============================================================================
  WCSLIB 8.4 - an implementation of the FITS WCS standard.
  Copyright (C) 1995-2024, Mark Calabretta

  This file is part of WCSLIB.

  WCSLIB is free software: you can redistribute it and/or modify it under the
  terms of the GNU Lesser General Public License as published by the Free
  Software Foundation, either version 3 of the License, or (at your option)
  any later version.

  WCSLIB is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
  FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for
  more details.

  You should have received a copy of the GNU Lesser General Public License
  along with WCSLIB.  If not, see http://www.gnu.org/licenses.

  Author: Mark Calabretta, Australia Telescope National Facility, CSIRO.
  http://www.atnf.csiro.au/people/Mark.Calabretta
  $Id: doxextr.l,v 8.4 2024/10/28 13:56:17 mcalabre Exp $
*=============================================================================
*
* doxextr.l is a Flex description file containing a lexical scanner definition
* used to extract comments from the prologue of WCSLIB header files and
* produce mark-up for doxygen.  It relies on strict formatting of comments
* in the header file.
*
* Header sections are:
*   - SUMMARY:   Introduced by '* Summary of the {NAME} '
*       where {NAME} is the name of the header file without .h suffix.
*
*   - FUNCTION:  Introduced by '* {NAME}() - '
*       where {NAME} is the name of the function.
*
*   - STRUCTURE: Introduced by '* {NAME} struct - ' or '* {NAME} union - '
*       where {NAME} is the name of the struct or union.
*
*   - DEFINE:    Introduced by '* {NAME} define - ' or '* {NAME}() macro - '
*       where {NAME} is the name of the preprocessor definition.
*
*   - VARIABLE:  Introduced by '* Global variable: {NAME} - '
*       where {NAME} is the name of a global variable.
*
* It requires Flex v2.5.4 or later.
*
*===========================================================================*/

/* Options. */
/* %option full */
%option never-interactive
%option noinput
%option nounput
%option noyywrap
%option outfile="doxextr.c"
%option prefix="doxextr"

/* Indentation levels. */
I   "  "
IT  {I}{5}
ID  {I}{10}

/* Patterns. */
NAME [a-zA-Z_][a-zA-Z_0-9]*

/* Optional whitespace. */
WS0  " "*

/* Required whitespace. */
WS1  " "+

/* Sequence of non-whitespace characters. */
NWS  [^ ]+

/* Hyphen. */
DASH {WS1}-{WS1}

/* Exclusive start states. */
%x PROLOG BODY
%x DEFINE FUNCTION STRUCTURE SUMMARY VARIABLE
%x DEFMARK FILEMARK FNMARK STRUCTMARK UNIONMARK VARMARK
%x BRIEF NOTES PARAM RETURN STRUCTVAR TABLEROW
%x FLUSH PRINTE PRINTF

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define TABLE 1
#define VERBATIM 2
%}

%%
	const int id = 24;
	
	char *(func[128]), listype[8], *(proto[128]), name[32], *param,
	     text[128];
	int  ifunc, ilist, indent, listndt[8], lmore, nfunc, pass1, pcont,
	     plist, section, special, subsection, td;
	
	void listitem(int indent, char listype[8], int listndt[8],
	              int *ilist);
	void endlist(int isItem, int indent, char listype[8], int listndt[8],
	             int *ilist);
	void endspecial(int *special);
	void printe(const char *text, const char *name);

	*listype = '-';
	memset(name, 0, 32);
	
	ilist      = 0;
	*listndt   = -1;
	lmore      = 0;
	nfunc      = 0;
	pass1      = 1;
	pcont      = 0;
	plist      = 0;
	section    = PROLOG;
	special    = 0;
	subsection = 0;
	td         = 0;
	
	BEGIN(PROLOG);
	
<PROLOG>\n {}

<PROLOG>^\/ |
<PROLOG>^{WS1} |
<PROLOG>^\*=+ {
	  // Copyright notice.
	  BEGIN(FLUSH);
	}

<*>^\*{WS0}\n\*{WS0}\n {
	  // Consecutive blank lines denoting the end of a section.
	  if (pass1) {
	    BEGIN(FLUSH);
	  } else if (section != BODY) {
	    if (section != PROLOG) {
	      endlist(0, 0, listype, listndt, &ilist);
	      endspecial(&special);
	
	      printf("*/\n");
	      section = PROLOG;
	    }
	
	    BEGIN(PROLOG);
	  }
	}

<*>^\*=+\*\/ {
	  // End of prologue.
	  if (pass1) {
	    section = BODY;
	    BEGIN(FLUSH);
	  } else {
	    if (section != PROLOG) {
	      endlist(0, 0, listype, listndt, &ilist);
	      endspecial(&special);
	
	      printf("*/\n");
	    }
	
	    for (ifunc = 0; ifunc < nfunc; ifunc++) {
	      free(proto[ifunc]);
	      free(func[ifunc]);
	    }
	
	    return 0;
	  }
	}

<*>{WS0}--+\n {
	  // Discard underlining.
	}

<*>^\*{WS0}\n {
	  if (!pass1) {
	    endspecial(&special);
	
	    lmore = yyleng;
	    yymore();
	  }
	}

<*>^\*" " {
	  // First-level prologue indentation.
	  if (pass1) {
	    BEGIN(FLUSH);
	  } else {
	    endspecial(&special);
	
	    lmore = yyleng;
	    yymore();
	  }
	}

<*>^-/\n {
	  // Horizontal rule.
	  if (!pass1) {
	    printf("* <HR>\n");
	  }
	  BEGIN(FLUSH);
	}

<*>^#{WS0} {
	  // HTML table.
	  if (pass1) {
	    BEGIN(FLUSH);
	  } else {
	    if (special != TABLE) {
	      endspecial(&special);
	
	      printf("* <HR><TABLE BORDER=0>\n");
	      special = TABLE;
	    }
	    printf("* <TR>\n*");
	    if (lmore+1 < yyleng) {
	      printf("%s", yytext+lmore+1);
	    }
	    td = 0;
	    BEGIN(TABLEROW);
	  }
	}

<*>^=" ".* |
<*>^=/\n {
	  // Verbatim text (code).
	  if (!pass1) {
	    if (special != VERBATIM) {
	      endspecial(&special);
	
	      printf("* @code\n");
	      special = VERBATIM;
	    }
	    printf(" %s\n", yytext+lmore+1);
	  }
	  BEGIN(FLUSH);
	}

<PROLOG>"Summary of the"{WS1} |
<PROLOG>"Summary of"{WS1} {
	  // The next token will be the file name.
	  section = SUMMARY;
	  BEGIN(FILEMARK);
	}

<PROLOG>{NAME}"()"{DASH} {
	  // Description of a function API.
	  section = FUNCTION;
	  subsection = 0;
	
	  yyless(lmore);
	  BEGIN(FNMARK);
	}

<PROLOG>{NAME}{WS1}struct{DASH} {
	  // Description of structure members.
	  section = STRUCTURE;
	  subsection = 0;
	
	  yyless(lmore);
	  BEGIN(STRUCTMARK);
	}

<PROLOG>{NAME}{WS1}union{DASH} {
	  // Description of union members.
	  section = STRUCTURE;
	  subsection = 0;
	
	  yyless(lmore);
	  BEGIN(UNIONMARK);
	}

<PROLOG>Global" "variable:" ".*{DASH} {
	  // Description of global variable.
	  section = VARIABLE;
	
	  yyless(lmore+17);
	  BEGIN(VARMARK);
	}

<PROLOG>{NAME}("()")*{WS1}(define|macro){DASH} {
	  // Description of preprocessor definition.
	  section = DEFINE;
	
	  yyless(lmore);
	  BEGIN(DEFMARK);
	}

<PROLOG>. {
	  BEGIN(FLUSH);
	}

<FILEMARK>{NAME} {
	  printf("/** @file %s.h\n*\n", yytext);
	  BEGIN(FLUSH);
	}

<SUMMARY>[A-Z].{1,50}: {
	  // Sub-section header.
	  endlist(0, 0, listype, listndt, &ilist);
	
	  printf("*\n* <B>%*s</B> @n\n", yyleng-(lmore+1), yytext+lmore);
	  BEGIN(FLUSH);
	}

<SUMMARY>{WS1}"- " |
<SUMMARY>{WS1}/{NWS}:\[^:] {
	  // Unnumbered list item.
	  lmore -= 2;
	  indent = yyleng - lmore;
	  if (yytext[yyleng-2] == '-') {
	    // The two-character pattern was matched.
	    indent -= 2;
	  }
	  endlist(1, indent, listype, listndt, &ilist);
	
	  if (lmore) printf("*\n");
	
	  if (indent > listndt[ilist]) {
	    ilist++;
	    listndt[ilist] = indent;
	    listype[ilist] = 'U';
	    printf("%-*s<%cL>\n", indent, "*", listype[ilist]);
	  }
	  printf("%-*s<LI> ", indent, "*");
	
	  BEGIN(PRINTE);
	}

<SUMMARY>{WS1} {
	  lmore -= 2;
	  indent = yyleng - lmore;
	  endlist(0, indent, listype, listndt, &ilist);
	
	  yymore();
	  BEGIN(PRINTE);
	}

<SUMMARY>. {
	  endlist(0, 0, listype, listndt, &ilist);
	
	  yymore();
	  BEGIN(PRINTE);
	}

<FNMARK>{NAME} {
	  strncpy(name, yytext, 31);
	  for (ifunc = 0; ifunc < nfunc; ifunc++) {
	    if (strncmp(yytext, func[ifunc], 32) == 0) {
	      printf("\n/** @fn %s\n*\n", proto[ifunc]);
	      break;
	    }
	  }
	
	  if (ifunc == nfunc) {
	    printf("\n/** @fn %s\n*\n", yytext);
	  }
	}

<FNMARK>"()"{DASH} {
	  BEGIN(BRIEF);
	}

<FUNCTION>Given: {
	  printf("*\n");
	  subsection = PARAM;
	  param = "in";
	  BEGIN(FLUSH);
	}

<FUNCTION>"Given and returned:" {
	  printf("*\n");
	  subsection = PARAM;
	  param = "in,out";
	  BEGIN(FLUSH);
	}

<FUNCTION>Returned: {
	  printf("*\n");
	  subsection = PARAM;
	  param = "out";
	  BEGIN(FLUSH);
	}

<FUNCTION>"Function return value:" {
	  printf("*\n");
	  subsection = RETURN;
	  BEGIN(FLUSH);
	}

<FUNCTION>"Notes:" {
	  printf("*\n* @b Notes: @n\n");
	  subsection = NOTES;
	  ilist = 0;
	  BEGIN(FLUSH);
	}

<FUNCTION>{I} {
	  if (!subsection || subsection == NOTES) {
	    // Lists in the function prologue or notes section.
	    lmore = yyleng;
	    yymore();
	  }
	
	  if (subsection) BEGIN(subsection);
	}

<FUNCTION>. {
	  yymore();
	  BEGIN(PRINTE);
	}

<PARAM>[a-zA-Z].{17}"  ".* |
<PARAM>"..."" "{7}.{8}"  ".* {
	  if (pcont) {
	    printf("%s\n%-*s", strtok(yytext, " "), id, "*");
	    pcont = 0;
	  } else {
	    snprintf(text, 128, "* @param[%s] %s ", param,
	      strtok(yytext, " "));
	    printf("%-24s", text);
	  }
	  printe(yytext+20, name);
	  plist = 0;
	  BEGIN(FLUSH);
	}

<PARAM>({NAME},)+{WS0} {
	  if (pcont) {
	    printf("%s", yytext);
	  } else {
	    printf("* @param[%s] %s", param, yytext);
	    pcont = 1;
	  }
	  plist = 0;
	  BEGIN(FLUSH);
	}

<PARAM>{NAME}(,{NAME})? {
	  if (pcont) {
	    pcont = 0;
	  } else {
	    printf("* @param[%s] ", param);
	  }
	  printf("%s\n", yytext);
	  plist = 0;
	  BEGIN(FLUSH);
	}

<PARAM>{IT}[a-z].* {
	  pcont = 0;
	  printe(yytext+20, name);
	  BEGIN(FLUSH);
	}

<RETURN>{IT}[a-z].{6}"  ".* {
	  // Function return type.
	  printf("* @return ");
	  printe(yytext+20, name);
	  plist = 0;
	  BEGIN(FLUSH);
	}

<RETURN>{IT}[a-z].* {
	  // Function return type.
	  printf("* @return\n");
	  plist = 0;
	  BEGIN(FLUSH);
	}

<RETURN>{ID}" "[-1].*:{WS1}.* {
	  // Status return value, less than 0 or greater than 9.
	  if (lmore > 2) printf("* @n\n");
	  printf("%-*s- ", id, "*");
	  printe(yytext+(id-3), name);
	  plist = 1;
	  BEGIN(FLUSH);
	}

<PARAM,RETURN>{ID}"  ".*:{WS1}.* {
	  // List of parameter or status return values.
	  if (lmore > 2) printf("* @n\n");
	  printf("%-*s- ", id, "*");
	  printe(yytext+(id-2), name);
	  plist = 1;
	  BEGIN(FLUSH);
	}

<PARAM,RETURN>{ID}"  ".* {
	  // List of parameter or status return values.
	  if (lmore > 2) printf("* @n\n");
	  printf("*   ");
	  printe(yytext, name);
	  BEGIN(FLUSH);
	}

<PARAM,RETURN>{ID}.* {
	  // List of parameter or status return values.
	  if (plist) {
	    printf("%-*s.\n", id, "*");
	    plist = 0;
	  } else if (lmore > 2) {
	    printf("* @n\n");
	  }
	  printf("*   ");
	  printe(yytext, name);
	  BEGIN(FLUSH);
	}

<NOTES>{WS0}-" " |
<NOTES>{WS0}[1-9a-z]:" " {
	  // List item.
	  lmore -= 4;
	  indent = yyleng - lmore;
	  if (yytext[yyleng-2] == '-') {
	    // The two-character pattern was matched.
	    indent -= 2;
	  } else {
	    // The three-character pattern was matched.
	    indent -= 3;
	  }
	  endlist(1, indent, listype, listndt, &ilist);
	
	  if (lmore) printf("*\n");
	
	  listitem(indent, listype, listndt, &ilist);
	
	  BEGIN(PRINTE);
	}

<NOTES>{WS1} {
	  lmore -= 4;
	  indent = yyleng - lmore;
	  endlist(0, indent, listype, listndt, &ilist);
	
	  yymore();
	  BEGIN(PRINTE);
	}

<NOTES>. {
	  endlist(0, 4, listype, listndt, &ilist);
	
	  yymore();
	  BEGIN(PRINTE);
	}

<STRUCTMARK>{NAME} {
	  strncpy(name, yytext, 31);
	  printf("\n/** @struct %s\n*\n", yytext);
	}

<STRUCTMARK>{WS1}struct{DASH} {
	  BEGIN(BRIEF);
	}

<UNIONMARK>{NAME} {
	  strncpy(name, yytext, 31);
	  printf("\n/** @union %s\n*\n", yytext);
	}

<UNIONMARK>{WS1}union{DASH} {
	  BEGIN(BRIEF);
	}

<STRUCTURE>{I}(char|int|long|double|struct{WS1}{NAME}|union|void) {
	  endlist(0, 0, listype, listndt, &ilist);
	  printf("*/\n");
	  printf("\n/** @var %s", yytext+lmore+2);
	  BEGIN(STRUCTVAR);
	}

<STRUCTURE>{I}{I}{WS0}-" " |
<STRUCTURE>{I}{I}{WS0}[0-9a-z]:" " {
	  // Start of list.
	  lmore -= 2;
	  indent = yyleng - lmore;
	  if (yytext[yyleng-2] == '-') {
	    // The two-character pattern was matched.
	    indent -= 2;
	  } else {
	    // The three-character pattern was matched.
	    indent -= 3;
	  }
	  endlist(1, indent, listype, listndt, &ilist);
	
	  if (lmore) printf("*\n");
	
	  listitem(indent, listype, listndt, &ilist);
	
	  BEGIN(PRINTE);
	}

<STRUCTURE>{WS1} {
	  lmore -= 2;
	  indent = yyleng - lmore;
	  endlist(0, indent, listype, listndt, &ilist);
	
	  yymore();
	  BEGIN(PRINTE);
	}

<STRUCTURE>. {
	  endlist(0, 0, listype, listndt, &ilist);
	
	  yymore();
	  BEGIN(PRINTE);
	}

<STRUCTVAR>\*{WS1}  |
<STRUCTVAR>{WS1}\*? |
<STRUCTVAR>"("\*+ {
	  printf("%s", yytext);
	}

<STRUCTVAR>{NAME}, {
	  printf("%s::%s\n*\n*   (See next ...)\n", name, yytext);
	  BEGIN(FLUSH);
	}

<STRUCTVAR>{NAME} |
<STRUCTVAR>{NAME}")(".*")" {
	  printf("%s::%s\n*\n", name, yytext);
	  BEGIN(FLUSH);
	}

<STRUCTVAR>"(*"{NAME}")" {
	  printf("(*%s::%s\n*\n", name, yytext+2);
	  BEGIN(FLUSH);
	}


<VARMARK>.*{DASH} {
	  printf("\n/** @var %.*s\n*\n", yyleng-3, yytext);
	  BEGIN(BRIEF);
	}

<VARIABLE>. {
	  yymore();
	  BEGIN(PRINTE);
	}


<DEFMARK>{NAME} {
	  strncpy(name, yytext, 31);
	  printf("\n/** @def %s\n*\n", yytext);
	}

<DEFMARK>("()")*{WS1}(define|macro){DASH} {
	  BEGIN(BRIEF);
	}

<DEFINE>. {
	  yymore();
	  BEGIN(PRINTE);
	}

<TABLEROW>. {
	  if (!td) {
	    printf("<TD>");
	    td = 1;
	  }
	  printf("%s", yytext);
	}

<TABLEROW>" "{2,} {
	  printf("</TD>%s", yytext);
	  td = 0;
	}

<TABLEROW>\n {
	  if (!td) printf("<TD>");
	  printf("</TD>\n* </TR>\n");
	  td = 0;
	  yyless(0);
	  BEGIN(FLUSH);
	}

<BODY>^(void|char|int|double){WS1}("*"*){NAME}{WS0}\([^;]* {
	  proto[nfunc] = malloc((yyleng+2)*sizeof(char));
	  sprintf(proto[nfunc], "%s", yytext);
	  func[nfunc] = malloc(32*sizeof(char));
	  func[nfunc][31] = '\0';
	  strtok(yytext, " ");
	  strncpy(func[nfunc], strtok(0x0, " *("), 31);
	  nfunc++;
	  BEGIN(FLUSH);
	}

<BODY>^. {
	  BEGIN(FLUSH);
	}

<BODY>\n {}


<BRIEF>.* {
	  printf("* @brief %s.\n*\n", yytext);
	  BEGIN(FLUSH);
	}

<PRINTE>.* {
	  printe(yytext, name);
	  BEGIN(FLUSH);
	}

<PRINTF>.* {
	  printf("%s\n", yytext);
	  BEGIN(FLUSH);
	}

<FLUSH>.*\n {
	  // Throw away the rest of the line and begin the next cycle.
	  lmore = 0;
	  BEGIN(section);
	}

<<EOF>> {
	  if (pass1) {
	    lmore = 0;
	    *name = '\0';
	    pass1 = 0;
	    section = PROLOG;
	    subsection = 0;
	
	    BEGIN(PROLOG);
	    rewind(yyin);
	    yyrestart(yyin);
	
	  } else {
	    printf("*/\n");
	
	    for (ifunc = 0; ifunc < nfunc; ifunc++) {
	      free(proto[ifunc]);
	      free(func[ifunc]);
	    }
	
	    return 0;
	  }
	}

%%

/*----------------------------------------------------------------------------
* Output a list item, starting a new list if necessary.
*---------------------------------------------------------------------------*/

void listitem(
  int indent,
  char listype[8],
  int listndt[8],
  int *ilist)

{
  if (indent > listndt[*ilist]) {
    (*ilist)++;
    listndt[*ilist] = indent;

    if (yytext[yyleng-2] == '-') {
      listype[*ilist] = 'U';
    } else {
      listype[*ilist] = 'O';
    }

    if (yytext[yyleng-3] == 'a') {
      printf("%-*s<OLa>\n", indent, "*");
    } else {
      printf("%-*s<%cL>\n", indent, "*", listype[*ilist]);
    }
  }

  printf("%-*s<LI> ", indent, "*");
}

/*----------------------------------------------------------------------------
* Finish any lists.
*---------------------------------------------------------------------------*/

void endlist(
  int isItem,
  int indent,
  char listype[8],
  int listndt[8],
  int *ilist)

{
  // Plain text at the same level of indentation as an item tag signals
  // end-of-list.
  while (*ilist && (indent <  listndt[*ilist] ||
                   (indent == listndt[*ilist] && !isItem))) {
    printf("%-*s</%cL>\n", listndt[*ilist], "*", listype[*ilist]);
    (*ilist)--;
  }
}

/*----------------------------------------------------------------------------
* Finish tables or code sections.
*---------------------------------------------------------------------------*/

void endspecial(
  int *special)

{
  if (*special) {
    if (*special == TABLE) {
      printf("* </TABLE><HR>\n");
    } else if (*special == VERBATIM) {
      printf("* @endcode\n");
    }

    *special = 0;
  }
}

/*----------------------------------------------------------------------------
* Print text with name escaped by '%' to prevent a document reference.
*---------------------------------------------------------------------------*/

void printe(const char *text, const char *name)

{
  char *cp;
  int  i, len;

  if ((len = strlen(name))) {
    while ((cp = strstr(text, name))) {
      if (cp > text && (*(cp-1) == '_' ||
          ('a' <= *(cp-1) && *(cp-1) <= 'z') ||
          ('A' <= *(cp-1) && *(cp-1) <= 'Z'))) {
        // Not a match.
        i = cp - text + len;
        printf("%.*s", i, text);

      } else {
        if (*(cp+len) == ':' && *(cp+len+1) == ':') {
          // Allow references to struct members.
          i = cp - text + len;
          printf("%.*s", i, text);
        } else {
          // Disallow a reference and use bold font.
          i = cp - text;
          printf("%.*s@b %%%s", i, text, name);
        }
      }
      text = cp + len;
    }
  }

  printf("%s\n", text);
}


//----------------------------------------------------------------------------

int main(int argc, char *argv[])

{
  // Check inputs.
  if (argc != 2) {
    fprintf(stderr, "Usage: doxextr <header file>\n");
    return 1;
  }

  // Check accessibility of the input file.
  if (access(argv[1], R_OK) == -1) {
    perror(argv[1]);
    return 1;
  }

  if ((yyin = fopen(argv[1], "r")) == NULL) {
    perror(argv[1]);
    return 1;
  }

  // Set line buffering in case stdout is redirected to a file, otherwise
  // stdout and stderr messages will be jumbled (stderr is unbuffered).
  setvbuf(stdout, NULL, _IOLBF, 0);

  return yylex();
}
