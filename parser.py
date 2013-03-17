# https://tdparser.readthedocs.org/en/latest/
import tdparser

class Integer(tdparser.Token):
    regexp = r'\d+'
    def nud(self, context):
        return int(self.text)
        
class Addition(tdparser.Token):
    regexp = r'\+'
    lbp = 10

    def led(self, left, context):
        return left + context.expression(self.lbp)

class Multiplication(tdparser.Token):
    regexp = r'\*'
    lbp = 20

    def led(self, left, context):
        return left * context.expression(self.lbp)
        
lexer = tdparser.Lexer(with_parens=True)
lexer.register_tokens(Integer, Addition, Multiplication)

print lexer.parse ('3 + (1 + 4)')