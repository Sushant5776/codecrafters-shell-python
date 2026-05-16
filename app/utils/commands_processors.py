import os
from ..utils.helpers import builtins, is_executable_command_in_path

def process_type(user_input: str):
    command_name = user_input.split()[1]  # command name to check for existing 0 is the type command itself
    if command_name in builtins:
        print(f"{command_name} is a shell builtin")
    elif full_path := is_executable_command_in_path(command_name):
        print(f"{command_name} is {full_path}")
    else:
        print(f"{command_name}: not found")

def process_cd(user_input: str):
    directory = user_input.split()[1]

    if os.path.exists(directory):
        os.chdir(directory)
    else:
        print(f"cd: {directory}: No such file or directory")