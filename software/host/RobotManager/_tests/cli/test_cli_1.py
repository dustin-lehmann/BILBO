import cmd

class MyCLI(cmd.Cmd):
    intro = "Welcome to the CLI. Type help or ? to list commands."
    prompt = "(mycli) "

    def do_exit(self, arg):
        "Exit the program."
        print("Goodbye!")
        return True

    def do_hello(self, arg):
        "Say hello."
        print(f"Hello, {arg or 'World'}!")

if __name__ == "__main__":
    MyCLI().cmdloop()
