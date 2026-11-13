"""
Задача 4.4. Асинхронный код, который не стал быстрее

Ситуация: обработчик переписали на async и запускают проверки через gather,
но время не изменилось - 5 документов всё так же обрабатываются ~1 секунду.
Внутри вызывается старая синхронная функция legacy_lookup из библиотеки,
которую переписать нельзя.

Что сделать: исправить enrich так, чтобы проверки шли параллельно.
legacy_lookup не трогать.

На собесе: "Что будет, если внутри async-функции вызвать time.sleep или
обычный requests.get? Как вызвать синхронный код из асинхронного?"
"""

import asyncio
import time


def legacy_lookup(doc_id):
    time.sleep(0.2)
    return {"id": doc_id, "status": "ok"}


async def enrich_one(doc_id):
    return legacy_lookup(doc_id)


async def enrich(doc_ids):
    return await asyncio.gather(*(enrich_one(d) for d in doc_ids))
