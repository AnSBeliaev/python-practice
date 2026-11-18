"""
Задача 2.3. Повтор запроса к нестабильному сервису

Ситуация: сервис эмбеддингов иногда отвечает ошибкой сети. Повторы сейчас
написаны руками в каждом месте вызова через while и try. Нужен один декоратор.

Что сделать: retry(times, exceptions, delay, backoff, sleep)
- вызывает функцию до times раз
- повторяет только при исключениях из exceptions, остальные пробрасывает сразу
- между попытками ждёт delay, delay * backoff, delay * backoff^2 ...
- после последней неудачи пробрасывает последнее исключение
- функция после декоратора сохраняет своё имя и docstring
- sleep передаётся параметром, чтобы тесты не ждали по-настоящему

Использование:
    @retry(times=3, exceptions=(ConnectionError,), delay=1)
    def get_embedding(text): ...

На собесе: "Что такое декоратор? Как написать декоратор с параметрами?
Зачем functools.wraps?"
"""

import time
from functools import wraps

def retry(times=3, exceptions=(Exception,), delay=0.0, backoff=2.0, sleep=time.sleep):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times - 1:
                        raise
                    else:
                        sleep(delay * (backoff ** attempt))
        return wrapper
    return decorator