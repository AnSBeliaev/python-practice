"""
Задача 2.4. Транзакция и замер времени

Ситуация: в коде импорта десятки мест с ручным commit / rollback, и в паре мест
rollback забыли - в базе остаются половинчатые данные.

Что сделать:
1) transaction(conn) - контекстный менеджер для sqlite3-соединения.
   Успешный выход - commit. Исключение внутри блока - rollback, и исключение
   пробрасывается дальше (не глушить!).
       with transaction(conn):
           conn.execute("INSERT ...")
2) Timer - контекстный менеджер-класс. После выхода из блока в t.elapsed
   лежит время выполнения в секундах (float). Время меряется и при исключении.
       with Timer() as t:
           heavy_work()
       print(t.elapsed)

Можно сделать через contextlib.contextmanager или через __enter__ / __exit__ -
попробовать оба способа.

На собесе: "Что делает with? Какие методы нужны для контекстного менеджера?
Что будет, если __exit__ вернёт True?"
"""
from contextlib import contextmanager
import time

@contextmanager
def transaction(conn):
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
        
class Timer:
    def __init__(self):
        self.elapsed = 0.0

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start