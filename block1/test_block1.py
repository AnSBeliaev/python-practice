from decimal import Decimal

from block1.t01_default_args import build_tags
from block1.t02_config_copy import DEFAULT_CONFIG, build_config
from block1.t03_dedupe import unique_emails
from block1.t04_grouping import summarize, top_customers
from block1.t05_sync_ids import plan_sync
from block1.t06_kwargs import build_url
from block1.t07_is_vs_eq import find_user, is_paid


def test_01_tags_do_not_leak_between_calls():
    assert build_tags("web") == ["source:web"]
    assert build_tags("mobile") == ["source:mobile"]
    assert build_tags("api", ["vip"]) == ["vip", "source:api"]


def test_02_defaults_stay_untouched():
    prod = build_config({"db": {"host": "prod-db"}, "features": ["ai"], "debug": True})
    assert prod["db"] == {"host": "prod-db", "port": 5432}
    assert prod["features"] == ["search", "ai"]
    stage = build_config({})
    assert stage["db"]["host"] == "localhost"
    assert stage["features"] == ["search"]
    assert DEFAULT_CONFIG == {
        "db": {"host": "localhost", "port": 5432},
        "features": ["search"],
        "debug": False,
    }


def test_03_unique_emails():
    users = [
        {"email": " Anna@Mail.ru"},
        {"email": "petr@mail.ru"},
        {"email": None},
        {"email": "anna@mail.ru "},
        {"email": ""},
        {"email": "PETR@MAIL.RU"},
        {"email": "ivan@mail.ru"},
    ]
    assert unique_emails(users) == ["anna@mail.ru", "petr@mail.ru", "ivan@mail.ru"]


def test_03_unique_emails_is_fast():
    users = [{"email": f"user{i % 50000}@mail.ru"} for i in range(200000)]
    assert len(unique_emails(users)) == 50000


ORDERS = [
    {"customer_id": 1, "city": "Ростов", "status": "paid", "amount": "100.10"},
    {"customer_id": 2, "city": "Ростов", "status": "paid", "amount": "0.20"},
    {"customer_id": 1, "city": "Ростов", "status": "new", "amount": "50.00"},
    {"customer_id": 3, "city": "Москва", "status": "paid", "amount": "300.00"},
    {"customer_id": 2, "city": "Ростов", "status": "paid", "amount": "0.10"},
]


def test_04_summarize():
    result = summarize(ORDERS)
    assert result[("Ростов", "paid")] == {"count": 3, "total": Decimal("100.40")}
    assert result[("Ростов", "new")] == {"count": 1, "total": Decimal("50.00")}
    assert result[("Москва", "paid")] == {"count": 1, "total": Decimal("300.00")}
    assert len(result) == 3
    assert all(isinstance(v["total"], Decimal) for v in result.values())


def test_04_top_customers():
    assert top_customers(ORDERS, 2) == [(3, Decimal("300.00")), (1, Decimal("100.10"))]


def test_05_plan_sync():
    plan = plan_sync([1, 2, 3, 3, 4], [3, 4, 5, 6, 6])
    assert plan == {"to_create": [5, 6], "to_delete": [1, 2], "unchanged": [3, 4]}


def test_05_plan_sync_empty():
    assert plan_sync([], [1]) == {"to_create": [1], "to_delete": [], "unchanged": []}


def test_06_build_url():
    url = build_url("https://api.shop.ru/", "/orders", status="paid", page=2, city=None)
    assert url == "https://api.shop.ru/orders?status=paid&page=2"


def test_06_build_url_bool_and_list():
    url = build_url("https://api.shop.ru", "orders", active=True, tags=["a", "b"])
    assert url == "https://api.shop.ru/orders?active=true&tags=a&tags=b"


def test_06_build_url_without_params():
    assert build_url("https://api.shop.ru", "/ping") == "https://api.shop.ru/ping"


def test_06_build_url_from_dict():
    filters = {"status": "new", "limit": 10}
    assert build_url("https://api.shop.ru", "/orders", **filters) == (
        "https://api.shop.ru/orders?status=new&limit=10"
    )


def test_07_is_paid_with_status_from_json():
    status = "".join(["pa", "id"])
    assert is_paid({"status": status}) is True
    assert is_paid({"status": "new"}) is False


def test_07_find_user_with_big_ids():
    users = [{"id": int("1000"), "name": "Анна"}, {"id": int("1001"), "name": "Пётр"}]
    assert find_user(users, int("1001"))["name"] == "Пётр"
    assert find_user(users, 5) is None
