"""
Задача 3.4. Примеси для моделей

Ситуация: в проекте у моделей есть общие куски: время создания и мягкое
удаление (запись не удаляется, а помечается). Их вынесли в классы-примеси.
Но у Document после создания нет то created_at, то deleted_at - зависит от
того, в каком порядке перечислены родители.

Что сделать: исправить классы так, чтобы Document получал все поля при любом
порядке примесей. Сигнатуры и порядок родителей у Document не менять.

На собесе: "Что такое MRO? Как работает super() при множественном
наследовании? Зачем примесям вызывать super().__init__?"
"""

from datetime import datetime, timezone


class BaseModel:
    def __init__(self, id, **kwargs):
        self.id = id


class TimestampMixin:
    def __init__(self, **kwargs):
        self.created_at = datetime.now(timezone.utc)


class SoftDeleteMixin:
    def __init__(self, **kwargs):
        self.deleted_at = None

    def delete(self):
        self.deleted_at = datetime.now(timezone.utc)

    @property
    def is_deleted(self):
        return self.deleted_at is not None


class Document(SoftDeleteMixin, TimestampMixin, BaseModel):
    def __init__(self, id, title):
        super().__init__(id=id)
        self.title = title
