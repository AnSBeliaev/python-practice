"""
Задача 1.2. Настройки по умолчанию

Ситуация: сервис собирает конфиг из настроек по умолчанию и переопределений для
окружения. Тестировщик заметил: после сборки конфига для prod следующий конфиг для
stage тоже смотрит на prod-базу.

Что сделать: найти причину и исправить. DEFAULT_CONFIG не должен меняться никогда.

На собесе: "Чем copy() отличается от deepcopy()?"
"""

DEFAULT_CONFIG = {
    "db": {"host": "localhost", "port": 5432},
    "features": ["search"],
    "debug": False,
}


def build_config(overrides):
    config = DEFAULT_CONFIG.copy()
    for section, values in overrides.items():
        if isinstance(values, dict):
            config[section].update(values)
        elif isinstance(values, list):
            config[section].extend(values)
        else:
            config[section] = values
    return config
