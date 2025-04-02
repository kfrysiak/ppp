import sys
import subprocess
from pathlib import Path
from rich.console import Console
from typing import Any, Optional
from ppp.toml_service import (
    Script,
    extract_scripts,
)


console = Console()


def list_scripts(scripts: list[Script]) -> None:
    console.print("[bold cyan]Available scripts:[/bold cyan]")
    for script in scripts:
        console.print(f"[bold yellow]{script.name}[/bold yellow]", end=" ")
        if script.inline_comment is not None and script.inline_comment != "":
            console.print(script.inline_comment, end="", style="dim", markup=False)
        if len(script.comments) > 0:
            console.print(" - " + "\n".join(script.comments))
        else:
            console.print("")


def run_script(scripts: list[Script], script_name: str, args: Any) -> None:
    print("Running script:", script_name)

    found_script: Optional[Script] = None

    for script in scripts:
        if script.name == script_name:
            found_script = script
            break

    if found_script is None:
        console.print(f"[bold red]Error: Script '{script_name}' not found![/bold red]")
        sys.exit(1)

    if not found_script.command:
        console.print(
            f"[bold red]Error: Script '{script_name}' doesn't have a command![/bold red]"
        )
        sys.exit(1)

    subprocess.run(
        " ".join([found_script.command, *args]), shell=True, executable="/bin/zsh"
    )


def show_help() -> None:
    console.print("[bold green]Usage:[/bold green]")
    console.print(
        "  [bold yellow]ppp run <script> [args][/bold yellow] - Run a script with optional arguments"
    )
    console.print(
        "  [bold yellow]ppp list[/bold yellow] - List available scripts with descriptions"
    )
    console.print("  [bold yellow]ppp help[/bold yellow] - Show this help message")


def main() -> None:
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    command = sys.argv[1]

    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        console.print("[bold red]Error: pyproject.toml not found![/bold red]")
        sys.exit(1)

    scripts = extract_scripts(pyproject_path, console=console)

    if command == "list":
        list_scripts(scripts)
    elif command == "help":
        show_help()
    elif command == "run" and len(sys.argv) > 2:
        script_name = sys.argv[2]
        args = sys.argv[3:]
        run_script(scripts, script_name, args)
    else:
        console.print(
            "[bold red]Invalid command. Use 'ppp help' for usage information.[/bold red]"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
