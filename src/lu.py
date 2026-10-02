import sys
from scanner import Scanner

#Controls how scanner interprets different number of arguments.
def main():
    num_args = len(sys.argv) - 1

    if num_args == 0:
        repl()
    
    elif num_args == 1:
        execute(sys.argv[1])

    elif num_args > 1: 
        print(f"Error: Expected 0 or 1 argument, received {num_args}. Please try again using the format 'python src/lu.py or python src/lu.py your_file.lu'.")

#Echo the command followed by the error message.
def repl():
    while True:
        try:
            source = (input("> "))
            scanner = Scanner(source)
            tokens = scanner.scan_tokens()

            for token in tokens:
                print(token.type, token.lexeme, token.literal, token.line)
        
        #When the user presses ctrl C, break/leave repl mode.
        except KeyboardInterrupt:
            print()
            break

#Echo the contents of the file followed by the error message.
def execute(filename):
    with open(filename, "r") as file:
        source = file.read()
    
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    for token in tokens:
        print(token.type, token.lexeme, token.literal, token.line)

if __name__ == "__main__":
    main()