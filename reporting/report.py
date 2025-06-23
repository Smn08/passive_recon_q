# ...existing code from report.py...
from rich import print
from datetime import datetime
import os
from reporting.export_report import export_to_csv, export_to_pdf

def save_report(results, target, fmt='md'):
    """Сохраняет отчет в выбранном формате (md, html, pdf, csv)"""
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    base = f'report_{target}_{now}'
    if fmt == 'md':
        fname = f'{base}.md'
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(f'# OSINT Report for {target}\n\n')
            for k, v in results.items():
                f.write(f'## {k}\n')
                if isinstance(v, list):
                    for item in v:
                        f.write(f'- {item}\n')
                else:
                    f.write(f'{v}\n')
        print(f'[green]Отчет сохранён: {fname}[/green]')
    elif fmt == 'html':
        fname = f'{base}.html'
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(f'<h1>OSINT Report for {target}</h1>')
            for k, v in results.items():
                f.write(f'<h2>{k}</h2>')
                if isinstance(v, list):
                    f.write('<ul>')
                    for item in v:
                        f.write(f'<li>{item}</li>')
                    f.write('</ul>')
                else:
                    f.write(f'<p>{v}</p>')
        print(f'[green]HTML-отчет сохранён: {fname}[/green]')
    elif fmt == 'pdf':
        fname = f'{base}.pdf'
        export_to_pdf(results, target, fname)
        print(f'[green]PDF-отчет сохранён: {fname}[/green]')
    elif fmt == 'csv':
        fname = f'{base}.csv'
        export_to_csv(results, fname)
        print(f'[green]CSV-отчет сохранён: {fname}[/green]')
    else:
        print(f'[red]Неизвестный формат отчета: {fmt}[/red]')
