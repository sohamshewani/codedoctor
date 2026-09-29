import subprocess
import sys
from pathlib import Path
import click
import ollama
from rich.console import Console
from rich.panel import Panel

console = Console()

def run_script(file_path: Path):
    try:
        result = subprocess.run(
            [sys.executable, str(file_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Execution timed out."

@click.command()
@click.argument("target_file", type=click.Path(exists=True))
def main(target_file):
    path = Path(target_file)
    console.print(f"[bold cyan]Running {path.name}...[/bold cyan]")

    code_content = path.read_text(encoding="utf-8")
    returncode, stdout, stderr = run_script(path)

    if returncode == 0:
        console.print("[bold green]Success: Code executed without errors![/bold green]")
        if stdout:
            console.print(Panel(stdout.strip(), title="Program Output", border_style="green"))
        return

    console.print(Panel(stderr.strip(), title="Captured Error", border_style="red"))
    console.print("[bold yellow]Qwen 2.5 is diagnosing the bug...[/bold yellow]")

    prompt = f"The script failed with this error:\n{stderr}\n\nOriginal Code:\n{code_content}\n\nExplain the cause briefly and give the corrected code."

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[
            {"role": "system", "content": "You are an expert code debugger. Provide clear explanations and clean fixes."},
            {"role": "user", "content": prompt}
        ]
    )

    console.print(Panel(response["message"]["content"], title="Diagnosis & Fix", border_style="cyan"))

if __name__ == "__main__":
    main()

