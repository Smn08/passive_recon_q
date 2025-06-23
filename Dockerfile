FROM kalilinux/kali-rolling:latest

# Установка системных зависимостей и инструментов
RUN apt-get update && \
    apt-get install -y python3 python3-pip git curl nmap && \
    apt-get install -y golang && \
    go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && \
    go install github.com/projectdiscovery/httpx/cmd/httpx@latest && \
    go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest && \
    go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest && \
    go install github.com/projectdiscovery/asnmap/cmd/asnmap@latest && \
    ln -s /root/go/bin/subfinder /usr/local/bin/subfinder && \
    ln -s /root/go/bin/httpx /usr/local/bin/httpx && \
    ln -s /root/go/bin/nuclei /usr/local/bin/nuclei && \
    ln -s /root/go/bin/naabu /usr/local/bin/naabu && \
    ln -s /root/go/bin/asnmap /usr/local/bin/asnmap

# Копируем проект
WORKDIR /app
COPY . /app

# Установка Python-зависимостей
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "recon.py", "--help"]
