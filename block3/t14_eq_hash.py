"""
Задача 3.3. Склейка каталогов из двух источников

Ситуация: товары приходят из двух систем. Один и тот же товар (одинаковый id)
может прийти из обеих, с разным названием. Нужен общий каталог без дублей.

Что сделать:
1) Product(id, name, price) - обычный класс. Два товара равны, если равны id.
   Товар можно положить в set и использовать как ключ dict.
   repr(product) -> "Product(id=1, name='Чайник')"
2) merge_catalogs(primary, secondary) - список без дублей. Если товар есть в
   обоих, берётся версия из primary. Порядок: сначала все из primary,
   затем новые из secondary.

На собесе: "Что будет, если переопределить __eq__ и не определить __hash__?
Почему изменяемый объект опасно класть в set?"
"""


class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price


def merge_catalogs(primary, secondary):
    raise NotImplementedError
