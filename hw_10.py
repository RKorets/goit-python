
from collections import UserDict


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return self.value

    def __str__(self) -> str:
        return self.value


class Phone(Field):
    pass


class Name(Field):
    pass


class Record:
    def __init__(self, name: Name, phone: Phone) -> None:
        self.name = name
        self.phones = []  # спиисок экземпляр класа Phone
        self.phones.append(phone)

    def add_phone(self, phone: Phone):
        self.phones.append(phone)

    def __str__(self) -> str:
        return f'name: {self.name}, phones: {", ".join([str(p) for p in self.phones])}'


class AddressBook(UserDict):
    def add_record(self, *args):
        for item in args:
            self.data[item.name] = item

    def __str__(self) -> str:
        result = "\n".join([str(v) for v in self.data.values()])
        return result
