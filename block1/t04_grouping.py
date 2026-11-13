"""
Задача 1.4. Отчёт по заказам

Ситуация: из API приходит список заказов. Суммы приходят строками, как это часто
бывает в JSON: {"customer_id": 7, "city": "Ростов", "status": "paid", "amount": "199.90"}.

Что сделать:
1) summarize(orders) - словарь, где ключ - пара (city, status), значение -
   {"count": число заказов, "total": сумма}. Сумма - Decimal, не float.
2) top_customers(orders, n) - n пар (customer_id, сумма) по убыванию суммы,
   считаются только заказы со статусом "paid".

На собесе: "Почему деньги не считают во float? Почему ключом dict может быть
tuple, а list - нет?"
"""


def summarize(orders):
    raise NotImplementedError


def top_customers(orders, n):
    raise NotImplementedError
