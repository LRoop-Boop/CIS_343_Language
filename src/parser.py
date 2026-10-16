from token import TokenType
from expr import Binary, Grouping, Literal, Unary

class ParseError(Exception):
    '''Represent a syntax error during parsing.'''
    pass

class Parser:
    '''Parse tokens into an abstract syntax tree (AST).'''
    def __init__(self, tokens):
        '''Initialize the parser with a list of tokens.'''
        self.tokens = tokens
        self.current = 0

    def parse(self):
        '''Parse an expression and check for unexpected trailing tokens.'''
        expr = self.expression()

        #--- Start AI code ---
        # Ignore trailing newline tokens before checking for extra input.
        while self.match(TokenType.NEWLINE):
            pass
        #--- End AI code ---

        if not self.is_at_end():
            raise self.error(self.peek(), "Unexpected token after expression.")
        return expr

    def expression(self):
        '''Parse an expression.'''
        return self.equality()

    def equality(self):
        '''Parse equality operators.'''
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        '''Parse comparison operators.'''
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self):
        '''Parse addition and subtraction.'''
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)

        return expr


    def factor(self):
        '''Parse multiplication and division.'''
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr


    def unary(self):
        '''Parse unary operators.'''
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)

        return self.primary()

    def primary(self):
        '''Parse literals and grouped expressions.'''
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(
                TokenType.RIGHT_PAREN,
                "Expect ')' after expression."
            )
            return Grouping(expr)

        # Detect a binary operator that appears without a left operand.
        if self.match(
            TokenType.PLUS, TokenType.STAR, TokenType.SLASH, TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL, 
            TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL
        ):
            operator = self.previous()
            raise self.error(
                operator,
                f"Missing left operand for '{operator.lexeme}'."
            )

        raise self.error(self.peek(), "Expect expression.")

    #--- Start AI code ---
    def match(self, *types):
        '''Check whether the current token matches any given types.'''
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    #--- End AI code ---

    def check(self, token_type):
        '''Check the type of the current token.'''
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self):
        '''Consume and return the current token.'''
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def peek(self):
        '''Return the current token without consuming it.'''
        return self.tokens[self.current]

    def previous(self):
        '''Return the previously consumed token.'''
        return self.tokens[self.current - 1]

    def is_at_end(self):
        '''Check whether the parser has reached the end of the input.'''
        return self.peek().type == TokenType.EOF

    def consume(self, token_type, message):
        '''Consume a token of the expected type or raise a parse error.'''
        if self.check(token_type):
            return self.advance()

        raise self.error(self.peek(), message)

    def error(self, token, message):
        '''Error method to handle parse errors with specific conditional messages'''
        if token.type == TokenType.EOF:
            print(
                f"[line {token.line}, column {token.column}] "
                f"Error at end: {message}"
            )
        else:
            print(
                f"[line {token.line}, column {token.column}] "
                f"Error at '{token.lexeme}': {message}"
            )

        return ParseError(message)