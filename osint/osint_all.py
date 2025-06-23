# ...existing code from osint_all.py...
from osint.osint_sources import run_crtsh, run_virustotal
from osint.shodan_censys import shodan_ports, censys_services
from osint.securitytrails import securitytrails_subdomains
from osint.fofa import fofa_search
from rich import print
import os

def run_all_osint(domain, apikeys):
    """Запуск поиска по всем OSINT-источникам одновременно. Если ключа нет — ищет только в открытых источниках."""
    results = {}
    # crt.sh всегда доступен
    results['crt.sh'] = run_crtsh(domain)
    # VirusTotal
    if apikeys.get('virustotal'):
        results['VirusTotal'] = run_virustotal(domain, apikeys['virustotal'])
    # Shodan
    if apikeys.get('shodan'):
        results['Shodan'] = shodan_ports(domain, apikeys['shodan'])
    # Censys
    if apikeys.get('censys_id') and apikeys.get('censys_secret'):
        results['Censys'] = censys_services(domain, apikeys['censys_id'], apikeys['censys_secret'])
    # SecurityTrails
    if apikeys.get('securitytrails'):
        results['SecurityTrails'] = securitytrails_subdomains(domain, apikeys['securitytrails'])
    # FOFA
    if apikeys.get('fofa_email') and apikeys.get('fofa_key'):
        results['FOFA'] = fofa_search(domain, apikeys['fofa_email'], apikeys['fofa_key'])
    print(f'[green]OSINT-агрегация завершена для {domain}[/green]')
    return results
