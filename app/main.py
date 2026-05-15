import sys

# dict of builtin commands
commands = {
    "exit": lambda userInput: sys.exit(0),
    "echo": lambda userInput: print(userInput[5:]),
    "type": lambda userInput: print(f"{args} is a shell builtin")
    if (args := userInput[5:]) in commands
    else print(f"{args}: not found"),
}


def main():
    # REPL loop
    while True:
        # Print prompt
        sys.stdout.write("$ ")

        # wait for user input
        userInput = input()

        if (command := userInput.split()[0]) in commands:
            commands[command](userInput)
        else:
            print(f"{userInput}: command not found")


if __name__ == "__main__":
    main()