"""
Задача 2.1. Импорт большого CSV

Ситуация: каждую ночь приходит выгрузка товаров в CSV на несколько гигабайт.
Прошлая версия импорта читала файл целиком в список и падала по памяти.

Что сделать:
1) read_rows(path) - генератор. Отдаёт строки по одной как dict (ключи из
   заголовка), значения без пробелов по краям, пустые строки файла пропускает.
   Разделитель - ";" (так выгружает русский Excel). Кодировка - utf-8-sig.
2) batched(iterable, size) - генератор, отдаёт списки по size элементов,
   последний может быть короче. Должен работать с генератором, у которого
   нет len().
3) import_file(path, save_batch, size=1000) - читает файл и передаёт строки
   в save_batch пачками. Возвращает число импортированных строк.

На собесе: "Чем генератор отличается от списка? Что такое yield? Как
обработать файл, который не помещается в память?"
"""

def read_rows(path):
    with open(path, encoding="utf-8-sig") as f:
        keys = []
        for line in f:
            clean_line = line.strip()
            if not clean_line: continue
            keys = [key.strip() for key in clean_line.split(";")]
            break
        for line in f:
            clean_line = line.strip()
            if not clean_line: continue
            values = [value.strip() for value in clean_line.split(";")]
            row = dict(zip(keys, values))
            yield row

def batched(iterable, size):
    lists = []
    for item in iterable:
        lists.append(item) 
        if len(lists) == size:
            yield lists
            lists = []
    if lists:
        yield lists
        lists = []

def import_file(path, save_batch, size=1000):
    rows = read_rows(path)
    batched_rows = batched(rows, size)
    count = 0
    for row in batched_rows:
        save_batch(row)
        count += len(row)
    return count