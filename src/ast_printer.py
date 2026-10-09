from expr import Binary, Expr, Grouping, Literal, Unary

class AstPrinter:
    def __init__(self, output_type="ast"):
        '''Create an attribute so that printing format can differ for Reverse Polish Notation if needed.'''
        self.output_type = output_type

    def print(self, expression):
        '''Create a print method which returns the formatting specified in the visiting methods.'''
        # --- start AI code ---
        #This call switches to my ASCII printer helper method, and therefore utilizes a different structure than calling the visitor helpers.
        if self.output_type == "tree":
            return "\n".join(self.tree_lines(expression))
        # --- end AI code ---
        
        if isinstance(expression, Literal):
            return self.visit_literal(expression)
        elif isinstance(expression, Unary):
            return self.visit_unary(expression)
        elif isinstance(expression, Binary):
            return self.visit_binary(expression)
        elif isinstance(expression, Grouping):
            return self.visit_grouping(expression)

    def visit_literal(self, expression):
        '''Return a literal expression's value, handling lox-style edge-cases.'''
        if expression.value is True:
            return "true"
        elif expression.value is False:
            return "false"
        elif expression.value is None:
            return "nil"
        else:
            return str(expression.value)

    def visit_unary(self, expression):
        '''Return the unary expression with a nested expression and operator.'''
        operator = expression.operator.lexeme
        printed_right = self.print(expression.right)
        if self.output_type == "rpn":
            return f"{printed_right} {operator}"
        return f"({operator} {printed_right})"

    def visit_binary(self, expression):
        '''Return a binary expression with the nested expressions and operator.'''
        printed_left = self.print(expression.left)
        operator = expression.operator.lexeme
        printed_right = self.print(expression.right)
        if self.output_type == "rpn":
            return f"{printed_left} {printed_right} {operator}"
        return f"({operator} {printed_left} {printed_right})"

    def visit_grouping(self, expression):
        '''Return the printed expression in parantheses for a grouping.'''
        printed_expression = self.print(expression.expression)
        if self.output_type == "rpn":
            return printed_expression
        return f"(group {printed_expression})"

    def tree_lines(self, expression, prefix="", field="", connector=""):
        '''The following code is adapted from the in-class example breakfast_parser to visualize an ASCII tree structure.
        The most fundamental change is that this method belongs to the printer rather than the node class.'''
        label = expression.__class__.__name__
        children = []
        for name, value in vars(expression).items():
            if isinstance(value, Expr):
                children.append((name, value))
            # --- start AI code ---
            #Handle edge cases for naming convention rather than python typing.
            elif value is not None or name == "value":
                if name == "operator":
                    value = value.lexeme
                elif value is True:
                    value = "true"
                elif value is False:
                    value = "false"
                elif value is None:
                    value = "nil"

                label += f" ({name}={value!r})"
            # --- end AI code ---

        lines = [f"{prefix}{connector}{field}{label}"]
        if connector:
            prefix += "    " if connector == "└── " else "│   "
        for index, (name, child) in enumerate(children):
            branch = "└── " if index == len(children) - 1 else "├── "
            lines.extend(self.tree_lines(child, prefix, f"{name}: ", branch))
        return lines
