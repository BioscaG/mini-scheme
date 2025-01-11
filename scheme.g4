grammar scheme;
root : expr* EOF           // l'etiqueta ja és root
     ;

expr
    : ( '\'(' | '(' ) expr* ')' #expression
    | BOOLEAN #bool
    | NUMBER #num
    | IDENTIFIER #id
    | OPERATOR #op
    | STRING #str
    ;



OPERATOR: '+'|'-'|'*'|'/'|'<'|'>'|'='|'<='|'>='|'and'|'or'|'not'|'mod';
IDENTIFIER: [a-zA-Z][a-zA-Z0-9\-]* '?'?;
NUMBER : '-'? [0-9]+ ;
BOOLEAN : '#t' | '#f';
STRING : '"' .*? '"';
WS  : [ \t\n\r]+ -> skip ;
COMMENT: ';' .*? '\n' -> skip ;
