import os
import sys
import subprocess
from ..utils.helpers import builtins, is_executable_command_in_path

def process_type(args):
    command_name = args[1]
    if command_name in builtins:
        print(f"{command_name} is a shell builtin")
    elif full_path := is_executable_command_in_path(command_name):
        print(f"{command_name} is {full_path}")
    else:
        print(f"{command_name}: not found")

def process_cd(args):
    directory = args[1]

    if directory == "~":
        os.chdir(os.environ["HOME"])
    elif os.path.exists(directory):
        os.chdir(directory)
    else:
        print(f"cd: {directory}: No such file or directory")


def process_echo(args):
    print(" ".join(args[1:]))


def process_external_commands(args):
    exec_result = subprocess.run(args=args, capture_output=True, text=True)
    sys.stdout.write(exec_result.stdout)
    sys.stdout.flush()
    sys.stderr.write(exec_result.stderr)
    sys.stderr.flush()
