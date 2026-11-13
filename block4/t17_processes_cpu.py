"""
Задача 4.2. Тяжёлый расчёт на всех ядрах

Ситуация: для каждого документа считается контрольная сумма текста, и это
долго - работа процессора, а не ожидание сети. Коллега попробовал потоки -
быстрее не стало. Потом переписал на процессы, но код падает с ошибкой.

Что сделать:
1) Запустить: python -m block4.t17_processes_cpu - увидеть ошибку и понять
   её причину.
2) Исправить fingerprints так, чтобы работало на процессах.
3) В блоке __main__ замерить три варианта: в цикле, на потоках, на процессах.
   Объяснить разницу в цифрах.

На собесе: "Когда потоки, а когда процессы? Почему потоки не ускоряют расчёты?
Что такое pickle и почему лямбду нельзя передать в другой процесс?"
"""

import hashlib
from concurrent.futures import ProcessPoolExecutor


def heavy_hash(text, rounds=20000):
    data = text.encode()
    for _ in range(rounds):
        data = hashlib.sha256(data).digest()
    return data.hex()


def fingerprints(texts, rounds=20000):
    with ProcessPoolExecutor() as pool:
        return list(pool.map(lambda t: heavy_hash(t, rounds), texts))


if __name__ == "__main__":
    import time

    docs = [f"документ {i}" for i in range(16)]
    start = time.perf_counter()
    fingerprints(docs, rounds=200000)
    print(f"процессы: {time.perf_counter() - start:.2f} сек")
