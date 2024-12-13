from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def main():
    layout = Layout()
    layout.split(
        Layout(name="output", ratio=3),
        Layout(name="input", size=3)
    )
    layout["output"].update(Panel("Program output will appear here."))
    layout["input"].update(Panel("Type commands below:"))

    console.print(layout)

    while True:
        cmd = Prompt.ask("[bold green]Enter command (type 'exit' to quit)[/]")
        if cmd == "exit":
            break
        console.log(f"[cyan]Command received:[/] {cmd}")

if __name__ == "__main__":
    main()
