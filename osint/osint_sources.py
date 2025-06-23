import requests
from rich import print

def run_crtsh(domain):
    """Получить поддомены через crt.sh"""
    url = f'https://crt.sh/?q=%25.{domain}&output=json'
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            subdomains = set()
            for entry in data:
                name = entry.get('name_value')
                if name:
                    for sub in name.split('\n'):
                        if sub.endswith(domain):
                            subdomains.add(sub.strip())
            print(f'[cyan]Найдено {len(subdomains)} поддоменов через crt.sh[/cyan]')
            return list(subdomains)
        else:
            print(f'[red]Ошибка запроса к crt.sh: {resp.status_code}[/red]')
            return []
    except Exception as e:
        print(f'[red]Ошибка при работе с crt.sh: {e}[/red]')
        return []

def run_virustotal(domain, api_key):
    """Получить поддомены через VirusTotal API v3"""
    headers = {'x-apikey': api_key}
    url = f'https://www.virustotal.com/api/v3/domains/{domain}/subdomains?limit=1000'
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            subdomains = [item['id'] for item in data.get('data', [])]
            print(f'[cyan]Найдено {len(subdomains)} поддоменов через VirusTotal[/cyan]')
            return subdomains
        else:
            print(f'[red]Ошибка запроса к VirusTotal: {resp.status_code}[/red]')
            return []
    except Exception as e:
        print(f'[red]Ошибка при работе с VirusTotal: {e}[/red]')
        return []
