from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from rich import print
import base64
import json
import time

def get_vuln_info(ip, port, protocol):
    """Получение информации о уязвимостях"""
    url = f'https://vulners.com/api/v3/search/id/?id={ip}:{port}'
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return data.get('data', {})
        else:
            print(f'[red]Ошибка Vulners API: {resp.status_code}[/red]')
            return {}
    except Exception as e:
        print(f'[red]Ошибка при работе с Vulners: {e}[/red]')
        return {}

def fofa_search(domain, email, api_key):
    """Поиск сервисов через FOFA API"""
    query = f'domain="{domain}"'
    b64_query = base64.b64encode(query.encode()).decode()
    url = f'https://fofa.info/api/v1/search/all?email={email}&key={api_key}&qbase64={b64_query}&fields=host,ip,port,protocol,title&size=100'
    try:
        resp = requests.get(url, timeout=20)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get('results', [])
            print(f'[cyan]Найдено {len(results)} сервисов через FOFA[/cyan]')
            return results
        else:
            print(f'[red]Ошибка FOFA API: {resp.status_code}[/red]')
            return []
    except Exception as e:
        print(f'[red]Ошибка при работе с FOFA: {e}[/red]')
        return []

def process_service(service, email, api_key):
    """Обработка найденного сервиса"""
    ip = service.get('ip')
    port = service.get('port')
    protocol = service.get('protocol')
    title = service.get('title', '')
    
    vuln_info = get_vuln_info(ip, port, protocol)
    
    if vuln_info:
        print(f'[green]Уязвимость найдена на {ip}:{port} ({protocol})[/green]')
        print(f'  Заголовок: {title}')
        print(f'  Информация об уязвимости: {vuln_info}')
    else:
        print(f'[yellow]Сервис без известных уязвимостей: {ip}:{port} ({protocol})[/yellow]')

def main(domain, email, api_key):
    """Основная функция"""
    start_time = time.time()
    services = fofa_search(domain, email, api_key)
    
    if services:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(process_service, service, email, api_key): service for service in services}
            for future in as_completed(futures):
                service = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f'[red]Ошибка при обработке сервиса {service}: {e}[/red]')
    
    print(f'[blue]Поиск завершен за {time.time() - start_time:.2f} секунд[/blue]')

if __name__ == "__main__":
    DOMAIN = "example.com"
    EMAIL = "your_email@example.com"
    API_KEY = "your_api_key"
    main(DOMAIN, EMAIL, API_KEY)
