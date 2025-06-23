from googlesearch import search
import requests
from rich import print
import os

def google_dorks(domain, api_key, cse_id):
    """Ищет через Google Dorks (Custom Search API)"""
    dorks = [
        f'site:{domain} ext:sql',
        f'site:{domain} ext:env',
        f'site:{domain} inurl:admin',
        f'site:{domain} password',
    ]
    results = []
    for dork in dorks:
        url = f'https://www.googleapis.com/customsearch/v1?q={dork}&key={api_key}&cx={cse_id}'
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get('items', []):
                    results.append(item.get('link'))
            else:
                print(f'[red]Ошибка Google API: {resp.status_code}[/red]')
        except Exception as e:
            print(f'[red]Ошибка Google Dorks: {e}[/red]')
    return results

def github_dorks(domain, token):
    """Ищет через GitHub Dorks (поиск по коду)"""
    dorks = [
        f'{domain} password',
        f'{domain} secret',
        f'{domain} api_key',
    ]
    headers = {'Authorization': f'token {token}'}
    results = []
    for dork in dorks:
        url = f'https://api.github.com/search/code?q={dork}'
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                for item in data.get('items', []):
                    results.append(item.get('html_url'))
            else:
                print(f'[red]Ошибка GitHub API: {resp.status_code}[/red]')
        except Exception as e:
            print(f'[red]Ошибка GitHub Dorks: {e}[/red]')
    return results

def search_google(query):
    """Ищет в Google"""
    results = list(search(query, num_results=10))
    return results

def search_github(query, token):
    """Ищет на GitHub"""
    headers = {'Authorization': f'token {token}'}
    url = f'https://api.github.com/search/repositories?q={query}'
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            results = [item['html_url'] for item in data.get('items', [])]
            return results
        else:
            print(f'[red]Ошибка GitHub API: {resp.status_code}[/red]')
    except Exception as e:
        print(f'[red]Ошибка поиска на GitHub: {e}[/red]')
    return []
