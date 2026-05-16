import os
import sys
import shlex
from .utils.commands_processors import process_echo, process_type, process_cd, process_external_commands
from .utils.helpers import is_executable_command_in_path


def main():
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        user_input = input()

        if not user_input:
            continue

        args = shlex.split(user_input)
        command = args[0]

        if user_input == "exit":
            break
        elif command == "echo":
            process_echo(args)
        elif command == "type":
            process_type(args)
        elif command == "pwd":
            print(os.getcwd())
        elif command == "cd":
            process_cd(args)
        elif is_executable_command_in_path(command):
            process_external_commands(args)
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()