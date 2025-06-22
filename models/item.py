from abc import ABC, abstractmethod


class Item(ABC):
    """Абстрактный класс Item. Нужен как шаблон для классов GPU и Radiator"""
    @abstractmethod
    def current_price(self):
        pass

    @abstractmethod
    def status(self):
        pass