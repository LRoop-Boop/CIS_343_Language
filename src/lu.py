import sys

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
            print(input("> "))
            print("Scanner Not Implemented")
        #When the user presses ctrl C, break/leave repl mode.
        except KeyboardInterrupt:
            print()
            break

#Echo the contents of the file followed by the error message.
def execute(filename):
    with open(filename, "r") as file:
        source = file.read()
    print(source)
    print("Scanner Not Implemented")

if __name__ == "__main__":
    main()