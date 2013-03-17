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

print lexer.parse ('3 + (1 + 4)')