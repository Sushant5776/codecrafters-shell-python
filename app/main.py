import sys
from .utils.helpers import builtins
from .utils.commands_processors import process_type


def main():
    # REPL loop
    while True:
        # Print prompt
        sys.stdout.write("$ ")

        # wait for user input
        user_input = input()
        
        if user_input == "exit":
            break
        elif user_input.startswith("echo "):
            print(user_input[5:])
        elif user_input.startswith("type "):
            process_type(user_input=user_input)            
        else:
            print(f"{user_input}: command not found")


if __name__ == "__main__":
    main()