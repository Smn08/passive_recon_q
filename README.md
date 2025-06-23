# Фреймворк пассивной разведки

Этот проект — модульный open-source фреймворк для пассивной разведки, вдохновлённый лучшими практиками и рабочими процессами из сообщества информационной безопасности.

## Возможности
- Пассивный сбор поддоменов (subfinder, crt.sh, VirusTotal)
- Поиск живых HTTP(S) хостов (httpx)
- Пассивная проверка уязвимостей (nuclei, с выбором шаблонов)
- Хранение данных в MongoDB
- Сбор email-адресов, поиск утечек, Google/GitHub Dorks
- Пассивное сканирование портов (naabu, nmap)
- Получение ASN-информации (asnmap)
- Проверка утечек (leakix.net)
- Интеграция с OSINT-источниками (VirusTotal, crt.sh, Shodan, Censys, SecurityTrails, FOFA и др.)
- Расширяемость и скриптуемость для кастомных сценариев

## Требования
- Python 3.8+
- MongoDB (локально или удалённо)
- Kali Linux или любая современная Linux/Windows система
- CLI-инструменты: subfinder, httpx, nuclei, naabu, nmap, asnmap, EmailHarvester и др.

## Быстрый старт
1. Установите зависимости Python:
   ```powershell
   pip install -r requirements.txt
   ```
