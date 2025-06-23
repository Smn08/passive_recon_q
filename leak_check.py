import subprocess
from rich import print

def run_leakcheck(domain):
    try:
        # Пример: интеграция с leakix.net через curl-impersonate или аналогичный инструмент
        print(f'[yellow]Проверьте утечки вручную на https://leakix.net/domain/{domain}[/yellow]')
        # Можно добавить автоматизацию через API, если потребуется
    except Exception as e:
        print(f'[red]Ошибка проверки утечек: {e}[/red]')
