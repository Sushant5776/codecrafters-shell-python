import os

builtins = ["echo", "type", "exit", "pwd"]
path_sep = os.pathsep
path_dirs = os.environ["PATH"].split(sep=path_sep)

def is_executable_command_in_path(user_input):
    command_name = user_input.split()[0]  # the command user has called xyz ar1 ar2 then xyz

    for path in path_dirs:
        full_path = os.path.join(path, command_name)
        if os.path.exists(path=full_path) and os.access(path=full_path, mode=os.X_OK):
            return full_path
        
    return None
