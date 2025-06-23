import subprocess
from rich import print

def run_naabu(domain):
    try:
        result = subprocess.run([
            'naabu', '-host', domain, '-silent'
        ], capture_output=True, text=True, check=True)
        ports = result.stdout.strip().split('\n')
        print(f'[bold cyan]Открытые порты для {domain}:[/bold cyan]')
        for port in ports:
            print(port)
        return ports
    except Exception as e:
        print(f'[red]Ошибка запуска naabu: {e}[/red]')
        return []

def run_nmap(domain, extra_args=None):
    cmd = [
        'nmap', '-Pn', '-sS', '-T4', '--open', '--min-rate', '1000', '-n', '-oG', '-', domain
    ]
    if extra_args:
        cmd += extra_args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f'[bold cyan]Результаты nmap для {domain}:[/bold cyan]')
        print(result.stdout)
        return result.stdout
    except Exception as e:
        print(f'[red]Ошибка запуска nmap: {e}[/red]')
        return ''
