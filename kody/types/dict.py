from typing import Dict as _Dict
from typing import Generic, TypedDict, TypeVar

from kody.utils import get_keys

R = TypeVar("R", bound=TypedDict)


class Dict(dict, Generic[R]):
    """ Custom dictionary subclass to support storing and retrieving
    multiple values in a single database field.

    Must extend a database model class and a dict type, and provide the field
    to use when instantiating this class.
    """

    def __init__(self, source, field: str, typed_dict: R, *, separator: str = ';', boolean: bool = False):
        self.dict: R = {}
        self.__source = source
        self.__field = field
        self.__separator = separator
        self.__boolean = boolean

        if separator:
            data = getattr(source, field).split(
                separator)
        else:
            data = getattr(source, field)

        for index, item in enumerate(get_keys(typed_dict)):
            self[item] = int(data[index])

    def __setitem__(self, key: str, item: int):
        if self.__boolean:
            self.dict[key] = int(item)
        else:
            self.dict[key] = item

        string = (self.__separator or '') \
            .join(str(value) for value in self.dict.values())

        setattr(self.__source, self.__field, string)

    def __getitem__(self, key: str):
        return bool(self.dict[key]) if self.__boolean else self.dict[key]

    def __str__(self):
        return str(self.dict)

    def __repr__(self):
        return repr(self.dict)

    def __len__(self):
        return len(self.dict)

    def __delitem__(self, key: str):
        return

    def clear(self):
        return

    def copy(self):
        return self.dict.copy()

    def has_key(self, k: str):
        return k in self.dict

    def update(self, *args, **kwargs):
        return self.dict.update(*args, **kwargs)

    def keys(self):
        return self.dict.keys()

    def values(self):
        return self.dict.values()

    def items(self):
        return self.dict.items()

    def pop(self, *args):
        return

    def __cmp__(self, dict_: _Dict):
        return self.__cmp__(self.dict, dict_)

    def __contains__(self, item):
        return item in self.dict
