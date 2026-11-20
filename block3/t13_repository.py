"""
Задача 3.2. Сервис пользователей и хранилище

Ситуация: сервис регистрации пользователей ходит в базу напрямую, и его
невозможно протестировать без базы. Решили отделить работу с хранилищем.

Что сделать:
1) UserRepository - абстрактный класс (abc.ABC) с методами
   get(user_id), get_by_email(email), add(user), list_active().
   Создать его экземпляр напрямую должно быть нельзя.
2) InMemoryUserRepository(UserRepository) - хранит пользователей в dict.
   Плюс: len(repo) - число пользователей, user_id in repo - есть ли такой,
   for user in repo - перебор пользователей.
3) User - dataclass: id, email, is_active (по умолчанию True).
4) UserService(repo):
   - register(email) - создаёт пользователя с id = следующий по порядку
     (1, 2, 3 ...), email приводит к нижнему регистру. Если email уже есть -
     ValueError.
   - deactivate(user_id) - is_active = False. Нет такого пользователя - KeyError.

Сервис не знает, где лежат данные: в тестах ему дают InMemory, в проде дали бы
репозиторий с PostgreSQL.

На собесе: "Что такое абстрактный класс? Зачем __len__, __contains__,
__iter__? Что такое внедрение зависимостей и как оно помогает тестам?"
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

class UserRepository(ABC):
    @abstractmethod
    def get(self, user_id: int):
        pass
    
    @abstractmethod
    def get_by_email(self, email: str):
        pass

    @abstractmethod
    def add(self, user: User):
        pass

    @abstractmethod
    def list_active(self):
        pass

class InMemoryUserRepository(UserRepository):
    def __init__(self):
      self.users: dict = {}

    def __len__(self):
      return len(self.users)
   
    def __contains__(self, user_id: int):
       return user_id in self.users
   
    def __iter__(self):
       for user in self.users.values():
          yield user

    def get(self, user_id: int):
      if self.__contains__(user_id):
         return self.users.get(user_id)
      else: return None

    def get_by_email(self, email: str):
        for user in self.users.values():
            if user.email == email:
               return user

    def add(self, user: User) -> None:
        self.users[user.id] = user

    def list_active(self) -> list[User]:
      return [user for user in self.users.values() if user.is_active]

@dataclass
class User:
    id: int
    email: str
    is_active: bool = True

class UserService:
    def __init__(self, repo: UserRepository):
      self._repo = repo
      self._next_id = 1
  
    def register(self, email):
        normalized_email = email.lower()
        if self._repo.get_by_email(normalized_email) is not None:
            raise ValueError(f"Email {normalized_email} уже занят")

        user = User(id=self._next_id, email=normalized_email)
        self._repo.add(user)
        self._next_id += 1
        return user
    
    def deactivate(self, user_id):
        user = self._repo.get(user_id)
        if user is None:
            raise KeyError("Юзера не существует")
        user.is_active = False
        return user
    