#Rather than call the test files with the main lu.py file, I opted to use this workaround to test the ast printer directly.
import sys
sys.path.insert(0, "src")

from token import Token, TokenType
from expr import Binary, Grouping, Literal, Unary
from ast_printer import AstPrinter

#Swap out this line in testing to determine which printer format to use for the AST
printer = AstPrinter()
#printer = AstPrinter("rpn")
#printer = AstPrinter("tree")

def make_token(token_type, lexeme):
    return Token(token_type, lexeme, None, 1)


print("TEST 1: Literals")

print(printer.print(Literal(123)))
print(printer.print(Literal(45.67)))
print(printer.print(Literal("hello")))
print(printer.print(Literal(True)))
print(printer.print(Literal(False)))
print(printer.print(Literal(None)))
print()


print("TEST 2: Unary")

minus = make_token(TokenType.MINUS, "-")
bang = make_token(TokenType.BANG, "!")

print(printer.print(Unary(minus, Literal(123))))
print(printer.print(Unary(bang, Literal(True))))
print()


print("TEST 3: Binary")

plus = make_token(TokenType.PLUS, "+")
minus = make_token(TokenType.MINUS, "-")
star = make_token(TokenType.STAR, "*")
slash = make_token(TokenType.SLASH, "/")

print(printer.print(Binary(Literal(1), plus, Literal(2))))
print(printer.print(Binary(Literal(5), minus, Literal(3))))
print(printer.print(Binary(Literal(4), star, Literal(6))))
print(printer.print(Binary(Literal(8), slash, Literal(2))))
print()


print("TEST 4: Comparison and Equality")

equal_equal = make_token(TokenType.EQUAL_EQUAL, "==")
bang_equal = make_token(TokenType.BANG_EQUAL, "!=")
greater = make_token(TokenType.GREATER, ">")
greater_equal = make_token(TokenType.GREATER_EQUAL, ">=")
less = make_token(TokenType.LESS, "<")
less_equal = make_token(TokenType.LESS_EQUAL, "<=")

print(printer.print(Binary(Literal(1), equal_equal, Literal(1))))
print(printer.print(Binary(Literal(1), bang_equal, Literal(2))))
print(printer.print(Binary(Literal(5), greater, Literal(3))))
print(printer.print(Binary(Literal(5), greater_equal, Literal(5))))
print(printer.print(Binary(Literal(2), less, Literal(4))))
print(printer.print(Binary(Literal(2), less_equal, Literal(2))))
print()


print("TEST 5: Grouping")

print(printer.print(Grouping(Literal(123))))
print(printer.print(Grouping(Binary(Literal(1), plus, Literal(2)))))
print()


print("TEST 6: Nested Expression")

expression = Binary(
    Unary(
        minus,
        Literal(123)
    ),
    star,
    Grouping(
        Literal(45.67)
    )
)

print(printer.print(expression))
print()


print("TEST 7: Complicated Nesting")

expression = Unary(
    bang,
    Binary(
        Literal(True),
        equal_equal,
        Grouping(
            Binary(
                Literal(3),
                plus,
                Literal(4)
            )
        )
    )
)

print(printer.print(expression))
print()