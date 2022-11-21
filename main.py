from bs4 import BeautifulSoup
from time import sleep
import itertools
import requests
import re
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

base_url = "https://www.pkobp.pl/centrum-analiz"
parts = [
        "analizy-makroekonomiczne",
        "gielda",
        "waluty-i-stopy-procentowe",
        "analizy-sektorowe",
        "nieruchomosci",
        "rynki-zagraniczne",
        "fundusze-inwestycyjne"]

current_path = os.getcwd()

for part in parts:
    html = requests.get(f"{base_url}/{part}").text
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup.find('ul', class_="pagination")
    tmp = list(pagination.children)
    last_page = list(tmp[-2].children)[0].text
    print(f"\n====== Sekcja {part} ({last_page}) ======\n")
    for page in range(1, int(last_page)):
        full_url = f"{base_url}/{part}/?page={page}"
        print(f"\n____ Page {page}/{last_page} ____\n")

        html = requests.get(full_url).text

        soup = BeautifulSoup(html, "html.parser")

        links = soup.find_all('a', class_="news__main-link")
        titles = soup.find_all('h3', class_="news__title")
        dates = soup.find_all('div', class_="news__date")

        j = 0
        for link in links:
            pdf_url = link.get('href')
            title = titles[j].text
            date = dates[j].text.strip()
            print(f'{j+1}. {title} - {date}')

            pdf = requests.get(pdf_url)

            filename = title.lower().replace(' ', '_').replace(':', '').replace('.', '').replace(',', '').replace('"', '').replace('\'', '').replace('?', '').replace('\\', '').replace('//', '')

            f_name = f"{filename}_{date}.pdf"
            dir_path = f"{part}"
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            with open(f"{dir_path}/{f_name}", 'wb') as f:
                f.write(pdf.content)

            j += 1
            sleep(2)
