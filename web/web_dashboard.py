from flask import Flask, render_template_string
import os
import glob

app = Flask(__name__)

@app.route('/')
def index():
    # Ищем все отчеты в рабочей папке
    reports = []
    for ext in ('*.md', '*.html', '*.pdf', '*.csv'):
        reports.extend(glob.glob(ext))
    reports = sorted(reports, reverse=True)
    html = '''
    <h1>OSINT Reports Dashboard</h1>
    <ul>
    {% for r in reports %}
      <li><a href="/report/{{r}}">{{r}}</a></li>
    {% endfor %}
    </ul>
    '''
    return render_template_string(html, reports=reports)

@app.route('/report/<path:filename>')
def show_report(filename):
    ext = os.path.splitext(filename)[1]
    if ext == '.md':
        with open(filename, encoding='utf-8') as f:
            content = f.read()
        # Простой markdown->html (можно заменить на markdown2)
        content = content.replace('\n', '<br>')
        return f'<h2>{filename}</h2><div>{content}</div>'
    elif ext == '.html':
        with open(filename, encoding='utf-8') as f:
            return f.read()
    elif ext == '.csv':
        with open(filename, encoding='utf-8') as f:
            content = f.read()
        return f'<h2>{filename}</h2><pre>{content}</pre>'
    elif ext == '.pdf':
        return f'<h2>PDF-файл: <a href="/{filename}">{filename}</a></h2>'
    else:
        return 'Unknown file type.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
