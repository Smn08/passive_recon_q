# Фреймворк пассивной разведки

Этот проект — модульный open-source фреймворк для пассивной разведки, вдохновлённый лучшими практиками и рабочими процессами из сообщества информационной безопасности.

## Возможности
- Пассивный сбор поддоменов (subfinder, crt.sh, VirusTotal)
- Поиск живых HTTP(S) хостов (httpx)
- Пассивная проверка уязвимостей (nuclei, с выбором шаблонов)
- Хранение данных в MongoDB
- Сбор email-адресов (EmailHarvester)
- Пассивное сканирование портов (naabu, nmap)
- Получение ASN-информации (asnmap)
- Проверка утечек (leakix.net)
- Интеграция с OSINT-источниками (VirusTotal, crt.sh и др.)
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
3. Настройте файл `.env` для подключения к MongoDB:
   ```env
   MONGO_URI=mongodb://localhost:27017/
   MONGO_DB=recon
   MONGO_COLLECTION=subdomains
   ```
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

## Запуск через Docker Compose

1. Соберите контейнеры:
   ```powershell
   docker-compose build
   ```
2. Запустите MongoDB и фреймворк:
   ```powershell
   docker-compose run --rm recon python3 recon.py --target example.com --subdomains --report-format md
   ```
   Все результаты и отчеты будут доступны в вашей рабочей папке.

3. Для запуска с HTML-отчетом:
   ```powershell
   docker-compose run --rm recon python3 recon.py --target example.com --subdomains --report-format html
   ```

4. Для интерактивной работы с MongoDB:
   - MongoDB будет доступна на порту 27017 (можно подключаться с хоста)

## Примечания
- Все зависимости и инструменты устанавливаются автоматически.
- Работает одинаково на Windows, Linux, MacOS (требуется Docker Desktop).
- Для использования дополнительных CLI-инструментов (например, EmailHarvester) их нужно добавить в Dockerfile.

## Дорожная карта
- Модульная CLI
- Поиск активов (ASN, email, leaks, etc.)
- Пассивное сканирование портов
- Проверка уязвимостей
- Оповещения и отчёты
- Интеграция с новыми OSINT-источниками (Censys, Shodan, SecurityTrails и др.)
