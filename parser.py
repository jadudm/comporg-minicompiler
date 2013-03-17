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
    
def compile (expr, offset):
    if checkType(expr, 'Integer'):
        result = "@%s" % expr.value
        result += "\n"
        result += "D=A"
        result += "\n"
        return result
        
    if checkType(expr, 'Binop'):
        # Pre-compile the LHS and RHS
        # Increment our offset as we go.
        lhs_result = compile(expr.lhs, offset + 1)
        rhs_result = compile(expr.rhs, offset + 1)
        result = ""
        
        # Collect up the LHS compilation
        result += lhs_result
        # The LHS result will be left in
        # the D register.

        # Store D in RAM[0 + offset]
        result += "@%s" % (0 + offset)
        result += "\n"
        result += "M=D"
        result += "\n"

        # Collect up the RHS
        result += rhs_result
        # The RHS result will be left in
        # the D register.

        # Store D in RAM[1 + offset]
        result += "@%s" % (1 + offset)
        result += "\n"
        result += "M=D"
        result += "\n"
        
        # Now, load things back, and add them.
        
        # Load RAM[0 + offset] into D
        result += "@%s" % (0 + offset)
        result += "\n"
        result += "M=D"
        result += "\n"
        
        # Add D and RAM[1] ; store back into D
        result += "@%s" % (1 + offset)
        result += "\n"
        result += "D=D+M"
        result += "\n"
                
        # We have now (recursively) computed 
        # the addition of two numbers. The result
        # is left in the D register. 
        
        # Return the resulting assembly
        return result

print compile(lexer.parse('(8 + 9) + (10 + 11)'), 0)