2. Установите необходимые CLI-инструменты (subfinder, httpx, nuclei, naabu, nmap и др.) согласно [ProjectDiscovery](https://github.com/projectdiscovery) и официальной документации.
3. Скопируйте и заполните файл .env на основе .env.example:
   ```powershell
   copy .env.example .env
   # или вручную создайте .env и заполните все ключи/переменные
   ```
   В этом файле хранятся все API-ключи и настройки для интеграций (MongoDB, OSINT, Dorks и др.).
4. Запустите основной скрипт:
   ```powershell
   python recon.py --help
   ```

## Примеры запуска
- Сбор поддоменов:
  ```powershell
  python recon.py --target example.com --subdomains
  python recon.py --target example.com --crtsh
  python recon.py --target example.com --virustotal --vt-api-key <API_KEY>
  ```
- Поиск живых HTTP(S) хостов:
  ```powershell
  python recon.py --target example.com --httpx
  ```
- Пассивная проверка уязвимостей (выбор шаблона):
  ```powershell
  python recon.py --target example.com --nuclei --nuclei-templates "c:\path\to\template.yaml"
  ```
- Сбор email-адресов:
  ```powershell
  python recon.py --target example.com --emails
  ```
- Пассивное сканирование портов:
  ```powershell
  python recon.py --target example.com --ports
  ```
- Получение ASN-информации:
  ```powershell
  python recon.py --target example.com --asn
  ```
- Проверка утечек:
  ```powershell
  python recon.py --target example.com --leaks
  ```
- Использование nmap вручную для обхода фильтрации и тихого режима:
  ```powershell
  nmap -Pn -sS -T4 --open --min-rate 1000 -n -v -oG - example.com
  ```
  - `-Pn` — не пинговать, сразу сканировать
  - `-sS` — SYN scan (тихий)
  - `-T4` — ускорение
  - `--min-rate 1000` — минимальная скорость
  - `-n` — не резолвить DNS
  - `--open` — показывать только открытые порты
  - `-oG -` — вывод в grepable формате
- Использование дополнительных OSINT-источников:
  ```powershell
  python recon.py --target example.com --shodan --shodan-api-key <API_KEY>
  python recon.py --target example.com --censys --censys-api-id <ID> --censys-api-secret <SECRET>
  python recon.py --target example.com --securitytrails --securitytrails-api-key <API_KEY>
  python recon.py --target example.com --fofa --fofa-email <EMAIL> --fofa-api-key <API_KEY>
  ```
- Google Dorks и GitHub Dorks:
  ```powershell
  python recon.py --target example.com --google-dorks --google-api-key <API> --google-cse-id <CSE>
  python recon.py --target example.com --github-dorks --github-token <TOKEN>
  ```
- Поиск по всем OSINT-источникам (ключи можно не указывать — будут использованы только открытые источники):
  ```powershell
  python recon.py --target example.com --osint-all
  ```
  Все API-ключи и чувствительные данные указываются только в файле `.env` (см. пример `.env.example`). Перед запуском убедитесь, что вы скопировали `.env.example` в `.env` и заполнили нужные переменные. Передавать ключи через параметры командной строки не требуется — это возможно только для тестов или CI/CD, но не рекомендуется для production.

  Если ключи не заданы, будут использованы только открытые источники (например, crt.sh).
- Экспорт отчетов в PDF и CSV:
  ```powershell
  python recon.py --target example.com --subdomains --report-format pdf
  python recon.py --target example.com --subdomains --report-format csv
  ```

## Запуск через Docker Compose

1. Соберите контейнеры:
   ```powershell
   docker compose build
   ```
   > **Важно:**
   > - Если видите предупреждение `the attribute version is obsolete`, просто удалите строку `version:` из docker-compose.yml.
   > - Если появляется ошибка `Cannot connect to the Docker daemon`, убедитесь, что Docker запущен (например, командой `sudo service docker start` в Linux или через Docker Desktop в Windows/Mac). Без запущенного демона Docker ни одна команда не будет работать.
   > - Если команда `sudo service docker start` не работает (ошибка Unit docker.service not found), попробуйте запустить Docker через:
   >   - `sudo systemctl start docker` (для большинства современных дистрибутивов Linux)
   >   - Или используйте графический Docker Desktop (для Windows/Mac)
   >   - Для Kali Linux: установите пакет docker.io командой `sudo apt install docker.io`, затем `sudo systemctl start docker`
2. Запустите MongoDB и фреймворк:
   ```powershell
   docker-compose run --rm recon python3 recon.py --target example.com --subdomains --report-format md
   ```
   Все результаты и отчеты будут доступны в вашей рабочей папке.

3. Для запуска с HTML-, PDF- или CSV-отчетом:
   ```powershell
   docker-compose run --rm recon python3 recon.py --target example.com --subdomains --report-format html
   docker-compose run --rm recon python3 recon.py --target example.com --subdomains --report-format pdf
   docker-compose run --rm recon python3 recon.py --target example.com --subdomains --report-format csv
   ```

4. Для интерактивной работы с MongoDB:
   - MongoDB будет доступна на порту 27017 (можно подключаться с хоста)

## Структура проекта

```
OpenSource Research/
├── recon.py                # Главный скрипт запуска
├── requirements.txt        # Python-зависимости
├── Dockerfile              # Docker-образ для запуска
├── docker-compose.yml      # Docker Compose для orchestration
├── .env.example            # Пример переменных окружения
├── modules/                # Модули для интеграции с CLI-инструментами
│   ├── subdomains.py
│   ├── httpx_scan.py
│   ├── nuclei_scan.py
│   ├── asn_lookup.py
│   ├── leak_check.py
│   ├── email_harvest.py
│   ├── portscan.py
│   └── __init__.py
├── osint/                  # Модули для работы с OSINT-источниками
│   ├── osint_sources.py
│   ├── shodan_censys.py
│   ├── securitytrails.py
│   ├── fofa.py
│   ├── dorks.py
│   ├── osint_all.py
│   └── __init__.py
├── reporting/              # Модули экспорта и генерации отчетов
│   ├── report.py
│   ├── export_report.py
│   └── __init__.py
├── web/                    # Веб-интерфейс (Flask)
│   ├── web_dashboard.py
│   └── __init__.py
└── README.md
```

## Переменные окружения
Все ключи и чувствительные данные хранятся в `.env` (см. `.env.example`).

- Все переменные для интеграций (VT_API_KEY, SHODAN_API_KEY, CENSYS_API_ID, CENSYS_API_SECRET, SECURITYTRAILS_API_KEY, FOFA_EMAIL, FOFA_API_KEY и др.) указываются только в `.env`.
- Не храните ключи в командной строке или в открытом виде в скриптах!
- MONGO_URI — строка подключения к MongoDB

## Безопасность
- Не публикуйте свой `.env` в публичных репозиториях.
- Для CI/CD используйте секреты среды, а не явные ключи.

## Советы по расширению
- Для добавления нового OSINT-источника создавайте модуль в папке `osint/` и подключите его в `recon.py`.
- Для интеграции нового CLI-инструмента — добавьте модуль в `modules/`.
- Для новых форматов отчетов — расширяйте `reporting/`.

## Лицензия
Проект открыт для коммьюнити и доработок!
