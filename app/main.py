import os
import sys
import shlex
import readline
from .utils.commands_processors import process_echo, process_type, process_cd, process_external_commands
from .utils.helpers import is_executable_command_in_path, parse_redirects, redirect_stdout, command_completer


def main():
    readline.set_completer(command_completer)
    readline.parse_and_bind("tab: complete")
    
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        user_input = input()

        if not user_input:
            continue

        if user_input == "exit":
            break

        args = shlex.split(user_input)
        command = args[0]

        clean_args, output_file, is_append, is_stdout = parse_redirects(args=args)

        with redirect_stdout(output_file, is_append, is_stdout):
            if command == "echo":
                process_echo(clean_args)
            elif command == "type":
                process_type(clean_args)
            elif command == "pwd":
                print(os.getcwd())
            elif command == "cd":
                process_cd(clean_args)
            elif is_executable_command_in_path(command):
                process_external_commands(clean_args)
            else:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()