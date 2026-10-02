from token import Token, TokenType

class Scanner:
    def __init__(self, source):
        '''Initialize source file, tokens list, location information, and keyword types.'''
        self.source = source
        self.tokens = []

        self.start = 0
        self.curr = 0
        self.line = 1
        self.column = 1

        self.had_error = False

        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

    def scan_tokens(self):
        '''Call the scan token function and append EOF token to token list for return'''
        while not self.is_at_end():
            self.start = self.curr
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        '''Determine character type and call helper functions to scan the token.'''
        char = self.advance()

        if char == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif char == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif char == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif char == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        
        elif char == ',':
            self.add_token(TokenType.COMMA)
        elif char == '.':
            if self.is_digit(self.peek()):
                self.number(leading_dot=True)
            else:
                self.add_token(TokenType.DOT)
        elif char == '+':
            self.add_token(TokenType.PLUS)
        elif char == '-':
            self.add_token(TokenType.MINUS)
        elif char == ';':
            self.add_token(TokenType.SEMICOLON)
        elif char == '*':
            self.add_token(TokenType.STAR)
        
        #Use digits to determine numbers, quotes for strings, and alpha characters for identifiers
        elif char == '"':
            self.string()
        elif self.is_digit(char):
            self.number()
        elif self.is_alpha(char):
            self.identifier()
        
        #Check maximal munch rules for multi-character tokens
        elif char == '!':
            if self.match('='):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)

        elif char == '=':
            if self.match('='):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)

        elif char == '<':
            if self.match('='):
                self.add_token(TokenType.LESS_EQUAL)
            else:
                self.add_token(TokenType.LESS)

        elif char == '>':
            if self.match('='):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)

        elif char == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            elif self.match('*'):
                self.block_comment()
            else:
                self.add_token(TokenType.SLASH)

        elif char == ' ' or char == '\r' or char == '\t':
            # ignore whitespace
            pass

        #---- start AI code ----
        #Add the newline character token for statement ending with line - 1, so that we count where the newline started and not where it ends.
        elif char == '\n':
            self.add_token(TokenType.NEWLINE, line = self.line - 1)
        #---- end AI code ----

        else:
            self.error("Unexpected character.", char)
    
    def is_at_end(self):
        return self.curr >= len(self.source)

    def advance(self):
        '''Return/consume the character, updating location information.'''
        curr_char = self.source[self.curr]
        self.curr += 1

        if curr_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        return curr_char

    def add_token(self, token_type, literal=None, line=None):
        '''Create a token for the lexeme and append it to the tokens list.'''
        lexeme = self.source[self.start:self.curr]

        #---- start AI code ----
        if line is None:
            line = self.line
        #---- end AI code ----

        token = Token(token_type, lexeme, literal, line)
        self.tokens.append(token)

    #Use helper functions to look ahead without consuming characters, or check for a match.
    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.curr]

    def peek_next(self):
        if self.curr + 1 >= len(self.source):
            return '\0'
        return self.source[self.curr + 1]

    def peek_next_next(self):
        if self.curr + 2 >= len(self.source):
            return '\0'
        return self.source[self.curr + 2]

    def match(self, expected):
        if self.is_at_end() or self.peek() != expected:
            return False
        self.advance()
        return True


    #Manually check regex rules for digit, alpha, and alphanumeric characters.
    def is_digit(self, char):
        return char in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    def is_alpha(self, char):
        return ('a' <= char <= 'z') or ('A' <= char <= 'Z') or char == '_'

    def is_alpha_numeric(self, char):
        return self.is_alpha(char) or self.is_digit(char)


    def string(self):
        '''Record the line in which the string started in case of error, consume everything within quotes except for excape sequences.
        Report an error if the escape sequence is not valid or the string does not terminate. Add the string to the token list.'''
        start_line = self.line
        value = ''
        escape_sequences = {'\\': '\\', '"': '"', 'n': '\n', 't': '\t'}

        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\\':
                if self.peek_next() in escape_sequences:
                    value += escape_sequences[self.peek_next()]
                    self.advance()
                    self.advance()
                else:
                    self.error("Invalid escape sequence.")
                    self.advance()
                    if not self.is_at_end():
                        self.advance()
            else:
                value += self.advance()

        if self.is_at_end():
            self.error("Unterminated string.")
            return

        self.advance()
        self.add_token(TokenType.STRING, value, line=start_line)

    def number(self, leading_dot = False):
        '''Continue to advance if the character is a digit. If you encounter a decimal, ensure the next character is a digit before continuing, otherwise
        the number token is complete. Call the exponent helper to check and consume exponents, and add the numerical value as a float to the token list.'''
        #----start of AI code----
        #Determine if there is a leading dot and advance through digits.
        if leading_dot:
            while self.is_digit(self.peek()):
                self.advance()
        #----end of AI code----
        else:
            while self.is_digit(self.peek()):
                self.advance()

            if self.peek() == '.' and self.is_digit(self.peek_next()):
                self.advance()

                while self.is_digit(self.peek()):
                    self.advance()

        #----start of AI code----
        #Call the exponent helper regardless of the number, control flow filters out scientific notation and advances when necessary.
        self.exponent()
        #----end of AI code----
        
        value = float(self.source[self.start:self.curr])
        self.add_token(TokenType.NUMBER, value)

    def identifier(self):
        '''Continue if the digits are alpha numeric. Check if the identifier is a reserved word and assign tokens accordingly.'''
        while self.is_alpha_numeric(self.peek()):
            self.advance()
        value = self.source[self.start:self.curr]
        token_type = self.keywords.get(value, TokenType.IDENTIFIER)
        self.add_token(token_type)

    def error(self, message, char=None):
        '''Return location information and error message. If the error involves a specific character, return the character.'''
        if char is not None:
            print(f"[line {self.line}, column {self.column - 1}] Error: {message} '{char}'")
        else:
            print(f"[line {self.line}, column {self.column}] Error: {message}")
        self.had_error = True

    def block_comment(self):
        '''Utilize a C-style block comment with maximal munch principle for the slash. Use a depth counter to include nested block comments
        and return an error if a block comment is unterminated. Ignore all commented text and do not store it as a token.'''
        depth = 1
        while not self.is_at_end():
            if self.peek() == '/' and self.peek_next() == '*':
                depth += 1
                self.advance()
                self.advance()
                continue
            elif self.peek() == '*' and self.peek_next() == '/':
                depth -= 1
                self.advance()
                self.advance()
                if depth == 0: 
                    return
                continue
            self.advance()
        self.error("Unterminated block comment.")

    def exponent(self):
        '''Check to see if the next character is either e followed by a digit or e followed by a +/- followed by a digit. 
        If so, consume all of the following digits. Return if the number is not in scientific notation.'''
        if self.peek() not in ['e', 'E']:
            return

        if self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()
            return

        #----start AI code----
        #Check for the +/- char followed by digits and then consume all following digits. 
        if self.peek_next() in ['+', '-'] and self.is_digit(self.peek_next_next()):
            self.advance()
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()
        #----end AI code----