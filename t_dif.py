import pandas as pd
from bs4 import BeautifulSoup

# Путь к исходному Excel-файлу
INPUT_FILE = 'product.xls'
OUTPUT_FILE = 'differentiate.xls'

# Загружаем файл
df = pd.read_excel(INPUT_FILE, engine='xlrd')

# Проверка, что нужные колонки существуют
if df.shape[1] < 2:
    raise ValueError("Ожидается как минимум две колонки: название товара и HTML-таблица.")

# Названия колонок
product_col = df.columns[0]
html_col = df.columns[1]

# Результирующий список строк (словарей)
processed_data = []

for idx, row in df.iterrows():
    product_name = row[product_col]
    html_content = row[html_col]

    # Парсим HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')
    row_data = {'Товар': product_name}

    if table:
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) >= 2:
                key = tds[0].get_text(strip=True)
                value = tds[1].get_text(strip=True)
                row_data[key] = value
    else:
        print(f"[!] Предупреждение: не найдена таблица для строки {idx + 1}")

    processed_data.append(row_data)

# Создаём финальный DataFrame
final_df = pd.DataFrame(processed_data)

# Сохраняем результат
final_df.to_excel(OUTPUT_FILE, index=False)
print(f"[✓] Обработано: {len(final_df)} строк. Сохранено в '{OUTPUT_FILE}'")
