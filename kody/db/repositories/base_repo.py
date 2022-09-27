from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from ..db import Database

T = TypeVar("T")

class BaseRepo(Generic[T], metaclass=ABCMeta):
    def __init__(self) -> None:
        self.session = Database.get_instance()
    
    @abstractmethod
    def get(self, _id: int) -> T:
        pass

    @abstractmethod
    def add(self, target: T) -> T:
        pass

    @abstractmethod
    def remove(self, target: T) -> bool:
        pass

    @abstractmethod
    def update(self, target: T) -> T:
        pass