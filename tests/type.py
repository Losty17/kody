from typing import Generic, TypedDict, TypeVar

R = TypeVar('R', bound=TypedDict)


def get_keys(dict_): return dict_.__annotations__.keys()


class Dict(dict, Generic[R]):
    __dict: R = {}

    def __init__(self, source, field: str, typed_dict: R):
        self.__source = source
        self.__field = field

        data = source.__dict__[field].split(";")

        for index, item in enumerate(get_keys(typed_dict)):
            self[item] = int(data[index])

    def __setitem__(self, key: str, item: int):
        self.__dict[key] = item

        self.__source.__dict__[self.__field] = ';'.join(
            str(value) for value in self.__dict.values())

    def __str__(self) -> str:
        return str(self.__dict)


class Preferences(TypedDict):
    language: bool
    hide_labels: bool


class User:
    def __init__(self):
        self.teste = "0;1"


t = Dict[Preferences](User(), "teste", Preferences)
