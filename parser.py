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
        result = "@%s" % expr.value
        result += "\n"
        result += "D=A"
        return result
        
    if checkType(expr, 'Binop'):
        # Compile the LHS
        result = "%s" % compile(expr.lhs)
        result += "\n"
        # Store that in RAM[0]
        result += "@0"
        result += "\n"
        result += "M=D"
        result += "\n"
        # Compile the RHS
        result += "%s" % compile(expr.rhs)
        result += "\n"
        # Store that in RAM1
        result += "@1"
        result += "\n"
        result += "D=M"
        result += "\n"
        # Load RAM[0] into D
        result += "@0"
        result += "\n"
        result += "D=M"
        result += "\n"
        # Add D and RAM[1] ; store back into D
        result += "@1"
        result += "\n"
        result += "D=D+M"
        
        # Return the resulting assembly
        return result

print compile(lexer.parse('3 + (1 + 4)'))