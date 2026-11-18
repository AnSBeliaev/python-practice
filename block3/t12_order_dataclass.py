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
from dataclasses import dataclass, field
from decimal import Decimal

@dataclass(order=True)
class OrderItem:
    sku: str = field(compare=False)
    price: Decimal
    qty: int

    def __post_init__(self):
      if self.price < 0:
         raise ValueError("Цена не может быть отрицательной")
      if self.qty <= 0:
         raise ValueError("Количество должно быть больше нуля")

@dataclass
class Order:
    id: int
    items: list[OrderItem] = field(default_factory=list)
    
    @property
    def total(self) -> Decimal:
      return sum((item.price * item.qty for item in self.items), Decimal("0"))

    def add_item(self, item):
      self.items.append(item)

    @classmethod
    def from_dict(cls, data):
      id = data["id"]
      order_items = [OrderItem(sku=order_item["sku"], price=Decimal(order_item["price"]), qty=order_item["qty"]) for order_item in data.get("items", [])]
      return cls(id=id, items=order_items)

    def to_dict(self):
      items = [{"sku": item.sku, "price": str(item.price), "qty": item.qty} for item in self.items]
      id = self.id
      return {
         "id": id,
         "items": items
      }