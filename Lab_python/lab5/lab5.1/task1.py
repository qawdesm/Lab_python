import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import argparse
from urllib.parse import quote
import re
import shutil

class CountryDataParser:
    def __init__(self, cache_dir="cache"):
        self.session = requests.Session()
        
        self.cache_dir = cache_dir
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    
    def clear_cache(self):
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
            os.makedirs(self.cache_dir)
            print("Кэш очищен")        


    def get_page_content(self, country_name):
        country_name = country_name.strip()
        country_name = re.sub(r'[^\x00-\x7F]+', '', country_name)
        country_name = country_name.replace('\ufeff', '').replace('\u200b', '')
        
        if not country_name:
            return None
            
        cache_file = os.path.join(self.cache_dir, f"{country_name.replace(' ', '_').replace('/', '_')}.html")
        
        if os.path.exists(cache_file):
            print(f"  Используется кэш для {country_name}")
            with open(cache_file, 'r', encoding='utf-8') as f:
                return f.read()
        
        encoded_name = quote(country_name.replace(' ', '_'))
        url = f"https://en.wikipedia.org/wiki/{encoded_name}"
        
        print(f"  Загрузка: {url}")
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            return response.text
            
        except requests.RequestException as e:
            print(f"  Ошибка при загрузке страницы для '{country_name}': {e}")
            return None

    def clean_number(self, number_str):
        if not number_str:
            return ""
        
        cleaned = re.sub(r'[^\d]', '', str(number_str))
        
        return cleaned if cleaned else ""

    def parse_population(self, infobox):
        for row in infobox.find_all('tr'):
            th = row.find('th')
            if th:
                th_text = th.get_text().strip().lower()
                if 'population' in th_text:
                    td = row.find('td')
                    if td:
                        text = td.get_text()
                        numbers = re.findall(r'\d{1,3}(?:,\d{3}){2,}', text)
                        if numbers:
                            max_number = max(numbers, key=lambda x: len(x.replace(',', '')))
                            population = self.clean_number(max_number)
                            if len(population) >= 7:
                                print(f"    Население найдено (основной способ): {population}")
                                return population

        for row in infobox.find_all('tr'):
            th = row.find('th')
            td = row.find('td')
            if th and td:
                th_text = th.get_text().strip().lower()
                td_text = td.get_text()
                if any(word in th_text for word in ['estimate', 'census']) and any(year in td_text for year in ['2020', '2021', '2022', '2023', '2024']):
                    numbers = re.findall(r'\d{1,3}(?:,\d{3}){2,}', td_text)
                    if numbers:
                        max_number = max(numbers, key=lambda x: len(x.replace(',', '')))
                        population = self.clean_number(max_number)
                        if len(population) >= 7:
                            print(f"    Население найдено (estimate): {population}")
                            return population

        demo_header = infobox.find('th', string=re.compile('.*Demographics.*', re.IGNORECASE))
        if demo_header:
            demo_section = demo_header.find_parent('tr').find_next_siblings('tr')
            for row in demo_section[:5]:
                td = row.find('td')
                if td:
                    text = td.get_text()
                    numbers = re.findall(r'\d{1,3}(?:,\d{3}){2,}', text)
                    if numbers:
                        max_number = max(numbers, key=lambda x: len(x.replace(',', '')))
                        population = self.clean_number(max_number)
                        if len(population) >= 7:
                            print(f"    Население найдено (demographics): {population}")
                            return population

        largest_number = ""
        for td in infobox.find_all('td'):
            text = td.get_text()
            numbers = re.findall(r'\d{1,3}(?:,\d{3}){2,}', text)
            for num in numbers:
                cleaned_num = self.clean_number(num)
                if len(cleaned_num) >= 7 and len(cleaned_num) > len(largest_number):
                    largest_number = cleaned_num
        
        if largest_number:
            print(f"    Население найдено (самое большое число): {largest_number}")
            return largest_number

        return ""

    def parse_country_data(self, country_name):
        """Парсит данные о стране с Википедии"""
        country_name = country_name.strip()
        country_name = re.sub(r'[^\x00-\x7F]+', '', country_name)
        country_name = country_name.replace('\ufeff', '').replace('\u200b', '')
        
        html_content = self.get_page_content(country_name)
        if not html_content:
            return None
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        infobox = soup.find('table', {'class': re.compile('infobox.*')})
        if not infobox:
            print(f"  Не найдена информационная таблица для {country_name}")
            return None
        
        data = {'country': country_name, 'capital': '', 'area': '', 'population': ''}
        
        try:
            for row in infobox.find_all('tr'):
                th = row.find('th')
                if th:
                    th_text = th.get_text().strip().lower()
                    if 'capital' in th_text:
                        td = row.find('td')
                        if td:
                            capital_link = td.find('a')
                            if capital_link:
                                data['capital'] = capital_link.get_text().strip()
                                break

            for row in infobox.find_all('tr'):
                th = row.find('th')
                if th:
                    th_text = th.get_text().strip().lower()
                    if 'area' in th_text or 'total' in th_text:
                        td = row.find('td')
                        if td:
                            area_text = td.get_text()
                            area_match = re.search(r'(\d[\d,.]*)\s*(?:km|sq)', area_text)
                            if area_match:
                                data['area'] = self.clean_number(area_match.group(1))
                                break

            print("    Поиск населения...")
            data['population'] = self.parse_population(infobox)
                    
        except Exception as e:
            print(f"  Ошибка при парсинге данных для '{country_name}': {e}")
            return None
        
        return data

    def process_countries(self, input_file, output_file, clear_cache=False):
        if clear_cache:
            self.clear_cache()
            
        countries = []
        try:
            encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(input_file, 'r', encoding=encoding) as f:
                        countries = [line.strip() for line in f if line.strip()]
                    if countries:
                        print(f"Файл прочитан с кодировкой: {encoding}")
                        break
                except UnicodeDecodeError:
                    continue
                    
            if not countries:
                print(f"Не удалось прочитать файл {input_file} с доступными кодировками")
                return
                
        except FileNotFoundError:
            print(f"Файл {input_file} не найден")
            return
        except Exception as e:
            print(f"Ошибка при чтении файла {input_file}: {e}")
            return
        
        cleaned_countries = []
        for country in countries:
            cleaned = country.strip()
            cleaned = re.sub(r'[^\x00-\x7F]+', '', cleaned)
            cleaned = cleaned.replace('\ufeff', '').replace('\u200b', '')
            if cleaned:
                cleaned_countries.append(cleaned)
        
        countries = cleaned_countries
        
        if not countries:
            print("Файл со странами пуст или содержит только недопустимые символы")
            return
        
        print(f"Найдено стран для обработки: {len(countries)}")
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['country', 'capital', 'area', 'population'])
                writer.writeheader()
                
                success_count = 0
                
                for i, country in enumerate(countries, 1):
                    print(f"\n[{i}/{len(countries)}] Обрабатывается: '{country}'")
                    
                    data = self.parse_country_data(country)
                    
                    if data:
                        writer.writerow(data)
                        success_count += 1
                        print(f"  Результат:")
                        print(f"     Столица: {data['capital']}")
                        print(f"     Площадь: {data['area']}")
                        print(f"     Население: {data['population']}")
                    else:
                        writer.writerow({'country': country, 'capital': '', 'area': '', 'population': ''})
                        print(f"Не удалось получить данные")
                    
                    if i < len(countries):
                        time.sleep(1.5)
                
                print(f"ОБРАБОТКА ЗАВЕРШЕНА!")
                print(f"Успешно обработано: {success_count} из {len(countries)} стран")
                print(f"Итоговый файл: {output_file}")
                
        except Exception as e:
            print(f"Ошибка при записи в CSV файл: {e}")

def main():
    parser = argparse.ArgumentParser(description='Парсер данных о странах с Википедии')
    parser.add_argument('--input', '-i', default='countries.txt', 
                       help='Входной файл со списком стран (по умолчанию: countries.txt)')
    parser.add_argument('--output', '-o', default='countries_data.csv',
                       help='Выходной CSV файл (по умолчанию: countries_data.csv)')
    parser.add_argument('--clear-cache', action='store_true',
                       help='Очистить кэш перед запуском')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Файл {args.input} не найден!")
        return
    
    parser = CountryDataParser()
    parser.process_countries(args.input, args.output, clear_cache=args.clear_cache)

if __name__ == "__main__":
    main()