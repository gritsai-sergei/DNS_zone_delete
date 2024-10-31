import re
import requests


url = "http://testbn.byit.by/belgie.by/lists_access_xml-3f4eedda26401346653f54757c044b243490a500d"
exceptions_file = "exceptions.txt"

IP_ADDRESS = '212.98.160.60'


try:
    # Отправка запроса GET на URL
    response = requests.get(url)

    # Проверка успешности запроса
    response.raise_for_status()  # Проверка на успешный статус

    # Содержимое XML в памяти
    xml_content = response.text

    # Извлечение всех значений DNS и URL
    dns_list = re.findall(r'<dns>(.*?)</dns>', xml_content)
    url_list = re.findall(r'<url>(.*?)</url>', xml_content)

    # Регулярное выражение для разрешенных символов (латиница, кириллица, точки, тире)
    allowed_pattern = r'[0-9a-zA-Zа-яА-ЯёЁ.-]'

    filtered_dns_list = []
    formatted_list = []
    domains_set = set()

    for dns in dns_list:
        if re.findall(allowed_pattern, dns):
            if dns != '-' and not dns.startswith('-'):
                cleaned_dns = dns.replace('*.', '')  # Удаление символа "*"
                filtered_dns_list.append(cleaned_dns)

    for urlx in url_list:
        parts = urlx.split("/")
        if len(parts) > 2:
            domain = parts[2].split(';')[0]
            domain = domain.split(' ')[0]
            domains_set.add(domain)  # Добавляем в множество (дубликаты автоматически исключаются)

    unique_domains = list(domains_set)

    # Объединение двух списков
    combined_list = filtered_dns_list + unique_domains

    # Загрузка исключений из файла
    with open(exceptions_file, 'r', encoding='utf-8') as f:
        exceptions = f.read().splitlines()

    # Удаление строк, которые присутствуют в исключениях
    final_list = filtered_dns_list + unique_domains
    final_list = [item for item in final_list if item not in exceptions]

    # Вывод всех отфильтрованных и очищенных записей
    for item in final_list:
        print(item)

    print(f"\nКоличество строк в результате: {len(final_list)}")
    print(f"\nКоличество строк в filtered_dns_list: {len(filtered_dns_list)}")
    print(f"\nКоличество строк в unique_domains: {len(unique_domains)}")
    print(f"\nКоличество строк в combined_list: {len(combined_list)}")

    # Создание итогового списка в формате "domain A IP_ADDRESS"
    formatted_list = [f"{domain} A {IP_ADDRESS}" for domain in final_list if domain.strip()]

    # Запись в файл
    with open('result.txt', 'w', encoding='utf-8') as file:
         for entry in formatted_list:
             file.write(f"{entry}\n")

except requests.exceptions.RequestException as e:
    print(f"Ошибка при загрузке файла: {e}")
except Exception as e:
    print(f"Произошла ошибка: {e}")
