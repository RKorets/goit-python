import re
import datetime

class Field:

    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return f'{self.value}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if type(value) == str:
            self.__value = value
        elif type(value) == datetime.datetime:
            self.__value = value
    
    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes

    def __setstate__(self, value):
        self.__dict__ = value


class Name(Field):
    pass


class Address(Field):
    pass

class Note(Field):
    pass

class Phone(Field):

    @Field.value.setter
    def value(self, new_value):
        if len(new_value) >= 10:
            Field.value.fset(self, new_value)
        else:
            print(
                '\033[31m' + 'Номер не додано! Номер повинен містити не меньше 11 цифр')
            return


class Birthday(Field):

    @Field.value.setter
    def value(self, new_value):
        try:
            birthday = datetime.datetime.strptime(new_value, '%Y-%m-%d')
            Field.value.fset(self, birthday)
        except ValueError:
            print(
                '\033[31m' + 'Некоректний формат дати! Потрібний формам ррр-мм-дд. Дата не додана')


class Email(Field):

    @Field.value.setter
    def value(self, add_value):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if (re.search(regex, add_value)):
            Field.value.fset(self, add_value)
        else:
            print(
                "\033[31m" + "Емейл не доданий не коректний формат! Формат excample@mail.com")
            return
