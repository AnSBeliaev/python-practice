"""
Задача 3.1. Модель заказа

Ситуация: заказы приходят из API в JSON. Сейчас по коду гуляют словари, и
ошибки вида order["itmes"] находятся только в проде. Нужна нормальная модель.

Что сделать (через dataclasses):
1) OrderItem: sku (str), price (Decimal), qty (int).
   При создании проверять: qty > 0, price >= 0, иначе ValueError.
2) Order: id (int), items (список OrderItem, по умолчанию пустой).
   - total - свойство (@property), сумма price * qty по позициям
   - add_item(item) - добавить позицию
   - from_dict(data) - classmethod, создаёт заказ из JSON-словаря:
     {"id": 1, "items": [{"sku": "A1", "price": "10.50", "qty": 2}]}
     Цена приходит строкой.
   - to_dict() - обратно в словарь, цена строкой

Ловушка: у двух разных заказов не должен оказаться общий список позиций.

На собесе: "Зачем dataclass? Что делает field(default_factory=list) и почему
нельзя написать items: list = []? Чем classmethod отличается от staticmethod?"
"""
