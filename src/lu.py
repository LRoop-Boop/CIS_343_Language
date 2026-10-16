import sys
from scanner import Scanner
from parser import Parser, ParseError
from ast_printer import AstPrinter

#Controls how scanner interprets different number of arguments.
def main():
    num_args = len(sys.argv) - 1

    if num_args == 0:
        repl()
    
    elif num_args == 1:
        execute(sys.argv[1])

    elif num_args > 1: 
        print(f"Error: Expected 0 or 1 argument, received {num_args}. Please try again using the format 'python src/lu.py or python src/lu.py your_file.lu'.")

def run_expression(source):
    '''Scan, parse, and print one expression.'''
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    # --- Start AI code ---
    #Include an error handler for the scanner and the parser before it reaches the printer.
    if scanner.had_error:
        return

    parser = Parser(tokens)

    try:
        expression = parser.parse()
    except ParseError:
        return
    # --- End AI code ---

    printer = AstPrinter()
    print(printer.print(expression))

#Echo the command followed by the error message.
def repl():
    while True:
        try:
            source = (input("> "))
            run_expression(source)

        #When the user presses ctrl C, break/leave repl mode.
        except KeyboardInterrupt:
            print()
            break

        except EOFError:
            print()
            break

#Echo the contents of the file followed by the error message.
def execute(filename):
    try:
        with open(filename, "r") as file:
            source = file.read()

        #--- Start AI code ---
        #Parse each line so that files can parse through multiple lines at once.
        for line_number, line in enumerate(source.splitlines(), start=1):
            if not line.strip():
                continue
        #--- End AI code ---

            print(f"\n[line {line_number}] {line.strip()}")
            run_expression(line)

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except OSError as error:
        print(f"Error reading file '{filename}': {error}")

if __name__ == "__main__":
    main()