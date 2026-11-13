from decimal import Decimal

import pytest

from block3 import t12_order_dataclass as m12
from block3 import t13_repository as m13
from block3.t14_eq_hash import Product, merge_catalogs
from block3.t15_mixins import BaseModel, Document, SoftDeleteMixin, TimestampMixin


def test_12_item_validation():
    with pytest.raises(ValueError):
        m12.OrderItem(sku="A1", price=Decimal("10"), qty=0)
    with pytest.raises(ValueError):
        m12.OrderItem(sku="A1", price=Decimal("-1"), qty=1)


def test_12_orders_do_not_share_items():
    a = m12.Order(id=1)
    b = m12.Order(id=2)
    a.add_item(m12.OrderItem(sku="A1", price=Decimal("10.50"), qty=2))
    assert b.items == []
    assert a.total == Decimal("21.00")
    assert b.total == 0


def test_12_from_dict_and_back():
    data = {
        "id": 7,
        "items": [
            {"sku": "A1", "price": "10.50", "qty": 2},
            {"sku": "B2", "price": "0.10", "qty": 3},
        ],
    }
    order = m12.Order.from_dict(data)
    assert isinstance(order, m12.Order)
    assert order.total == Decimal("21.30")
    assert isinstance(order.items[0].price, Decimal)
    assert order.to_dict() == data


def test_13_repository_is_abstract():
    with pytest.raises(TypeError):
        m13.UserRepository()


def test_13_service_register_and_deactivate():
    repo = m13.InMemoryUserRepository()
    service = m13.UserService(repo)
    anna = service.register("Anna@Mail.ru")
    petr = service.register("petr@mail.ru")
    assert (anna.id, petr.id) == (1, 2)
    assert anna.email == "anna@mail.ru"
    with pytest.raises(ValueError):
        service.register("ANNA@mail.ru")
    service.deactivate(1)
    assert [u.email for u in repo.list_active()] == ["petr@mail.ru"]
    with pytest.raises(KeyError):
        service.deactivate(99)


def test_13_repository_protocol():
    repo = m13.InMemoryUserRepository()
    repo.add(m13.User(id=5, email="a@b.ru"))
    assert len(repo) == 1
    assert 5 in repo
    assert 6 not in repo
    assert [u.id for u in repo] == [5]
    assert repo.get_by_email("a@b.ru").id == 5
    assert repo.get_by_email("x@b.ru") is None


def test_14_equality_and_hash():
    a = Product(1, "Чайник", 100)
    b = Product(1, "Чайник электрический", 120)
    assert a == b
    assert a != Product(2, "Чайник", 100)
    assert len({a, b}) == 1
    assert {a: "есть"}[b] == "есть"
    assert repr(a) == "Product(id=1, name='Чайник')"


def test_14_merge_catalogs():
    primary = [Product(1, "Чайник", 100), Product(2, "Кружка", 50)]
    secondary = [Product(2, "Кружка белая", 55), Product(3, "Ложка", 10), Product(3, "Ложка", 10)]
    merged = merge_catalogs(primary, secondary)
    assert [(p.id, p.name) for p in merged] == [(1, "Чайник"), (2, "Кружка"), (3, "Ложка")]


def test_15_document_has_all_fields():
    doc = Document(id=1, title="Патент")
    assert doc.id == 1
    assert doc.title == "Патент"
    assert doc.created_at is not None
    assert doc.is_deleted is False
    doc.delete()
    assert doc.is_deleted is True


def test_15_works_with_other_order():
    class Report(TimestampMixin, SoftDeleteMixin, BaseModel):
        pass

    report = Report(id=2)
    assert report.id == 2
    assert report.created_at is not None
    assert report.deleted_at is None
    assert Report.__mro__[1:4] == (TimestampMixin, SoftDeleteMixin, BaseModel)
