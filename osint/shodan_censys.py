# ...existing code from shodan_censys.py...

import requests
from rich import print

def shodan_ports(domain, api_key):
    """Получить открытые порты и сервисы через Shodan API"""
    url = f'https://api.shodan.io/dns/domain/{domain}?key={api_key}'
    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            subdomains = data.get('subdomains', [])
            print(f'[cyan]Найдено {len(subdomains)} поддоменов через Shodan[/cyan]')
            return subdomains
        else:
            print(f'[red]Ошибка Shodan API: {resp.status_code}[/red]')
            return []
    except Exception as e:
        print(f'[red]Ошибка при работе с Shodan: {e}[/red]')
        return []

def censys_services(domain, api_id, api_secret):
    """Получить сервисы через Censys API v2"""
    url = f'https://search.censys.io/api/v2/hosts/search?q={domain}'
    try:
        resp = requests.get(url, auth=(api_id, api_secret), timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get('result', {}).get('hits', [])
            print(f'[cyan]Найдено {len(results)} сервисов через Censys[/cyan]')
            return results
        else:
            print(f'[red]Ошибка Censys API: {resp.status_code}[/red]')
            return []
    except Exception as e:
        print(f'[red]Ошибка при работе с Censys: {e}[/red]')
        return []
