import asyncio
import threading
import time

from block4.t16_threads_io import check_links
from block4.t17_processes_cpu import fingerprints, heavy_hash
from block4.t18_async_limit import embed_all
from block4.t19_async_blocking import enrich
from block4.t20_async_timeout import get_prices
from block4.t21_race_condition import Account


def test_16_check_links_parallel_and_ordered():
    def check(url):
        time.sleep(0.2)
        if "broken" in url:
            raise ConnectionError(url)
        return f"ok:{url}"

    urls = [f"https://site{i}.ru" for i in range(9)] + ["https://broken.ru"]
    start = time.perf_counter()
    results = check_links(urls, check, max_workers=10)
    elapsed = time.perf_counter() - start
    assert elapsed < 0.8
    assert results[:9] == [f"ok:{u}" for u in urls[:9]]
    assert isinstance(results[9], ConnectionError)


def test_17_fingerprints_on_processes():
    texts = ["a", "b", "c"]
    assert fingerprints(texts, rounds=100) == [heavy_hash(t, 100) for t in texts]


def test_18_embed_all_respects_limit():
    state = {"now": 0, "max": 0}

    async def embed(text):
        state["now"] += 1
        state["max"] = max(state["max"], state["now"])
        await asyncio.sleep(0.05)
        state["now"] -= 1
        return [len(text)]

    texts = ["a" * i for i in range(1, 21)]
    start = time.perf_counter()
    result = asyncio.run(embed_all(texts, embed, limit=5))
    elapsed = time.perf_counter() - start
    assert result == [[i] for i in range(1, 21)]
    assert state["max"] == 5
    assert elapsed < 0.5


def test_19_enrich_runs_in_parallel():
    start = time.perf_counter()
    result = asyncio.run(enrich([1, 2, 3, 4, 5]))
    elapsed = time.perf_counter() - start
    assert [r["id"] for r in result] == [1, 2, 3, 4, 5]
    assert elapsed < 0.6


def test_20_get_prices():
    async def fast():
        await asyncio.sleep(0.05)
        return 100

    async def slow():
        await asyncio.sleep(5)
        return 90

    async def broken():
        raise ConnectionError("поставщик недоступен")

    start = time.perf_counter()
    prices = asyncio.run(get_prices({"fast": fast, "slow": slow, "broken": broken}, timeout=0.3))
    elapsed = time.perf_counter() - start
    assert prices == {"fast": 100, "slow": None, "broken": None}
    assert elapsed < 1


def test_21_no_negative_balance():
    account = Account(100)
    results = []

    def worker():
        results.append(account.withdraw(10))

    threads = [threading.Thread(target=worker) for _ in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert account.balance == 0
    assert results.count(True) == 10
