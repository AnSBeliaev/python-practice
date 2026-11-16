"""
Задача 1.5. Синхронизация справочника

Ситуация: справочник товаров синхронизируется с внешней системой. У нас есть
список id в нашей базе, у них - свой. Нужно понять, что создать, что удалить,
что оставить.

Что сделать: вернуть словарь с ключами to_create, to_delete, unchanged.
Значения - отсортированные списки id. Во входных списках бывают дубли.

На собесе: "Какие операции есть у set и когда set лучше list?"
"""


def plan_sync(local_ids, remote_ids):
    local_ids_set = set(local_ids)
    remote_ids_set = set(remote_ids)
    to_create = remote_ids_set.difference(local_ids_set)
    to_delete = local_ids_set.difference(remote_ids_set)
    unchanged = local_ids_set.intersection(remote_ids_set)

    final_ids = {}
    final_ids["to_create"] = sorted(to_create)
    final_ids["to_delete"] = sorted(to_delete)
    final_ids["unchanged"] = sorted(unchanged)
    return final_ids
