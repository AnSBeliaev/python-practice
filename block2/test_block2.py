import inspect
import sqlite3
import time

import pytest

from block2.t08_csv_import import batched, import_file, read_rows
from block2.t09_pagination import iter_items
from block2.t10_retry import retry
from block2.t11_context_managers import Timer, transaction

CSV_TEXT = "﻿sku;name;price\nA1; Чайник ;1990\n\nB2;Кружка; 350 \nC3;Ложка;90\n"


@pytest.fixture
def csv_file(tmp_path):
    path = tmp_path / "goods.csv"
    path.write_text(CSV_TEXT, encoding="utf-8")
    return path


def test_08_read_rows_is_generator(csv_file):
    assert inspect.isgenerator(read_rows(csv_file))


def test_08_read_rows_values(csv_file):
    rows = list(read_rows(csv_file))
    assert rows == [
        {"sku": "A1", "name": "Чайник", "price": "1990"},
        {"sku": "B2", "name": "Кружка", "price": "350"},
        {"sku": "C3", "name": "Ложка", "price": "90"},
    ]


def test_08_batched():
    assert list(batched(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert list(batched((x for x in range(4)), 2)) == [[0, 1], [2, 3]]
    assert list(batched([], 3)) == []
    assert inspect.isgenerator(batched(range(3), 2))


def test_08_import_file(csv_file):
    saved = []
    count = import_file(csv_file, saved.append, size=2)
    assert count == 3
    assert [len(b) for b in saved] == [2, 1]


def make_api(pages):
    calls = []

    def fetch_page(cursor):
        calls.append(cursor)
        return pages[cursor]

    return fetch_page, calls


PAGES = {
    None: {"items": [1, 2, 3], "next": "p2"},
    "p2": {"items": [4, 5], "next": "p3"},
    "p3": {"items": [], "next": "p4"},
    "p4": {"items": [6], "next": None},
}


def test_09_iter_items_all():
    fetch_page, calls = make_api(PAGES)
    assert list(iter_items(fetch_page)) == [1, 2, 3, 4, 5, 6]
    assert calls == [None, "p2", "p3", "p4"]


def test_09_iter_items_is_lazy():
    fetch_page, calls = make_api(PAGES)
    items = iter_items(fetch_page)
    assert calls == []
    first = [next(items) for _ in range(3)]
    assert first == [1, 2, 3]
    assert calls == [None]


def test_10_retry_succeeds_after_failures():
    pauses = []
    attempts = []

    @retry(times=3, exceptions=(ConnectionError,), delay=1, backoff=2, sleep=pauses.append)
    def get_embedding(text):
        """Получить вектор текста."""
        attempts.append(text)
        if len(attempts) < 3:
            raise ConnectionError("timeout")
        return [0.1, 0.2]

    assert get_embedding("абзац") == [0.1, 0.2]
    assert len(attempts) == 3
    assert pauses == [1, 2]
    assert get_embedding.__name__ == "get_embedding"
    assert get_embedding.__doc__ == "Получить вектор текста."


def test_10_retry_gives_up():
    attempts = []

    @retry(times=2, exceptions=(ConnectionError,), sleep=lambda s: None)
    def always_fails():
        attempts.append(1)
        raise ConnectionError("down")

    with pytest.raises(ConnectionError):
        always_fails()
    assert len(attempts) == 2


def test_10_retry_does_not_retry_other_errors():
    attempts = []

    @retry(times=5, exceptions=(ConnectionError,), sleep=lambda s: None)
    def bad_input():
        attempts.append(1)
        raise ValueError("пустой текст")

    with pytest.raises(ValueError):
        bad_input()
    assert len(attempts) == 1


@pytest.fixture
def conn():
    connection = sqlite3.connect(":memory:")
    connection.execute("CREATE TABLE goods (sku TEXT PRIMARY KEY, price INTEGER)")
    connection.commit()
    yield connection
    connection.close()


def test_11_transaction_commits(conn):
    with transaction(conn):
        conn.execute("INSERT INTO goods VALUES ('A1', 100)")
    other = conn.execute("SELECT count(*) FROM goods").fetchone()[0]
    assert other == 1
    assert not conn.in_transaction


def test_11_transaction_rolls_back_and_reraises(conn):
    with pytest.raises(sqlite3.IntegrityError):
        with transaction(conn):
            conn.execute("INSERT INTO goods VALUES ('A1', 100)")
            conn.execute("INSERT INTO goods VALUES ('A1', 200)")
    assert conn.execute("SELECT count(*) FROM goods").fetchone()[0] == 0


def test_11_timer():
    with Timer() as t:
        time.sleep(0.05)
    assert 0.04 < t.elapsed < 0.5


def test_11_timer_on_error():
    t = Timer()
    with pytest.raises(RuntimeError):
        with t:
            time.sleep(0.02)
            raise RuntimeError("упало")
    assert t.elapsed > 0.01
