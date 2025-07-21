import pandas as pd
import hashlib
import time

# Загрузка Excel-файла
df = pd.read_excel("Ваш_файл_с_данными.xlsx")

# Список колонок, которые нужно обработать
columns = [
    "Тип установки",
    "Высота",
    "Ширина",
    "Глубина",
    "Количество камер",
    "Количество дверей",
    "Общий объем",
    "Объем морозильной камеры",
    "Цвет",
    "Расположение морозильной камеры",
    "Объем холодильной камеры",
    "Класс энергопотребления",
    "Размораживание морозильной камеры",
    "Размораживание холодильной камеры",
    "Дисплей",
    "Генератор льда",
    "Зона свежести"
]

# Генерация HTML-таблицы как строки
def generate_html_table(row):
    html = ['<table class="description_table_style">']
    html.append('<tr><td>Атрибут</td><td>Значение</td></tr>')

    for col in columns:
        value = row[col]
        if pd.notna(value):
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            html.append(f'<tr><td>{col}</td><td>{value}</td></tr>')
    
    html.append('</table>')
    return "\n".join(html)

# Применение ко всем строкам
df["HTML"] = df.apply(generate_html_table, axis=1)

# Генерация безопасного имени с хэшем (на основе времени)
timestamp = str(time.time()).encode("utf-8")
hash_suffix = hashlib.md5(timestamp).hexdigest()[:8]
filename = f"обработанный_файл_{hash_suffix}.xlsx"

# Сохранение в новый Excel-файл
df[["HTML"]].to_excel(filename, index=False)
