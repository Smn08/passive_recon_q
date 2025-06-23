from rich import print
from datetime import datetime
import os

def save_report(results, target, fmt='md'):
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'report_{target}_{now}.{fmt}'
    if fmt == 'md':
        content = _make_markdown(results, target)
    elif fmt == 'html':
        content = _make_html(results, target)
    else:
        print(f'[red]Неизвестный формат отчета: {fmt}[/red]')
        return None
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'[green]Отчет сохранен: {filename}[/green]')
    return filename

def _make_markdown(results, target):
    lines = [f'# Отчет по пассивной разведке: {target}\n', f'Дата: {datetime.now()}\n']
    for section, data in results.items():
        lines.append(f'## {section}')
        if isinstance(data, list):
            for item in data:
                lines.append(f'- {item}')
        elif isinstance(data, str):
            lines.append(data)
        else:
            lines.append(str(data))
        lines.append('')
    return '\n'.join(lines)

def _make_html(results, target):
    html = [f'<h1>Отчет по пассивной разведке: {target}</h1>', f'<p>Дата: {datetime.now()}</p>']
    for section, data in results.items():
        html.append(f'<h2>{section}</h2>')
        if isinstance(data, list):
            html.append('<ul>')
            for item in data:
                html.append(f'<li>{item}</li>')
            html.append('</ul>')
        elif isinstance(data, str):
            html.append(f'<pre>{data}</pre>')
        else:
            html.append(f'<pre>{str(data)}</pre>')
    return '\n'.join(html)
