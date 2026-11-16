from decimal import Decimal
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
    final_orders = {}
    for order in orders:
        key = (order["city"], order["status"])
        if key in final_orders:
            final_orders_cell = final_orders[key]
            final_orders_cell["count"] += 1
            final_orders_cell["total"] += Decimal(order["amount"])
        if (order["city"], order["status"]) not in final_orders:
            final_orders[key] = {"count": 1, "total": Decimal(order["amount"])}
    return final_orders

def top_customers(orders, n):
    final_dict = {}
    final_list = []

    for order in orders:
        key = order["customer_id"]
        if order["status"] != "paid": continue
            
        if key in final_dict:
            final_dict[key] += Decimal(order["amount"])
        else:
            final_dict[key] = Decimal(order["amount"])
    final_list = final_dict.items()

    sorted_final_list = sorted(final_list, key=lambda order_info: order_info[1], reverse=True)
    return sorted_final_list[:n]