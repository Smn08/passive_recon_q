import subprocess
from rich import print

def run_emailharvester(domain):
    try:
        result = subprocess.run([
            'python3', 'EmailHarvester.py', '-d', domain, '-s', f'emails_{domain}.txt'],
            capture_output=True, text=True, check=True)
        print(f'[bold cyan]EmailHarvester завершил сбор email для {domain}[/bold cyan]')
        print(result.stdout)
        return f'emails_{domain}.txt'
    except Exception as e:
        print(f'[red]Ошибка запуска EmailHarvester: {e}[/red]')
        return ''
