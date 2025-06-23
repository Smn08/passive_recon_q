import argparse
from rich import print
from modules.subdomains import run_subfinder
from modules.httpx_scan import run_httpx
from modules.nuclei_scan import run_nuclei
from modules.asn_lookup import run_asn
from modules.leak_check import run_leakcheck
from modules.email_harvest import run_emailharvester
from modules.portscan import run_naabu, run_nmap
from osint.osint_sources import run_crtsh, run_virustotal
from osint.shodan_censys import shodan_ports, censys_services
from osint.securitytrails import securitytrails_subdomains
from osint.fofa import fofa_search
from osint.dorks import google_dorks, github_dorks
from osint.osint_all import run_all_osint
from reporting.report import save_report
import os

def main():
    parser = argparse.ArgumentParser(description='Passive Reconnaissance Framework')
    parser.add_argument('--target', help='Target domain or company name')
    parser.add_argument('--scope', help='Scope file with domains (one per line)')
    parser.add_argument('--mongo', help='MongoDB connection string')
    parser.add_argument('--subdomains', action='store_true', help='Собрать поддомены через subfinder')
    parser.add_argument('--httpx', action='store_true', help='Проверить живые HTTP(S) хосты через httpx')
    parser.add_argument('--nuclei', action='store_true', help='Пассивно проверить уязвимости через nuclei')
    parser.add_argument('--nuclei-templates', help='Путь к шаблонам nuclei (опционально)')
    parser.add_argument('--asn', action='store_true', help='Получить ASN-информацию через asnmap')
    parser.add_argument('--leaks', action='store_true', help='Проверить утечки через leakix.net')
    parser.add_argument('--emails', action='store_true', help='Собрать email-адреса через EmailHarvester')
    parser.add_argument('--ports', action='store_true', help='Пассивно просканировать порты через naabu')
    parser.add_argument('--nmap', action='store_true', help='Сканировать порты через nmap (тихий режим, обход фильтрации)')
    parser.add_argument('--virustotal', action='store_true', help='Получить поддомены через VirusTotal')
    parser.add_argument('--crtsh', action='store_true', help='Получить поддомены через crt.sh')
    parser.add_argument('--vt-api-key', help='API-ключ VirusTotal (или через переменную окружения VT_API_KEY)')
    parser.add_argument('--nmap-extra', nargs='*', help='Дополнительные параметры для nmap')
    parser.add_argument('--report-format', choices=['md', 'html'], default='md', help='Формат итогового отчета (md или html)')
    parser.add_argument('--google-dorks', action='store_true', help='Искать через Google Dorks (требуется API и CSE)')
    parser.add_argument('--google-api-key', help='Google API key для Dorks')
    parser.add_argument('--google-cse-id', help='Google Custom Search Engine ID для Dorks')
    parser.add_argument('--github-dorks', action='store_true', help='Искать через GitHub Dorks (требуется токен)')
    parser.add_argument('--github-token', help='GitHub Personal Access Token для Dorks')
    parser.add_argument('--shodan', action='store_true', help='Получить поддомены через Shodan (API)')
    parser.add_argument('--shodan-api-key', help='Shodan API key')
    parser.add_argument('--censys', action='store_true', help='Получить сервисы через Censys (API)')
    parser.add_argument('--censys-api-id', help='Censys API ID')
    parser.add_argument('--censys-api-secret', help='Censys API Secret')
    parser.add_argument('--securitytrails', action='store_true', help='Получить поддомены через SecurityTrails (API)')
    parser.add_argument('--securitytrails-api-key', help='SecurityTrails API key')
    parser.add_argument('--fofa', action='store_true', help='Поиск сервисов через FOFA (API)')
    parser.add_argument('--fofa-email', help='FOFA email')
    parser.add_argument('--fofa-api-key', help='FOFA API key')
    parser.add_argument('--osint-all', action='store_true', help='Искать по всем OSINT-источникам одновременно')
    args = parser.parse_args()

    print('[bold green]Passive Reconnaissance Framework[/bold green]')
    results = {}
    if args.subdomains and args.target:
        subs = run_subfinder(args.target)
        results['Поддомены (subfinder)'] = subs
    elif args.httpx and args.target:
        subs = run_subfinder(args.target)
        alive = run_httpx(subs)
        results['Живые HTTP(S) хосты (httpx)'] = alive
    elif args.nuclei and args.target:
        subs = run_subfinder(args.target)
        alive = run_httpx(subs)
        results['Живые HTTP(S) хосты (httpx)'] = alive
        vulns = run_nuclei(alive, args.nuclei_templates)
        results['Уязвимости (nuclei)'] = vulns
    elif args.asn and args.target:
        asn = run_asn(args.target)
        results['ASN-информация (asnmap)'] = asn
    elif args.leaks and args.target:
        run_leakcheck(args.target)
        results['Проверка утечек (leakix.net)'] = f'https://leakix.net/domain/{args.target}'
    elif args.emails and args.target:
        emails = run_emailharvester(args.target)
        results['Email-адреса (EmailHarvester)'] = emails
    elif args.ports and args.target:
        ports = run_naabu(args.target)
        results['Открытые порты (naabu)'] = ports
    elif args.nmap and args.target:
        nmap_out = run_nmap(args.target, args.nmap_extra)
        results['Результаты nmap'] = nmap_out
    elif args.virustotal and args.target:
        api_key = args.vt_api_key or os.getenv('VT_API_KEY')
        if not api_key:
            print('[red]Необходимо указать API-ключ VirusTotal через --vt-api-key или переменную окружения VT_API_KEY[/red]')
        else:
            vt = run_virustotal(args.target, api_key)
            results['Поддомены (VirusTotal)'] = vt
    elif args.crtsh and args.target:
        crt = run_crtsh(args.target)
        results['Поддомены (crt.sh)'] = crt
    elif args.google_dorks and args.target:
        api_key = args.google_api_key or os.getenv('GOOGLE_API_KEY')
        cse_id = args.google_cse_id or os.getenv('GOOGLE_CSE_ID')
        if not api_key or not cse_id:
            print('[red]Укажите --google-api-key и --google-cse-id или переменные окружения GOOGLE_API_KEY, GOOGLE_CSE_ID[/red]')
        else:
            dorks_res = google_dorks(args.target, api_key, cse_id)
            results = {'Google Dorks': dorks_res}
            save_report(results, args.target, args.report_format)
            return
    elif args.github_dorks and args.target:
        token = args.github_token or os.getenv('GITHUB_TOKEN')
        if not token:
            print('[red]Укажите --github-token или переменную окружения GITHUB_TOKEN[/red]')
        else:
            dorks_res = github_dorks(args.target, token)
            results = {'GitHub Dorks': dorks_res}
            save_report(results, args.target, args.report_format)
            return
    elif args.shodan and args.target:
        api_key = args.shodan_api_key or os.getenv('SHODAN_API_KEY')
        if not api_key:
            print('[red]Укажите --shodan-api-key или переменную окружения SHODAN_API_KEY[/red]')
        else:
            shodan_res = shodan_ports(args.target, api_key)
            results = {'Shodan': shodan_res}
            save_report(results, args.target, args.report_format)
            return
    elif args.censys and args.target:
        api_id = args.censys_api_id or os.getenv('CENSYS_API_ID')
        api_secret = args.censys_api_secret or os.getenv('CENSYS_API_SECRET')
        if not api_id or not api_secret:
            print('[red]Укажите --censys-api-id и --censys-api-secret или переменные окружения CENSYS_API_ID, CENSYS_API_SECRET[/red]')
        else:
            censys_res = censys_services(args.target, api_id, api_secret)
            results = {'Censys': censys_res}
            save_report(results, args.target, args.report_format)
            return
    elif args.securitytrails and args.target:
        api_key = args.securitytrails_api_key or os.getenv('SECURITYTRAILS_API_KEY')
        if not api_key:
            print('[red]Укажите --securitytrails-api-key или переменную окружения SECURITYTRAILS_API_KEY[/red]')
        else:
            st_res = securitytrails_subdomains(args.target, api_key)
            results = {'SecurityTrails': st_res}
            save_report(results, args.target, args.report_format)
            return
    elif args.fofa and args.target:
        email = args.fofa_email or os.getenv('FOFA_EMAIL')
        api_key = args.fofa_api_key or os.getenv('FOFA_API_KEY')
        if not email or not api_key:
            print('[red]Укажите --fofa-email и --fofa-api-key или переменные окружения FOFA_EMAIL, FOFA_API_KEY[/red]')
        else:
            fofa_res = fofa_search(args.target, email, api_key)
            results = {'FOFA': fofa_res}
            save_report(results, args.target, args.report_format)
            return
    elif args.osint_all and args.target:
        apikeys = {
            'virustotal': args.vt_api_key or os.getenv('VT_API_KEY'),
            'shodan': args.shodan_api_key or os.getenv('SHODAN_API_KEY'),
            'censys_id': args.censys_api_id or os.getenv('CENSYS_API_ID'),
            'censys_secret': args.censys_api_secret or os.getenv('CENSYS_API_SECRET'),
            'securitytrails': args.securitytrails_api_key or os.getenv('SECURITYTRAILS_API_KEY'),
            'fofa_email': args.fofa_email or os.getenv('FOFA_EMAIL'),
            'fofa_key': args.fofa_api_key or os.getenv('FOFA_API_KEY'),
        }
        results = run_all_osint(args.target, apikeys)
        save_report(results, args.target, args.report_format)
        return
    else:
        print('Это каркас. Добавьте модули для сбора поддоменов, утечек и т.д.')
        return
    # Генерация отчета
    if results:
        save_report(results, args.target, args.report_format)

if __name__ == '__main__':
    main()
