import os
import sys
import shlex
import tty
import termios
from pathlib import Path
from contextlib import contextmanager
from typing import List

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


def get_available_autocomplete_options(command: str) -> list[str]:
    options_builtins = [builtin_command for builtin_command in builtins if builtin_command.startswith(command)]
    options_external = set()

    for directory in path_dirs:
        dir_path = Path(directory)

        if not dir_path.is_dir():
            continue

        try:
            for entry in dir_path.iterdir():
                if entry.name.lower().startswith(command) and os.access(entry, os.X_OK):
                    options_external.add(entry.name)
        except PermissionError:
            continue


    options = list(set(options_builtins + list(options_external)))
    options.sort()

    return options

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd=fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def find_longest_common_prefix(options: List[str]) -> str:
    if not len(options): return ""
    
    prefix = options[0]

    i = 0

    while i  < len(options):
        if prefix == "":
            break

        temp = options[i]

        while len(prefix) and not temp.startswith(prefix):
            prefix = prefix[:-1]
        
        i += 1

    return prefix


def get_input():
    buffer = ""
    tab_count = 0

    sys.stdout.write("$ ")
    sys.stdout.flush()

    while True:
        current_input_char = getch()

        # In raw mode, Enter is often read as '\r' (carriage return)
        if current_input_char in ('\n', '\r'):
            # Move to a new line before printing the final buffer
            sys.stdout.write("\n")
            return buffer.strip()
        elif current_input_char == "\t":
            tab_count += 1

            args = shlex.split(buffer)

            if not len(args):
                tab_count = 0
                continue

            command = args[-1]

            options = get_available_autocomplete_options(command)

            if tab_count == 1:
                # Ring the bell instantly!
                sys.stdout.write("\x07")
                sys.stdout.flush()

                if len(options) == 1:
                    buffer = f"{options[0]} "  # might need -1 when you want to complete arguments

                    sys.stdout.write("\r\033[K")
                    sys.stdout.write(f"$ {buffer}")
                    sys.stdout.flush()
                else:
                    # autocomplete longest common prefix
                    prefix = find_longest_common_prefix(options)
                    buffer = prefix
                    # clear the screen
                    sys.stdout.write("\r\033[K")
                    sys.stdout.write(f"$ {prefix}")
                    sys.stdout.flush()
                
                # tab_count = 0

            elif tab_count == 2:
                tab_count = 0

                args = shlex.split(buffer)

                if not len(args):
                    tab_count = 0
                    continue

                command = args[0]

                options = get_available_autocomplete_options(command)

                sys.stdout.write("\n")
                suggestions_str = "  ".join(options).strip()
                sys.stdout.write(suggestions_str + "\n")
                sys.stdout.write(f"$ {buffer}")
                sys.stdout.flush()

        # Handle backspace or delete keys (optional but helpful in raw mode)
        elif current_input_char in ('\x08', '\x7f'):
            tab_count = 0
            if len(buffer) > 0:
                buffer = buffer[:-1]
                # Erase character from terminal: move back, print space, move back
                sys.stdout.write("\b \b")
                sys.stdout.flush()
        else:
            tab_count = 0
            buffer += current_input_char
            # We have to manually echo the character back to the screen
            # because raw mode disables automatic terminal echoing
            sys.stdout.write("\r\033[K")
            sys.stdout.write(f"$ {buffer}")
            sys.stdout.flush()