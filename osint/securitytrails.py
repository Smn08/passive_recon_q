import requests
from rich import print

def securitytrails_subdomains(domain, api_key):
    """Получить поддомены через SecurityTrails API"""
    url = f'https://api.securitytrails.com/v1/domain/{domain}/subdomains'
    headers = {'APIKEY': api_key}
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            subs = data.get('subdomains', [])
            subdomains = [f'{s}.{domain}' for s in subs]
            print(f'[cyan]Найдено {len(subdomains)} поддоменов через SecurityTrails[/cyan]')
            return subdomains
        else:
            print(f'[red]Ошибка SecurityTrails API: {resp.status_code}[/red]')
            return []
    except Exception as e:
        print(f'[red]Ошибка при работе с SecurityTrails: {e}[/red]')
        return []
