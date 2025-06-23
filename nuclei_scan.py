import subprocess
from rich import print

def run_nuclei(urls, templates=None):
    cmd = ['nuclei', '-silent']
    if templates:
        cmd += ['-t', templates]
    try:
        process = subprocess.run(
            cmd,
            input='\n'.join(urls),
            capture_output=True, text=True, check=True
        )
        results = [line for line in process.stdout.strip().split('\n') if line]
        print(f'[bold cyan]Nuclei: найдено {len(results)} потенциальных уязвимостей[/bold cyan]')
        return results
    except Exception as e:
        print(f'[red]Ошибка запуска nuclei: {e}[/red]')
        return []
