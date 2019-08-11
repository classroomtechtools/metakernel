from pygments.lexer import RegexLexer
from pygments.token import *
from pygments import highlight
from pygments.formatters import TerminalFormatter



code = """
STOCK = Stack.from_x_integers(1000)  # make 1000 random ints

COUNT = 0
TOTAL = 0
RANDOM = 3343.5
SOMETHING = true
loop N from 0 to 999
    if STOCK[N] > 0 then
        COUNT = COUNT + 1
        TOTAL = TOTAL + STOCK[N]
    end if
end loop

if NOT COUNT = 0 then
    AVERAGE = TOTAL / COUNT
    output "Count is " , COUNT
    output "Average = " , AVERAGE
else
    output "There are no non-zero values"
end if
"""

class PassThrough:
    pass

class ConvertString:
    pass

class VanillaPythonLexer(RegexLexer):
    name = "Vanilla Python"
    filesnames = ['.vanilla']
    minetypes = ['text/x-python']
    tokens = {
        'root': [
            (r"'(.*)'", Keyword.Builtin),
            # (r'\bCollection\b', Keyword.Declaration),
            # (r'\bStack\b', Keyword.Declaration),
            # (r'\bloop\b', Name.Builtin),
            # (r'\bif\b', Name.Builtin),
            # (r'\belse\b', Name.Builtin),
            # (r'\bthen\b', Name.Builtin),
            # (r'\bwhile\b', Name.Builtin),
            # (r'\bend\b', Name.Builtin),
            # (r'\bfrom\b', Keyword),
            # (r'\buntil\b', Keyword),
            # (r'\bto\b', Keyword),
            # (r'\boutput\b', Keyword),
            # (r'\bNOT\b', Operator),
            # (r'\b[A-Z_]+\b', Name.Variable),
            # (r'".*?"', Literal.String),
            # (r'//.*', Comment),
            # (r'#.*', Comment),
            # (r'\b[0-9]+\.[0-9]+\b', Literal.Number.Float),
            # (r'\b[0-9]+\b', Literal.Number.Integer),
            # (r'[.,=≠<>+-\\*]', Operator),
            # (r'\bmod\b', Operator),
            # (r'\bdiv\b', Operator),
            # (r'[()\[\]]', Name.Entity),
            # (r'\btrue\b', Generic.Emph),
            # (r'\bfalse\b', Generic.Emph),
            # (r'\bfrom_.*?\b', Name.Function),
            # (r'\bhasNext\b', Name.Function),
            # (r'\baddItem\b', Name.Function),
            # (r'\bgetNext\b', Name.Function),
            # (r'\bpush\b', Name.Function),
            # (r'\bpop\b', Name.Function)
        ]
    }

pl = VanillaPythonLexer()
for lex in pl.get_tokens(code):
    print(lex)

#result = highlight(code, pl, TerminalFormatter())
#print(result)
