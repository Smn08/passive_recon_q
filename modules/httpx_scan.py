import subprocess
from rich import print

def run_httpx(domains):
    try:
        process = subprocess.run(
            ['httpx', '-silent'],
            input='\n'.join(domains),
            capture_output=True, text=True, check=True
        )
        alive = [line for line in process.stdout.strip().split('\n') if line]
        print(f'[bold cyan]Найдено {len(alive)} живых HTTP(S) хостов[/bold cyan]')
        return alive
    except Exception as e:
        print(f'[red]Ошибка запуска httpx: {e}[/red]')
        return []
