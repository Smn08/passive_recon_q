import requests
from rich import print

def run_virustotal(domain, api_key):
    url = f'https://www.virustotal.com/api/v3/domains/{domain}/subdomains'
    headers = {'x-apikey': api_key}
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            subdomains = [item['id'] for item in data.get('data', [])]
            print(f'[bold cyan]VirusTotal: найдено {len(subdomains)} поддоменов[/bold cyan]')
            for s in subdomains:
                print(s)
            return subdomains
        else:
            print(f'[yellow]VirusTotal: статус {resp.status_code}, {resp.text}[/yellow]')
            return []
    except Exception as e:
        print(f'[red]Ошибка запроса к VirusTotal: {e}[/red]')
        return []

def run_crtsh(domain):
    url = f'https://crt.sh/?q=%25.{domain}&output=json'
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            subdomains = set()
            for entry in data:
                name = entry.get('name_value')
                if name:
                    for s in name.split('\n'):
                        if s.endswith(domain):
                            subdomains.add(s.strip())
            print(f'[bold cyan]crt.sh: найдено {len(subdomains)} поддоменов[/bold cyan]')
            for s in subdomains:
                print(s)
            return list(subdomains)
        else:
            print(f'[yellow]crt.sh: статус {resp.status_code}[/yellow]')
            return []
    except Exception as e:
        print(f'[red]Ошибка запроса к crt.sh: {e}[/red]')
        return []
