import os
import sys
from utils.helpers import builtins

def process_type(user_input: str):
    command_name = user_input[5:]
    if command_name in builtins:
        print(f"{command_name} is a shell builtin")
    else:
        path_sep = os.pathsep
        path_dirs = os.environ["PATH"].split(sep=path_sep)
        
        for path in path_dirs:
            full_path = os.path.join(path, command_name)
            if os.path.exists(path=full_path) and os.access(full_path, os.X_OK):
                print(f"{command_name} is {full_path}")
                return
        
        print(f"{command_name}: not found")