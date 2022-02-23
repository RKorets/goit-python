from collections import UserDict

class Record:

    def __init__(self, name, phone) -> None:
        value = Name(name) #экземпляр класа Name
        self.name = value
        telephone = Phone(phone) #экземпляр класа Phone
        self.phones = [] #спиисок экземпляр класа Phone
        self.phones.append(telephone)

    def add_phone(self,phone):
        add_ph = Phone(phone)
        self.phones.append(add_ph)

    def change_phone(self,phone,new_phone):
        for el in self.phones:
            if phone in el.phones:
                 el.phones = [new_phone]
                 return
        print("Phone number not exist! Try again")

    def delete_phone(self,phone):
        for el in self.phones:
            if phone in el.phones:
                el.phones.remove(phone)
                return
        print("Phone number not exist! Try again")


class AddressBook(UserDict):

    def add_record(self, obj):
        if isinstance(obj, Record):
            self.data[obj.name.value] = obj

    def __str__(self) -> str:
        result = "\n".join([str(v) for v in self.data.values()])
        return result

    def show_all_contact(self):
        print("Имя           Номер телефона")
        for name, phone in self.data.items():
            phone_number = [ph.phones[0] for ph in phone.phones if len(ph.phones)!=0]
            print('{:<10} - {}'.format(name,phone_number))


class Field:
    pass


class Phone(Field):

    def __init__(self,phone=None):
        self.phones = [phone]


class Name(Field):

    def __init__(self,name):
        self.value = name





ab = AddressBook()
record = Record('Bill', '23456777')
ab.add_record(record)

record.add_phone("09543242342")
record.add_phone("0961019231")
record.change_phone("0961019231","000007")
record.delete_phone("23456777")
record.delete_phone("0969019233")

print(record.phones)
print(record.name.value)
print(ab.data['Bill'].phones)
ab.show_all_contact()

