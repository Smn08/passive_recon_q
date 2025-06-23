import subprocess
from rich import print

def run_asn(domain):
    try:
        result = subprocess.run([
            'asnmap',
            '-d', domain,
            '-silent'
        ], capture_output=True, text=True, check=True)
        asn_info = result.stdout.strip()
        print(f'[bold cyan]ASN информация для {domain}:[/bold cyan]\n{asn_info}')
        return asn_info
    except Exception as e:
        print(f'[red]Ошибка запуска asnmap: {e}[/red]')
        return ''
