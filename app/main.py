import os
import sys
import subprocess
from .utils.commands_processors import process_type
from .utils.helpers import is_executable_command_in_path


def main():
    # REPL loop
    while True:
        sys.stdout.write("$ ")

        user_input = input()
        
        if user_input == "exit":
            break
        elif user_input.startswith("echo "):
            print(user_input[5:])
        elif user_input.startswith("type "):
            process_type(user_input=user_input)
        elif user_input == "pwd":
            print(os.getcwd())
        elif is_executable_command_in_path(user_input=user_input):
            exec_result = subprocess.run(args=user_input.split(), capture_output=True, text=True)
            sys.stdout.write(exec_result.stdout)
            sys.stdout.flush()
        else:
            print(f"{user_input}: command not found")


if __name__ == "__main__":
    main()