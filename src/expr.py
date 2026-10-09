class Expr:
    pass

class Binary(Expr):
    '''Create a class for the binary expression type with two expressions and an operator.'''
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Grouping(Expr):
    '''Create a class for a grouping with an expression.'''
    def __init__(self, expression):
        self.expression = expression

class Literal(Expr):
    '''Create a class for the literal type with a value.'''
    def __init__(self, value):
        self.value = value

class Unary(Expr):
    '''Create a class for the unary expression type with an operator and an expression.'''
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right