from field import Name, Phone, Email, Address, Birthday
from datetime import datetime


class Record:

    def __init__(self, name, address=None, phone=None, email=None, birthday=None):

        self.name = name if name.value else None
        self.addresses = []
        self.phones = []
        self.emails = []
        self.birthday = birthday
    
    def __repr__(self):
        if self.birthday:
            birthday = datetime.strftime(self.birthday.value, '%Y-%m-%d')
        else:
            birthday = None
        return f"{self.name}: {self.phones}, {self.emails}, {self.addresses}, {birthday}"

    def add_address(self, address):
        address_list = []
        for address in self.addresses:
            address_list.append(str(address.value))
        if address in address_list:
            print("This address alredy been added.")
        else:
            new_address = Address(address)
            self.addresses.append(new_address)
            print(f"for {self.name} add address {address}.")
            
    def add_phone(self, phone):
        phones_list = []
        if phone in phones_list:
            print("This num has already been added.")
        else:
            new_phone = Phone(phone)
            self.phones.append(new_phone)
            print(f"for {self.name} add phone {new_phone}.")

    def add_mail(self, mail):
        mail_list = []
        for email in self.emails:
            mail_list.append(str(email.value))
        if mail in mail_list:
            print("This mail has alredy been added.")
        else:
            new_mail = Email(mail)
            self.emails.append(new_mail)
            print(f"for {self.name} add mail {mail}.")
    
    def change_data(self, old, new, type_check):
        attributes = self.__dict__
        new_num_check = next(
            filter(lambda x: x.value == new, attributes[type_check]), None)
        old_num = next(filter(lambda x: x.value ==
                       old, attributes[type_check]), None)

        if not new_num_check and old_num:
            old_num.value = new
            print(f"Number successfully changed to {new.value}")
        else:
            print("Old data not registered or new data already exist")


    def change_adress(self, new_address, old_address):
        self.change_data(new_address, old_address, "addresses")

    def change_phone(self, new_num, old_num):
        self.change_data(new_num, old_num, "phones")

    def change_email(self, new_email, old_email):
        self.change_data(new_email, old_email, "emails")

    def change_birthday(self, new_birthday):
            self.birthday = new_birthday

    def delete_data(self, info, type_check):
        attributes = self.__dict__

        num = next(filter(lambda x: x.value ==
                   info, attributes[type_check]), None)
        if num:
            print(f"Параметр {num.value} видалений")
            if type_check == "phones":
                self.phones.remove(num)
            elif type_check == "emails":
                self.emails.remove(num)
            elif type_check == "addresses":
                self.addresses.remove(num)
        else:
            print("Такого параметру немає")

    def delete_number(self, phone):
        self.delete_data(phone, "phones")

    def delete_mail(self, mail):
        self.delete_data(mail, "emails")
        
    def delete_adress(self, address):
       self.delete_data(address, "addresses")

    def add_birthday(self, bd):
        self.birthday = Birthday(bd)
        print(f"{self.name} was born {bd}.")
    
    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes

    def __setstate__(self, value):
        self.__dict__ = value
