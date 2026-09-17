import sys

#Controls how scanner interprets different number of arguments.
def main():
    num_args = len(sys.argv) - 1

    if num_args == 0:
        repl()
    
    elif num_args == 1:
        execute(sys.argv[1])

    elif num_args > 1: 
        print("Usage: lox.py [script]")

#
def repl():
    print("Scanner Not Implemented")

#
def execute(filename):
    print("Scanner Not Implemented")

if __name__ == "__main__":
    main()