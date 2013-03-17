# https://tdparser.readthedocs.org/en/latest/
import tdparser

# http://pysnippet.blogspot.com/2010/01/named-tuple.html
from collections import namedtuple as NT

Integer = NT('Integer', 'value')
Binop   = NT('Binop', 'kind, lhs, rhs')

class ParseInteger(tdparser.Token):
    regexp = r'\d+'
    def nud(self, context):
        return Integer(int(self.text))
        
class ParseAddition(tdparser.Token):
    regexp = r'\+'
    lbp = 10

    def led(self, left, context):
        return Binop('+', left, context.expression(self.lbp))

class ParseMultiplication(tdparser.Token):
    regexp = r'\*'
    lbp = 20

    def led(self, left, context):
        return Binop('*', left, context.expression(self.lbp))
        
lexer = tdparser.Lexer(with_parens=True)
lexer.register_tokens(ParseInteger, ParseAddition, ParseMultiplication)

# print lexer.parse ('3 + (1 + 4)')

def checkType (struct, name):
    return type(struct).__name__ == name
    
def compile (expr):
    if checkType(expr, 'Integer'):
        print "Found an Integer: %s" % expr.value
        
    if checkType(expr, 'Binop'):
        print "Found a Binop: %s" % expr.kind
        compile(expr.lhs)
        compile(expr.rhs)

compile(lexer.parse('3 + (1 + 4)'))