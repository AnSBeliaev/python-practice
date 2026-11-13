"""
Задача 1.6. Адрес запроса к внешнему API

Ситуация: в коде много вызовов вида
build_url("https://api.shop.ru", "/orders", status="paid", page=2, city=None).
Параметры передаются как попало, кто-то передаёт None, кто-то True, кто-то список.

Что сделать: собрать адрес.
- параметры со значением None не попадают в адрес
- True / False превращаются в "true" / "false"
- список превращается в повторяющийся параметр: tags=["a", "b"] -> tags=a&tags=b
- между base и path ровно один слэш
- без параметров - без знака "?"
Подсказка: urllib.parse.urlencode.

На собесе: "Что такое *args и **kwargs? Как передать словарь в функцию как
именованные аргументы?"
"""


def build_url(base, path, **params):
    raise NotImplementedError
