import pandas as pd
import hashlib
import time

# Загрузка Excel-файла
df = pd.read_excel("Ваш_файл_с_данными.xlsx")

# Список колонок, которые объединяем
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

# Функция преобразования строки
def combine_row(row):
    parts = []
    for col in columns:
        value = row[col]
        if pd.notna(value):
            # Преобразуем float вида 1.0 → 1 (без .0)
            if isinstance(value, float) and value.is_integer():
                value = int(value)
            parts.append(f"{col}:{value}")
    return "|".join(parts)

# Применение к каждой строке
df["Объединённые данные"] = df.apply(combine_row, axis=1)

# Генерация безопасного имени с хэшем (на основе времени)
timestamp = str(time.time()).encode("utf-8")
hash_suffix = hashlib.md5(timestamp).hexdigest()[:8]
filename = f"обработанный_файл_{hash_suffix}.xlsx"

# Сохранение результата
df[["Объединённые данные"]].to_excel(filename, index=False)
