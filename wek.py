import csv
import re
import idna
import sys

csv.field_size_limit(10_000_000)

# Путь к исходному и результирующему файлам
input_file = 'dump.csv'
output_file = 'out.txt'

# Функция для обработки строк
def process_line(line):
    # Регулярное выражение для фильтрации строк
    pattern = re.compile(r'^[а-яА-Яa-zA-Z0-9\-\_\.\*]*+$')
    
    # Пропускаем пустые строки и строки с обратным слешем
    if not line or '\\' in line:
        return None
    
    # Проверка строки на соответствие шаблону
    if not pattern.match(line):
        return None
    
    # Замена `*.` на пустую строку и удаление точки в конце строки
    line = line.replace('*.', '').rstrip('.')
    
    return line

# Чтение CSV файла и обработка строк
with open(input_file, mode='r', encoding='cp1251') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    unique_lines = set()
    
    for row in reader:
        if len(row) > 1:  # Проверяем, есть ли второй столбец
            processed_line = process_line(row[1])
            if processed_line and 'bеllonа' not in processed_line:
                unique_lines.add(processed_line)

# Сортировка и запись в файл с преобразованием в Punycode
with open(output_file, mode='w', encoding='utf-8') as outfile:
    for line in sorted(unique_lines):
        try:
            punycode_line = idna.encode(line).decode('utf-8')
            outfile.write(punycode_line + '\n')
        except idna.IDNAError:
            continue
