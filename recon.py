import argparse
from rich import print
from subdomains import run_subfinder
from httpx_scan import run_httpx
from nuclei_scan import run_nuclei
from asn_lookup import run_asn
from leak_check import run_leakcheck
from email_harvest import run_emailharvester
from portscan import run_naabu, run_nmap
from osint_sources import run_virustotal, run_crtsh
from report import save_report
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
    else:
        print('Это каркас. Добавьте модули для сбора поддоменов, утечек и т.д.')
        return
    # Генерация отчета
    if results:
        save_report(results, args.target, args.report_format)

if __name__ == '__main__':
    main()
