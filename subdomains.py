import subprocess
from rich import print
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
MONGO_DB = os.getenv('MONGO_DB', 'recon')
MONGO_COLLECTION = os.getenv('MONGO_COLLECTION', 'subdomains')

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

def run_subfinder(domain):
    try:
        result = subprocess.run([
            'subfinder',
            '-d', domain,
            '-silent'
        ], capture_output=True, text=True, check=True)
        subdomains = [s for s in result.stdout.strip().split('\n') if s]
        print(f'[bold cyan]Найдено {len(subdomains)} поддоменов для {domain}[/bold cyan]')
        if subdomains:
            docs = [{"domain": domain, "subdomain": s} for s in subdomains]
            collection.insert_many(docs)
            print(f'[green]Сохранено в MongoDB: {len(docs)}[/green]')
        return subdomains
    except Exception as e:
        print(f'[red]Ошибка запуска subfinder: {e}[/red]')
        return []
