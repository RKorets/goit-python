import datetime
from collections import UserDict
from records import Record, Birthday, Address, Name, Phone, Email


class AddressBook(UserDict):


    def add_record(self, record):

        if self.data.get(record.name.value):
            print(f"User name {record.name.value} already exists")
        else:
            self.data[record.name.value] = record
            print(f"User {record.name.value} successfully added")
        # if isinstance(set, Record):
        #     self.data.__setitem__(
        #         set.name, (set.addresses, set.phones, set.emails, set.birthday))
        # else:
        #     print("try add Record.")


    def get_bd(self, day=None):
        if day.isdigit():
            now = datetime.datetime.now()
            delta = now + datetime.timedelta(days=int(day))
            birthday_people = {}
            for k, v in self.data.items():
                for el in v:
                    if isinstance(el, Birthday):
                        date_val = (el.value).replace(year=now.year)
                        if now < date_val.replace(hour=23, minute=59, second=59, microsecond=0) < delta:
                            birthday_people[k] = str(date_val.date())
            print(birthday_people)
        else:
            print("Неправильний формат")



    def search_by(self, text, list_name=None):  
        result = []

        for user in self.data.values():
            if not list_name:
                if text in user.name.value:
                    result.append(user)
            else:
                if [type for type in user.list_name if text in type.value]:
                    result.append(user)
        return self.data.get(text)

    def search_by_name(self, text):
        return self.search_by(text)

    def search_by_phone(self, number):
        return self.search_by(number, "phones")

    def search_by_email(self, mail):
        return self.search_by(mail, "emails")

    def search_by_address(self, address):
        return self.search_by(address, "addresses")

    

    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes

    def __setstate__(self, value):
        self.__dict__ = value
