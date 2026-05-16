import os

builtins = ["echo", "type", "exit", "pwd", "cd"]
path_sep = os.pathsep
path_dirs = os.environ["PATH"].split(sep=path_sep)

def is_executable_command_in_path(command_name: str):
    for path in path_dirs:
        full_path = os.path.join(path, command_name)
        if os.path.exists(path=full_path) and os.access(path=full_path, mode=os.X_OK):
            return full_path
        
    return None
