# BaseSku.py
from abc import ABCMeta, abstractmethod
from enum import EnumMeta

class ABCEnumMeta(ABCMeta, EnumMeta):
    """Lets a class be both an ABC and usable as an Enum mixin."""
    pass


class BaseSku:
    """Not an Enum — just a normal base class."""
    @property
    def url(self) -> str:
        raise NotImplementedError

    @property
    def product_name(self) -> str:
        raise NotImplementedError