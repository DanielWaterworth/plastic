import ply.lex as lex

tokens = [
    "NUMBER",
    "COLON",
    "SEMICOLON",
    "COMMA",
    "ASSIGNMENT",
    "ARROW",
    "OPEN_PARENS",
    "CLOSE_PARENS",
    "UPPER_NAME",
    "LOWER_NAME",
    "STRING",
    "PLUS",
    "MINUS",
    "MUL",
    "DIV",
    "EQ",
    "NE",
    "LT",
    "GT",
    "LE",
    "GE",
    "COMMENT",
    "WHITESPACE",
]
keywords = {
    'define' : 'DEFINE',
    'end' : 'END',
    'sys' : 'SYS',
    'store' : 'STORE',
    'load' : 'LOAD',
    'return' : 'RETURN',
    'do': 'DO',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'true': 'TRUE',
    'false': 'FALSE',
    'bool': 'BOOL',
    'uint': 'UINT',
    'void': 'VOID',
}
tokens += keywords.values()

t_NUMBER = r'\d+'
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_ASSIGNMENT = r':='
t_ARROW = r'->'
t_OPEN_PARENS = r'\('
t_CLOSE_PARENS = r'\)'
t_UPPER_NAME = r'[A-Z][a-zA-Z]*'

def t_LOWER_NAME(t):
    r'[a-z][a-z0-9_]*'
    if t.value in keywords:
        t.type = keywords[t.value]
    return t

t_STRING = r'"(\\.|[^"])*"'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_MUL = r'\*'
t_DIV = r'\\'
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='

def t_COMMENT(t):
    r'\#[^\n]*\n'
    pass

def t_WHITESPACE(t):
    r'\s'
    pass

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lexer = lex.lex()