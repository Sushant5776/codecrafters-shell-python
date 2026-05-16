import os
import sys
from contextlib import contextmanager

builtins = ["echo", "type", "exit", "pwd", "cd"]
path_sep = os.pathsep
path_dirs = os.environ["PATH"].split(sep=path_sep)

def is_executable_command_in_path(command_name: str):
    for path in path_dirs:
        full_path = os.path.join(path, command_name)
        if os.path.exists(path=full_path) and os.access(path=full_path, mode=os.X_OK):
            return full_path
        
    return None


def parse_redirects(args: list[str]) -> tuple[list[str], str | None, bool, bool]:
    """
    Strips redirect tokens from args.
    Returns (clean_args, output_file, is_append).
    Supports: '>'  (overwrite) and '>>' (append).
    """
    clean_args = []
    output_file = None
    is_append = False
    is_stdout = False
    i = 0
    while i < len(args):
        if (args[i] == ">>" or args[i] == "1>>") and i + 1 < len(args):
            output_file = args[i + 1]
            is_append = True
            is_stdout = True
            i += 2
        elif (args[i] == ">" or args[i] == "1>") and i + 1 < len(args):
            output_file = args[i + 1]
            is_append = False
            is_stdout = True
            i += 2
        elif args[i] == "2>>" and i + 1 < len(args):
            output_file = args[i + 1]
            is_append = True
            is_stdout = False
            i += 2
        elif args[i] == "2>" and i + 1 < len(args):
            output_file = args[i + 1]
            is_append = False
            is_stdout = False
            i += 2
        else:
            clean_args.append(args[i])
            i += 1
    return clean_args, output_file, is_append, is_stdout


@contextmanager
def redirect_stdout(filepath: str | None, is_append: bool = False, is_stdout: bool = False):
    """Context manager that temporarily redirects stdout to a file."""
    if filepath is None:
        yield  # No redirection; behave normally
        return

    mode = "a" if is_append else "w"

    if is_stdout:
        original = sys.stdout
    else:
        original = sys.stderr
    
    try:
        with open(filepath, mode) as f:
            if is_stdout:
                sys.stdout = f
            else:
                sys.stderr = f
            yield
    finally:
        if is_stdout:
            sys.stdout = original  # Always restore, even on exception
        else:
            sys.stderr = original